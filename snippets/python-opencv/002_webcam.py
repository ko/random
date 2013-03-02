#!/usr/bin/python2.7

import cv

capture = cv.CaptureFromCAM(0)
temp = cv.QueryFrame(capture)
writer_dst = '/home/ko/out.avi'
writer = cv.CreateVideoWriter(writer_dst, 0, 15, cv.GetSize(temp), 1)
count = 0

while count < 250:
    image = cv.QueryFrame(capture)
    cv.Circle(image, (5,100), 3, (0, 255, 0), -1, 50, 0)
    cv.WriteFrame(writer, image)
    cv.ShowImage('img window', image)
    cv.WaitKey(2)
    count += 1
