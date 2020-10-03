import numpy as np
from init import examine
from feature import extract
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='''
Process the input image to detect features that can be used for aligning it with a 
second one when it is desired to stack them on top of each other.
''', epilog='''estare is a Persian word for star.''')

parser.add_argument('image', action='store', type=str)
parser.add_argument('kapa', action='store', type=float)
args=parser.parse_args()

imagePath = args.image
threshold = args.kapa

img_as_array, x_range, y_range = examine(imagePath, save=True, verbose=False, graphics=False)

print(f'Image has x-range = {x_range}, and y-range = {y_range}')

imgGray  = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale

fig2, frame = plt.subplots(1,1)
image_features = frame.imshow(imgGray, cmap='gray')
frame.set_title('Marked features', fontsize=14)

numFeatures, indices, markers = extract( imgGray, xRng=[0, x_range], yRng=[0, y_range],
                                         kapa=threshold )

print(f'Total number of features detected: {numFeatures}')

# Loop over features and ask the user if a feature is of interest to be saved
keepFeature = False
selectedFeatures = 0 #counter
#TODO: add a feature to use matplotlib.ginput
if numFeatures > 0:
    print('Press any key to save the current feature, or click the mouse to discard it...')
    for pair_0, pair_1 in zip(indices[0], indices[1]):
        if pair_0 > 3 and pair_1 > 3:
            imgGray[pair_0-4:pair_0+4, pair_1-4:pair_1+4] = 0
            image_features.set_data(imgGray)
            image_features.autoscale()
            plt.draw()  #, plt.pause(0.01)
            btnpress = plt.waitforbuttonpress(-1) 
            if btnpress:                
                selectedFeatures += 1
                np.save('./data/feature_{}'.format(selectedFeatures), indices)
                plt.waitforbuttonpress(0.1)

            #right.annotate('O', xy = (pair_1, pair_0), arrowprops=dict(arrowstyle='->'))               

print('Feature detection completed.')
plt.show()



