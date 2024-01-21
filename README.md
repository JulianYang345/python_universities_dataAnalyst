# python_universities_dataAnalyst
a data analyst project where I make a script to clean up and visualize the data with outputs being both csv and pdf files

functionality:
main.py to read all of the base csv files from uni_databank, clean up all the data(drop unnecessary column, fill up empty column with logarithmic regressions, normalization, etc.)

pdf_processing.py to read the pdf journals and filter out the main df rows base on the pdf data

transform_table.py to read the filtered file and pivot it one by one base on the value and save it to seperate files

visualize.py to read the pivoted files and then visualize the data with line chart followed by trend lines

to use it, you only need to run main.py as all the other module have already been imported and called in main.py
make sure all the csv you need to clean up is inside the folder named uni_databank 

- the output of main.py will be a unified cleaned data of all those csv from uni_databank
- then pdf_processing will take the file as input and filter out the data base on the pdf. the output will be the filtered csv
- transform_table then will take the filtered csv as input and pivot all the column with numeric values while adding average row down at the bottom. output will be all the pivoted csv
- lastly visualize.py will take all the normalised csv then output a pdf containing all of the charts  
