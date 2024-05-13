import seaborn as sns


iris = sns.load_dataset('iris')
titanic = sns.load_dataset('titanic')

sns.pairplot(iris)
sns.pairplot(titanic)