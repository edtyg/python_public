import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(
    {
     "a": np.random.randn(1000) + 1,
     "b": np.random.randn(1000),
     "c": np.random.randn(1000) - 1
    },
    columns=["a", "b", "c"],
)

plt.figure()

# plot histogram
df.plot.hist(alpha=0.5)

# plot stacked histogram
df.plot.hist(stacked=True, bins=20);

# plot horizontal histogram
df["a"].plot.hist(orientation="horizontal", cumulative=True);
