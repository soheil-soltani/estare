from skimage import io
from skimage import img_as_float as imfloat
import numpy as np
from matplotlib import pyplot as plt


def align(image_1, image_2, pivot_1, pivot_2):
  
    img_1 = imfloat(io.imread(image_1))  # 'tests/IMG_1740.JPG'
    img_2 = imfloat(io.imread(image_2))  # 'tests/IMG_1741.JPG'

    coord_1 = np.load(pivot_1)  # 'data_new_layer_1/feature_1.npy'
    coord_2 = np.load(pivot_2)  # 'data_new_layer_2/feature_1.npy'

    print(f'x1 = {coord_1[1]}; y1 = {coord_1[0]}')
    print(f'x2 = {coord_2[1]}; y2 = {coord_2[0]}')

    # TODO: x_range and y_range should be inferred
    x_range = 2256
    y_range = 1504

    # TODO: number of layers (3) must be inferred
    stacked = np.zeros((y_range, x_range, 3), dtype=float)
    del_x = coord_2[1] - coord_1[1] 
    del_y = coord_2[0] - coord_1[0] 

    for i in range(x_range):
        for j in range(y_range):
            stacked[j, i, 0] = img_1[j, i, 0]
            stacked[j, i, 1] = img_1[j, i, 1]
            stacked[j, i, 2] = img_1[j, i, 2]

    for i in range(y_range-abs(del_y)):
        for j in range(abs(del_x), x_range):            
            stacked[i, j, 0] += img_2[i+del_y, j+del_x, 0] 
            stacked[i, j, 1] += img_2[i+del_y, j+del_x, 1] 
            stacked[i, j, 2] += img_2[i+del_y, j+del_x, 2] 

    fig, ((frame, signal), (pile, dummy)) = plt.subplots(2, 2)
    frame.imshow(img_1)
    frame.set_title('Original')

    signal.plot(img_1[coord_1[0], coord_1[1]-10:coord_1[1]+10, 0], 'b', label='original')
            
    signal.plot(stacked[coord_1[0], coord_1[1]-10:coord_1[1]+10, 0]/2.0, 'k', label='del_x fr. feat.')
    
    signal.grid('True')
    signal.legend()

    pile.imshow(stacked)
    pile.set_title('Stacked')
    
    plt.show()    

    # TODO: Clip the final image to remove the edge bands

    
def mismatch(parameters):
    m, n = parameters
    img_1 = imfloat(io.imread('tests/IMG_1735.JPG'))
    img_2 = imfloat(io.imread('tests/IMG_1736.JPG'))

    coord_1 = np.load('data_layer1/feature_1.npy')
    coord_2 = np.load('data_layer2/feature_1.npy')

    x_range = 2256
    y_range = 1504

    stacked = np.zeros((y_range, x_range, 3), dtype=float)
    del_x = (coord_2[1] - coord_1[1]) + int(round(m))
    del_y = (coord_2[0] - coord_1[0]) + int(round(n))

    for i in range(y_range-abs(del_y)):
        for j in range(abs(del_x), x_range):
            stacked[i - del_y, j - del_x, 0] = img_2[i, j, 0] + img_1[i - del_y, j - del_x, 0]
            stacked[i - del_y, j - del_x, 1] = img_2[i, j, 1] + img_1[i - del_y, j - del_x, 1]
            stacked[i - del_y, j - del_x, 2] = img_2[i, j, 2] + img_1[i - del_y, j - del_x, 2]

    errorRed = stacked[:, :, 0] - img_1[:, :, 0]
    errorGreen = stacked[:, :, 1] - img_1[:, :, 1]
    errorBlue = stacked[:, :, 2] - img_1[:, :, 2]

    error = (np.sum(errorRed) + np.sum(errorGreen) + np.sum(errorBlue))/np.sum(img_1[...])

    return error


