from skimage.io import imsave, imread
from skimage import img_as_float
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
'''
To detect if there has been any rotation:
1- calculate the initial angel of the feature in frame 0
2- calculate the del_x and del_y by comparing with the same feature in frame 1
3- shift the roigo in frame 1 by [del_x, del_y]
4- calculate the angel in frame 1 using the shifted origo

We need:
- a function to calculate angel recieves a reference(default 0, 0) and a feature coordinate
- a function that takes an angel and a pair of coordinates and rotates the point (below)
- a function that takes [del_x, del_y] and a pair of coordinates and translates the point (below)

___________________>  Y
|*
| *
|  *
|   *
|
v

X
'''

a = np.zeros( (400, 400), dtype=float )
#####position = np.array( [[50,50]] ).T
position = np.array( [[200,100]] ).T

position_1 = np.array( [[200,100]] ).T
position_2 = np.array( [[257,34]] ).T 
position_3 = np.array( [[20,30]] ).T

a[position_1[0], position_1[1]] = 0.5
a[position_2[0], position_2[1]] = 0.5
a[position_3[0], position_3[1]] = 0.5

fig, (axis1, axis2) = plt.subplots(1,2)
axis1.imshow(a)
axis1.set_title('Before')



rho = np.sqrt(position[0]**2 + position[1]**2)
alpha_0 = np.arccos(position[0]/rho)
alpha_0_deg = alpha_0*180.0/np.pi


def arc(position, origo=np.array([0, 0]), radians=False):
    '''
Returns the angle between the input coordinate and the vertical axis Y
'''
    rho = np.sqrt( (position[0]-origo[0])**2 + (position[1]-origo[1])**2 )
    angle = np.arccos( (position[0]-origo[0]) / rho )
    
    if radians==False:
        angle = angle*180.0/np.pi
        
    return angle

print(arc(position) )
print(arc(position, origo=np.array([0, -100])) )

# apply rotation
def rotate(position, angle, radians=False):
    theta = angle + arc(position, radians=radians)
    if radians==False:
        theta = theta*(np.pi/180.0)   # convert degree to radians

    rho = np.sqrt(position[0]**2 + position[1]**2)
    x = rho*np.cos(theta)
    y = rho*np.sin(theta)

    rotated_position = np.rint([x, y]) 

    return np.array( [int(rotated_position[0]), int(rotated_position[1])] )

pos1_rot = rotate(position_1, 20)
pos2_rot = rotate(position_2, 20)
pos3_rot = rotate(position_3, 20)

a[pos1_rot[0], pos1_rot[1]] = 1
a[pos2_rot[0], pos2_rot[1]] = 1
a[pos3_rot[0], pos3_rot[1]] = 1


def mismatch(parameters):
    theta, m, n = parameters
    #theta  = theta*(np.pi/180.0)
    
    position_1 = np.array( [[200,100]] ).T
    position_2 = np.array( [[257,34]] ).T 
    #position_3 = np.array( [[20,30]] ).T

    pos1_rot = rotate(position_1, 20)
    pos2_rot = rotate(position_2, 20)
    #pos3_rot = rotate(position_3, 20)

        
    # rho_1 = np.sqrt(position_1[0]**2 + position_1[1]**2)
    # rho_2 = np.sqrt(position_2[0]**2 + position_2[1]**2)
    # rho_3 = np.sqrt(position_3[0]**2 + position_3[1]**2)

    # rotation_mtx1 = np.array([rho_1*np.cos(theta), rho_1*np.sin(theta)])
    # rotation_mtx2 = np.array([rho_2*np.cos(theta), rho_2*np.sin(theta)])
    # rotation_mtx3 = np.array([rho_3*np.cos(theta), rho_3*np.sin(theta)])
    
    # pos1_out = np.rint(np.multiply(position_1, rotation_mtx1)) 
    # pos2_out = np.rint(np.multiply(position_2, rotation_mtx2)) 
    # pos3_out = np.rint(np.multiply(position_3, rotation_mtx3)) 

    # pos1_out = np.array([int(pos1_out[0]), int(pos1_out[1])])
    # pos2_out = np.array([int(pos2_out[0]), int(pos2_out[1])])
    # pos3_out = np.array([int(pos3_out[0]), int(pos3_out[1])])

    pos1_out = rotate(position_1, theta) + [m, n]
    pos2_out = rotate(position_2, theta) + [m, n]
    #pos3_out = rotate(position_3, theta) + [m, n]
            
    error = 0.0
    error = np.abs((np.sum(pos1_out - pos1_rot) + np.sum(pos2_out - pos2_rot))) # + np.sum(pos3_out - pos3_rot))) #/np.sum(img_1[...])

    print(error)
    return error


x0 = np.array([12, 0, 0])
#res = minimize(mismatch, x0, method='nelder-mead',options={'xatol': 1e-4, 'disp': True})
res = minimize(mismatch, x0, method='BFGS',options={'gatol': 1e-4, 'disp': True})
print(res.x)
    
# del_x = 5
# del_y = 10

# tr_pos = np.array([position[0]+del_x, position[1]+del_y])


# theta = alpha_0_deg + 0
# theta = theta*(np.pi/180.0)   # deg to radians

# rho = np.sqrt(tr_pos[0]**2 + tr_pos[1]**2)
# x = rho*np.cos(theta)
# y = rho*np.sin(theta)

# rotated_position = np.rint([x, y]) #rotation_matrix.dot(position)

# a[int(rotated_position[0]), int(rotated_position[1])] = 0.5


# new_origo = np.array([[del_x, del_y]]).T
# tr_pos = tr_pos - new_origo

# rho_2 = np.sqrt(rotated_position[0]**2 + rotated_position[1]**2)
# alpha_1 = np.arccos(rotated_position[0]/rho_2)
# alpha_1_deg = alpha_1*180.0/np.pi

# print(f'Initial angel: {alpha_0_deg}')
# print(f'New angel: {alpha_1_deg}')


axis2.imshow(a)
axis2.set_title('After')
plt.show()

print('Success')
