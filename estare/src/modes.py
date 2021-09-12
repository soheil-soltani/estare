"""This module should be imported by the entry-point script.

It implements the functions scan() and assemble(). The former 
is used for detecting features that are suitable for aligning 
two images. The latter proceeds to the alignment and stacking 
steps.
"""

from estare.src.align import align
from estare.src.init import examine, setup

from matplotlib import pyplot as plt
from skimage.io import imsave

import estare.scan.cutoff as cutoff 
import estare.scan.feature as  feature

import os
import numpy as np


def scan(args):
    """Finds features that are suitable for aligning two images.

    This function shows the input image in a graph first. It then 
    goes through every pixel of it and compares its brightness with 
    a given threshold (kapa) specified by the user. If the pixel's 
    brightness is higher than or equal to the threshold, a marker 
    will be shown on that location in the graph and the user can 
    accept it as a feature by pressing any key. The pixel can 
    alternatively be discarded by a left click.

    Args:
        args : user inputs parsed by argparse
    """
    
    # handle input arguments
    imagePath = args.image
    info_only = args.info_only   # just check image properties and skip feature detection
    save_pixs = args.save_pxs    # save also the pixel values
    save_gifs = args.save_gif    # save the features as PNG too
    
    if (info_only):
        img_as_array, x_range, y_range = examine(imagePath, verbose=True, graphics=False)
        return 
    else:
        setup()   # setup the program directory structure
        img_as_array, x_range, y_range = examine(imagePath, verbose=False, graphics=False)
    # Replace with:
    # img_as_array = FloatImage(imagePath)
    # img_as_array.print_info()
    # img_as_array.save()
    # x_range, y_range = img_as_array.size()

    imgGray = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale
    # Replace with (makes FloatImage redundant):
    # imgGray = GrayImage(imagePath)
    # imgGray.print_info()
    # imgGray.save()
    # x_range, y_range = imgGray.size()

    fig2, frame = plt.subplots(1, 1)
    image_features = frame.imshow(imgGray, cmap='gray')
    frame.set_title('Marked features', fontsize=14)
    #TODO: Parse threshold in the beginning of the function
    if args.kapa != None:
        threshold = args.kapa
    else:
        threshold = cutoff.find_threshold(imgGray, x_range, y_range)
        
    numFeatures, indices, markers = feature.extract(imgGray, xRng=[0, x_range], yRng=[0, y_range],
                                            kapa=threshold)
    # Replace with:
    # numFeatures, indices, markers = imgGray.extract(xRng=[0, x_range], yRng=[0, y_range], kapa=threshold)

    print(f'''Total number of features detected: {numFeatures} (cutoff brightness = {threshold}). 
              If this is too many, consider increasing the threshold input.''')

    # Loop over features and ask the user if a feature is of interest to be saved            
    selectedFeatures = 0  # counter
    refusedFeatures  = 0  # counter

    xy_FeatureCount = 0   # number of already-saved feature coordinates initialized to zero
    binFeatureCount = 0   # number of already-saves feature images in binary format initialized to zero
    imgFeatureCount = 0   # number of already-saves feature images in .png format initialized to zero
    
    # TODO: add a feature to use matplotlib.ginput
    if numFeatures > 0:
        print('''A detected feature is displayed by a black square. Press any key to save the current feature, or click 
        the mouse to discard it...''')
        for pair_0, pair_1 in zip(indices[0], indices[1]):
            if pair_0 > 3 and pair_1 > 3:
                arrow = frame.annotate('O', xy=(pair_1, pair_0), arrowprops=dict(color='lime',arrowstyle='->'))
                plt.draw()  # , plt.pause(0.01)
                btnpress = plt.waitforbuttonpress(-1)
                if btnpress:
                    selectedFeatures += 1
                    np.save('./estare_data/features/coordinates/feature_{}'.format(xy_FeatureCount), [pair_0, pair_1])
                    xy_FeatureCount += 1
                    if save_pixs:
                        np.save('./estare_data/features/pixels/feature_{}_pixels'.format(binFeatureCount), \
                                imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                        binFeatureCount += 1
                    if save_gifs:
                        imsave('./estare_data/features/feature_{}.png'.format(imgFeatureCount), \
                               imgGray[pair_0-10:pair_0+10, pair_1-10:pair_1+10])
                        imgFeatureCount += 1
                        
                    plt.waitforbuttonpress(0.1)

                arrow.remove()   # removing the arrow must be the last thing to do at the end of the if-block
                
    print('Feature detection completed.')
    plt.show()


def assemble(args):
    """unpacks input arguments, then passes them to align() 

    This function prepares the input arguments to be passed to align() 
    for the algorithm to proceed to alignment and then stacking steps.

    Args:
        args : input arguments parsed by argparse
    """

    # TODO: design a stack-only mode that bypasses alignment
    
    # unpack the arguments
    img_1 = args.layer_1
    img_2 = args.layer_2
    pivot_1 = args.feature_1
    pivot_2 = args.feature_2

    # align and stack the two input frames
    stacked_frame = align(img_1, img_2, pivot_1, pivot_2, save=True)
    
