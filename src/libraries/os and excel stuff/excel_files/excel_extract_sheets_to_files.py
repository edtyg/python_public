import os
import pandas as pd

filepath = 'C:/Users/Edgar Tan/OneDrive/Github/python/os and excel stuff/excel_files/' # folder containing all your excel files
print('Your excel folder')
print(filepath)
print('\n')

filename = os.listdir(filepath) # this will create a list of all the files in the folder
print('filenames')
print(filename)
print('\n')


# put location of where you want your output file to be
export_file_location = 'C:/Users/Edgar Tan/OneDrive/Github/python/os and excel stuff/excel_files/' 


# list of sheet names you want to extract - if all same thats good if not it'll be troublesome
sheet_names = [
    'name_age',
    'rank_salary',
    'country',
    ]

for sheet in sheet_names:
    df_main = pd.DataFrame()
    for file in filename:
        path = filepath + file
        print(path)
        try:
            df = pd.read_excel(path, sheet_name = sheet)
        except ValueError:
            continue
        df['filename'] = sheet
        df_main = pd.concat([df_main, df], axis = 0)
        
    writer = pd.ExcelWriter(export_file_location + sheet + '.xlsx')
    df_main.to_excel(writer)
    writer.save()
    writer.close()
    print('file Saved')