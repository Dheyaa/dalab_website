from PIL import Image, ImageDraw, ImageFont, ImageTransform
import math

size = 512
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx, cy = size // 2, size // 2

# Colors
dark_text = (30, 30, 35)
cyan = (0, 160, 210)

# 3D cube corners as brackets (isometric)
s = 140

def iso(x, y, z):
    px = cx + (x - z) * math.cos(math.radians(30)) * 0.85
    py = cy - y * 0.85 + (x + z) * math.sin(math.radians(30)) * 0.85
    return (px, py)

vertices = [
    iso(-s, -s, -s), iso(s, -s, -s), iso(s, -s, s), iso(-s, -s, s),  # bottom
    iso(-s, s, -s), iso(s, s, -s), iso(s, s, s), iso(-s, s, s),       # top
]

bw = 4
bracket_ratio = 0.3

# Back edges (subtle)
back_edges = [(0,1),(0,3),(0,4)]
for e in back_edges:
    p1 = vertices[e[0]]
    p2 = vertices[e[1]]
    mid1_x = p1[0] + (p2[0] - p1[0]) * bracket_ratio
    mid1_y = p1[1] + (p2[1] - p1[1]) * bracket_ratio
    draw.line([p1, (mid1_x, mid1_y)], fill=(0, 160, 210, 80), width=3)
    mid2_x = p2[0] + (p1[0] - p2[0]) * bracket_ratio
    mid2_y = p2[1] + (p1[1] - p2[1]) * bracket_ratio
    draw.line([p2, (mid2_x, mid2_y)], fill=(0, 160, 210, 80), width=3)

# Front edges (bold)
front_edges = [(1,2),(2,3),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(4,7)]
for e in front_edges:
    p1 = vertices[e[0]]
    p2 = vertices[e[1]]
    mid1_x = p1[0] + (p2[0] - p1[0]) * bracket_ratio
    mid1_y = p1[1] + (p2[1] - p1[1]) * bracket_ratio
    draw.line([p1, (mid1_x, mid1_y)], fill=cyan, width=bw)
    mid2_x = p2[0] + (p1[0] - p2[0]) * bracket_ratio
    mid2_y = p2[1] + (p1[1] - p2[1]) * bracket_ratio
    draw.line([p2, (mid2_x, mid2_y)], fill=cyan, width=bw)

# Helper: draw text transformed onto a quad (perspective)
def draw_text_on_face(img, text, font, color, quad):
    """Draw text mapped onto a quadrilateral face"""
    # Create text image
    txt_img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    bbox = txt_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    txt_draw.text((100 - tw//2, 100 - th//2), text, fill=color, font=font)
    
    # Source corners (square text image)
    src_w, src_h = 200, 200
    
    # Find perspective transform coefficients
    # quad = [(x0,y0), (x1,y1), (x2,y2), (x3,y3)] - target corners
    # Map from quad back to square
    def find_coeffs(source, target):
        matrix = []
        for s, t in zip(source, target):
            matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
            matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
        A = matrix
        B = [coord for pair in source for coord in pair]
        
        # Solve using basic gaussian elimination
        import numpy
        A = numpy.array(A, dtype=float)
        B = numpy.array(B, dtype=float)
        res = numpy.linalg.solve(A, B)
        return res.tolist()
    
    try:
        import numpy
        src_pts = [(0, 0), (src_w, 0), (src_w, src_h), (0, src_h)]
        coeffs = find_coeffs(src_pts, quad)
        txt_warped = txt_img.transform((size, size), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        img.paste(txt_warped, (0, 0), txt_warped)
    except:
        pass
    
    return img

# Font for face text
try:
    font_face_da = ImageFont.truetype("bahnschrift.ttf", 110)
    font_face_lab = ImageFont.truetype("bahnschrift.ttf", 85)
except:
    font_face_da = ImageFont.load_default()
    font_face_lab = ImageFont.load_default()

# "DA" on the front face - correct reading orientation
front_face = [vertices[7], vertices[6], vertices[2], vertices[3]]
img = draw_text_on_face(img, "DA", font_face_da, dark_text, front_face)

# "LAB" on the right face - correct reading orientation
right_face = [vertices[6], vertices[5], vertices[1], vertices[2]]
img = draw_text_on_face(img, "LAB", font_face_lab, cyan, right_face)

# Crop to content and re-center
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)
    pad = 20
    new_size = (img.width + pad * 2, img.height + pad * 2)
    final = Image.new('RGBA', new_size, (0, 0, 0, 0))
    final.paste(img, (pad, pad))
    img = final

# Save
img.save('logo.png', 'PNG')
img_small = img.resize((128, 128), Image.LANCZOS)
img_small.save('logo_small.png', 'PNG')
print("Logo generated!")
