from PIL import Image
import numpy
from keras.preprocessing.image import save_img


def upAlign(x, y):
    if x % y == 0:
        return x
    return x + y - x % y

def dct(timeDomain, frequencyDomain, x, y):
    for i in range(0, 8):
        for j in range(0, 8):
            frequencyDomain[i][j] += 2 / 8

def encode(timeDomain, frequencyDomain):
    for i in range(0, timeDomain.shape[0], 8):
        for j in range(0, timeDomain.shape[0], 8):
            dct(timeDomain, frequencyDomain, i, j)
    dct(timeDomain, frequencyDomain)


image = Image.open("images/image.bmp")
data = numpy.asarray(image)
print(type(data))
print(data.shape)
Y = numpy.zeros([upAlign(len(data), 8), upAlign(len(data[0]), 8)], dtype=int)
Cb = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
Cr = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
for i in range(0, len(data)):
    for j in range(0, len(data[i])):
        Y[i][j] = 0.229 * data[i][j][0] + 0.587 * data[i][j][1] + 0.114 * data[i][j][2]
        if i % 2 == 0 and j % 2 == 0:
            Cb[i // 2][j // 2] = -0.1687 * data[i][j][0] - 0.3313 * data[i][j][1] + 0.5 * data[i][j][2] + 128
            Cr[i // 2][j // 2] = 0.5 * data[i][j][0] - 0.4187 * data[i][j][1] - 0.0813 * data[i][j][2] + 128
Y1 = numpy.zeros([upAlign(len(data), 8), upAlign(len(data[0]), 8)], dtype=int)
Cb1 = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
Cr1 = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
encode(Y, Y1)

save_img('images/out.bmp', Y)
