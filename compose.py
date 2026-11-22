#!/usr/bin/env python3
"""Draw the front page for 21 November 2026, full-day edition.

A newspaper front page that sums up Saturday 21 November 2026, built from
the whole day's reporting: the overnight strike on Ukraine that spilled
into Poland, the double-tap attack on Kryvyi Rih, the capture of
"El Chapo Isidro", COP31 running into overtime with no deal, the Wall
Street AI rout, the pancreatic-cancer pill, BepiColombo reaching Mercury
and the Gen Z day of action. Drawn from scratch with Pillow: no network,
no downloaded assets, and the same bytes on every run.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
CRIMSON = (163, 22, 33)
NAVY = (22, 50, 79)
SLATE = (28, 38, 52)
OCHRE = (176, 124, 22)
LEAF = (46, 107, 52)
ASH = (110, 108, 100)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def load_face(filename, size):
    return ImageFont.truetype(os.path.join(DEJAVU, filename), size)


def serif_bold(size):
    return load_face("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_face("DejaVuSerif.ttf", size)


def sans_bold(size):
    return load_face("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_face("DejaVuSans.ttf", size)


def fit_lines(canvas, text, face, width):
    """Greedy wrap of text into lines no wider than width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if canvas.textlength(trial, font=face) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(canvas, x, y, lines, face, color=INK, leading=None):
    """Draw each line under the last; return the y below the block."""
    if leading is None:
        leading = int(face.size * 1.28)
    for line in lines:
        canvas.text((x, y), line, font=face, fill=color)
        y += leading
    return y


def hline(canvas, x0, x1, y, color=INK, weight=2):
    canvas.line([(x0, y), (x1, y)], fill=color, width=weight)


# ------------------------------------------------------------------ artwork
def art_market(canvas, x, y, w, h):
    canvas.rectangle([x, y, x + w, y + h], fill=(246, 226, 224))
    canvas.line([(x + 12, y + h - 14), (x + w - 10, y + h - 14)],
                fill=INK, width=2)
    canvas.line([(x + 12, y + 10), (x + 12, y + h - 14)], fill=INK, width=2)
    points = [(x + 16, y + 22), (x + 38, y + 34), (x + 58, y + 30),
              (x + 80, y + 52), (x + 100, y + 66), (x + w - 16, y + h - 26)]
    canvas.line(points, fill=CRIMSON, width=5, joint="curve")
    tip_x, tip_y = points[-1]
    canvas.polygon([(tip_x, tip_y), (tip_x - 14, tip_y - 2),
                    (tip_x - 2, tip_y + 12)], fill=CRIMSON)


def art_badge(canvas, x, y, w, h):
    """A gold star badge: the cartel boss was on the FBI's most-wanted list."""
    canvas.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx, cy = x + w // 2, y + h // 2
    canvas.ellipse([cx - 42, cy - 42, cx + 42, cy + 42],
                   outline=NAVY, width=4)
    canvas.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=NAVY)
    star = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi / 2
        radius = 26 if i % 2 == 0 else 11
        star.append((cx + int(radius * math.cos(angle)),
                     cy + int(radius * math.sin(angle))))
    canvas.polygon(star, fill=OCHRE)
    canvas.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=NAVY)


def art_world(canvas, x, y, w, h):
    canvas.rectangle([x, y, x + w, y + h], fill=(222, 236, 226))
    cx, cy, r = x + w // 2, y + h // 2 + 2, 40
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    canvas.ellipse([cx - 18, cy - r, cx + 18, cy + r], outline=NAVY, width=3)
    canvas.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=3)
    canvas.arc([cx - r, cy - 22, cx + r, cy + 22], 200, 340,
               fill=NAVY, width=3)
    canvas.arc([cx - r, cy - 22, cx + r, cy + 22], 20, 160,
               fill=NAVY, width=3)


def art_planet(canvas, x, y, w, h):
    """Mercury, cratered, with BepiColombo's orbit around it."""
    canvas.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    cx, cy, r = x + w // 2, y + h // 2 + 2, 34
    canvas.ellipse([cx - 52, cy - 20, cx + 52, cy + 20],
                   outline=OCHRE, width=2)
    canvas.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 178, 150))
    for (ox, oy, cr) in [(-14, -10, 7), (10, -16, 5), (14, 8, 8),
                         (-6, 14, 5), (2, -2, 4)]:
        canvas.ellipse([cx + ox - cr, cy + oy - cr,
                        cx + ox + cr, cy + oy + cr],
                       fill=(150, 132, 108))
    canvas.ellipse([cx + 44, cy - 24, cx + 50, cy - 18], fill=CRIMSON)


