import pandas as pd


df = pd.DataFrame( {"Undergraduate": {"Straight A's": 240, "Not": 3_760},"Graduate": {"Straight A's": 60, "Not": 440},})

#Total sum per column: 
df.loc['Total',:]= df.sum(axis=0)

#Total sum per row: 
df.loc[:,'Total'] = df.sum(axis=1)