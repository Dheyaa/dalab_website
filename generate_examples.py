from PIL import Image, ImageDraw, ImageFont
import math

# Generate examples of each style
examples = []

cyan = (0, 160, 210)
dark = (30, 30, 35)

# --- 1. STENCIL CUT ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("bahnschrift.ttf", 60)
draw.text((30, 20), "DA LAB", fill=dark, font=font)
# Cut horizontal gaps through letters
for y in [48, 52]:
    draw.rectangle([(0, y), (300, y+4)], fill=(240, 242, 245))
draw.text((30, 100), "1. Stencil Cut", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_1_stencil.png')

# --- 2. DOT MATRIX ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
# Draw "DA LAB" as dots on a grid
text = "DALAB"
dot_size = 4
grid = {
    'D': [[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0]],
    'A': [[0,1,1,0],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
    'L': [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],
    'B': [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,1,1,0]],
}
start_x = 25
for ch in text:
    if ch in grid:
        for row_i, row in enumerate(grid[ch]):
            for col_i, val in enumerate(row):
                if val:
                    x = start_x + col_i * (dot_size * 2 + 2)
                    y = 20 + row_i * (dot_size * 2 + 2)
                    draw.ellipse([(x, y), (x+dot_size*2, y+dot_size*2)], fill=cyan)
        start_x += len(grid[ch][0]) * (dot_size * 2 + 2) + 12
draw.text((30, 100), "2. Dot Matrix", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_2_dots.png')

# --- 3. LINE/WIREFRAME ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("bahnschrift.ttf", 60)
# Draw outline only by drawing text multiple times offset, then erasing center
for offset in [(-1,-1),(-1,1),(1,-1),(1,1),(0,-1),(0,1),(-1,0),(1,0)]:
    draw.text((30+offset[0], 20+offset[1]), "DA LAB", fill=cyan, font=font)
draw.text((30, 20), "DA LAB", fill=(240, 242, 245), font=font)
draw.text((30, 100), "3. Wireframe", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_3_wireframe.png')

# --- 4. HEXAGONAL ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("bahnschrift.ttf", 55)
draw.text((30, 20), "DA LAB", fill=dark, font=font)
# Overlay hex pattern
hex_r = 8
for row in range(10):
    for col in range(25):
        hx = col * hex_r * 1.8 + (row % 2) * hex_r * 0.9
        hy = row * hex_r * 1.5 + 20
        pts = [(hx + hex_r * math.cos(math.radians(60*i)), hy + hex_r * math.sin(math.radians(60*i))) for i in range(6)]
        draw.polygon(pts, outline=(0, 160, 210, 40))
draw.text((30, 100), "4. Hexagonal", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_4_hex.png')

# --- 5. CIRCUIT BOARD ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("consola.ttf", 50)
draw.text((25, 25), "DA LAB", fill=dark, font=font)
# Add circuit nodes and lines
nodes = [(20,80),(60,80),(100,90),(140,80),(180,90),(220,80),(270,85)]
for i in range(len(nodes)-1):
    draw.line([nodes[i], nodes[i+1]], fill=cyan, width=2)
for n in nodes:
    draw.ellipse([(n[0]-3, n[1]-3), (n[0]+3, n[1]+3)], fill=cyan)
draw.text((30, 100), "5. Circuit Board", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_5_circuit.png')

# --- 6. PIXEL ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
px = 6
pixel_font = {
    'D': [[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0]],
    'A': [[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,0,0,1]],
    'L': [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],
    'B': [[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,1,1,0]],
}
start_x = 30
for ch in "DALAB":
    if ch in pixel_font:
        for row_i, row in enumerate(pixel_font[ch]):
            for col_i, val in enumerate(row):
                if val:
                    x = start_x + col_i * (px + 1)
                    y = 20 + row_i * (px + 1)
                    draw.rectangle([(x, y), (x+px, y+px)], fill=cyan)
        start_x += len(pixel_font[ch][0]) * (px + 1) + 10
draw.text((30, 100), "6. Pixel", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_6_pixel.png')

# --- 7. LOW-POLY / TRIANGULATED ---
img = Image.new('RGBA', (300, 150), (240, 242, 245, 255))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("bahnschrift.ttf", 60)
# Draw text with triangle fill pattern
draw.text((30, 20), "DA LAB", fill=dark, font=font)
# Overlay triangles
import random
random.seed(42)
for _ in range(30):
    x = random.randint(30, 260)
    y = random.randint(20, 75)
    s = random.randint(8, 15)
    tri = [(x, y), (x+s, y+s), (x-s//2, y+s)]
    draw.polygon(tri, outline=(0, 160, 210, 80))
draw.text((30, 100), "7. Low-Poly", fill=(100,100,100), font=ImageFont.truetype("arial.ttf", 18))
img.save('example_7_lowpoly.png')

# --- Combine all into one image ---
final = Image.new('RGBA', (940, 340), (240, 242, 245, 255))
for i in range(7):
    ex = Image.open(f'example_{i+1}_{"stencil,dots,wireframe,hex,circuit,pixel,lowpoly".split(",")[i]}.png')
    col = i % 4
    row = i // 4
    final.paste(ex, (col * 310 + 10, row * 160 + 10))

final.save('font_examples.png')
print("All 7 examples generated! Check font_examples.png and individual example_*.png files")
