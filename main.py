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

img_as_array, x_range, y_range = examine(imagePath, verbose=False, graphics=False)
imgGray  = img_as_array @ [0.2126, 0.7152, 0.0722]  # image in grayscale

print(f'The input image has x_range = {x_range}, and y_range = {y_range}')


x_factor = x_range // 30
y_factor = y_range // 30

discret_x = np.linspace(0, x_range, x_factor)
discret_y = np.linspace(0, y_range, y_factor)

x_pair = list(zip(discret_x[0:-1], discret_x[1:]))
y_pair = list(zip(discret_y[0:-1], discret_y[1:]))

fig2,(left, right) = plt.subplots(1,2)
left.imshow(imgGray)
left.set_title('Raw image', fontsize=14)

for x in x_pair:
    for y in y_pair:

        numFeatures, indices, markers = extract( imgGray,
                                                 xRng=[int(x[0]), int(x[1])],
                                                 yRng=[int(y[0]), int(y[1])],
                                                 kapa=threshold )
        
        imgGray[ int(x[0]):int(x[1]), int(y[0]):int(y[1]) ] = markers[:, :]
        

right.imshow(imgGray)
right.set_title('Marked features', fontsize=14)
plt.show()
        
# now continue tiling up the image in intervals of 30 x 30 pixels


