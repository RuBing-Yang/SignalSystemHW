import numpy
from skimage import io

image = io.imread("images/demo.bmp")
data = numpy.array(image, dtype=float)
data = numpy.delete(data, [0, 1, 498, 499], axis=1)
data = numpy.delete(data, [0, 1, 498, 499], axis=0)
io.imsave("demo.bmp", data)
