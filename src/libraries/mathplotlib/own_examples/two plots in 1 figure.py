import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# plt.style.use('classic')
plt.style.use('ggplot')

x = np.linspace(0,10,100)


# create plot figure
plt.figure()

plt.subplot(2,1,1) # row, col, panel
plt.plot(x, np.sin(x))

plt.subplot(2,1,2) # row, col, panel
plt.plot(x, np.cos(x))

plt.show()