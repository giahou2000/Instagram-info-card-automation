import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt

filename = os.path.join(ski.data_dir, 'IMG_2515.JPG')
img = ski.io.imread(filename)

print("shape")
print(img.shape)
print("size")
print(img.size)
print("min and max")
print(img.min(), img.max())
print("mean")
print(img.mean())

blur_img = ski.filters.gaussian(img, sigma=0.4)
# ski.filters.gaussian(img, sigma=1, mode='reflect')

ski.io.imshow(blur_img)
plt.show()