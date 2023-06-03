import pandas as pd

df1 = pd.DataFrame({'A':['A1','A2'], 'B':['B1','B2']}, index = [1,2])
df2 = pd.DataFrame({'A':['A3','A4'], 'B':['B3','B4']}, index = [3,4])

print(df1)
print(df2)


# default concatenation is row wise #
c = pd.concat([df1,df2])
print(c)

c_row = pd.concat([df1,df2], axis = 0) # alternatively u can specify axis = 0 (by row)
print(c_row)

# concats by index
c_col = pd.concat([df1,df2], axis = 1) # alternatively u can specify axis = 1 (by col)
print(c_col)


## set index to be same in order to concat by columns
df1 = pd.DataFrame({'A':['A1','A2'], 'B':['B1','B2']}, index = [1,2])
df2 = pd.DataFrame({'A':['A3','A4'], 'B':['B3','B4']}, index = [1,2])

c_col = pd.concat([df1,df2], axis = 1) # or also by columns axis = 1
print(c_col)


# inner join
df5 = pd.DataFrame({'A':['A1','A2'], 'B':['B1','B2'], 'C':['C2','C2']}, index = [1,2])
df6 = pd.DataFrame({'B':['B3','B4'], 'C':['C3','C4'], 'D':['D3','D4']}, index = [3,4])
print(pd.concat([df5,df6]))
print(pd.concat([df5,df6], join='inner'))
