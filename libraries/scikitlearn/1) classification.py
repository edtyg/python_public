import seaborn as sns

iris = sns.load_dataset('iris')

sns.pairplot(iris, hue = 'species')

y_var = iris['species'] # categorial y variable
x_var = iris.drop(columns = 'species')