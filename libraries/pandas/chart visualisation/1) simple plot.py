import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")


# basic plotting
ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
ts = ts.cumsum()
ts.plot()


# same as above but 4 different series
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
df = df.cumsum()
plt.figure()
df.plot()

# plot y against x
df3 = pd.DataFrame(np.random.randn(1000, 2), columns=["B", "C"]).cumsum()
df3["A"] = pd.Series(list(range(len(df))))
df3.plot(x="A", y="B");