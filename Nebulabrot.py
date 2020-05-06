# %%

# ! /usr/bin/python
import png
from datetime import datetime
import numpy as np


def c_set(num_samples, iterations):
    # return a sampling of complex points outside of the mset

    # Allocate an array to store our non-mset points as we find them.
    non_msets = np.zeros(num_samples, dtype=np.complex128)
    non_msets_found = 0

    # create an array of random complex numbers (our 'c' points)
    c = (np.random.random(num_samples) * 4 - 2 +
         (np.random.random(num_samples) * 4 - 2) * 1j)

    # Optimizations: most of the mset points lie within the
    # cardioid or in the period-2 bulb. (The two most prominent
    # shapes in the mandelbrot set.) We can eliminate these
    # from our search straight away and save a lot of time.
    # see: http://en.wikipedia.org/wiki/Mandelbrot_set#Optimizations

    print("{0} random complex points chosen".format(len(c)))
    # First eliminate points within the cardioid
    # Get polar components of c
    c_r, c_phi = np.abs(c), np.angle(c)

    # If the magnitude of c is larger than the magnitude of
    # boundary at the same angle, we are outside the main bulb
    c = c[np.abs(c) > np.abs(np.exp(1j * c_phi) /
                             2 - np.exp(2 * 1j * c_phi) / 4)]
    print("{0} points remain after filtering the cardioid".format(len(c)))

    # Next eliminate points within the period-2 bulb
    # (circle with radius 1/4, center (-1,0))
    c = c[((c.real + 1) ** 2) + (c.imag ** 2) > 0.0625]
    print("{0} points remain after filtering the period-2 bulb".format(len(c)))

    # optimizations done.. time to do the escape time algorithm.
    # Use these c-points as the initial 'z' points.
    # (saves one iteration over starting from origin)
    z = np.copy(c)

    for i in range(iterations):
        # apply mandelbrot dynamic
        z = z ** 2 + c

        # collect the c points that have escaped
        mask = abs(z) < 2
        mask_inverse = abs(z) >= 2
        new_non_msets = c[mask_inverse]
        non_msets[non_msets_found:non_msets_found + len(new_non_msets)] \
            = new_non_msets
        non_msets_found += len(new_non_msets)

        # then shed those points from our test set before continuing.
        c = c[mask]
        z = z[mask]

        if i % 100 == 0 or i == iterations - 1:
            print("Iteration {0}: {1} points have escaped!".format(
                i, len(new_non_msets)))

    # return only the points that are not in the mset
    return non_msets[:non_msets_found]


def buddhabrot(c, size):
    # initialise an empty array to store the results
    img_array = np.zeros([size, size], int)

    # Declare a counter used for reporting
    i = 1
    # use these c-points as the initial 'z' points.
    z = np.copy(c)

    while len(z):
        if i % 100 == 0:
            print("Pass {0}: {1} orbits in play".format(i, len(z)))

        # translate z points into image coordinates
        x = np.array((z.real + 2.) / 4 * size, int)
        y = np.array((z.imag + 2.) / 4 * size, int)

        # add value to all occupied pixels
        img_array[x, y] += 1

        # apply mandelbrot dynamic
        z = z ** 2 + c

        # shed the points that have escaped
        mask = abs(z) < 2
        c = c[mask]
        z = z[mask]

        i += 1

    print("{0} passes completed for all points to escape.".format(i))
    return img_array


if __name__ == "__main__":

    size = 1600  # size of final image
    # bailout values (red, green, blue) -- higher means more details
    iterations = (2500, 250, 25)
    samples = int(0.5 * 10 ** 8)  # number of random complex points chosen
    loops = 50  # number of times to repeat process

    img_array_red = np.zeros([size, size], int)
    img_array_green = np.zeros([size, size], int)
    img_array_blue = np.zeros([size, size], int)
    pngArray = np.zeros([size, 3 * size], int)

    loop = 1

    while loop <= loops:
        print(loop)
        print(loops)
        print("{1}: Loop {2} - Choosing {0} random complex numbers".format(samples,
                                                                           datetime.now().time(), loop))
        c_red = c_set(samples, iterations[0])
        c_green = c_set(samples, iterations[1])
        c_blue = c_set(samples, iterations[2])

        print("{0}: Rendering image...".format(datetime.now().time()))
        img_array_red += buddhabrot(c_red, size)
        img_array_green += buddhabrot(c_green, size)
        img_array_blue += buddhabrot(c_blue, size)

        img_array_red_scaled = np.array(
            img_array_red / float(img_array_red.max()) * ((2 ** 16) - 1), int)
        img_array_green_scaled = np.array(
            img_array_green / float(img_array_green.max()) * ((2 ** 16) - 1), int)
        img_array_blue_scaled = np.array(
            img_array_blue / float(img_array_blue.max()) * ((2 ** 16) - 1), int)

        print(
            "{0}: Loop {1} - Adjusting image levels...".format(datetime.now().time(), loop))
        for i in range(size):
            for j in range(size):
                pngArray[i][j * 3 + 0] = img_array_blue_scaled[i][j]
                pngArray[i][j * 3 + 1] = img_array_green_scaled[i][j]
                pngArray[i][j * 3 + 2] = img_array_red_scaled[i][j]

        # pngArray_scaled = np.array(pngArray / float(pngArray.max()) * ((2 ** 16) - 1), int)

        loop += 1

    print("{1}: Saving image to buddhabrot_n_{0}.png".format(
        iterations, datetime.now().time()))
    # save to final render to png file
    imgWriter = png.Writer(size, size, bitdepth=16,
                           greyscale=False, alpha=False)

    file = open("buddhabrot_n_{0}.png".format(iterations), "wb")
    imgWriter.write(file, pngArray)
    file.close()

    print("{0}: Rendering complete.".format(datetime.now().time()))
