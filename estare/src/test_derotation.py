import numpy as np
import align

#from reference_markers import reference_markers 

#targets, markers = reference_markers()

del_x, del_y, theta, theta_rad = align.find_offset('../tests/pivot.npy', '../tests/target.npy')

test_size=4
x_array = np.zeros( (test_size, test_size), dtype=float )
y_array = np.zeros( (test_size, test_size), dtype=float )


for i in range(test_size):
    x_array[:,i] = [0, 1, 2, 3]
    y_array[i,:] = [0, 1, 2, 3]

#TODO: rotate/derotate should not be applied to the anchor (origin)
x_array_, y_array = align.derotate(x_array, y_array, theta, roundup=False)

print(x_array)

print(y_array)

# [[       nan 0.00840537 0.01681075 0.02521612]
#  [0.99996467 1.00837005 1.01677542 1.02518079]
#  [1.99992935 2.00833472 2.01674009 2.02514547]
#  [2.99989402 3.0082994  3.01670477 3.02511014]]
# [[        nan  0.99996467  1.99992935  2.99989402]
#  [-0.00840537  0.9915593   1.99152398  2.99148865]
#  [-0.01681075  0.98315393  1.9831186   2.98308328]
#  [-0.02521612  0.97474856  1.97471323  2.9746779 ]]
