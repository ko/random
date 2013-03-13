#!/usr/local/bin/python2.7
#!/usr/bin/python2.7

import numpy
from scipy import interpolate, ndimage


testArr = numpy.array([
                        [-.1, .2, 0],
                        [ .3,-.5, .3],
                        [ 0, -.234, .854]
                    ])

out = numpy.round(ndimage.interpolation.zoom(a, 5./3), 1, order=2)
print out

