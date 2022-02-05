
import numpy as np
from estare.src.rotate import rotate_vectorized
import skimage.transform as trf
import skimage.io as io

def stack(img_1, img_2, x_array, y_array, x_range, y_range, deflection, discrete=True):
    """ theta was changed to deflection
    """
    
    ###angle_matrix = np.load('../aux/angle_table.npy')
    ###norm_matrix  = np.load('../aux/norm_matrix.npy')
    ###rho = norm_matrix[i, j]
    ###theta = angle_matrix[i, j]
    
    #x_corrected, y_corrected = rotate_vectorized(x_array, y_array, -deflection, origo=np.array([0., 0.]), radians=False, discrete=discrete)
    #rotate using skimage
    img_2 = trf.rotate(img_2, deflection, center=(0,0), resize=True)
    ###img_2 = trf.resize(img_2, [640, 960], mode='constant', preserve_range=True, anti_aliasing=True) 
    #img_3 = img_1 + img_2   #np.ubyte(0.5*img_1 + 0.5*img_2)
    # img_3 = img_2[0:x_range, 0:y_range]   #np.ubyte(0.5*img_1 + 0.5*img_2)
    # for i in range(x_range):
    #     for j in range(y_range):
    #         img_3[i,j] += img_1[i,j]
            
    io.imsave('./estare_derotated.jpeg', img_2)
    
    # for i in range(x_range):
    #     for j in range(y_range):
    #         # stack needs unittesting if the stacking algorithm is to be changed+
    #         #if x_array[i, j] > 0 and x_array[i, j] < x_range and y_array[i, j] > 0 and y_array[i, j] < y_range:
    #         #    img_1[x_array[i, j], y_array[i, j]] += img_2[i, j]   # Broadcasting to all three channels is implicit
    #         # Can this be vectorized too?    
    #         if (x_corrected[i,j] > 0) and (x_corrected[i,j] < x_range) and (y_corrected[i,j] > 0) and (y_corrected[i,j] < y_range):
    #             img_1[int(x_corrected[i,j]), int(y_corrected[i,j])] += img_2[i, j]   # Broadcasting to all three channels is implicit

    return img_1
                
            
