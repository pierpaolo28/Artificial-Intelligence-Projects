import math
import numpy as np
from scipy import signal
from scipy import ndimage
import imageio
import matplotlib.pyplot as plt
from PIL import Image
import scipy.misc

from MyConvolution import convolve
from MyHybridImages import myHybridImages, makeGaussianKernel

img = imageio.imread('batman.PNG')
mix = imageio.imread('jocker.PNG')

res = myHybridImages(mix[:, :, 0:3], 9, img[:, :, 0:3], 9)

out = (res - res.min())/(res.max() - res.min())*255
out = out.astype(np.uint8)
imageio.imwrite('test.png', out)