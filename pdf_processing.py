import pandas as pd
import glob
import os
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import chardet
import fitz

def is_float(val):
    try:
        float_val = float(val)
        return True
    except ValueError:
        return False

def sort_uni(df, text_list, sorted_uni):
    uni_names = []
    for name in df['name']:
        if name not in uni_names:
            uni_names.append(name.lower())
    
    for name in uni_names:
        for index, sentence in enumerate(text_list):
            if name in sentence.lower() and name not in sorted_uni.keys():
                i = 0
                while index + i < len(text_list):
                    if '-' in text_list[index + i]:
                        break 
                    elif is_float(text_list[index + i].strip()):
                        break
                    else:
                        i += 1
                strategy_year = text_list[index + i]

                sorted_uni[name] = strategy_year

    return sorted_uni

def clean_strategy_year(sorted_df, sorted_uni):
    if 'strategy_year' not in sorted_df.columns:
            sorted_df.insert(sorted_df.columns.get_loc((sorted_df.columns[-1])) + 1, 'strategy_year', '')
    
    for index, value in sorted_df.iterrows():
        if value['name'].lower() in sorted_uni:
            sorted_df.at[index, 'strategy_year'] = sorted_uni[value['name'].lower()]
    
    for index, value in sorted_df.iterrows():
        if '-' in value['strategy_year']:
            sorted_df.at[index, 'strategy_year'] = value['strategy_year'].split('-')[0]
    
    return sorted_df

def normalization_strategy_year(sorted_df):
    if 'strategy_year_n' not in sorted_df.columns:
        sorted_df.insert(sorted_df.columns.get_loc((sorted_df.columns[-1])) + 1, 'strategy_year_n', '')

    for index, value in sorted_df.iterrows():
        sorted_df.at[index, 'strategy_year_n'] = str(float(value['tahun']) - float(value['strategy_year']))

    return sorted_df

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def pdf_processing():
    #operate pdf
    pdf_files = glob.glob("uni_databank/*.pdf")
    union_df = pd.read_csv("Cleaned_csv_pandas/03-unified-normalised.csv", encoding='utf-16')
    sorted_df = pd.DataFrame()
    sorted_uni = {}    
    for pdf_file in pdf_files:
        detected_encoding = detect_encoding(pdf_file)
        opened_pdf = fitz.open(pdf_file)
        num_pages = len(opened_pdf) # Get the number of pages

        page = opened_pdf[2] # Get the page object
        text = page.get_text() # Extract text from the page
        text_list = text.split("\n")
            
        '''
        file = open('pdf_content.txt', 'a', encoding='utf-8')
        file.write(f"Page {3}:")
        file.write(text)'''

        sorted_uni = sort_uni(union_df, text_list, sorted_uni)

        opened_pdf.close()
    
    for name in sorted_uni:
        sorted_df = pd.concat([sorted_df, union_df.loc[(union_df['name'].str.lower() == name)]])
    
    sorted_df = clean_strategy_year(sorted_df, sorted_uni)
    sorted_df = normalization_strategy_year(sorted_df)

    sorted_df.to_csv("Cleaned_csv_pandas/07-unified-strategy-year-normalised.csv", index=False, encoding='utf-16')

