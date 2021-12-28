from PIL import Image
import numpy
import numpy as np
import math
from skimage import io


def dbg(tag, img):
    print(f"{tag}: max: {np.max(img)}, min: {np.min(img)}, shape: {img.shape}, type: {img.dtype}, mean: {np.mean(img)}")
    return img

def up_align(x, y):
    if x % y == 0:
        return x
    return x + y - x % y


def quantification(frequency_domain: numpy.ndarray, standard_table: numpy.ndarray) -> None:
    for i in range(0, 8):
        for j in range(0, 8):
            frequency_domain[i][j] = round(frequency_domain[i][j] / standard_table[i][j])


def encode(time_domain: numpy.ndarray, frequency_domain: numpy.ndarray,
           standard_table: numpy.ndarray, res) -> None:
    for i in range(0, time_domain.shape[0], 8):
        for j in range(0, time_domain.shape[1], 8):
            t = numpy.empty([8, 8], dtype=float)
            for u in range(0, 8):
                for v in range(0, 8):
                    t[u][v] = time_domain[i + u][j + v]
            f = numpy.matmul(A, t)
            f = numpy.matmul(f, A_T)
            quantification(f, standard_table)
            for u in range(0, 8):
                for v in range(0, 8):
                    frequency_domain[i + u][j + v] = f[u][v]


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
            f = numpy.empty([8, 8])
            for u in range(0, 8):
                for v in range(0, 8):
                    f[u][v] = frequency_domain[i + u][j + v]
            t = numpy.matmul(A_i, f)
            t = numpy.matmul(t, A_iT)
            for u in range(0, 8):
                for v in range(0, 8):
                    time_domain[i + u][j + v] = t[u][v]


def main():
    image = Image.open("images/gray.bmp")
    data = numpy.array(image, dtype=float)
    dbg('input', data)
    print(data.shape)
    luminance_time_domain = numpy.zeros([len(data) // 8 * 8, len(data[0]) // 8 * 8], dtype=float)
    for i in range(0, luminance_time_domain.shape[0]):
        for j in range(0, luminance_time_domain.shape[1]):
            luminance_time_domain[i][j] = data[i][j] - 128
    luminance_frequency_domain = \
        numpy.zeros([luminance_time_domain.shape[0], luminance_time_domain.shape[1]], dtype=float)
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
    print("encode end")
    decode(luminance_time_domain, luminance_frequency_domain, luminance_quantification)
    res = numpy.empty([luminance_time_domain.shape[0], luminance_time_domain.shape[1]], dtype=float)
    for i in range(0, luminance_time_domain.shape[0]):
        for j in range(0, luminance_time_domain.shape[1]):
            res[i][j] = luminance_time_domain[i][j] + 128
    dbg('output', res)
    cliped = res.clip(0, 255)
    dbg('cliped', cliped)
    io.imsave("out.bmp", res)
    io.imsave("cliped.bmp", cliped)


def init(matrix):
    for i in range(8):
        for j in range(8):
            if i == 0:
                x = math.sqrt(1 / 8)
            else:
                x = math.sqrt(2 / 8)
            #x = 1
            matrix[i][j] = x * math.cos(math.pi * (j + 0.5) * i / 8)
    a = numpy.zeros([8, 8])
    x = 0
    y = 0
    cnt = 1
    for i in Z:
        x += i[0]
        y += i[1]
        a[x][y] = cnt
        cnt = cnt + 1
    print(a)


if __name__ == '__main__':
    A = numpy.zeros([8, 8])
    Z = numpy.array(
        [[0, 0],
         [0, 1], [1, -1],
         [1, 0], [-1, 1], [-1, 1],
         [0, 1], [1, -1], [1, -1], [1, -1],
         [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
         [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         ]
    )
    init(A)
    A_T = A.transpose()
    A_i = numpy.linalg.inv(A)
    A_iT = numpy.linalg.inv(A_T)
    main()
