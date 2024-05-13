import pandas as pd
import os

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

output_excel = "testing_output.xlsx"
writer = pd.ExcelWriter(save_path + output_excel) # writer for xlsx files

output_csv = "testing_output.csv"

# creating from a list
data = [10,20,30,40,50,60]
df_list = pd.DataFrame(data, columns=['Numbers'])


# exports to xlsx file
# can create multiple sheets in the same excel file
df_list.to_excel(writer, sheet_name = 'testing1', index = False) # sheet1
df_list.to_excel(writer, sheet_name = 'testing2', index = False) # sheet2
writer.save()
writer.close()
print('file Saved')

#
df_list.to_csv(
    output_csv, 
    index = False, # can choose to include index or not
    )