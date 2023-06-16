# Map defination

import numpy as np

def linefrommap(map):
    """
    Calculates the line equation from the map coordinates

    Args:
        map: Set of points [x1,y1,x2,y2] defining a map
    Returns
        line: Line equation coefficents
    """
    map = map.flatten()
    line = np.cross(np.array([map[0],map[1],1]) , np.array([map[2],map[3],1])) # line from x1 y1 x2 y2 format
    return line

def within_range(ip, map):
    """
    Conditional to check is the intersection point is with a map.

    Args:
        ip: Intersection point
        map: Set of points [x1,y1,x2,y2] defining a map
    Returns:
        bool: True or False
    """
    x1 = min(map[0],map[2])
    x2 = max(map[0],map[2])
    y1 = min(map[1],map[3])
    y2 = max(map[1],map[3])
    if y1 == y2:
        if (ip[0]>=x1 and ip[0]<=x2):
            return True
        else:
            return False
    elif x1 == x2:
        if (ip[1]>=y1 and ip[1] <= y2):
            return True
        else:
            return False
    else:
        if ((ip[0]>=x1 and ip[0]<=x2) and (ip[1]>=y1 and ip[1] <= y2)):
            return True
        else:
            return False
