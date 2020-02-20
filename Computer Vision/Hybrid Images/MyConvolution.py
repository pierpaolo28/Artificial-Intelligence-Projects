import numpy as np


def convolve(image, kernel):
    # In case the input is not an array, convert it to array
    image = np.array(image)
    kernel = np.array(kernel)
    # Flipping the kernel so that we can then use it for multiplication later
    kernel = np.flip(kernel)
    pad_dim = kernel.shape[0] // 2
    pad_dim2 = kernel.shape[1] // 2
    if len(image.shape) == 2:
        # Taking the dimensions of the input image
        r, c = image.shape
        # Adding zero padding to original image
        padded_img = np.pad(image, ((pad_dim, pad_dim), (pad_dim2, pad_dim2)), 'constant')
        # Creating an empty matrix where to store the resulting image
        result = np.empty((r, c))
        # Looping through all the pixels in the image
        for x in range(c):
            for y in range(r):
                # Creating convoluted matrix of kernel and subset of the image
                # for each possible combination in the image
                conv_mat = kernel * padded_img[y:y + kernel.shape[0], x:x + kernel.shape[1]]
                # Summing all the elements in the convoluted matrix and storing
                # the resulting number in our result matrix
                result[y, x] = conv_mat.sum()
    elif len(image.shape) == 3:
        r, c, dim = image.shape
        padded_img = np.pad(image, ((pad_dim, pad_dim), (pad_dim2, pad_dim2), (0, 0)), 'constant')
        result = np.empty((r, c, dim))
        for d in range(0, dim):
            for x in range(c):
                for y in range(r):
                    conv_mat = kernel * padded_img[y:y + kernel.shape[0], x:x + kernel.shape[1], d]
                    result[y, x, d] = conv_mat.sum()
    else:
        print("Only 2D or 3D Comvolution Possible")

    return result