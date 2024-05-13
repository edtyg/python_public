import pandas as pd
import seaborn as sns

df = sns.load_dataset('titanic')
df['empty'] = ''

df['survived'] = df['survived'].astype('string') # change type to string


df['empty'] = pd.to_numeric(df['empty'], errors='coerce') # if you have missing values and you want to convert to float use this instead

# .astype('float')
# .astype('string')
# .astype('bool')