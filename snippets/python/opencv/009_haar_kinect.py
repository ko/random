#!/usr/bin/python2.7

# RUN THIS AS SUDO FOR THE KINECT

import cv
import numpy
from freenect import sync_get_depth as get_depth
from freenect import sync_get_video as get_video

hc_src = '/home/ko/Downloads/head.Cascade.1.xml'
hc_src = '/home/ko/Downloads/haarcascade_frontalface_default.xml'
hc = cv.Load(hc_src)
storage = cv.CreateMemStorage(0)

global depth, rgb
while True:
    (depth,_), (rgb,_) = get_depth(), get_video()
    # depth map returns values in a larger range
    # than the rgb image. require scaling to
    # an uint8_t as a result.

    d3 = numpy.dstack((depth, depth, depth)).astype(numpy.uint8)
    da = numpy.hstack((d3, rgb))
    # lets create an image 
    image = cv.fromarray(numpy.array(da[::2,::2,::-1]))

    heads = cv.HaarDetectObjects(image, 
                                hc, storage,
                                1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING,
                                (0,0))
    for (x,y,w,h),n in heads:
        cv.Rectangle(image, (x,y), (x+w, y+h), 255)

    cv.ShowImage('both', image)
    c = cv.WaitKey(5)
    if c == 27:
        break

