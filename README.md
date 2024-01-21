# python_universities_dataAnalyst
a data analyst project where I make a script to clean up and visualize the data with outputs being both csv and pdf files

functionality:
main.py to read all of the base csv files from uni_databank, clean up all the data(drop unnecessary column, fill up empty column with logarithmic regressions, normalization, etc.)

pdf_processing.py to read the pdf journals and filter out the main df rows base on the pdf data

transform_table.py to read the filtered file and pivot it one by one base on the value and save it to seperate files

visualize.py to read the pivoted files and then visualize the data with line chart followed by trend lines
