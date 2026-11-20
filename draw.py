"""Draw the 20 November 2026 world-news front page, 1024x1024 PNG.

Everything is drawn with PIL primitives and crisp vector text — no image
model is used for any lettering, so nothing can come out garbled. Every
story below was verified for 20 Nov 2026 (BBC / PBS / UN News / CNBC /
Sky News / Just Security). No numbers, quotes or events are invented.
Run:  python3 draw.py   (writes entry.png next to this file)
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (22, 35, 63)
NAVY_LT = (38, 58, 96)
RED = (178, 28, 28)
GOLD = (197, 160, 90)
GREY = (90, 88, 82)
PANEL = (255, 255, 255)
PANEL_ALT = (238, 240, 244)
GREEN = (31, 122, 76)
TEAL = (14, 116, 116)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def icon_court(d, x, y, s, color):
    # Courthouse: pediment triangle, three columns, base.
    d.polygon([(x, y + s * 0.35), (x + s, y + s * 0.35), (x + s / 2, y)], fill=color)
    for i in range(3):
        cx = x + s * (0.18 + i * 0.32)
        d.rectangle([cx - s * 0.06, y + s * 0.42, cx + s * 0.06, y + s * 0.85], fill=color)
    d.rectangle([x, y + s * 0.88, x + s, y + s], fill=color)


def icon_skyline(d, x, y, s, color):
    # City skyline: bars of different heights.
    hs = [0.55, 0.85, 0.65, 1.0, 0.75, 0.9]
    bw = s / len(hs)
    for i, h in enumerate(hs):
        d.rectangle([x + i * bw + 2, y + s * (1 - h), x + (i + 1) * bw - 2, y + s], fill=color)


def icon_chart(d, x, y, s, color):
    # Line chart: rising zig-zag with an arrowhead.
    pts = [(x, y + s * 0.75), (x + s * 0.25, y + s * 0.6), (x + s * 0.45, y + s * 0.68),
           (x + s * 0.7, y + s * 0.35), (x + s * 0.95, y + s * 0.15)]
    d.line(pts, fill=color, width=6, joint="curve")
    d.polygon([(x + s * 0.95, y + s * 0.15), (x + s * 0.72, y + s * 0.12), (x + s * 0.88, y + s * 0.38)], fill=color)
    d.line([(x, y + s), (x + s, y + s)], fill=color, width=4)


def icon_tower(d, x, y, s, color):
    # Tall tower with a small burst above it.
    d.rectangle([x + s * 0.35, y + s * 0.25, x + s * 0.65, y + s], fill=color)
    d.rectangle([x + s * 0.28, y + s * 0.12, x + s * 0.72, y + s * 0.25], fill=color)
    cx, cy = x + s * 0.5, y + s * 0.06
    for dx, dy in [(0, -1), (0.7, -0.7), (1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7)]:
        d.line([(cx, cy), (cx + dx * s * 0.14, cy + dy * s * 0.14)], fill=RED, width=3)


def icon_bridge(d, x, y, s, color):
    # Bridge: deck, arch and suspenders.
    d.arc([x, y + s * 0.1, x + s, y + s * 1.1], start=180, end=360, fill=color, width=6)
    d.line([(x, y + s * 0.75), (x + s, y + s * 0.75)], fill=color, width=6)
    for i in range(5):
        bx = x + s * (0.1 + i * 0.2)
        d.line([(bx, y + s * 0.45), (bx, y + s * 0.75)], fill=color, width=3)


def icon_cross(d, x, y, s, color):
    # Medical cross in a circle.
    d.ellipse([x, y, x + s, y + s], outline=color, width=5)
    d.rectangle([x + s * 0.42, y + s * 0.2, x + s * 0.58, y + s * 0.8], fill=color)
    d.rectangle([x + s * 0.2, y + s * 0.42, x + s * 0.8, y + s * 0.58], fill=color)


def panel(d, x, y, w, h, tag, tag_color, headline, body, icon, bg=PANEL):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=(200, 196, 186), width=2)
    d.rectangle([x, y, x + w, y + 6], fill=tag_color)
    pad = 20
    ix = x + w - 78
    iy = y + 20
    if icon:
        icon(d, ix, iy, 56, tag_color)
    tag_f = font(SANS_B, 23)
    d.text((x + pad, y + 18), tag, font=tag_f, fill=tag_color)
    head_f = font(SERIF_B, 30)
    text_w = w - pad * 2 - (86 if icon else 0)
    lines = wrap(d, headline, head_f, text_w)
    yy = draw_lines(d, lines, x + pad, y + 52, head_f, INK, 36)
    body_f = font(SANS, 20)
    blines = wrap(d, body, body_f, w - pad * 2)
    draw_lines(d, blines, x + pad, yy + 8, body_f, (52, 52, 52), 26)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 122], fill=GOLD)
mast = font(SERIF_B, 84)
d.text((W / 2, 14), "WORLD NEWS", font=mast, fill=(255, 255, 255), anchor="ma")
sub = font(SANS, 19)
d.text((W / 2, 96), "T H E   W O R L D   I N   O N E   P A G E", font=sub, fill=GOLD, anchor="ma")

# ---- Date bar ----
date_f = font(SANS_B, 37)
d.text((W / 2, 138), "FRIDAY  20  NOVEMBER  2026", font=date_f, fill=RED, anchor="ma")
d.line([(28, 188), (W - 28, 188)], fill=INK, width=3)
d.line([(28, 193), (W - 28, 193)], fill=INK, width=1)

# ---- Lead story: The Hague ----
lx, ly, lw, lh = 28, 206, 968, 204
d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL, outline=(200, 196, 186), width=2)
d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
d.text((lx + 28, ly + 14), "THE HAGUE", font=font(SANS_B, 24), fill=RED)
icon_court(d, lx + lw - 118, ly + 26, 84, NAVY)
lead_head = font(SERIF_B, 40)
lines = wrap(d, "World Court: Myanmar committed genocide", lead_head, lw - 56 - 130)
draw_lines(d, lines, lx + 28, ly + 46, lead_head, INK, 47)
lead_body = font(SANS, 21)
blines = wrap(d, "Judges rule 9–6 against Myanmar over the Rohingya — the first time the court has held a state responsible for genocide.", lead_body, lw - 56 - 130)
draw_lines(d, blines, lx + 28, ly + 46 + len(lines) * 47 + 6, lead_body, (52, 52, 52), 26)

# ---- Grid: 2 x 2 ----
gx, gy = 28, 422
gw, gh, gap = 476, 224, 14
panel(d, gx, gy, gw, gh, "SHENZHEN", NAVY_LT,
      "Trump, Xi and Putin meet in first three-way summit",
      "Leaders sign a four-point joint declaration; no breakthrough on Ukraine or Iran.",
      icon_skyline)
panel(d, gx + gw + gap, gy, gw, gh, "MARKETS", GREEN,
      "Anthropic soars on debut; stocks slide",
      "Shares close 17% above the $83 IPO price at about $97. S&P 500 falls about 2% for a fifth day; Nikkei down 4.8%.",
      icon_chart, bg=PANEL_ALT)
panel(d, gx, gy + gh + gap, gw, gh, "RIYADH", RED,
      "Houthi missile damages Riyadh finance tower",
      "A missile damages the Public Investment Fund tower in the financial district; no injuries reported.",
      icon_tower)
panel(d, gx + gw + gap, gy + gh + gap, gw, gh, "KYIV", NAVY_LT,
      "Russian strikes hit Kyiv bridges; 8 killed",
      "Overnight strikes target bridges in Kyiv, killing 8 and injuring 28; Ukraine's allies meet in Berlin.",
      icon_bridge, bg=PANEL_ALT)

# ---- Bottom strip: Kenya ----
bx, by, bw, bh = 28, 896, 968, 100
d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
d.text((bx + 22, by + 10), "KENYA", font=font(SANS_B, 22), fill=(255, 214, 120))
icon_cross(d, bx + bw - 84, by + 20, 58, (255, 255, 255))
d.text((bx + 22, by + 38), "Kenya discharges its last Ebola patient", font=font(SERIF_B, 29), fill=(255, 255, 255))
d.text((bx + 22, by + 74), "The last patient leaves hospital 37 days after Kenya's first case.", font=font(SANS, 19), fill=(214, 220, 232))

# ---- Footer: sources ----
d.text((W / 2, 1004), "Sources: BBC  •  PBS  •  UN News  •  CNBC  •  Sky News  •  Just Security  —  20 November 2026",
       font=font(SANS, 15), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
