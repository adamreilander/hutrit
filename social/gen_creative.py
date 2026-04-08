"""
Generates Hutrit Club job-posting creative PNG (1080x1920)
Fullstack Developer campaign
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "C:/Windows/Fonts/"
OUT   = os.path.dirname(os.path.abspath(__file__))

# Colours
BG           = (245, 245, 243)
DARK_GREEN   = (0,  60,  47)
BRIGHT_GREEN = (23, 168, 91)
WHITE        = (255, 255, 255)
GRAY_TEXT    = (80,  80,  80)
GRAY_LIGHT   = (51, 51, 51)
BORDER_GRAY  = (200, 215, 210)

W, H = 1080, 1920
img  = Image.new("RGB", (W, H), BG)
d    = ImageDraw.Draw(img)

def fnt(size, bold=False, italic=False):
    if bold and italic: return ImageFont.truetype(FONTS + "arialbi.ttf", size)
    if bold:            return ImageFont.truetype(FONTS + "arialbd.ttf", size)
    if italic:          return ImageFont.truetype(FONTS + "ariali.ttf", size)
    return ImageFont.truetype(FONTS + "arial.ttf", size)

def rr(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def text_w(text, f):
    bb = f.getbbox(text)
    return bb[2] - bb[0]

def text_h(text, f):
    bb = f.getbbox(text)
    return bb[3] - bb[1]

# ── Dot background ─────────────────────────────────────────────────────────────
dot_layer = Image.new("RGBA", (W, H), (0,0,0,0))
dd = ImageDraw.Draw(dot_layer)
for row in range(0, H + 44, 44):
    for col in range(0, W + 44, 44):
        dd.ellipse([col-2, row-2, col+2, row+2], fill=(160, 195, 185, 55))
base = img.convert("RGBA")
base.alpha_composite(dot_layer)
img = base.convert("RGB")
d   = ImageDraw.Draw(img)

PAD = 76

# ── 1. LOGO BADGE ──────────────────────────────────────────────────────────────
badge_y = 80
badge_h = 72
f_hutrit = fnt(36, bold=True)
f_club   = fnt(36, bold=True, italic=True)
hw = text_w("Hutrit", f_hutrit)
cw = text_w("Club",   f_club)
badge_w = hw + cw + 50
rr(d, [PAD, badge_y, PAD + badge_w, badge_y + badge_h], radius=60, fill=DARK_GREEN)
ty = badge_y + (badge_h - text_h("H", f_hutrit)) // 2
d.text((PAD + 25, ty), "Hutrit", font=f_hutrit, fill=WHITE)
d.text((PAD + 25 + hw, ty), "Club", font=f_club, fill=WHITE)

# ── 2. ESTAMOS CONTRATANDO ─────────────────────────────────────────────────────
f_ec = fnt(50, bold=True)
for i, line in enumerate(["ESTAMOS", "CONTRATANDO"]):
    lw = text_w(line, f_ec)
    d.text((W - PAD - lw, badge_y + i * 58), line, font=f_ec, fill=BRIGHT_GREEN)

# ── 3. JOB TITLE ───────────────────────────────────────────────────────────────
f_title = fnt(152, bold=True)

# measure to ensure it fits; shrink if needed
title_lines = ["FULLSTACK", "DEVELOPER"]
max_title_w = max(text_w(l, f_title) for l in title_lines)
while max_title_w > (W - 2 * PAD + 10):
    f_title = fnt(f_title.size - 4, bold=True)
    max_title_w = max(text_w(l, f_title) for l in title_lines)

title_y = badge_y + badge_h + 68
for line in title_lines:
    d.text((PAD, title_y), line, font=f_title, fill=DARK_GREEN)
    title_y += text_h(line, f_title) + 6

title_bottom = title_y

# ── 4. SKILL PILLS ─────────────────────────────────────────────────────────────
skills   = [".NET / .NET Core", "C#", "Angular", "SQL"]
gap      = 22
pill_h   = 88
inner_w  = W - 2 * PAD
pill_w   = (inner_w - gap) // 2
f_skill  = fnt(38, bold=True)
skills_y = title_bottom + 58

for i, sk in enumerate(skills):
    col = i % 2
    row = i // 2
    px  = PAD + col * (pill_w + gap)
    py  = skills_y + row * (pill_h + gap)
    rr(d, [px, py, px + pill_w, py + pill_h], radius=55, fill=WHITE, outline=DARK_GREEN, width=4)
    cx = px + pill_w // 2
    cy = py + pill_h // 2
    sw = text_w(sk, f_skill)
    sh = text_h(sk, f_skill)
    d.text((cx - sw // 2, cy - sh // 2), sk, font=f_skill, fill=DARK_GREEN)

skills_bottom = skills_y + 2 * (pill_h + gap) - gap

# ── 5. INFO BOX ────────────────────────────────────────────────────────────────
f_info_r = fnt(36)
f_info_b = fnt(36, bold=True)

row_h     = 76
box_pad_x = 52
box_pad_y = 42
n_rows    = 3
box_h     = box_pad_y * 2 + n_rows * row_h - 10
box_top   = skills_bottom + 54

# soft shadow
for s in range(10, 0, -1):
    a = int(12 * (1 - s/11))
    sh = Image.new("RGBA", (W, H), (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [PAD + s, box_top + s, W - PAD + s, box_top + box_h + s],
        radius=28, fill=(0, 60, 47, a))
    base2 = img.convert("RGBA")
    base2.alpha_composite(sh)
    img = base2.convert("RGB")
    d   = ImageDraw.Draw(img)

rr(d, [PAD, box_top, W - PAD, box_top + box_h], radius=28, fill=WHITE, outline=BORDER_GRAY, width=2)

# Small square bullet icons (no emoji)
rows_data = [
    ("$",  "Salario inicial: ",  "$700 - $1.000 USD",  True),
    ("@",  "Modalidad: ",        "remoto - desde LATAM", False),
    ("O",  "Experiencia requerida: ", "3 a 5 Años",     False),
]

f_icon = fnt(30, bold=True)
icon_symbols = ["⊙", "⊘", "⊗"]  # fallback to ascii circles

# Use simple geometric indicators
icon_size = 28
for i, (_, lbl, val, green_val) in enumerate(rows_data):
    ry = box_top + box_pad_y + i * row_h + (row_h - text_h("A", f_info_r)) // 2
    ix = PAD + box_pad_x
    # draw small circle bullet
    d.ellipse([ix, ry + 6, ix + icon_size, ry + icon_size + 6],
              outline=GRAY_TEXT, width=2)

    tx = ix + icon_size + 18
    lw = text_w(lbl, f_info_r)
    d.text((tx, ry), lbl, font=f_info_r, fill=GRAY_TEXT)
    val_col = BRIGHT_GREEN if green_val else (17, 17, 17)
    d.text((tx + lw, ry), val, font=f_info_b, fill=val_col)

# ── 6. CTA BUTTON ──────────────────────────────────────────────────────────────
cta_h  = 108
cta_y  = H - 90 - cta_h
rr(d, [PAD, cta_y, W - PAD, cta_y + cta_h], radius=65, fill=BRIGHT_GREEN)

f_cta = fnt(42, bold=True)
cta_t = "REGÍSTRATE CON TU CV"
tw    = text_w(cta_t, f_cta)
th    = text_h(cta_t, f_cta)
d.text((PAD + 55, cta_y + (cta_h - th) // 2), cta_t, font=f_cta, fill=WHITE)

# circle with down-arrow
cr     = 40
cx_c   = W - PAD - cr - 14
cy_c   = cta_y + cta_h // 2
d.ellipse([cx_c - cr, cy_c - cr, cx_c + cr, cy_c + cr],
          fill=(255,255,255,0), outline=WHITE, width=3)
# arrow stem
d.line([(cx_c, cy_c - 18), (cx_c, cy_c + 10)], fill=WHITE, width=4)
# arrowhead
aw = 16
d.polygon([
    (cx_c - aw, cy_c + 2),
    (cx_c + aw, cy_c + 2),
    (cx_c,      cy_c + 22),
], fill=WHITE)

# ── Save ───────────────────────────────────────────────────────────────────────
out_path = os.path.join(OUT, "hutritclub-fullstack-developer.png")
img.save(out_path, "PNG", dpi=(300, 300))
print(f"OK -> {out_path}")
print(f"Title font size used: {f_title.size}")
