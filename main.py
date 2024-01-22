import pandas as pd
import glob
import os
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import chardet
import fitz
import pdf_processing
import transform_table
import visualize

def is_float(val):
    try:
        float_val = float(val)
        return True
    except ValueError:
        return False
    
def clean_tahun(df):
    # Check if 'Year' column exists before renaming
    if 'year' in df.columns:
        # Move content of 'Year' to 'tahun' and drop 'tahun'
        df['tahun'] = df['year']
        df = df.drop(columns=['year'])

    elif 'Year' in df.columns:
        # Move content of 'Year' to 'tahun' and drop 'tahun'
        df['tahun'] = df['Year']
        df = df.drop(columns=['Year'])

    elif 'tahun_address' in df.columns:
        df['tahun'] = df['tahun_address']
        df = df.drop(columns=['tahun_address'])

    elif 'year' in df.columns and 'tahun' in df.columns:
        df = df.drop(columns=['year'])

    elif 'Year' in df.columns and 'tahun' in df.columns:
        df = df.drop(columns=['Year'])
    
    return(df)

def log_reg(df, dependent, independent):
    yes_empty = df.loc[(df[dependent].isin(['-', 'n/', '%', '']))]
    not_empty = df.loc[~(df[dependent].isin(['-', 'n/', '%', '']))]

    if not not_empty.empty:

        X_train = (pd.to_numeric(not_empty[independent])).to_numpy()
        y_train = (pd.to_numeric(not_empty[dependent])).to_numpy()

        a,b = np.polyfit(np.log(X_train), y_train, 1)

        for index, value in yes_empty.iterrows():
            imputed_value = round(a * np.log(float(df.at[index, independent])) + b, 1)
            df.at[index, dependent] = str(imputed_value)
                

def rank_cleaner(df):
    df.reset_index(drop=True, inplace=True)
    df['rank'] = df.index + 1

    return df

def drop_collumn(df):
    if 'Unnamed: 0' in df.columns:
        df.reset_index(drop=True, inplace=True)
        df = df.drop(columns=['Unnamed: 0'])
    if 'female_male_ratio' in df.columns:
        df.reset_index(drop=True, inplace=True)
        df = df.drop(columns=['female_male_ratio'])
    if 'international_students' in df.columns:
        df.reset_index(drop=True, inplace=True)
        df['intl_students'] = df['international_students']
        df = df.drop(columns=['international_students'])
    return df

def clean_empty(df):
    for column in df.columns:
        if column != 'overall_score':
            for index, value in df[column].items():
                if value in ('', '-', 'n/', '%'):
                    df.at[index, column] = 'n/a'
                        
    return df.astype(str)

def clean_score_range(df, score_columns):
    value_list = []
    for value in df[score_columns]:
        value = str(value)
        if value not in value_list and ('-' in value or '—' in value or '–' in value):
            value_list.append(value)

    for value in value_list:
        val_range = df.loc[(df[score_columns] == value)]

        if '-' in value:
            splitted_value = value.split("-")
        elif '—' in value:
            splitted_value = value.split("—")
        elif '–' in value:
            splitted_value = value.split("–")
        
        if not '' in splitted_value:
            max_value = float(splitted_value[1])
            min_value = float(splitted_value[0])

            for index, value in val_range.iterrows():
                df.at[index, score_columns] = str(round(float(df.at[index-1, score_columns])-(max_value-min_value) / len(val_range), 1))
        
    return df
    
def clean_score_empty(df, score_columns):
    df[score_columns] = df[score_columns].astype(str)
    df[score_columns] = df[score_columns].str.replace('%', '')
    df[score_columns] = df[score_columns].str.replace(',', '')
    df[score_columns] = df[score_columns].str.replace('nan', '')

    log_reg(df, score_columns, 'rank')
    
    return df

def clean_percent(df):
    columns = ["student_staff_ratio", "intl_students"]
    for column in columns:
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('%', '')
        df[column] = df[column].str.replace(',', '')
        df[column] = df[column].str.replace('nan', '')
        df[column] = df[column].str.replace('n/', '')

        if len(df[column]) == 0:
            return df

        log_reg(df, column, 'rank')

        for index, value in df.iterrows():
            if float(df.at[index, column]) < 1:
                df.at[index, column] = str(round(float(df.at[index, column]), 2))
            else:
                df.at[index, column] = str(round(float(df.at[index, column])/100, 2))

    return df

def clean_number_student(df):
    df['number_students'] = df['number_students'].astype(str)
    df['number_students'] = df['number_students'].str.replace(',', '')
    df['number_students'] = df['number_students'].str.replace('nan', '')

    log_reg(df, 'number_students', 'rank')

    for index, value in df.iterrows():
        df.at[index, 'number_students'] = str(int(float(df.at[index, 'number_students'])))

    return df
            

def normalization(df):
    for column in df.columns:
        if not any(keyword in column for keyword in ['name', 'tahun', 'address','_n']) and is_float(df[column].iloc[0]):
            value_list = []
            temp_column = df[column].astype(float)
            max_val = round(temp_column.max(), 4)
            min_val = round(temp_column.min(), 4)
            for value in df[column]:
                value = float(value)
                normalized_value = (value - min_val) / (max_val - min_val)
                value_list.append(str(round(normalized_value, 4)))
            df.insert(df.columns.get_loc((df.columns[-1])) + 1, column+'_n', value_list)

    return df

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def main():
    #operate csv
    csv_files = []
    csv_names = []
    csv_files = glob.glob("uni_databank/*.csv")
    result_df = pd.DataFrame()
    
    for file in csv_files:
        detected_encoding = detect_encoding(file)
        df = pd.read_csv(file, encoding=detected_encoding)
        df = drop_collumn(df)
        df = clean_tahun(df)
        df = rank_cleaner(df)

        if df.columns.isin(["student_staff_ratio", "intl_students"]).any():
            df = clean_percent(df)
        
        for score_columns in df.columns:
            if 'score' in score_columns:
                df = clean_score_range(df, score_columns)
                df = clean_score_empty(df, score_columns)

        df = clean_number_student(df)
        df = clean_empty(df)

        folder, csv_names = file.split('\\')

        # Save with index=False
        df.to_csv(f"Cleaned_csv_pandas/modified_{csv_names}", index=False, encoding='utf-16')

        result_df = pd.concat([result_df, df])

    result_df = normalization(result_df)
    result_df = result_df.drop_duplicates().reset_index(drop=True)
    result_df.to_csv("Cleaned_csv_pandas/03-unified-normalised.csv", index=False, encoding='utf-16')

    pdf_processing.pdf_processing()
    transform_table.transform_table()
    visualize
    
    
if __name__=="__main__":
    new_directory = "Cleaned_csv_pandas"  # Replace with the desired path
    os.makedirs(new_directory, exist_ok=True)  # Create the directory if it doesn't exist

    new_directory_child = "Cleaned_csv_pandas/transformed"  # Replace with the desired path
    os.makedirs(new_directory_child, exist_ok=True)  # Create the directory if it doesn't exist
    main()

