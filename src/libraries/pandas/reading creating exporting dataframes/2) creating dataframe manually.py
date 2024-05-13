import pandas as pd


# creating from a list
data = [10,20,30,40,50,60]
df_list = pd.DataFrame(data, columns=['Numbers'])


# creating from a list of lists
data = [['tom', 10], ['nick', 15], ['juli', 14]]
df_lists = pd.DataFrame(data, columns=['Name', 'Age'])


# creating from a dictionary
data = {
        'Name': ['Tom', 'nick', 'krish', 'jack'],
        'Age': [20, 21, 19, 18],
        }
df_dict = pd.DataFrame(data)