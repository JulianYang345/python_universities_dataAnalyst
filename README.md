# python_universities_dataAnalyst
A data analyst project where a script is used to clean up and visualize data, with outputs being both CSV and PDF files.

## Functionality:

1. **main.py:**
   - Reads all base CSV files from the 'uni_databank' folder.
   - Cleans up the data (drops unnecessary columns, fills up empty columns with logarithmic regressions, normalization, etc.).
   - Output will be all the modified csv and the unified version containing all the csv. it will be in the folder cleaned_csv_pandas

2. **pdf_processing.py:**
   - Read the unified file from the previous step
   - Reads PDF journals and filters out rows from the unified file based on the PDF data.
   - Output will be the filtered csv in the folder cleaned_csv_pandas

4. **transform_table.py:**
   - Reads the filtered file.
   - Pivots the DataFrame one by one based on the columns with numeric values(ex: overall_score column) and saves them to separate files.
   - Output will be at cleaned_csv_pandas/transformed containing all the pivoted csv

5. **visualize.py:**
   - Reads the pivoted files.
   - Visualizes the data with line charts followed by trend lines.
   - Output will be named plot.pdf at the same directory as the main.py

To use it, run `main.py`. Ensure all the CSV files you need to clean up are inside the 'uni_databank' folder. no need to run the other files as those were already being called inside main.py.

Library used:
1. Pandas (the main library to read and manipulate csv)
2. NumPy (to perform complex calculation)
3. MatPlotLib (to visualize data)
4. Chardet (to detect encoding)
5. fitz (to read pdf)
6. glob (to read path)
7. sklearn (to do regression)

## Usage:
```bash
python main.py
