import matplotlib.pyplot as plt
import numpy as np

### line chart ###
step = 1
x = np.arange(0, 5+step, step)
y = np.exp(x)

plt.figure(figsize=(10, 7))
plt.plot(x, y, color = 'r', alpha = 0.5, label = '1')      #label 1
plt.plot(x, y+10, color = 'b', alpha = 0.5, label = '2')   #label 2
plt.xlabel('X axis', fontsize = 20)
plt.ylabel('Y axis', fontsize = 20)
plt.title('Line Graph', fontsize=20)
plt.legend(fontsize = 20) # need label for legend
plt.show()


### Scatter chart ###
step = 1
x = np.arange(0, 5+step, step)
y = np.exp(x)

plt.figure(figsize=(10, 7))
plt.scatter(x, y, color = 'r', alpha = 0.5, label = '1')      #label 1
plt.scatter(x, y+10, color = 'b', alpha = 0.5, label = '2')   #label 2
plt.xlabel('X axis', fontsize = 20)
plt.ylabel('Y axis', fontsize = 20)
plt.title('Line Graph', fontsize=20)
plt.legend(fontsize = 20) # need label for legend
plt.show()


### Bar chart ###
# for multiple bars
step = 1
x = np.arange(0, 5+step, step)
y = np.exp(x)

width = 0.35  # the width of the bars
plt.figure(figsize=(10, 7))
plt.bar(x + width/2, y, color = 'r', width = width, alpha = 0.5, label = '1',)      #label 1
plt.bar(x - width/2, y, color = 'b', width = width, alpha = 0.5, label = '2')   #label 2
plt.xlabel('X axis', fontsize = 20)
plt.ylabel('Y axis', fontsize = 20)
plt.title('Line Graph', fontsize=20)
plt.legend(fontsize = 20) # need label for legend
plt.show()
