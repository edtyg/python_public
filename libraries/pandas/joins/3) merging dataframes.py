import pandas as pd


df1 = pd.DataFrame({'employee': ['Bob', 'Jake', 'Lisa', 'Sue'],'group': ['Accounting', 'Engineering', 'Engineering', 'HR']})
df2 = pd.DataFrame({'employee': ['Lisa', 'Bob', 'Jake', 'Sue'],'hire_date': [2004, 2008, 2012, 2014]})
df3 = pd.DataFrame({'name': ['Bob', 'Jake', 'Lisa', 'Sue', 'Sally'],'salary': [70000, 80000, 120000, 90000, 65000]})
print(df1)
print(df2)
print(df3)


# merge by a column name
# both dataframes must have the specified column name
print(pd.merge(df1, df2, on = 'employee'))

# if the columns u want to merge by have different names set left on and right on column names
# left join = match whatever is in the left df that is in the right df
pd.merge(df1, df3, how = 'left', left_on='employee', right_on='name')

# outer join = match all - if left df doesnt contain right df's values - it is still joined
# could possibly have na values
pd.merge(df1, df3, how = 'outer', left_on = 'employee', right_on = 'name')

# merge by index - make sure index matches correctly i.e unique for the specific rows
pd.merge(df1, df3, left_index=True, right_index=True)

# outer join - can also join on multiple cols
final_df = df1.merge(
    df2, 
    how='outer', 
    left_on = ['df1_col', 'df2_col'], 
    right_on = ['df1_col', 'df2_col'],
    ) 
