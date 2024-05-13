import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


rng = np.random.RandomState(42)

x = 10 * rng.rand(50) # create x values
x = x[:,np.newaxis] # making x 2d array

y = 2*x-1+rng.randn(50) # create y values
plt.scatter(x,y) # plot sample data

model = LinearRegression(fit_intercept=True) # creating model


model.fit(x,y) # fit x and y
model.coef_ # c (y = mx + c)
model.intercept_ # m (y = mx + c)

xfit = np.linspace(-1,11) # creates new set of x variables to be fitted in model
xfit = xfit[:, np.newaxis] # makes x 2d array

yfit = model.predict(xfit) # y = mx + c

plt.scatter(x,y)
plt.scatter(xfit,yfit)