from PIL import Image, ImageFilter, ImageDraw, ImageFont
import piexif

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

# Create shadow layer for the panel
shadow = Image.new("RGBA", (panel_width + 40, panel_height + 40), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
# Draw shadow with blur effect
shadow_draw.rectangle(
    [(5, 5), (panel_width + 35, panel_height + 35)],
    fill=(0, 0, 0, 60)
)
# Blur the shadow
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=100))
# Paste shadow
blurred.paste(shadow, (panel_x + 60, panel_y - 60), shadow)

# Glass effect: semi-transparent white rectangle
glass_panel = Image.new("RGBA", (panel_width, panel_height), (255, 255, 255, 200))
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

draw.multiline_text(
    (text_x, text_y),
    metadata_text,
    fill=(255, 255, 255, 230),
    font=font,
    spacing=10
)

# -------------------------
# Save Output
# -------------------------

blurred.convert("RGB").save(output_path)
print("Saved:", output_path)
