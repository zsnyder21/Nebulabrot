import cv2
import numpy as np
import png

# read image
src = cv2.imread('buddhabrot_(5000, 500,50)_highres - Copy.png', cv2.IMREAD_UNCHANGED)
size = src.shape[0]
print(size)

pngArray = np.zeros([size, 3 * size], int)

# extract red channel
red_channel = src[:, :, 2]
green_channel = src[:, :, 1]
blue_channel = src[:, :, 0]

for i in range(size):
    for j in range(size):
        pngArray[i][j * 3 + 0] = blue_channel[i][j]  # Red
        pngArray[i][j * 3 + 1] = red_channel[i][j]   # Green
        pngArray[i][j * 3 + 2] = green_channel[i][j]   # Blue

# Create a new image
imgWriter = png.Writer(size, size, bitdepth=16,
                           greyscale=False, alpha=False)

file = open("test123.png", "wb")
imgWriter.write(file, pngArray)
file.close()
