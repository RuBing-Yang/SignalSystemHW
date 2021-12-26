from PIL import Image
import numpy
import math
from keras.preprocessing.image import save_img


def upAlign(x, y):
    if x % y == 0:
        return x
    return x + y - x % y


def dct(time_domain, frequency_domain, x, y):
    for u in range(0, 8):
        for v in range(0, 8):
            if u == 0 and v == 0:
                c = 1 / 8
            else:
                c = 1 / 16
            for i in range(0, 8):
                for j in range(0, 8):
                    frequency_domain[x + u][y + v] += \
                        c * time_domain[x + i][y + j] * math.cos(math.pi * u * (2 * i + 1) / 16) * \
                        math.cos(math.pi * v * (2 * j + 1) / 16)


def quantification(frequency_domain: numpy.ndarray, standard_table: numpy.ndarray) -> None:
    for i in range(0, frequency_domain.shape[0], 8):
        for j in range(0, frequency_domain.shape[1], 8):
            for u in range(0, 8):
                for v in range(0, 8):
                    frequency_domain[i + u][j + v] //= standard_table[u][v]


def encode(time_domain: numpy.ndarray, frequency_domain: numpy.ndarray) -> None:
    for i in range(0, time_domain.shape[0], 8):
        for j in range(0, time_domain.shape[1], 8):
            dct(time_domain, frequency_domain, i, j)


def main():
    image = Image.open("images/image.bmp")
    data = numpy.asarray(image)
    print(type(data))
    luminance_time_domain = numpy.zeros([upAlign(len(data), 8), upAlign(len(data[0]), 8)], dtype=int)
    chrominance_time_domain = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
    saturation_time_domain = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            luminance_time_domain[i][j] = 0.229 * data[i][j][0] + 0.587 * data[i][j][1] + 0.114 * data[i][j][2]
            if i % 2 == 0 and j % 2 == 0:
                chrominance_time_domain[i // 2][j // 2] = -0.1687 * data[i][j][0] - 0.3313 * data[i][j][1] + 0.5 * data[i][j][2] + 128
                saturation_time_domain[i // 2][j // 2] = 0.5 * data[i][j][0] - 0.4187 * data[i][j][1] - 0.0813 * data[i][j][2] + 128
    luminance_frequency_domain = numpy.zeros([upAlign(len(data), 8), upAlign(len(data[0]), 8)], dtype=int)
    chrominance_frequency_domain = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
    saturation_frequency_domain = numpy.zeros([upAlign((len(data) + 1) // 2), upAlign((len(data[0]) + 1) // 2)], dtype=int)
    encode(luminance_time_domain, luminance_frequency_domain)
    save_img('images/out.bmp', luminance_time_domain)


if __file__ == 'main':
    main()
