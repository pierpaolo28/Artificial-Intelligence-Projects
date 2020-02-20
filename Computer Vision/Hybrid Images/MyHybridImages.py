import math
import numpy as np

from MyConvolution import convolve


def myHybridImages(lowImage, lowSigma, highImage, highSigma):
    low1 = convolve(lowImage, makeGaussianKernel(lowSigma))
    low2 = convolve(highImage, makeGaussianKernel(highSigma))
    high2 = highImage - low2
    res = low1 + high2
    return res


def makeGaussianKernel(sigma):
    size = int(np.floor(8*sigma+1))
    if size % 2 == 0:
        size += 1
    centre = size//2
    g = np.empty((size, size))
    sum = 0
    for i in range(0, size):
        for j in range(0, size):
            g[j][i] = np.exp(-(((j-centre)*(j-centre))+((i-centre)*(i-centre)))/(2*sigma*sigma))
            sum = sum + g[j][i]
    return np.array(g/sum)