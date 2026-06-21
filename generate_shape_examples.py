from PIL import Image, ImageDraw, ImageFont
import math

cyan = (0, 160, 210)
dark = (30, 30, 35)
bg = (240, 242, 245, 255)

# --- 1. TEXT INSIDE HEXAGON ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 140
radius = 110
pts = [(cx + radius * math.cos(math.radians(60*i - 30)), cy + radius * math.sin(math.radians(60*i - 30))) for i in range(6)]
draw.polygon(pts, outline=cyan, fill=None)
draw.polygon(pts, outline=cyan)
# Draw thicker hex
for i in range(6):
    draw.line([pts[i], pts[(i+1)%6]], fill=cyan, width=4)
font_da = ImageFont.truetype("bahnschrift.ttf", 70)
font_lab = ImageFont.truetype("bahnschrift.ttf", 35)
da_bb = draw.textbbox((0,0), "DA", font=font_da)
draw.text((cx - (da_bb[2]-da_bb[0])//2, cy - 45), "DA", fill=dark, font=font_da)
lab_bb = draw.textbbox((0,0), "LAB", font=font_lab)
draw.text((cx - (lab_bb[2]-lab_bb[0])//2, cy + 30), "LAB", fill=cyan, font=font_lab)
draw.text((50, 265), "1. Hexagon", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_1_hexagon.png')

# --- 2. TEXT AROUND CIRCLE ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 150
radius = 100
draw.ellipse([(cx-radius, cy-radius), (cx+radius, cy+radius)], outline=cyan, width=3)
draw.ellipse([(cx-70, cy-70), (cx+70, cy+70)], outline=cyan, width=2)
font_c = ImageFont.truetype("bahnschrift.ttf", 28)
# Place letters around top arc
text = "DA LAB"
for i, ch in enumerate(text):
    angle = math.radians(-90 + (i - len(text)/2 + 0.5) * 25)
    tx = cx + (radius - 20) * math.cos(angle) - 8
    ty = cy + (radius - 20) * math.sin(angle) - 10
    draw.text((tx, ty), ch, fill=dark, font=font_c)
# Center icon
font_sm = ImageFont.truetype("bahnschrift.ttf", 40)
draw.text((cx-25, cy-20), "3D", fill=cyan, font=font_sm)
draw.text((50, 265), "2. Circle", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_2_circle.png')

# --- 3. TRIANGLE/PYRAMID ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 150
# Triangle outline
tri = [(150, 40), (50, 230), (250, 230)]
for i in range(3):
    draw.line([tri[i], tri[(i+1)%3]], fill=cyan, width=4)
font_da = ImageFont.truetype("bahnschrift.ttf", 55)
font_lab = ImageFont.truetype("bahnschrift.ttf", 38)
da_bb = draw.textbbox((0,0), "DA", font=font_da)
draw.text((cx - (da_bb[2]-da_bb[0])//2, 95), "DA", fill=dark, font=font_da)
lab_bb = draw.textbbox((0,0), "LAB", font=font_lab)
draw.text((cx - (lab_bb[2]-lab_bb[0])//2, 160), "LAB", fill=cyan, font=font_lab)
draw.text((50, 265), "3. Triangle", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_3_triangle.png')

# --- 4. TEXT ON CUBE FACES ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 150
s = 70
def iso(x, y, z):
    px = cx + (x - z) * math.cos(math.radians(30)) * 0.9
    py = cy - y * 0.9 + (x + z) * math.sin(math.radians(30)) * 0.9
    return (px, py)
verts = [
    iso(-s,-s,-s), iso(s,-s,-s), iso(s,-s,s), iso(-s,-s,s),
    iso(-s,s,-s), iso(s,s,-s), iso(s,s,s), iso(-s,s,s),
]
draw.polygon([verts[4],verts[5],verts[6],verts[7]], fill=(0,200,240,150))
draw.polygon([verts[1],verts[5],verts[6],verts[2]], fill=(0,140,190,150))
draw.polygon([verts[2],verts[6],verts[7],verts[3]], fill=(0,100,160,150))
edges = [(0,1),(0,3),(0,4),(1,2),(2,3),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(4,7)]
for e in edges:
    draw.line([verts[e[0]], verts[e[1]]], fill=cyan, width=2)
# Text on front face
font_sm = ImageFont.truetype("bahnschrift.ttf", 22)
draw.text((130, 155), "DA", fill=(255,255,255), font=font_sm)
draw.text((95, 140), "LAB", fill=(255,255,255), font=ImageFont.truetype("bahnschrift.ttf", 16))
draw.text((50, 265), "4. Cube Faces", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_4_cube.png')

# --- 5. TEXT FILLING AR BRACKETS ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 140
bl = 50
bw = 5
left, right, top, bottom = 40, 260, 60, 220
# Brackets
draw.line([(left, top), (left+bl, top)], fill=cyan, width=bw)
draw.line([(left, top), (left, top+bl)], fill=cyan, width=bw)
draw.line([(right, top), (right-bl, top)], fill=cyan, width=bw)
draw.line([(right, top), (right, top+bl)], fill=cyan, width=bw)
draw.line([(left, bottom), (left+bl, bottom)], fill=cyan, width=bw)
draw.line([(left, bottom), (left, bottom-bl)], fill=cyan, width=bw)
draw.line([(right, bottom), (right-bl, bottom)], fill=cyan, width=bw)
draw.line([(right, bottom), (right, bottom-bl)], fill=cyan, width=bw)
# Big text filling the frame
font_big = ImageFont.truetype("bahnschrift.ttf", 72)
font_med = ImageFont.truetype("bahnschrift.ttf", 45)
da_bb = draw.textbbox((0,0), "DA", font=font_big)
draw.text((cx - (da_bb[2]-da_bb[0])//2, 80), "DA", fill=dark, font=font_big)
lab_bb = draw.textbbox((0,0), "LAB", font=font_med)
draw.text((cx - (lab_bb[2]-lab_bb[0])//2, 150), "LAB", fill=cyan, font=font_med)
draw.text((50, 265), "5. AR Brackets", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_5_brackets.png')

# --- 6. DIAMOND ---
img = Image.new('RGBA', (300, 300), bg)
draw = ImageDraw.Draw(img)
cx, cy = 150, 145
diamond_size = 115
diamond = [(cx, cy-diamond_size), (cx+diamond_size, cy), (cx, cy+diamond_size), (cx-diamond_size, cy)]
for i in range(4):
    draw.line([diamond[i], diamond[(i+1)%4]], fill=cyan, width=4)
font_da = ImageFont.truetype("bahnschrift.ttf", 60)
font_lab = ImageFont.truetype("bahnschrift.ttf", 32)
da_bb = draw.textbbox((0,0), "DA", font=font_da)
draw.text((cx - (da_bb[2]-da_bb[0])//2, cy - 40), "DA", fill=dark, font=font_da)
lab_bb = draw.textbbox((0,0), "LAB", font=font_lab)
draw.text((cx - (lab_bb[2]-lab_bb[0])//2, cy + 25), "LAB", fill=cyan, font=font_lab)
draw.text((50, 275), "6. Diamond", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('shape_6_diamond.png')

# Combine all
final = Image.new('RGBA', (940, 640), bg)
for i in range(6):
    names = ['hexagon','circle','triangle','cube','brackets','diamond']
    ex = Image.open(f'shape_{i+1}_{names[i]}.png')
    col = i % 3
    row = i // 3
    final.paste(ex, (col * 310 + 10, row * 320 + 10))
final.save('shape_examples.png')
print("All 6 shape examples generated! Check shape_examples.png")