def art_capsule(canvas, x, y, w, h):
    """A two-tone pill, drawn flat, with a small green cross beside it."""
    canvas.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    cx, cy = x + w // 2, y + h // 2
    canvas.rounded_rectangle([cx - 52, cy - 16, cx + 52, cy + 16],
                             radius=16, fill=(255, 255, 255),
                             outline=CRIMSON, width=3)
    canvas.rounded_rectangle([cx - 52, cy - 16, cx, cy + 16],
                             radius=16, fill=CRIMSON)
    canvas.rectangle([cx - 16, cy - 16, cx, cy + 16], fill=CRIMSON)
    canvas.ellipse([x + w - 34, y + 12, x + w - 14, y + 32],
                   outline=LEAF, width=3)
    canvas.line([(x + w - 24, y + 16), (x + w - 24, y + 28)],
                fill=LEAF, width=3)
    canvas.line([(x + w - 30, y + 22), (x + w - 18, y + 22)],
                fill=LEAF, width=3)


def art_march(canvas, x, y, w, h):
    canvas.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    base = y + h - 14
    canvas.line([(x + 62, base - 58), (x + 62, base - 34)], fill=INK, width=3)
    canvas.rectangle([x + 36, base - 80, x + 88, base - 58], fill=CRIMSON)
    canvas.text((x + 41, base - 77), "GEN Z", font=sans_bold(12),
                fill=(255, 255, 255))
    for head_x, head_r in [(x + 28, 12), (x + 62, 14), (x + 96, 12)]:
        canvas.ellipse([head_x - head_r, base - 46,
                        head_x + head_r, base - 46 + 2 * head_r], fill=INK)
        canvas.pieslice([head_x - head_r - 4, base - 22,
                         head_x + head_r + 4, base + 12],
                        180, 360, fill=INK)


def night_city(canvas, x, y, w, h):
    """A city skyline at night, lit by missile streaks and blasts."""
    canvas.rectangle([x, y, x + w, y + h], fill=SLATE)
    for sx, sy in [(x + 30, y + 14), (x + 120, y + 26), (x + 260, y + 10),
                   (x + 420, y + 22), (x + 560, y + 12), (x + 700, y + 28),
                   (x + 850, y + 16), (x + 920, y + 30), (x + 640, y + 40)]:
        canvas.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 220, 200))
    heights = [46, 70, 54, 84, 62, 92, 58, 76, 48, 88, 66, 74]
    bx = x
    block = w // len(heights)
    for height in heights:
        canvas.rectangle([bx, y + h - height, bx + block - 3, y + h],
                         fill=(12, 18, 30))
        for wy in range(y + h - height + 8, y + h - 6, 16):
            canvas.rectangle([bx + 5, wy, bx + 9, wy + 6],
                             fill=(240, 200, 90))
        bx += block
    for (x0, y0, x1, y1) in [(x + 90, y + 8, x + 180, y + 64),
                             (x + 380, y + 4, x + 470, y + 58),
                             (x + 700, y + 6, x + 780, y + 52)]:
        canvas.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=3)
        canvas.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=(255, 210, 90))
    for (ex, ey, r) in [(x + 210, y + h - 60, 26),
                        (x + 520, y + h - 78, 32),
                        (x + 830, y + h - 56, 24)]:
        for k in range(8):
            angle = math.pi * k / 4
            canvas.line([(ex, ey),
                         (ex + int(r * math.cos(angle)),
                          ey + int(r * math.sin(angle)))],
                        fill=(255, 150, 40), width=4)
        canvas.ellipse([ex - 10, ey - 10, ex + 10, ey + 10],
                       fill=(255, 190, 60))


# ------------------------------------------------------------------ the page
sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
draw = ImageDraw.Draw(sheet)
MX = 28  # side margin

