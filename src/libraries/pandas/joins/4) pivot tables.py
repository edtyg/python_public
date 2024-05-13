import pandas as pd
import seaborn as sns

titanic = sns.load_dataset('titanic')

# pulling mean of survived grouped by sex
df1 = titanic.groupby('sex').mean()['survived']
print('df1')
print(df1)

# group by multiple columns
df2 = titanic.groupby(['sex', 'class']).mean()['survived'].unstack()
print('df2')
print(df2)

# get same results above
pivot1 = titanic.pivot_table('survived', index='sex', columns='class')
print('pivot1')
print(pivot1)

# now group by sex and age
age = pd.cut(titanic['age'], [0,18,80])
pivot2 = titanic.pivot_table('survived', index = ['sex',age], columns = 'class')
print('pivot2')
print(pivot2)

## alternatively can try apply function to create a new column then group by ##

def age_group(x):
    if x <= 18:
        return('young')
    elif x <= 80:
        return('old')

# create new age_group column
titanic['age_group'] = titanic['age'].apply(age_group)

# now grp by that column
pivot3 = titanic.pivot_table('survived', index = ['sex','age_group'], columns = 'class')
print('pivot3')
print(pivot3)

# add margins to see sub total

pivot4 = titanic.pivot_table('survived', index = ['sex','age_group'], columns = 'class', margins=True)