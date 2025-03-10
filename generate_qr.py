<<<<<<< HEAD
# python generate_qr.py runserver 192.168.7.116:8001
# python manage.py runserver 192.168.7.116:8001

import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = "http://192.168.7.116:8001"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="red", back_color="white").convert('RGB')

logo = Image.open("D:/project/harshada/holiday/static/OIP.jfif")

logo = logo.convert("RGBA")

base_width = img.size[0]
logo_size = base_width // 4
logo.thumbnail((logo_size, logo_size))

combined = Image.new("RGBA", (img.size[0], img.size[1] + 50), (255, 255, 255, 255))
combined.paste(img, (0, 0))

logo_position = (
    (img.size[0] - logo.size[0]) // 2,
    (img.size[1] - logo.size[1]) // 2
)

combined.paste(logo, logo_position, mask=logo)

final_img = combined.convert("RGB")

draw = ImageDraw.Draw(final_img)
text = "Scan Me !!!"
font_size = 40

font = ImageFont.truetype("arial.ttf", font_size)

text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_position = ((final_img.size[0] - text_width) // 2, img.size[1] + (50 - text_height) // 3)

draw.text(text_position, text, font=font, fill="black")

final_img.save("QR_CODE.png")

=======
# python generate_qr.py runserver 192.168.7.116:8001
# python manage.py runserver 192.168.7.116:8001

import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = "http://192.168.7.116:8001"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="red", back_color="white").convert('RGB')

logo = Image.open("D:/project/harshada/holiday/static/OIP.jfif")

logo = logo.convert("RGBA")

base_width = img.size[0]
logo_size = base_width // 4
logo.thumbnail((logo_size, logo_size))

combined = Image.new("RGBA", (img.size[0], img.size[1] + 50), (255, 255, 255, 255))
combined.paste(img, (0, 0))

logo_position = (
    (img.size[0] - logo.size[0]) // 2,
    (img.size[1] - logo.size[1]) // 2
)

combined.paste(logo, logo_position, mask=logo)

final_img = combined.convert("RGB")

draw = ImageDraw.Draw(final_img)
text = "Scan Me !!!"
font_size = 40

font = ImageFont.truetype("arial.ttf", font_size)

text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_position = ((final_img.size[0] - text_width) // 2, img.size[1] + (50 - text_height) // 3)

draw.text(text_position, text, font=font, fill="black")

final_img.save("QR_CODE.png")

>>>>>>> 591af9b (Initial commit)
print("QR code generated and saved as QR_CODE.png")