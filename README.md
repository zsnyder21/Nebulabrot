# Nebulabrot
Colored Buddhabrot (Nebulabrot)

The Nebrulabrot.py file generates various sets of complex numbers and iterates a specified number of times to ensure they are indeed outside of the Mandelbrot set. From here, it processes and tracks the orbits of the points. This is done for each of the red, green, and blue channels. The arrays are then combined in a way that gives the image color when outputting to a png file.

In order to avoid memory issues, there is a loop at the bottom that repeats the process a specified number of times.

I've included a short script that can extract and flip around the color channels. This has the same effect as rerunning the Nebulabrot.py script but varying the parameters accordingly, but is much more cost effective. The ratios, however, remain the same. If new ratios are desired, rerunning Nebulabrot.py with the appropriate parameters is the way to go.
