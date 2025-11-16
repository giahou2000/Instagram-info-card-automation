from PIL import Image, ImageFilter, ImageDraw, ImageFont
import piexif
import textwrap

# -------------------------
# Load Image and Metadata
# -------------------------

image_path = "IMG_2515.jpg"
output_path = "output_glassmorph.jpg"

img = Image.open(image_path).convert("RGBA")

# Load EXIF data
exif_dict = piexif.load(image_path)

def get_exif_value(ifd, tag):
    try:
        return exif_dict[ifd][tag]
    except KeyError:
        return None

# Common EXIF tags
camera_model = get_exif_value("0th", piexif.ImageIFD.Model)
f_number     = get_exif_value("Exif", piexif.ExifIFD.FNumber)
exposure     = get_exif_value("Exif", piexif.ExifIFD.ExposureTime)
iso          = get_exif_value("Exif", piexif.ExifIFD.ISOSpeedRatings)
focal_len    = get_exif_value("Exif", piexif.ExifIFD.FocalLength)

# Convert rational values
def rational_to_float(rational):
    return round(rational[0] / rational[1], 2)

# Build metadata text
metadata_text = f"""
Camera: {camera_model}
Aperture: f/{rational_to_float(f_number)} 
Shutter: {exposure[0]}/{exposure[1]} sec
ISO: {iso}
Focal Length: {rational_to_float(focal_len)} mm
""".strip()

# -------------------------
# Create a blurred background
# -------------------------

blurred = img.filter(ImageFilter.GaussianBlur(radius=20))

# -------------------------
# Add Glassmorphism Panel
# -------------------------

draw = ImageDraw.Draw(blurred)

# Image dimensions
W, H = img.size

# Glass panel size: 80% of the image
panel_width = int(W * 0.8)
panel_height = int(H * 0.8)
# Center the panel
panel_x = (W - panel_width) // 2
panel_y = (H - panel_height) // 2

# Glass effect: semi-transparent white rectangle
glass_panel = Image.new("RGBA", (panel_width, panel_height), (255, 255, 255, 80))
blurred.paste(glass_panel, (panel_x, panel_y), glass_panel)

# -------------------------
# Add Text
# -------------------------

try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()

# Text box: 80% of panel
text_box_width = int(panel_width * 0.8)
text_box_height = int(panel_height * 0.8)

# Center text box in panel
text_x = panel_x + (panel_width - text_box_width) // 2
text_y = panel_y + (panel_height - text_box_height) // 2

# Wrap text to fit inside text box width
lines = textwrap.wrap(metadata_text, width=30)  # tweak width for line breaks

# Measure total height of text block
draw = ImageDraw.Draw(blurred)
line_height = font.getsize("A")[1] + 10  # line spacing
total_text_height = line_height * len(lines)

# Starting y position for vertical centering
start_y = text_y + (text_box_height - total_text_height) // 2

# Draw text
for i, line in enumerate(lines):
    w, h = draw.textsize(line, font=font)
    draw.text(
        (text_x + (text_box_width - w)//2, start_y + i*line_height),
        line,
        fill=(255, 255, 255, 230),
        font=font
    )

# -------------------------
# Save Output
# -------------------------

blurred.convert("RGB").save(output_path)
print("Saved:", output_path)
