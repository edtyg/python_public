import pandas as pd
from sklearn.datasets import load_iris

data = load_iris()
df1 = pd.DataFrame(data.data, columns=data.feature_names)


df1.head() # top 5 rows by default
df1.head(10)

df1.tail() # bottom 5 rows by default
df1.tail(10)

df1.describe() # gives useful statistics - count, mean, standard deviation etc
df1.shape # gives dimension of dataframe

df1.columns # get columns
df1.columns.tolist() # outputs columns in a list

df1.index # get index
df1.index.tolist() # outputs index in a list

df1.dtypes # shows the type of data in each column

df1.isnull() # returns true or false, true = empty values (NaN)
df1.isnull().sum() # check how many null objects in dataframe
df1.isnull().sum().sum() # count of NaN in entire dataframe

df1.info #
