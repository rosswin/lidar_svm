# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import laspy
import numpy as np
from scipy.spatial import cKDTree
from matplotlib import pyplot as plt
import math


in_file = laspy.file.File(r"C:\AAA\svm_haleiwa\raw\4QEJ591385_agl.las", mode = "r")



# 0 X, 1 Y, 2 Z, 3 HAGL, 4 STDEV_10, 5 RETURN, 6 NUMOF, 7 RET_NORM, 8 CLASS

scale = in_file.header.scale[0]
offset = in_file.header.offset[0]

arr = np.transpose(np.array([in_file.X * scale + offset, in_file.Y * scale + offset, in_file.Z * scale, in_file.user_data / 10.0,
                                 in_file.return_num, in_file.num_returns, in_file.raw_classification]))

#add fields to hold our normal variation and return norm values
pts_arr1 = np.insert(arr, 4, 9999, axis=1)
pts_arr = np.insert(pts_arr1, 7, 9999, axis=1)

#calculate normalized returns
pts_arr[:, 7] = pts_arr[:, 5] / pts_arr[:, 6] + pts_arr[:, 6]


#Drop noise (7), water (9), breakline (10), overlap water (25)
pts_arr = pts_arr[np.logical_not(np.logical_or(pts_arr[:,8] == 7, 
                                               np.logical_or(pts_arr[:,8] == 9, 
                                                             np.logical_or(pts_arr[:,8] == 10, pts_arr[:,8] == 25))))]

pts_arr[:,8][np.logical_or(pts_arr[:,8] == 1, pts_arr[:,8] == 17)] = -1
pts_arr[:,8][np.logical_or(pts_arr[:,8] == 2, pts_arr[:,8] == 18)] = 1

unique2, counts2 = np.unique(pts_arr[:, 8], return_counts=True)
print zip(unique2, counts2)


##calculate the STD of elevations within 10 meters
#ctree = cKDTree(pts_arr[:,:2])
#
#for idx, record in enumerate(pts_arr):
#    neighbors = ctree.query_ball_point(record[:2], 10)
#    
#    if len(neighbors) == 0:
#        z_std = 0
#    else:
#        
#        z_std = np.std(neighbors_pts['point']['Z'])
#    
#    pts_arr[idx][4] = z_std
#    
#    print idx
#    print z_std, pts_arr[idx][4]


##SHUFFLE and clip 150k points
#np.random.shuffle(pts_arr)
#pts_arr_150k = pts_arr[:150000,:]
#
##Save to a csv
#np.savetxt(r"C:\AAA\svm_haleiwa\raw\4QEJ591385_agl_150k.csv", pts_arr_150k, delimiter=",")


#min_z = np.min(pts_thin[:,2])
#max_z = np.max(pts_thin[:,2])
#plt.scatter(pts_thin[:, 0], pts_thin[:, 1], c=pts_thin[:, 2], vmin= min_z, vmax = max_z)
#plt.colorbar()
#
#plt.hist(pts_arr_150k[:,2], range = (-100, 100), bins=30)
