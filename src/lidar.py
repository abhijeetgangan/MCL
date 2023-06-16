# Simulate lidar data

import numpy as np

from src.map import linefrommap, within_range
from src.util import distance_fn, norm_homo_fn

def lidar_fn(map, pos, nlaserbeam, ax, viz):
    """
    Get lidar distances

    Args:
        map: Set of points [x1,y1,x2,y2] defining a map
        pos: position of the robot or particle
        nlaserbeam: Number of lidar detectors
        ax: axis for plotting
        viz: if visualization should be done
    Returns:
        lidardata: set of distances for each laser beam
    """
    lidardata = np.zeros(nlaserbeam)
    for i in range(lidardata.shape[0]):
        line_1 = np.array([np.tan(2*np.pi*i/nlaserbeam),-1,pos[1]-(pos[0]*np.tan(2*np.pi*i/nlaserbeam))])
        dist = []
        for j in range(map.shape[0]):
            line_2 = linefrommap(map[j,:])
            ip = norm_homo_fn(np.cross(line_1,line_2))
            if abs(np.arctan2((ip[1] - pos[1]) , (ip[0] - pos[0])) - (np.mod(2*np.pi*i/nlaserbeam, 2*np.pi) - np.pi)) < 1e-8:
                    if within_range(ip, map[j,:]):
                        dist.append(distance_fn(pos, ip))
                    else:
                        dist.append(100)
            else:
                dist.append(100)
        lidardata[i] = min(dist)
        idx = dist.index(min(dist))
        line_2 = linefrommap(map[idx,:])
        ip = norm_homo_fn(np.cross(line_1,line_2))
        if viz:
            if i == 0: # Skip the plotting of laser for theta = 0
                continue
            else:
                ax.plot([pos[0], ip[0]],[pos[1], ip[1]], c='red')
                ax.scatter(ip[0],ip[1], c='black')
                for k in range(map.shape[0]):
                    ax.plot([map[k,0],map[k,2]],[map[k,1],map[k,3]], c='black') 
                ax.scatter(pos[0],pos[1])
    return lidardata