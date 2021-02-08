import numpy as np
from src import align

from reference_markers import reference_markers 

targets, markers = reference_markers()

del_x, del_y, theta, theta_rad = align.find_offset('./tests/pivot.npy', './tests/target.npy')

test_size=4
x_array = np.zeros( (test_size, test_size), dtype=float )
y_array = np.zeros( (test_size, test_size), dtype=float )

for i in range(test_size):
    x_array[:,i] = [0, 1, 2, 3]
    y_array[i,:] = [0, 1, 2, 3]

x_array_, y_array = align.derotate(x_array, y_array, theta, roundup=False)

print(x_array)

print(y_array)
