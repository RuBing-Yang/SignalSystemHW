from PIL import Image
import numpy
from keras.preprocessing.image import save_img

image = Image.open("images/image.bmp")
data = numpy.asarray(image)
print(type(data))
print(data.shape[0])
Y = []
for i in data:
    tmp1 = []
    for j in i:
        tmp2 = []
        for k in j:
            tmp2.append(k)
        tmp1.append(tmp2)
    Y.append(tmp1)
x = numpy.array(Y)
print(x)
save_img('images/out.bmp', x)
