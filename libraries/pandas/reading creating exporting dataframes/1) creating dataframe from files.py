import pandas as pd
import os

# current folder path
full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

csv_filename = 'testing.csv'
excel_filename = 'testing.xlsx'
text_filename = 'testing.txt'

csv_filepath = save_path + csv_filename
excel_filename = save_path + excel_filename
text_filename = save_path + text_filename


# creating df from local files
df_csv = pd.read_csv(
    filepath_or_buffer = csv_filename,
    index_col = 'name',
    )

df_excel = pd.read_excel(
    io = excel_filename,
    sheet_name = 'testing', # reads specific sheet from xlsx file can use integer as well like 0
    index_col = 'name', # set column as index and use integer as well like 0
    # usecols = [0,1,2], # selects first 3 columns
    )

df_text = pd.read_table(
    filepath_or_buffer = text_filename,
    index_col = 'name',
    )
