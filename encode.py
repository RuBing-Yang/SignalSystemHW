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


def encode(time_domain: numpy.ndarray, standard_table: numpy.ndarray, directing, alternating) -> None:
    for i in range(0, time_domain.shape[0], 8):
        for j in range(0, time_domain.shape[1], 8):
            t = numpy.empty([8, 8], dtype=float)
            for u in range(0, 8):
                for v in range(0, 8):
                    t[u][v] = time_domain[i + u][j + v]
            f = numpy.matmul(A, t)
            f = numpy.matmul(f, A_T)
            quantification(f, standard_table)
            x = 0
            y = 0
            cnt = 0
            directing.append(f[0][0])
            for u in Z:
                x += u[0]
                y += u[1]
                if f[x][y] == 0:
                    cnt = cnt + 1
                else:
                    alternating.append([cnt, f[x][y]])
                    cnt = 0
            if f[7][7] == 0:
                alternating.append([0, 0])


def main():
    image = io.imread("images/demo.bmp")
    data = numpy.array(image, dtype=float)
    print(data.shape)
    file_handle = open('1.txt', mode='w')
    file_handle.write(str(int(len(data) // 16 * 16)) + '\n')
    file_handle.write(str(int(len(data[0]) // 16 * 16)) + '\n')

    luminance_time_domain = numpy.zeros([len(data) // 16 * 16, len(data[0]) // 16 * 16], dtype=float)
    blue_chrominance_time_domain = numpy.zeros([len(data) // 16 * 16, len(data[0]) // 16 * 16], dtype=float)
    red_chrominance_time_domain = numpy.zeros([len(data) // 16 * 16, len(data[0]) // 16 * 16], dtype=float)
    for i in range(0, luminance_time_domain.shape[0]):
        for j in range(0, luminance_time_domain.shape[1]):
            luminance_time_domain[i][j] = 0.299 * data[i][j][0] + 0.587 * data[i][j][1] + 0.114 * data[i][j][2]
            blue_chrominance_time_domain[i][j] = 0.492 * (data[i][j][2] - luminance_time_domain[i][j])
            red_chrominance_time_domain[i][j] = 0.877 * (data[i][j][0] - luminance_time_domain[i][j])
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
    luminance_alternating = []
    blue_chrominance_alternating = []
    red_chrominance_alternating = []
    luminance_directing = []
    blue_chrominance_directing = []
    red_chrominance_directing = []

    encode(luminance_time_domain, luminance_quantification, luminance_directing, luminance_alternating)
    file_handle.write(str(len(luminance_directing)) + '\n')
    for i in luminance_directing:
        file_handle.write(str(int(i)) + '\n')
    file_handle.write(str(len(luminance_alternating)) + '\n')
    for i in luminance_alternating:
        file_handle.write(str(int(i[0])) + '\n')
        file_handle.write(str(int(i[1])) + '\n')

    encode(blue_chrominance_time_domain, chrominance_quantification, blue_chrominance_directing,
           blue_chrominance_alternating)
    file_handle.write(str(len(blue_chrominance_directing)) + '\n')
    for i in blue_chrominance_directing:
        file_handle.write(str(int(i)) + '\n')
    file_handle.write(str(len(blue_chrominance_alternating)) + '\n')
    for i in blue_chrominance_alternating:
        file_handle.write(str(int(i[0])) + '\n')
        file_handle.write(str(int(i[1])) + '\n')

    encode(red_chrominance_time_domain, chrominance_quantification, red_chrominance_directing,
           red_chrominance_alternating)
    file_handle.write(str(len(red_chrominance_directing)) + '\n')
    for i in red_chrominance_directing:
        file_handle.write(str(int(i)) + '\n')
    file_handle.write(str(len(red_chrominance_alternating)) + '\n')
    for i in red_chrominance_alternating:
        file_handle.write(str(int(i[0])) + '\n')
        file_handle.write(str(int(i[1])) + '\n')
    print("encode end")
    file_handle.close()


def init(matrix):
    for i in range(8):
        for j in range(8):
            if i == 0:
                x = math.sqrt(1 / 8)
            else:
                x = math.sqrt(2 / 8)
            matrix[i][j] = x * math.cos(math.pi * (j + 0.5) * i / 8)


if __name__ == '__main__':
    A = numpy.zeros([8, 8])
    Z = numpy.array(
        [[0, 1], [1, -1],
         [1, 0], [-1, 1], [-1, 1],
         [0, 1], [1, -1], [1, -1], [1, -1],
         [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
         [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
         [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         [1, 0], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
         [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
         [1, 0], [1, -1], [1, -1], [1, -1],
         [0, 1], [-1, 1], [-1, 1],
         [1, 0], [1, -1],
         [0, 1]
         ]
    )
    init(A)
    A_T = A.transpose()
    A_i = numpy.linalg.inv(A)
    A_iT = numpy.linalg.inv(A_T)
    main()
