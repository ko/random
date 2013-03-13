#!/usr/bin/python2.7

import cv

# create the wanted images
eig = cv.CreateImage(cv.GetSize(grey), 32, 1)
temp = cv.CreateImage(cv.GetSize(grey), 32, 1)

# default params
quality = 0.01
min_distance = 10

# search for good points
features = cv.GoodFeaturesToTrack(grey, eig, temp,
                                  MAX_COUNT, quality,
                                  min_distance, None,
                                  3, 0, 0.04)
for (x,y) in features:
    print "Good feature a: " + x + "," + y
    cv.Circle(image, (x,y), 3, (0, 255, 0), -1, 8, 0)
