from PIL import Image, ImageFilter, ImageDraw, ImageFont
import piexif

# -------------------------
# Load Image and Metadata
# -------------------------

image_path = "input.jpg"
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
camera_make  = get_exif_value("0th", piexif.ImageIFD.Make)
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
Camera: {camera_make} {camera_model}
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

W, H = img.size
panel_width = int(W * 0.45)
panel_height = int(H * 0.35)
panel_x = 40
panel_y = H - panel_height - 40

# Glass effect: semi-transparent white rectangle
glass_panel = Image.new("RGBA", (panel_width, panel_height), (255, 255, 255, 80))
blurred.paste(glass_panel, (panel_x, panel_y), glass_panel)

# Add subtle border
border = Image.new("RGBA", (panel_width, panel_height), (255, 255, 255, 60))
draw.rounded_rectangle(
    [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height)],
    radius=20,
    outline=(255, 255, 255, 120),
    width=3
)

# -------------------------
# Add Text
# -------------------------

try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()

text_x = panel_x + 30
text_y = panel_y + 30

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
