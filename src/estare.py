import numpy as np
from init import examine
from feature import extract
from align import *

from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(prog='estare', description='''Program for aligning and stacking astro photos.''',
                                 epilog='''estare is a Persian word for star.''')

sub_parsers = parser.add_subparsers()

# create the parser for the feature detection command
parse_feature = sub_parsers.add_parser('scan', help='''Scan an input image to find suitable features such as (a) bright 
                                        star(s) that can be used for aligning multiple frames.''')

parse_feature.add_argument('image', action='store', type=str, help='The input image to be scanned.')
parse_feature.add_argument('kapa', action='store', type=float, help='''Threshold for picking pixels of a certain  
                            brightness. It takes a floating point values from the range [0, 1]. Pick a larger value to
                            limit the detected features to those of a higher brightness.''')
parse_feature.set_defaults(Mode='scan')

parse_stack = sub_parsers.add_parser('stack', help='''This mode should normally be used after the alignment features
                                        have been detected in the scan mode. The stack mode uses the coordinates of the 
                                        features to align two images. It then stacks them up. Two input images along 
                                        with one identical feature for each image are required.''')

parse_stack.add_argument('layer_1', help='Path and name of the reference image (base layer)')
parse_stack.add_argument('layer_2', help='Path and name of the second image (top layer)')
parse_stack.add_argument('feature_1', help='''Path and name of a .npy file containing the coordinates of the feature in 
                            the reference layer''')
parse_stack.add_argument('feature_2', help='''Path and name of a .npy file containing the coordinates of the feature in
                            the second layer which will be lined up with the identical feature in the reference 
                            layer.''')
parse_stack.set_defaults(Mode='stack')

args = parser.parse_args()

if args.Mode == 'scan':
    imagePath = args.image
    threshold = args.kapa

    img_as_array, x_range, y_range = examine(imagePath, save=True, verbose=False, graphics=False)

    print(f'Image has x-range = {x_range}, and y-range = {y_range}')

    imgGray = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale

    fig2, frame = plt.subplots(1, 1)
    image_features = frame.imshow(imgGray, cmap='gray')
    frame.set_title('Marked features', fontsize=14)

    numFeatures, indices, markers = extract(imgGray, xRng=[0, x_range], yRng=[0, y_range],
                                            kapa=threshold)

    print(f'''
        Total number of features detected: {numFeatures}. If this is too many, consider increasing  
        the threshold input.
    ''')

    # Loop over features and ask the user if a feature is of interest to be saved
    keepFeature = False
    selectedFeatures = 0  # counter
    refusedFeatures = 0  # counter
    # TODO: add a feature to use matplotlib.ginput
    if numFeatures > 0:
        print('''A detected feature is displayed by a black square. Press any key to save the current feature, or click 
                the mouse to discard it...''')
        for pair_0, pair_1 in zip(indices[0], indices[1]):
            if pair_0 > 3 and pair_1 > 3:
                arrow = frame.annotate('O', xy=(pair_1, pair_0), arrowprops=dict(arrowstyle='->'))
                plt.draw()  # , plt.pause(0.01)
                btnpress = plt.waitforbuttonpress(-1)
                if btnpress:
                    selectedFeatures += 1
                    np.save('../data/features/feature_{}'.format(selectedFeatures), [pair_0, pair_1])
                    # TODO: Find install path and cd to data
                    plt.waitforbuttonpress(0.1)
                else:
                    refusedFeatures += 1
                    np.save('../data/refuse/refused_{}'.format(refusedFeatures), [pair_0, pair_1])
                arrow.remove()   # removing the arrow must be the last thing to do at the end of the if-block

    print('Feature detection completed.')
    plt.show()

elif args.Mode == 'stack':
    img_1 = args.layer_1
    img_2 = args.layer_2
    pivot_1 = args.feature_1
    pivot_2 = args.feature_2

    align(img_1, img_2, pivot_1, pivot_2)