def align_archived():
    # img_1 = imfloat(io.imread('tests/IMG_1735.JPG'))
    # img_2 = imfloat(io.imread('tests/IMG_1736.JPG'))

    img_1 = imfloat(io.imread('tests/IMG_1740.JPG'))
    img_2 = imfloat(io.imread('tests/IMG_1741.JPG'))

    coord_1 = np.load('data_new_layer_1/feature_1.npy')
    coord_2 = np.load('data_new_layer_2/feature_1.npy')

    print(f'x1 = {coord_1[1]}; y1 = {coord_1[0]}')
    print(f'x2 = {coord_2[1]}; y2 = {coord_2[0]}')

    x_range = 2256
    y_range = 1504

    stacked = np.zeros((y_range, x_range, 3), dtype=float)
    del_x = 0   # coord_2[1] - coord_1[1] #- 2
    del_y = 0   # coord_2[0] - coord_1[0] #+ 3

    # for i in range(abs(del_x), x_range):
    #     for j in range(abs(del_y), y_range):
    #         stacked[j-del_y, i-del_x] = 1.0 #img_2[j, i, 0]

    # x0 = np.array([1, 1])
    # res = argmin.minimize(mismatch, x0, method='nelder-mead', bounds=([-5, 5], [-5, 5]),
    #                       options={'xatol' : 1e-3, 'disp' : True})
    # print(res.x)

    # del_x += int(round(res.x[0])) 
    # del_y += int(round(res.x[1]))
    
    # for i in range(y_range-abs(del_y)):
    #     for j in range(abs(del_x), x_range):
    for i in range(abs(del_y), y_range):
        for j in range(x_range-abs(del_x)):
            stacked[i - del_y, j - del_x, 0] = img_2[i, j, 0] + img_1[i - del_y, j - del_x, 0]
            stacked[i - del_y, j - del_x, 1] = img_2[i, j, 1] + img_1[i - del_y, j - del_x, 1]
            stacked[i - del_y, j - del_x, 2] = img_2[i, j, 2] + img_1[i - del_y, j - del_x, 2]

    # fig, (top, mid, bot) = plt.subplots(3, 1)
    # top.imshow(img_1)
    # mid.imshow(img_2)
    # bot.imshow(stacked)
    fig, (frame, signal) = plt.subplots(1, 2)
    frame.imshow(stacked)
    frame.set_title('Original')
    signal.plot(img_1[coord_1[0], coord_1[1]-10:coord_1[1]+10, 0], 'b', label='original')

    del_x = 1
    del_y = 0

    for i in range(abs(del_y), y_range):
        for j in range(abs(del_x), x_range):
            stacked[i - del_y, j - del_x, 0] = img_2[i, j, 0] + img_1[i - del_y, j - del_x, 0]
            stacked[i - del_y, j - del_x, 1] = img_2[i, j, 1] + img_1[i - del_y, j - del_x, 1]
            stacked[i - del_y, j - del_x, 2] = img_2[i, j, 2] + img_1[i - del_y, j - del_x, 2]

    signal.plot(stacked[coord_1[0], coord_1[1]-10:coord_1[1]+10, 0]/2.0, 'r', label='del_x=1')

    del_x = coord_2[1] - coord_1[1] 
    del_y = 0   # coord_2[0] - coord_1[0]

    for i in range(abs(del_y), y_range):
        for j in range(x_range-abs(del_x)):
            stacked[i - del_y, j - del_x, 0] = img_2[i, j, 0] + img_1[i - del_y, j - del_x, 0]
            stacked[i - del_y, j - del_x, 1] = img_2[i, j, 1] + img_1[i - del_y, j - del_x, 1]
            stacked[i - del_y, j - del_x, 2] = img_2[i, j, 2] + img_1[i - del_y, j - del_x, 2]

    signal.plot(stacked[coord_1[0], coord_1[1]-10:coord_1[1]+10, 0]/2.0, 'k', label='del_x fr. feat.')
    signal.grid('True')
    signal.legend()
    plt.show()
