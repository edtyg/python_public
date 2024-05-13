import numpy as np

a1 = np.array(
    [
     [18, 26, 17], 
     [25, 15.5, 12], 
     [24, 27, 20],
     [10, 5.5, 17],
     [27, 26, 15],
     [22, 21, 21],
     ]
    ) 


print(a1*2)
print(1/a1)

# arithmetic operations
np.add(a1,1)

np.subtract(a1,1)

np.negative(a1)

np.multiply(a1,2)

np.divide(a1,2)

np.floor_divide(a1,2)

np.power(a1,2)

np.mod(a1,2) # remainder


# other functions
np.min(a1)
np.max(a1)
np.mean(a1)
np.median(a1)

# sort
np.sort(a1, axis = 0) # sort by col
np.sort(a1, axis = 1) # sort by row
