import pandas as pd


# creating a dataframe

dataset1 = {'a':[100,200,300],
           'b':[400,500,600],
           'c':[700,800,900]
           }
df1 = pd.DataFrame(dataset1)
print(df1)


# creates a new column named index from your existing index
# resets your index to 0,1,2...n
df1.reset_index(inplace=True)
print(df1)


# resets index - does not create a new index col
df1.reset_index(drop=True, inplace=True)
print(df1)
