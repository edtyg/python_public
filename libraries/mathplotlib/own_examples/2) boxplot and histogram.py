import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_excel(
    'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
    sheet_name='Canada by Citizenship',
    skiprows=range(20),
    skipfooter=2)


plt.figure(figsize=(10, 7))
plt.hist(df1['AREA'], color = 'r', alpha = 0.5, label = '1')
#plt.hist(x, y, color = 'r', alpha = 0.5, label = '1')      #label 1
#plt.plot(x, y+10, color = 'b', alpha = 0.5, label = '2')   #label 2
plt.xlabel('X axis', fontsize = 20)
plt.ylabel('Y axis', fontsize = 20)
plt.title('Line Graph', fontsize=20)
plt.legend(fontsize = 20) # need label for legend
plt.show()