# Masthead
hline(draw, MX, PAGE_W - MX, 24, weight=3)
draw.text((PAGE_W // 2, 30), "THE WORLD TODAY", font=serif_bold(54),
          fill=INK, anchor="ma")
draw.text((PAGE_W // 2, 92), "SATURDAY, 21 NOVEMBER 2026",
          font=sans_bold(22), fill=CRIMSON, anchor="ma")
hline(draw, MX, PAGE_W - MX, 124, weight=2)
hline(draw, MX, PAGE_W - MX, 128, weight=1)
draw.text((PAGE_W // 2, 134), "One day's world news — in one picture",
          font=serif(17), fill=ASH, anchor="ma")

# Lead story: the strike that spilled into Poland, and the night that followed
y = 162
draw.text((MX, y), "UKRAINE  •  POLAND", font=sans_bold(18), fill=CRIMSON)
y += 24
y = draw_lines(draw, MX, y,
               fit_lines(draw, "Russia's biggest strike of the war — "
                    "missiles land in Poland", serif_bold(40),
                    PAGE_W - 2 * MX),
               serif_bold(40), leading=45)
y += 4
SCENE_H = 88
night_city(draw, MX, y, PAGE_W - 2 * MX, SCENE_H)
y += SCENE_H + 8
y = draw_lines(draw, MX, y,
               fit_lines(draw,
                    "More than 400 drones and 110 missiles hit Ukraine "
                    "overnight; at least eight were killed in Kyiv. Two "
                    "missiles and a drone came down in Poland — Warsaw "
                    "calls it a deliberate provocation. A day later, a "
                    "double-tap strike on Kryvyi Rih kills a boy of seven "
                    "and wounds 60.",
                    serif(19), PAGE_W - 2 * MX),
               serif(19))
y += 10

# Markets strip
draw.rectangle([MX, y, PAGE_W - MX, y + 38], fill=INK)
draw.text((PAGE_W // 2, y + 9),
          "MARKETS   S&P 500 −3.70%  ·  Nasdaq −5.28%  ·  Nikkei −5.06%  ·  "
          "DAX −2.60%  ·  Gold $3,515",
          font=sans_bold(16), fill=(255, 255, 255), anchor="ma")
y += 38 + 10

# Story grid: two columns, three rows
STORIES = [
    ("MARKETS", "AI rout drags Wall Street into correction",
     "Nvidia falls 14% and Anthropic slides on day two; the Nasdaq wipes "
     "out its 2026 gains.", art_market),
    ("MEXICO", "FBI's most-wanted cartel boss captured",
     "El Chapo Isidro is seized in Sinaloa; 11 are killed as gunmen fight "
     "the raid.", art_badge),
    ("ANTALYA", "Climate talks run into overtime",
     "COP31 ends its second week with no deal; fossil fuels are cut from "
     "the draft text.", art_world),
    ("HEALTH", "Pill makes tumours vanish in trial",
     "Daraxonrasib leaves pancreatic cancer undetectable on scans in one "
     "in 12 of 61 patients.", art_capsule),
    ("SPACE", "BepiColombo reaches Mercury",
     "After an eight-year voyage, the ESA-JAXA probe slips into orbit "
     "around Mercury.", art_planet),
    ("EUROPE", "Gen Z takes to the streets",
     "Protests spread across 25 European countries — and continue into "
     "Saturday.", art_march),
]
card_w = (PAGE_W - 2 * MX - 20) // 2
card_h = 132
for i, (kicker, head, deck, art) in enumerate(STORIES):
    cx = MX + (i % 2) * (card_w + 20)
    cy = y + (i // 2) * (card_h + 10)
    draw.rectangle([cx, cy, cx + card_w, cy + card_h], outline=INK, width=1)
    draw.line([(cx, cy + 28), (cx + card_w, cy + 28)], fill=ASH, width=1)
    draw.text((cx + 10, cy + 5), kicker, font=sans_bold(14), fill=CRIMSON)
    art(draw, cx + 8, cy + 36, 118, card_h - 44)
    tx = cx + 136
    tw = card_w - 146
    ty = draw_lines(draw, tx, cy + 36,
                    fit_lines(draw, head, serif_bold(19), tw),
                    serif_bold(19))
    deck_lines = fit_lines(draw, deck, sans(14), tw)
    room = (cy + card_h - 6 - (ty + 2)) // 17
    draw_lines(draw, tx, ty + 2, deck_lines[:room], sans(14))
y += 3 * card_h + 2 * 10 + 8

# Also today
hline(draw, MX, PAGE_W - MX, y, weight=2)
y += 6
draw.text((MX, y), "ALSO TODAY", font=sans_bold(15), fill=CRIMSON)
y += 22
y = draw_lines(draw, MX, y,
               fit_lines(draw,
                    "FBI crime database hacked  •  Houthis fire on Riyadh "
                    "— three missiles intercepted  •  Peru hit by a 6.7 "
                    "earthquake  •  GTA VI sets a $3.8bn first-day record  •  "
                    "Bitcoin bounces back above $60,000  •  Bayer pays "
                    "$7.25bn over Roundup",
                    sans(15), PAGE_W - 2 * MX),
               sans(15))
hline(draw, MX, PAGE_W - MX, PAGE_H - 26, weight=1)
draw.text((PAGE_W // 2, PAGE_H - 22),
          "Saturday 21 November 2026  ·  Every story reported on this day",
          font=sans(12), fill=ASH, anchor="ma")

print("layout: also-today band ends at y =", y,
      "(page height", PAGE_H, ")")
assert y <= PAGE_H - 26, "layout overflow: band ends past the footer"

sheet.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", os.path.getsize("entry.png"), "bytes", sheet.size)
