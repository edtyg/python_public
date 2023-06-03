import os
import pandas as pd
import numpy as np

filepath = 'C:/Users/Edgar Tan/OneDrive/Desktop/' # your excel file folder
filename = 'est_dummy.xlsx' # excel file name and type .xlsx, .xls

# put location of where you want your output file to be
export_file_location = 'C:/Users/Edgar Tan/OneDrive/Desktop/python outputs/' # final file location
export_file_name = 'est_dummy_checking.xlsx' # output file name


df = pd.read_excel(filepath + filename)
df = df.fillna(0) # replace na as 0 - cannot set to blank will have some issues with your date col - NaT seems like can only replace with number

sales_order_id = df['Sales Ord.'].unique().tolist() # creates a list of unique sales order_id

# make sure uppercase and lowercase match correctly with file
columns_to_check = [
    'Plnt', 
    'Vessel', 
    'ETD Date',
    'Disport ETA',
    'Port of Loading',
    'Port of discharge',
    'Fwd Agent',
    'Shipping Cond',
    'Sold-to-Party No',
    'Tonnes',
    'No. of Containers',
    ]

for i in sales_order_id:
    for cols in columns_to_check: 
        df_id = df.loc[df['Sales Ord.'] == i] # filter your sales order id
        indexes = df_id.index.tolist() # list of indexes
        df_id_checking_value = df_id.loc[indexes[0], cols] # take the first value of col selected 
        
        for j in indexes:
            check = df_id.loc[j, cols]
            if check == df_id_checking_value:
                df.loc[j, f'{cols}_check'] = 1
            elif check != df_id_checking_value:
                df.loc[j, f'{cols}_check'] = 0
                df_id_checking_value = df_id.loc[j, cols]
            
                
writer = pd.ExcelWriter(export_file_location + export_file_name)
df.to_excel(writer)
writer.save()
writer.close()
print('file Saved')