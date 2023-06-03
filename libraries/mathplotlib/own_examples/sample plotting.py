import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0,10,1000) # data

plt.style.use('ggplot')

fig = plt.figure()
ax = plt.axes()

ax.plot(x, np.sin(x), color = 'r', linestyle = 'solid', label = 'sin(x)')
ax.plot(x, np.cos(x), color = 'b', linestyle = 'dotted', label = 'cos(x)')

plt.ylim(-1,1)
plt.xlim(0,5)

plt.title('charting')
plt.ylabel('y')
plt.xlabel('x')

plt.legend()