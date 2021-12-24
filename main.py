from PIL import Image
from numpy import asarray
from keras.preprocessing.image import save_img

image = Image.open("images/image.bmp")
data = asarray(image)
print(data[1][1])
print(data.shape)
save_img('images/out.bmp', data)
