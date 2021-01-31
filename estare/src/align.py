from skimage import io
from skimage import img_as_float as imfloat
import numpy as np
from matplotlib import pyplot as plt

from src.init import examine
from src.rotate import rotate


# Fine-tuning
# - pick features from scattered regions
# - characterize error: does it vary if one goes towards the edges or far from the origin?
# - compare light curves and make adjustments if the stacked feature deviates too much

def align(image_1, image_2, pivot_1, pivot_2):
  
    img_1, x_range_1, y_range_1 = examine(image_1)  
    img_2, x_range_2, y_range_2 = examine(image_2)

    # TODO: How to raise error here?
    # if (x_range_1 != x_range_2) or (y_range_1 != y_range_2):
    #     #TODO: raise error and exit
    #     pass   # JUST FOR NOW!
    
    # two reference points for alignment
    coord_1 = np.load(pivot_1)
    a_1 = coord_1[0]
    b_1 = coord_1[1]
    
    # two target points that should match the reference points after alignment
    coord_2 = np.load(pivot_2)  
    a_2 = coord_2[0]
    b_2 = coord_2[1]

    # Use the two points to back calculate the angle of rotation
    slope_bef = ( b_1[1] - a_1[1] )/( b_1[0] - a_1[0] )
    
    slope_aft = ( b_2[1] - a_2[1] )/( b_2[0] - a_2[0] )

    theta = ( ((np.arctan(slope_aft))*180/np.pi) -
              ( (np.arctan(slope_bef))*180/np.pi ) )

    a2_derot = rotate(a_2, -theta, discrete=False)   # set discrete=False to get an exact value

    # compare the derotated one from its origin to calculate the relative translation magnitude 
    dxp = a2_derot[0] - a_1[0]
    dyp = a2_derot[1] - a_1[1]

    # Using the formulae, compute the absolute translation magnitude
    theta_rad = -theta * np.pi / 180   # radians

    del_y = ( dyp - dxp*np.tan(theta_rad) ) / \
            (np.sin(theta_rad)*np.tan(theta_rad) + np.cos(theta_rad))

    del_x = (dxp + del_y*np.sin(theta_rad)) / np.cos(theta_rad)
    
    # Allocate x- and y-array for holding the new coordinates after offseting
    x_array = np.zeros((x_range_1, y_range_1, 1), dtype=int)
    y_array = np.zeros((x_range_1, y_range_1, 1), dtype=int)


    # For the two following time-consuming loops, we need unit tests to ensure the correctness after each optimization:
    # Now we can detranslate all points
    for i in range(x_range_1):
        for j in range(y_range_1):
            x_array[i, j] = i-del_x
            y_array[i, j] = j-del_y
    
    # and now we can derotate them 
    for i in range(x_range_1):
        for j in range(y_range_1):
            uncorrected_coor = [x_array[i, j], y_array[i, j]]
            corrected_coor = rotate(uncorrected_coor, -theta, discrete=True)
            
            x_array[i, j] = corrected_coor[0]
            y_array[i, j] = corrected_coor[1]

            # stack
            if x_array[i, j] > 0 and x_array[i, j] < x_range_1 and y_array[i, j] > 0 and y_array[i, j] < y_range_1:
                img_1[x_array[i, j], y_array[i, j]] += img_2[i, j]   # Broadcasting to all three channels is implicit

    #io.imsave('/home/minter/workdir/Central_backup/Pictures/Test_images_for_estare_Ramberget_Dec_2020/estare_stacked.JPG', img_1)

    # # recons = imread('/home/minter/workdir/Central_backup/Pictures/Test_images_for_estare_Ramberget_Dec_2020/DSC00281_aligned.JPG')





    
