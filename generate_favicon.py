from PIL import Image

img = Image.open('logo.png')
# Resize to standard favicon sizes
img_32 = img.resize((32, 32), Image.LANCZOS)
img_16 = img.resize((16, 16), Image.LANCZOS)
img_48 = img.resize((48, 48), Image.LANCZOS)

img_32.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
print("Favicon generated!")
