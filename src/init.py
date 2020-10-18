from skimage import io, data
import numpy as np
from matplotlib import pyplot as plt
from skimage import img_as_float as imfloat


def examine(imagePath, save=False, verbose=False, graphics=False):
    image = imfloat(io.imread(imagePath))

    if verbose:
        np.set_printoptions(precision=2, linewidth=155)
        
        print('Image type: ', type(image))
        print('Image datatype: ', image.dtype)
        print('Image shape: ', image.shape)

    if graphics:
        gridShow = False
        fig, ax1 = plt.subplots(1, 1)

        # TODO: can we expand imagePath and loop over if it has more than 1 path?
        ax1.imshow(image, cmap='gray')
        ax1.set_title('Input image', fontsize=14)
        ax1.grid(gridShow)
        plt.show()

    # save the image
    if save:
        np.save('../data/input_image', image)   # TODO: Find the installation path; then cd to data/

    # return the x, and y ranges
    x_max = image.shape[1]
    y_max = image.shape[0]

    return image, x_max, y_max


if __name__ == '__main__':
    image, x_range, y_range = examine('./tests/test.jpg', save=False, verbose=True, graphics=False)
    print(f'Image has x-range = {x_range}, and y-range = {y_range}')
    
    imgGray = image @ [0.2126, 0.7152, 0.0722]  # image in grayscale

    gridShow = False
    fig, ax1 = plt.subplots(1, 1)

    ax1.imshow(imgGray, cmap='gray')
    ax1.set_title('Test image', fontsize=14)
    ax1.grid(gridShow)
    plt.show()
