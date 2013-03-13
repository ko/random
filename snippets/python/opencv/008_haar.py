#!/usr/bin/python2.7

import cv

capture = cv.CaptureFromCAM(0)

hc_src = '/home/ko/Downloads/Hand.Cascade.1.xml'
hc_src = '/home/ko/Downloads/haarcascade_frontalface_default.xml'
hc = cv.Load(hc_src)

storage = cv.CreateMemStorage(0)

while True:
    frame = cv.QueryFrame(capture)
    hands = cv.HaarDetectObjects(frame, hc, storage,
                            1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING,
                            (0,0))
    for (x,y,w,h),n in hands:
        cv.Rectangle(frame, (x,y), (x+w, y+h), 255)

    cv.ShowImage('web', frame)
    c = cv.WaitKey(2)
    if c == 27:
        break



