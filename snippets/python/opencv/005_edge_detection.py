#!/usr/bin/python2.7

import cv

# window prep
cv.NamedWindow('windowowow', cv.CV_WINDOW_AUTOSIZE)

# image loading
img_src = '/home/ko/Downloads/test.jpg'
img_color = cv.LoadImage(img_src, cv.CV_LOAD_IMAGE_COLOR)
img_size = cv.GetSize(img_color)
img = img_color

# greyscale
img_grey = cv.CreateImage(img_size, 8, 1)
cv.CvtColor(img, img_grey, cv.CV_BGR2GRAY);
img = img_grey

# smoothing
img_smooth = cv.CreateImage(img_size, 8, 1)
cv.Smooth(img, img_smooth, cv.CV_MEDIAN)
img = img_smooth

# edge detection
dst_16s2 = cv.CreateImage(img_size, cv.IPL_DEPTH_16S, 1)
cv.Laplace(img, dst_16s2, 3)
cv.Convert(dst_16s2, img)

# display
cv.ShowImage('windowowow', img)
cv.WaitKey(100000)
