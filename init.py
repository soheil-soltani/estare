from feature import extract
from skimage import io, data
import numpy as np
from matplotlib import pyplot as plt
from skimage import img_as_float as imfloat
from skimage import filters


def examine( imagePath, verbose=False, graphics=False ):
    image = imfloat( io.imread( imagePath ) )

    if verbose:
        np.set_printoptions( precision = 2,
                             linewidth = 155 )
        
        print('Image type: ', type(image))
        print('Image datatype: ', image.dtype)
        print('Image shape: ', image.shape)

    if graphics:
        gridShow = 'off'
        fig, ax1 = plt.subplots(1,1)

        # TODO: can we expand imagePath and loop over if it has more than 1 path?
        ax1.imshow(image_1)
        ax1.set_title('Orion_1', fontsize=14)
        #ax1.axis('off')
        ax1.grid(gridShow)
        plt.show()

    # save the image
    np.save('image', image)

    # return the x, and y ranges
    x_max = image.shape[0]
    y_max = image.shape[1]

    return image, x_max, y_max
    
 
    






