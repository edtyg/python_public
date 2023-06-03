import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.DataFrame(np.random.rand(10, 5), columns=["A", "B", "C", "D", "E"])

plt.figure()

# plot box plot
df.plot.box()


# box plot with some customization
color = {
    "boxes": "DarkGreen",
    "whiskers": "DarkOrange",
    "medians": "DarkBlue",
    "caps": "Gray",
}

df.plot.box(color=color, sym="r+");


# plot horizontal box plots
df.plot.box(vert=False, positions=[1, 4, 5, 6, 8]);


# box plot grouped
df = pd.DataFrame(np.random.rand(10, 2), columns=["Col1", "Col2"])
df["X"] = pd.Series(["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"])
plt.figure()

bp = df.boxplot(by="X")