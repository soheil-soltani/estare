from skimage import io
from skimage import img_as_float as imfloat
import numpy as np
from matplotlib import pyplot as plt


def align():
    img_1 = imfloat(io.imread('tests/IMG_1735.JPG'))
    img_2 = imfloat(io.imread('tests/IMG_1736.JPG'))

    coord_1 = np.load('data_layer1/feature_1.npy')
    coord_2 = np.load('data_layer2/feature_1.npy')

    print(f'x1 = {coord_1[1]}; y1 = {coord_1[0]}')
    print(f'x2 = {coord_2[1]}; y2 = {coord_2[0]}')

    x_range = 2256
    y_range = 1504

    stacked = np.zeros( (y_range, x_range, 3), dtype=float)
    del_x = coord_2[1] - coord_1[1]
    del_y = coord_2[0] - coord_1[0]

    # for i in range(abs(del_x), x_range):
    #     for j in range(abs(del_y), y_range):
    #         stacked[j-del_y, i-del_x] = 1.0 #img_2[j, i, 0]

    for i in range(y_range-abs(del_y)):
        for j in range(abs(del_x), x_range):
            stacked[i - del_y, j - del_x, 0] = img_2[i, j, 0] + img_1[i - del_y, j - del_x, 0]
            stacked[i - del_y, j - del_x, 1] = img_2[i, j, 1] + img_1[i - del_y, j - del_x, 1]
            stacked[i - del_y, j - del_x, 2] = img_2[i, j, 2] + img_1[i - del_y, j - del_x, 2]

    fig, (top, mid, bot) = plt.subplots(3, 1)
    top.imshow(img_1)
    mid.imshow(img_2)
    bot.imshow(stacked)
    plt.show()
