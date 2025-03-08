import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS

# path to the image or video
imagename = "IMG_2515.jpg"

# read the image data using PIL
image = Image.open(imagename)

# extract EXIF data
exifdata = image.getexif()

# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    # decode bytes 
    if isinstance(data, bytes):
        data = data.decode()
    print(f"{tag:25}: {data}")




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