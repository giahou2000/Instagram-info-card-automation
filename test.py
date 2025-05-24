# 1. Import libraries

import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ImageFilter
import imageio.v3 as iio


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

blur_img = ski.filters.gaussian(img, sigma=(sigma, sigma), truncate=3.5, channel_axis=-1)

ski.io.imshow(blur_img)
plt.show()


# 5. Figure out if it is portrait or landscape with 4:5 or 16:9 ratio

# Get the dimensions of the image
height, width = img.shape[:2]

# Determine the orientation and aspect ratio
if width > height:
    orientation = "landscape"
else:
    orientation = "portrait"
aspect_ratio = height / width

# Check if the aspect ratio is to 4:5 or 16:9
if abs(aspect_ratio - 4/5) == 0:
    ratio = "4:5"
    print(f"Orientation: {orientation}")
    print(f"Aspect Ratio: {ratio}")
elif abs(aspect_ratio - 16/9) == 0:
    ratio = "16:9"
    print(f"Orientation: {orientation}")
    print(f"Aspect Ratio: {ratio}")
else:
    ratio = "other"
    print(f"Orientation: {orientation}")
    print(f"Aspect Ratio: {ratio}")
    # exit()

# Import a black icon and add it with glass effect to the image

# Load the black icon
icon_path = "diaphragm.png"
icon = iio.imread(icon_path)
# for im_path in glob.glob("path/to/folder/*.png"):
#      im = iio.imread(im_path)
#      print(im.shape)
ski.io.imshow(icon)
plt.show()

# Get the size of the icon
icon_size = icon.size
print("icon size")
print(icon_size)

# Calculate the position to place the icon

# Overlay the icon on the original image

# Display the final image with the icon
ski.io.imshow(img)
plt.show()

# 6. Add the semintransparent texts and the icons to the right places

# 7. Export the image

# 8. Use AI to create tags
# 9. Write the caption
# 10. Find the hashtags
# 11. Post to Instagram