#!/usr/bin/python2.7

import cv

cv.NamedWindow('a_window', cv.CV_WINDOW_AUTOSIZE)

image_src = '/home/ko/Downloads/09-0289-r.jpg'
image = cv.LoadImage(image_src, cv.CV_LOAD_IMAGE_COLOR)

video_src = '/home/ko/Downloads/MVI_0572.AVI'
video= cv.CreateFileCapture(video_src)
image = cv.QueryFrame(video)

font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)

x = 5
y = 20

cv.PutText(image, "Hello World", (x,y), font, 255)
cv.ShowImage('a_window', image)
cv.WaitKey(100000)
cv.SaveImage('image.png', image)
