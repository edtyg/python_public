import pandas as pd
import os

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"

# creating dataframes

data1 = {'Height':[180,162,173,164], 'Weight': [72,54,56,48]}
data2 = {'Length':[100,200,300,400], 'Breadth': [10,20,30,40]}

df1 = pd.DataFrame(data1, index = ['Alice','Anna','Charlie','Diane'])
df2 = pd.DataFrame(data2, index = ['Alice','Anna','Charlie','Diane'])


# create separate writers
writer1 = pd.ExcelWriter(save_path + 'testing1.xlsx')
df1.to_excel(writer1, sheet_name = 'testing1')
writer1.save()
writer1.close()
print('file Saved')

writer2 = pd.ExcelWriter(save_path + 'testing2.xlsx')
df2.to_excel(writer2, sheet_name = 'testing2')
writer2.save()
writer2.close()
print('file Saved')

