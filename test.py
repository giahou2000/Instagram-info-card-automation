# 1. Import libraries
import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS


# 2. Read the metadata

# path to the image or video
imagename = "IMG_2515.jpg"

# read the image data using PIL
image = Image.open(imagename)

# extract EXIF data
exifdata = image._getexif()
 
# looping through all the tags present in exifdata
for tagid in exifdata:
     
    # getting the tag name instead of tag id
    tagname = TAGS.get(tagid, tagid)
 
    # passing the tagid to get its respective value
    value = exifdata.get(tagid)
   
    # printing the final result
    print(f"{tagname:25}: {value}")

# 3. Gather specific useful metadata in a dictionary
metadata = {}

# Define the specific tags we are interested in
specific_tags = {
    'DateTime': 'Date and Time',
    'Model': 'Camera Model',
    'LensModel': 'Lens Model',
    'FNumber': 'Aperture',
    'ExposureTime': 'Exposure Time',
    'ISOSpeedRatings': 'ISO',
    'FocalLength': 'Focal Length',
    'Software': 'Software'
}

# looping through all the tags present in exifdata
for tagid in exifdata:
     
    # getting the tag name instead of tag id
    tagname = TAGS.get(tagid, tagid)
 
    # if the tagname is in our specific tags list, store it
    if tagname in specific_tags:
        # passing the tagid to get its respective value
        value = exifdata.get(tagid)
        # storing the tagname and value in the dictionary
        metadata[specific_tags[tagname]] = value

# printing the metadata dictionary
print('Dictionary')
print(metadata)

# 4. Blur image

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

# 5. Figure out if it is portrait or landscape with 4:5 or 16:9 ratio

# 6. Configure the text

# 7. Import icons

# 8. Add the semintransparent texts and the icons to the right places

# 9. Export the image

# 10. Optional tasks: Use AI to create tags, write the instagram post text, make the instagram post