from PIL import Image
import numpy
import math
from keras.preprocessing.image import save_img


def up_align(x, y):
    if x % y == 0:
        return x
    return x + y - x % y


def dct(time_domain, frequency_domain, x, y):
    for u in range(0, 8):
        for v in range(0, 8):
            frequency_domain[x + u][y + v] = 0
            for i in range(0, 8):
                for j in range(0, 8):
                    frequency_domain[x + u][y + v] += time_domain[x + i][y + j] * \
                        math.cos(math.pi * u * (2 * i + 1) / 16) * math.cos(math.pi * v * (2 * j + 1) / 16)
            c = 2 / 8
            if u == 0:
                c /= math.sqrt(2)
            if v == 0:
                c /= math.sqrt(2)
            time_domain[x + u][y + v] *= c


def quantification(frequency_domain: numpy.ndarray, standard_table: numpy.ndarray) -> None:
    for i in range(0, frequency_domain.shape[0], 8):
        for j in range(0, frequency_domain.shape[1], 8):
            for u in range(0, 8):
                for v in range(0, 8):
                    frequency_domain[i + u][j + v] = round(frequency_domain[i + u][j + v] / standard_table[u][v])


def encode(time_domain: numpy.ndarray, frequency_domain: numpy.ndarray,
           standard_table: numpy.ndarray, res) -> None:
    for i in range(0, time_domain.shape[0], 8):
        for j in range(0, time_domain.shape[1], 8):
            dct(time_domain, frequency_domain, i, j)
    quantification(frequency_domain, standard_table)
    # for i in range(0, frequency_domain.shape[0], 8):
    #     for j in range(0, frequency_domain.shape[1], 8):
    #         u = 1
    #         v = -1
    #         x = i
    #         y = j
    #         while 1:
    #             if x == i + 7 and y == j + 7:
    #                 break
    #             x += u
    #             y += v


def inverse_dct(time_domain, frequency_domain, x, y):
    for u in range(0, 8):
        for v in range(0, 8):
            time_domain[x + u][y + v] = 0
            for i in range(0, 8):
                for j in range(0, 8):
                    c = 2 / 8
                    if u == 0:
                        c /= math.sqrt(2)
                    if v == 0:
                        c /= math.sqrt(2)
                    time_domain[x + u][y + v] += c * frequency_domain[x + i][y + j] * \
                        math.cos(math.pi * u * (2 * i + 1) / 16) * math.cos(math.pi * v * (2 * j + 1) / 16)


def inverse_quantification(frequency_domain: numpy.ndarray, standard_table: numpy.ndarray) -> None:
    for i in range(0, frequency_domain.shape[0], 8):
        for j in range(0, frequency_domain.shape[1], 8):
            for u in range(0, 8):
                for v in range(0, 8):
                    frequency_domain[i + u][j + v] *= standard_table[u][v]


def decode(time_domain: numpy.ndarray, frequency_domain: numpy.ndarray, standard_table: numpy.ndarray) -> None:
    inverse_quantification(frequency_domain, standard_table)
    for i in range(0, frequency_domain.shape[0], 8):
        for j in range(0, frequency_domain.shape[1], 8):
            inverse_dct(time_domain, frequency_domain, i, j)


def main():
    image = Image.open("images/image.bmp")
    data = numpy.asarray(image)
    print(type(data))
    luminance_time_domain = numpy.zeros([up_align(len(data), 8), up_align(len(data[0]), 8)])
    chrominance_time_domain = \
        numpy.zeros([up_align((len(data) + 1) // 2), up_align((len(data[0]) + 1) // 2)])
    saturation_time_domain = \
        numpy.zeros([up_align((len(data) + 1) // 2), up_align((len(data[0]) + 1) // 2)])
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            luminance_time_domain[i][j] = 0.229 * data[i][j][0] + 0.587 * data[i][j][1] + 0.114 * data[i][j][2]
            if i % 2 == 0 and j % 2 == 0:
                chrominance_time_domain[i // 2][j // 2] = \
                    -0.1687 * data[i][j][0] - 0.3313 * data[i][j][1] + 0.5 * data[i][j][2] + 128
                saturation_time_domain[i // 2][j // 2] = \
                    0.5 * data[i][j][0] - 0.4187 * data[i][j][1] - 0.0813 * data[i][j][2] + 128
    luminance_frequency_domain = numpy.zeros([up_align(len(data), 8), up_align(len(data[0]), 8)])
    chrominance_frequency_domain = \
        numpy.zeros([up_align((len(data) + 1) // 2), up_align((len(data[0]) + 1) // 2)])
    saturation_frequency_domain = \
        numpy.zeros([up_align((len(data) + 1) // 2), up_align((len(data[0]) + 1) // 2)])
    luminance_quantification = numpy.array(
        [[16, 11, 10, 16, 24, 40, 51, 61],
         [12, 12, 14, 19, 26, 58, 60, 55],
         [14, 13, 16, 24, 40, 57, 69, 56],
         [14, 17, 22, 29, 51, 87, 80, 62],
         [18, 22, 37, 56, 68, 109, 103, 77],
         [24, 35, 55, 64, 81, 104, 113, 92],
         [49, 64, 78, 87, 103, 121, 120, 101],
         [72, 92, 95, 98, 112, 100, 103, 99]]
    )
    chrominance_quantification = numpy.array(
        [[17, 18, 24, 47, 99, 99, 99, 99],
         [18, 21, 26, 66, 99, 99, 99, 99],
         [24, 26, 56, 99, 99, 99, 99, 99],
         [47, 66, 99, 99, 99, 99, 99, 99],
         [99, 99, 99, 99, 99, 99, 99, 99],
         [99, 99, 99, 99, 99, 99, 99, 99],
         [99, 99, 99, 99, 99, 99, 99, 99],
         [99, 99, 99, 99, 99, 99, 99, 99]]
    )
    luminance_res = []
    encode(luminance_time_domain, luminance_frequency_domain, luminance_quantification, luminance_res)
    chrominance_res = []
    encode(chrominance_time_domain, chrominance_frequency_domain, chrominance_quantification, chrominance_res)
    saturation_res = []
    encode(saturation_time_domain, saturation_frequency_domain, chrominance_quantification, saturation_res)
    save_img('images/out.bmp', luminance_time_domain)


if __file__ == 'main':
    main()
