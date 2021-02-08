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
