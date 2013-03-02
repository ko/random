#!/usr/bin/python2.7

import cv

cv.NamedWindow('windowowow', cv.CV_WINDOW_AUTOSIZE)


img_src = '/home/ko/Downloads/test.jpg'
img_color = cv.LoadImage(img_src, cv.CV_LOAD_IMAGE_COLOR)
img_size = cv.GetSize(img_color)
img = img_color

img_grey = cv.CreateImage(img_size, 8, 1)
cv.CvtColor(img, img_grey, cv.CV_BGR2GRAY);
img = img_grey

img_smooth = cv.CreateImage(img_size, 8, 1)
cv.Smooth(img, img_smooth, cv.CV_MEDIAN)
img = img_smooth

#cv.EqualizeHist(img, img)

#threshold=100
#colour=255
#cv.Threshold(img, img, threshold, colour, cv.CV_THRESH_BINARY)
#cv.Threshold(img, img, threshold, colour, cv.CV_THRESH_OTSU)

storage = cv.CreateMemStorage()

element_shape = cv.CV_SHAPE_ELLIPSE
pos=3
element = cv.CreateStructuringElementEx(pos*2 + 1, pos*2+1, 
                                        pos, pos, element_shape)
cv.Dilate(img, img, element, 2)
element_shape = cv.CV_SHAPE_RECT
pos=2
element = cv.CreateStructuringElementEx(pos*2 + 1, pos*2+1, 
                                        pos, pos, element_shape)
cv.Erode(img, img, element, 2)

cv.ShowImage('windowowow', img)
cv.WaitKey(100000)
