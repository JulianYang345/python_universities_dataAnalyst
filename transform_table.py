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

def get_gradient(df):
    row_index = 0

    # Ensure '0.0' is in the columns of the pivoted DataFrame
    
    zero_index = df.columns.get_loc(0.0)

    while row_index < len(df):
        before_strategy = []  # Reset before_strategy for each row
        after_strategy = []   # Reset after_strategy for each row
        column_index = 0

        while column_index < zero_index:
            if is_float(df.iloc[row_index, column_index]):
                before_strategy.append(float(df.iloc[row_index, column_index]))
            column_index += 1

                # Filter out NaN values from before_strategy
        before_strategy = np.array(before_strategy)
        before_strategy = before_strategy[~np.isnan(before_strategy)]

        if len(before_strategy) > 1:
            df.loc[row_index, 'm-1'] = str(round(np.nanmean(np.gradient(np.array(before_strategy))),4))

        column_index = zero_index

        while column_index < len(df.columns) - 2:
            if is_float(df.iloc[row_index, column_index]):
                after_strategy.append(float(df.iloc[row_index, column_index]))
            column_index += 1

                # Filter out NaN values from before_strategy
        after_strategy = np.array(after_strategy)
        after_strategy = after_strategy[~np.isnan(after_strategy)]
        if len(after_strategy) > 1:
            df.loc[row_index, 'm+1'] = str(round(np.nanmean(np.gradient(np.array(after_strategy))),4))
        row_index += 1

    return df



def transform_table():
    df = pd.read_csv("Cleaned_csv_pandas/07-unified-strategy-year-normalised.csv", encoding='utf-16')
    for column in df.columns:
        if '_n' in column:
            normal = 'normalised'
        else:
            normal = 'unnormalised'
        df_pivoted = pd.DataFrame()
        if is_float(df.at[0, column]):
            df_pivoted = df.pivot(index='name', columns='strategy_year_n', values=column)
            df_pivoted = df_pivoted.reset_index()

            '''
            print("Columns of df_pivoted:")
            print(df_pivoted.columns)
            '''
            
            '''
            df_pivoted.insert(df_pivoted.columns.get_loc((df_pivoted.columns[-1])) + 1, 'm-1', '')
            df_pivoted.insert(df_pivoted.columns.get_loc((df_pivoted.columns[-1])) + 1, 'm+1', '')
            df_pivoted = get_gradient(df_pivoted)
            '''

            mean_value = ['Average']
            for i in range(1, df_pivoted.shape[1]):
                df_pivoted.iloc[:, i] = df_pivoted.iloc[:, i].replace('', np.nan)
                df_pivoted.iloc[:, i] = df_pivoted.iloc[:, i].astype(float)
                mean_value.append(str(round(df_pivoted.iloc[:, i].mean(), 4)))#df_pivoted.iloc[:, i].mean())
            
            df_pivoted.loc[len(df_pivoted)] = mean_value

            for i in range(-12, 12):
                if (i < -6 or i > 6) and float(i) in df_pivoted.columns:
                    df_pivoted = df_pivoted.drop([float(i)], axis = 1)
            
            for index, value in df_pivoted.iterrows():
                splitted_name = df_pivoted.at[index, "name"].split(" ")
                code_name = ""
                i = 0
                for word in splitted_name:
                    if word == "of":
                        code_name += "o"
                    elif word.lower() == "university":
                        code_name += word[0]
                    #elif(i>=1):
                    #    code_name += word[0]
                    else:
                        code_name += word[0:2]
                    i += 1
                df_pivoted.at[index, "name"] = code_name

            df_pivoted.to_csv(f"Cleaned_csv_pandas/transformed/{column}_{normal}.csv", index=False, encoding='utf-16')

transform_table()