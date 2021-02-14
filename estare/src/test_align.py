import unittest
import numpy as np

import align

#from reference_markers import reference_markers 


class TestAlign(unittest.TestCase):

    def test_offset(self):
        #targets, markers = reference_markers()

        del_x, del_y, theta, theta_rad = align.find_offset('../tests/pivot.npy',
                                                           '../tests/target.npy')

        self.assertAlmostEqual(del_x, 26.74381464587602,
                               msg="Offset in the x-dir. is wrong.")
        
        self.assertAlmostEqual(del_y, -5.370829292101147,
                               msg="Offset in the y-dir. is wrong.")
        
        self.assertAlmostEqual(theta, 0.481598055901971,
                               msg="Rotation angle in degrees is wrong.")
        
        self.assertAlmostEqual(theta_rad, -0.008405471746693104,
                               msg="Rotation angle n radians is wrong.")


    def test_detrans(self):

        x_range = 400
        y_range = 300
        
        x_array = np.ones((x_range, y_range), dtype=int)
        y_array = np.ones((x_range, y_range), dtype=int)

        del_x = 1
        del_y = 1

        x_detrans, y_detrans = align.detrans(x_array, y_array, x_range,
                                             y_range, del_x, del_y)
        
        self.assertEqual(x_detrans[0, 0], -1)
        
        
    def test_derotate(self):
      
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
        
        x_desired = np.array([[0, 0.00840537, 0.01681075, 0.02521612],
                     [0.99996467, 1.00837005, 1.01677542, 1.02518079],
                     [1.99992935, 2.00833472, 2.01674009, 2.02514547],
                     [2.99989402, 3.0082994, 3.01670477, 3.02511014]])
        
        y_desired = np.array( [[None, 0.99996467, 1.99992935, 2.99989402],
                               [-0.00840537, 0.9915593, 1.99152398, 2.99148865],
                               [-0.01681075, 0.98315393, 1.9831186, 2.98308328],
                               [-0.02521612, 0.97474856, 1.97471323, 2.9746779]] )
    
    
        np.testing.assert_almost_equal(x_array[1:, 1:], x_desired[1:, 1:])
        np.testing.assert_almost_equal(y_array[1:, 1:], y_desired[1:, 1:])
