import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
from matplotlib.backends.backend_pdf import PdfPages

csv_files = glob.glob("Cleaned_csv_pandas/transformed/*_n_normalised.csv")

csv_files = [files for files in csv_files if "strategy_year_n_normalised.csv" not in files]

pdf_filename = "plots.pdf"
pdf_pages = PdfPages(pdf_filename)

for file in csv_files:
    df = pd.read_csv(file, encoding='utf-16')
    folder, subfolder = file.split('/')
    subfolder, file_name = subfolder.split('\\')
    label_name = file_name.replace("_n_normalised.csv", "")

    before = df.columns.get_loc("-6.0")
    after = df.columns.get_loc("6.0") + 1
    zero = df.columns.get_loc("0.0")
    x = np.array(df.columns[before:after].astype(float)) #year
    y = np.array(df.iloc[-1, before:after].astype(float))

    before_trend_x = np.array(df.columns[before:(zero+1)].astype(float))
    before_trend_y = np.array(df.iloc[-1, before:(zero+1)].astype(float))

    after_trend_x = np.array(df.columns[zero:after].astype(float))
    after_trend_y = np.array(df.iloc[-1, zero:after].astype(float))

    slope, intercept = np.polyfit(before_trend_x, before_trend_y, 1)
    trend_line = slope * np.array(before_trend_x) + intercept
    plt.plot(before_trend_x, trend_line, color='red', linestyle='--', label="Before IT strategy")

    slope, intercept = np.polyfit(after_trend_x, after_trend_y, 1)
    trend_line = slope * np.array(after_trend_x) + intercept
    plt.plot(after_trend_x, trend_line, color='green', linestyle='--', label="After IT strategy")


    mid_point = (max(x) + min(x)) / 2
    plt.plot(x, y, color='blue', label=label_name)
    #plt.plot(x, df.iloc[-1]['m-1'], color='green', label="m-1")
    #plt.plot(x, df.iloc[-1]['m+1'], color='red', label="m+1" )
    
    # second plot with x1 and y1 data
    
    plt.xlabel("strategy year")
    plt.ylabel(label_name)
    plt.title(file_name)
    plt.legend()
    plt.grid(True)
    plt.axvline(x=mid_point, color='black', linestyle='--')

    pdf_pages.savefig()

    # Clear the current figure
    plt.clf()

# Close the PDF file
pdf_pages.close()
print("Plots saved to", pdf_filename)