import numpy


def func(a):
    a[1][2] = 10
    print(a.shape)


b = numpy.zeros([10, 3], dtype=int)
func(b)
print(b)
