# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import laspy
import numpy as np
from scipy.spatial import cKDTree
import matplotlib as plt
import math

in_file = laspy.file.File(r"C:\AAA\svm_haleiwa\raw\4QEJ591385_agl.las", mode = "r")

pt_recs = in_file.points.copy()

#ground = np.where(np.logical_or(in_file.raw_classification == 2, in_file.raw_classification == 18))
#non_ground = np.where(np.logical_or(in_file.raw_classification == 1, in_file.raw_classification == 17))
#
#ground_pts = in_file.points[ground]
#ground_pts['point']['raw_classification'] = 1
#
#ground_pts_arr = np.array([ground_pts['point']['X'], ground_pts['point']['Y'], ground_pts['point']['Z'], ground_pts['point']['raw_classification']])
#
#non_ground_pts = in_file.points[non_ground]
#non_ground_pts['point']['raw_classification'] = -1


scale = in_file.header.scale[0]
offset = in_file.header.offset[0]

arr = np.transpose(np.array([in_file.X * scale + offset, in_file.Y * scale + offset, in_file.Z * scale, in_file.user_data,
                                 in_file.return_num, in_file.num_returns, in_file.raw_classification]))

#add a field to hold our normal variation value
pts_arr = np.insert(arr, 4, 1, axis=1)

ctree = cKDTree(pts_arr[:,:2])

for idx, record in enumerate(pts_arr):
    neighbors = ctree.query_ball_point(record[:2], 10)
    
    neighbors_arr = np.array([neighbors])
    
    std_dev = np.std(neighbors_arr)
    print std_dev
        


