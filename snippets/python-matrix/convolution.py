#!/usr/local/bin/python2.7
#!/usr/bin/python2.7
import numpy as np
import math

m = 5
n = 5
sigma = 1

#   h1: 
#   -2, -1, 0, 1, 2
#   -2, -1, 0, 1, 2
#   -2, -1, 0, 1, 2
#   -2, -1, 0, 1, 2
#   -2, -1, 0, 1, 2
#
#   h2:
#   -2, -2, -2, -2, -2
#   -1, -1, -1, -1, -1
#    0,  0,  0,  0,  0
#    1,  1,  1,  1,  1
#    2,  2,  2,  2,  2
nx, ny = (5, 5)
ma = np.linspace(-(m-1)/2,(m-1)/2, nx)
mb = np.linspace(-(n-1)/2,(n-1)/2, ny)
h1, h2 = np.meshgrid(ma, mb)

# stmt:
#   [[ 4.   2.5  2.   2.5  4. ]
#    [ 2.5  1.   0.5  1.   2.5]
#    [ 2.   0.5  0.   0.5  2. ]
#    [ 2.5  1.   0.5  1.   2.5]
#    [ 4.   2.5  2.   2.5  4. ]]
stmt = np.power(h1,2) + np.power(h2,2)
stmt = stmt / (2 * math.pow(sigma,2))
hg = np.exp(stmt)

h = np.divide(hg, np.sum(hg))
print h

x = np.random.random((2048, 2048)).astype(np.float32)
y = h
z = np.fft.irfft2(np.fft.rfft2(x) * np.fft.rfft2(y, x.shape))
