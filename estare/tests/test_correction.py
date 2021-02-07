import unittest
import numpy as np

from estare.src import align

print(align.__file__)

class TestAlign(unittest.TestCase):
    @profile
    def test_detrans(self):

        x_range = 4000
        y_range = 3000
        
        x_array = np.ones((x_range, y_range), dtype=int)
        y_array = np.ones((x_range, y_range), dtype=int)

        del_x = 1
        del_y = 1

        counts = 1000000   # no. iterative fcn. call for performance measurements
        for i in range(counts):
            x_detrans, y_detrans = align.detrans(x_array, y_array, x_range, y_range, del_x, del_y)
        
        self.assertEqual(x_detrans[0, 0], -1)
        
# # The following cqn be used to test the correction algorithm:

# # two reference points for alignment
#     coord_1 = np.load('pivot_1.npy')
#     a_1 = coord_1[0]
#     b_1 = coord_1[1]
    
#     # two target points that should match the reference points after alignment
#     coord_2 = np.load('pivot_2.npy')  
#     a_2 = coord_2[0]
#     b_2 = coord_2[1]
    
#     print(f'x1 = {a_1[0]}; y1 = {a_1[1]}')
#     print(f'x2 = {b_1[0]}; y2 = {b_1[1]}')    
#     print(f'x_p1 = {a_2[0]}; y_p1 = {a_2[1]}')   # [x', y'] of target no. 1
#     print(f'x_p2 = {b_2[0]}; y_p2 = {b_2[1]}')   # [x', y'] of target no. 2

    
#     a2_detran = [ a_2[0] - del_x, a_2[1] - del_y ]
#     b2_detran = [ b_2[0] - del_x, b_2[1] - del_y ] 
  
#     a2_detran_derot = rotate(a2_detran, -theta, discrete=True)
#     b2_detran_derot = rotate(b2_detran, -theta, discrete=True)
#     print(f'a2_corrected: {a2_detran_derot}')
#     print(f'ab_corrected: {b2_detran_derot}')



#     print('Presum. right one:', x_array[a_2[0], a_2[1]], y_array[a_2[0], a_2[1]])

if __name__ == '__main__':
    unittest.main()
