import os
import pandas as pd

# full_path = os.path.realpath(__file__) # full directory of this script
# save_path = os.path.dirname(full_path) + "/" # folder of this script


filepath = 'C:/Users/Edgar Tan/OneDrive/Github/python/os and excel stuff/excel_files/' # folder containing all your excel files
print('Your excel folder')
print(filepath)
print('\n')

filename = os.listdir(filepath) # this will create a list of all the files in the folder
print('filenames')
print(filename)
print('\n')


excel_files_sheets = []
for i in filename:
    path = filepath + i
    print('your excel file full path')
    print(path)
    print('\n')
    
    xlsx = pd.ExcelFile(path)
    sheet_names = xlsx.sheet_names # list of sheet names in that excel file
    print('\n')
    excel_files_sheets.append(sheet_names) # append list into a list
    

unique_sheet_names = []
# nested loop
for i in excel_files_sheets:
    for j in i:
        if j not in unique_sheet_names:
            unique_sheet_names.append(j)

# this will print all the sheet names from all the files in the folder
print('unique sheet names')
print(unique_sheet_names)