# -*- coding: utf-8 -*-
"""
W. Ross Winans
2018/05/15

Written in Python 2.7.?

This script preprocesses a LAS v1.2 or lower light detection and ranging "lidar" file into a csv with the following columns:
    X- Latitude coordinates
    Y- logitude coordinates
    Z- the elevation of the point above local mean sea level
    HAGL- the vertical distance between the point and its lowest neighbor within 1m
    STD_1m- the standard deviation of all neighbors’ elevation within 1m
    STD_10m- the standard deviation of all neighbors’ elevation within 10m
    RET_NUM- the return number of the point
    NUM_RET- the total number of returns for the point

This script was written to preprocess data for Ross Winans' ICS 635 final project (https://github.com/rosswin/lidar_svm). Therefore,
it is not a full-fledged piece of software and is highly specialized for this single task.

NOTE At the time this was written it was already using software that I would describe as "lightly maintained" (laspy). PDAL is the flavor of the day. If you are going down
this road please note it is probably a dead end... currently won't support LAS v1.4 or higher.

NOTE one thing of interst might be using a KDTree to quickly find neighbor points.
"""

import laspy
import numpy as np
from scipy.spatial import cKDTree
from matplotlib import pyplot as plt
import math


#### THIS IS WHERE YOU EDIT ######################
in_file = laspy.file.File(r"C:\AAA\svm_haleiwa\raw\4QEJ591385_agl.las", mode = "r")
#### STOP EDITING HERE      ######################
# 0 X, 1 Y, 2 Z, 3 HAGL, 4 STDEV_10, 5 RETURN, 6 NUMOF, 7 RET_NORM, 8 CLASS

#grab the scale and offset, which we will need to scale and adjust our coordinates when we read into array
scale = in_file.header.scale[0]
offset = in_file.header.offset[0]

#read all the LAS points and all their attributes that we may need
arr = np.transpose(np.array([in_file.X * scale + offset, in_file.Y * scale + offset, in_file.Z * scale, in_file.user_data / 10.0,
                                 in_file.return_num, in_file.num_returns, in_file.raw_classification]))

#add fields to hold our normal variation and return norm values
#NOTE final results show that return normalization didn't do much. I am leaving this here for legacy reasons though.
#pts_arr1 = np.insert(arr, 4, 9999, axis=1)
#pts_arr = np.insert(pts_arr1, 7, 9999, axis=1)

#calculate normalized returns
#pts_arr[:, 7] = pts_arr[:, 5] / pts_arr[:, 6] + pts_arr[:, 6]


#Drop the following classification so that only ground and object point remain: noise (7), water (9), breakline (10), overlap water (25)
pts_arr = pts_arr[np.logical_not(np.logical_or(pts_arr[:,8] == 7, 
                                               np.logical_or(pts_arr[:,8] == 9, 
                                                             np.logical_or(pts_arr[:,8] == 10, pts_arr[:,8] == 25))))]

pts_arr[:,8][np.logical_or(pts_arr[:,8] == 1, pts_arr[:,8] == 17)] = -1
pts_arr[:,8][np.logical_or(pts_arr[:,8] == 2, pts_arr[:,8] == 18)] = 1

unique2, counts2 = np.unique(pts_arr[:, 8], return_counts=True)
print zip(unique2, counts2)

#calculate the STD of elevations within 10 meters
#make a KDTree
ctree = cKDTree(pts_arr[:,:2])
#iterate through all our points and perform really fast queries on neighbor points within 10 meter radius
for idx, record in enumerate(pts_arr):
    neighbors = ctree.query_ball_point(record[:2], 10)
    
    #if there aren't any neighbors (shouldn't be the case... but maybe a misclass here or there)
    if len(neighbors) == 0:
        #set to 0 for null value
        z_std = 0
    else:
        
        #otherwise, calculate the standard deviation of neighbor points within 10m
        z_std = np.std(neighbors_pts['point']['Z'])
    
    pts_arr[idx][4] = z_std
    
    print idx
    print z_std, pts_arr[idx][4]

#SHUFFLE and clip to 150k points
np.random.shuffle(pts_arr)
pts_arr_150k = pts_arr[:150000,:]

#Save to a csv
np.savetxt(r"C:\AAA\svm_haleiwa\raw\4QEJ591385_agl_150k.csv", pts_arr_150k, delimiter=",")

#min_z = np.min(pts_thin[:,2])
#max_z = np.max(pts_thin[:,2])
#plt.scatter(pts_thin[:, 0], pts_thin[:, 1], c=pts_thin[:, 2], vmin= min_z, vmax = max_z)
#plt.colorbar()
#plt.hist(pts_arr_150k[:,2], range = (-100, 100), bins=30)