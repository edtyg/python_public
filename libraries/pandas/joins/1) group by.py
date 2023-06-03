import pandas as pd

df = pd.read_excel(
    'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
    sheet_name='Canada by Citizenship',
    skiprows=range(20),
    skipfooter=2,
    )
print(df)


# need to apply an aggregate function after grouping #
# count(), mean(), median(), min(), max(), std(), var(), mad(), prod(), sum()...
df_groupby_mean = df.groupby(['OdName', 'RegName'], as_index= False).mean() # group by columns - but do not set them as index
print(df_groupby_mean)
