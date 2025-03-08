import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt

sigma = 20.0

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

# blur_img = ski.filters.gaussian(img, sigma=0.4)
# blur_img = ski.filters.gaussian(img, sigma=1, mode='wrap')
blur_img = ski.filters.gaussian(img, sigma=(sigma, sigma), truncate=3.5, channel_axis=-1)

ski.io.imshow(blur_img)
plt.show()