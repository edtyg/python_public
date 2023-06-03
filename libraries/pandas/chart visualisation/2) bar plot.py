import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# creating a df
df = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
print(df)

# bar plot - 1 row of data
plt.figure()
df.iloc[5].plot.bar()
plt.axhline(0, color="k")


# bar plot - all 10 rows of data
df.plot.bar()


# bar plot - all 10 rows of data - stacked
df.plot.bar(stacked = True)


# horizontal bar plot - all 10 rows of data - stacked 
df.plot.barh(stacked = True)
