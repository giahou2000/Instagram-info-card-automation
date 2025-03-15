# 1. Import libraries

import skimage as ski
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ImageFilter


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

# Get the dimensions of the image
height, width = img.shape[:2]

# Determine the orientation and aspect ratio
if width > height:
    orientation = "landscape"
else:
    orientation = "portrait"
aspect_ratio = height / width

# Check if the aspect ratio is close to 4:5 or 16:9
if abs(aspect_ratio - 4/5) < 0.01:
    ratio = "4:5"
    print(f"Orientation: {orientation}")
    print(f"Aspect Ratio: {ratio}")
elif abs(aspect_ratio - 16/9) < 0.01:
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
icon = Image.open(icon_path).convert("RGBA")

# Get the size of the icon
icon_size = icon.size

# Create a glass effect by applying a Gaussian blur to the icon
icon_blur = icon.filter(ImageFilter.GaussianBlur(radius=5))

# Calculate the position to place the icon (bottom-right corner with some padding)
padding = 10
position = (img.shape[1] - icon_size[0] - padding, img.shape[0] - icon_size[1] - padding)

# Convert the blurred image to an array
icon_blur_array = np.array(icon_blur)

# Overlay the icon on the original image
for i in range(icon_size[1]):
    for j in range(icon_size[0]):
        if icon_blur_array[i, j, 3] > 0:  # Check the alpha channel
            img[position[1] + i, position[0] + j] = icon_blur_array[i, j, :3]

# Display the final image with the icon
ski.io.imshow(img)
plt.show()

# 6. Add the semintransparent texts and the icons to the right places

# 7. Export the image

# 8. Optional tasks: Use AI to create tags, write the instagram post text, make the instagram post