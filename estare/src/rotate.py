
import numpy as np



'''
We have:
- a function to calculate angle recieves a reference(default 0, 0) and a feature coordinate
- a function that takes an angle and a pair of coordinates and rotates the point (below)
- a function that takes [del_x, del_y] and a pair of coordinates and translates the point (below)

--------------->  Y
|*
| *
|  *
|   *
|
v

X

'''


def arc(position, origo=np.array([0., 0.]), radians=False):
    '''
Returns the angle between the input coordinate and the vertical axis Y
'''
    rho = np.sqrt( (position[0]-origo[0])**2 + (position[1]-origo[1])**2 )
    angle = np.arccos( (position[0]-origo[0]) / rho )
    
    if radians==False:
        angle = angle*180.0/np.pi
        
    return angle



# apply rotation
def rotate(position, angle, origo=np.array([0., 0.]), radians=False, discrete=True):
    theta = angle + arc(position, radians=radians)
    if radians==False:
        theta = theta*(np.pi/180.0)   # convert degree to radians

    rho = np.sqrt((position[0]-origo[0])**2 + (position[1]-origo[1])**2)
    x = rho*np.cos(theta)
    y = rho*np.sin(theta)

    if discrete:
        rotated_position = np.rint([x, y])     
        return np.array( [int(rotated_position[0]), int(rotated_position[1])] )
    else:
        return np.array( [x, y] )



