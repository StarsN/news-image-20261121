#!/usr/bin/env python3
"""Draw the news-image-20261121 front page.

A one-page newspaper front page summing up the world news of Saturday
21 November 2026, drawn from scratch with Pillow. Every story on the page
was first reported on that day. Deterministic: same bytes on every run.
Standard library + Pillow only; no network, no downloaded assets.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
RED = (163, 22, 33)
BLUE = (22, 50, 79)
DARK = (28, 38, 52)
GOLD = (176, 124, 22)
GREEN = (46, 107, 52)
GREY = (110, 108, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; returns y just below the block."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(246, 226, 224))
    draw.line([(x + 12, y + h - 14), (x + w - 10, y + h - 14)], fill=INK, width=2)
    draw.line([(x + 12, y + 10), (x + 12, y + h - 14)], fill=INK, width=2)
    pts = [(x + 16, y + 22), (x + 38, y + 34), (x + 58, y + 30),
           (x + 80, y + 52), (x + 100, y + 66), (x + w - 16, y + h - 26)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ax, ay = pts[-1]
    draw.polygon([(ax, ay), (ax - 14, ay - 2), (ax - 2, ay + 12)], fill=RED)


def icon_scales(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    cx, top = x + w // 2, y + 14
    draw.line([(cx, top), (cx, y + h - 22)], fill=INK, width=4)
    draw.line([(cx - 42, top + 8), (cx + 42, top + 8)], fill=INK, width=4)
    draw.ellipse([cx - 5, top - 6, cx + 5, top + 4], fill=GOLD)
    for sx in (cx - 42, cx + 42):
        draw.line([(sx, top + 8), (sx, top + 26)], fill=INK, width=2)
        draw.polygon([(sx - 20, top + 26), (sx + 20, top + 26),
                      (sx, top + 44)], outline=INK, width=3)
    draw.rectangle([cx - 26, y + h - 22, cx + 26, y + h - 14], fill=INK)


def icon_globe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 236, 226))
    cx, cy, r = x + w // 2, y + h // 2 + 2, 40
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    draw.ellipse([cx - 18, cy - r, cx + 18, cy + r], outline=BLUE, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=3)
    draw.arc([cx - r, cy - 22, cx + r, cy + 22], 200, 340, fill=BLUE, width=3)
    draw.arc([cx - r, cy - 22, cx + r, cy + 22], 20, 160, fill=BLUE, width=3)


def icon_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    # EU flag: blue field, circle of gold stars
    draw.rectangle([x + 12, y + 22, x + 58, y + h - 22], fill=BLUE)
    cx, cy = x + 35, y + h // 2
    for i in range(8):
        a = math.pi * 2 * i / 8 - math.pi / 2
        sx, sy = cx + int(14 * math.cos(a)), cy + int(14 * math.sin(a))
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    # UK flag: simplified cross on red
    draw.rectangle([x + 68, y + 22, x + w - 12, y + h - 22], fill=(200, 40, 50))
    draw.rectangle([x + 68, y + h // 2 - 7, x + w - 12, y + h // 2 + 7],
                   fill=(255, 255, 255))
    draw.rectangle([x + 84, y + 22, x + 98, y + h - 22], fill=(255, 255, 255))
    draw.rectangle([x + 68, y + h // 2 - 3, x + w - 12, y + h // 2 + 3],
                   fill=(200, 40, 50))
    draw.rectangle([x + 88, y + 22, x + 94, y + h - 22], fill=(200, 40, 50))


def icon_pill(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    cx, cy = x + w // 2, y + h // 2
    cap = Image.new("RGBA", (110, 44), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.rounded_rectangle([0, 0, 54, 43], radius=21, fill=RED)
    cd.rounded_rectangle([54, 0, 109, 43], radius=21, fill=(255, 255, 255))
    cd.rectangle([50, 0, 60, 43], fill=(255, 255, 255))
    cap = cap.rotate(38, expand=True, resample=Image.BICUBIC)
    img.paste(cap, (cx - cap.width // 2, cy - cap.height // 2), cap)
    draw.ellipse([x + w - 34, y + 12, x + w - 14, y + 32], outline=GREEN, width=3)
    draw.line([(x + w - 24, y + 16), (x + w - 24, y + 28)], fill=GREEN, width=3)
    draw.line([(x + w - 30, y + 22), (x + w - 18, y + 22)], fill=GREEN, width=3)


def icon_crowd(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    base = y + h - 14
    # placard held above the middle figure, kept inside the panel
    draw.line([(x + 62, base - 58), (x + 62, base - 34)], fill=INK, width=3)
    draw.rectangle([x + 36, base - 80, x + 88, base - 58], fill=RED)
    draw.text((x + 41, base - 77), "GEN Z", font=SANS_B(12),
              fill=(255, 255, 255))
    for i, (hx, r) in enumerate([(x + 28, 12), (x + 62, 14), (x + 96, 12)]):
        draw.ellipse([hx - r, base - 46, hx + r, base - 46 + 2 * r], fill=INK)
        draw.pieslice([hx - r - 4, base - 22, hx + r + 4, base + 12],
                      180, 360, fill=INK)


def lead_scene(draw, x, y, w, h):
    """Night sky over a city: missile streaks and bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    for sx, sy in [(x + 30, y + 14), (x + 120, y + 26), (x + 260, y + 10),
                   (x + 420, y + 22), (x + 560, y + 12), (x + 700, y + 28),
                   (x + 850, y + 16), (x + 920, y + 30), (x + 640, y + 40)]:
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 220, 200))
    heights = [46, 70, 54, 84, 62, 92, 58, 76, 48, 88, 66, 74]
    bx = x
    bw = w // len(heights)
    for hh in heights:
        draw.rectangle([bx, y + h - hh, bx + bw - 3, y + h], fill=(12, 18, 30))
        for wy in range(y + h - hh + 8, y + h - 6, 16):
            draw.rectangle([bx + 5, wy, bx + 9, wy + 6], fill=(240, 200, 90))
        bx += bw
    for (x0, y0, x1, y1) in [(x + 90, y + 8, x + 180, y + 64),
                             (x + 380, y + 4, x + 470, y + 58),
                             (x + 700, y + 6, x + 780, y + 52)]:
        draw.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=3)
        draw.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=(255, 210, 90))
    for (ex, ey, r) in [(x + 210, y + h - 60, 26), (x + 520, y + h - 78, 32),
                        (x + 830, y + h - 56, 24)]:
        for k in range(8):
            a = math.pi * k / 4
            draw.line([(ex, ey), (ex + int(r * math.cos(a)),
                                  ey + int(r * math.sin(a)))],
                      fill=(255, 150, 40), width=4)
        draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 190, 60))


# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img)
MX = 28  # margin

# Masthead
rule(draw, MX, W - MX, 24, width=3)
draw.text((W // 2, 30), "THE WORLD TODAY", font=SERIF_B(54), fill=INK, anchor="ma")
draw.text((W // 2, 92), "SATURDAY, 21 NOVEMBER 2026", font=SANS_B(22),
          fill=RED, anchor="ma")
rule(draw, MX, W - MX, 124, width=2)
rule(draw, MX, W - MX, 128, width=1)
draw.text((W // 2, 134), "One day's world news — in one picture",
          font=SERIF(17), fill=GREY, anchor="ma")

# Lead story (y positions flow from measured text)
y = 162
draw.text((MX, y), "UKRAINE  •  POLAND", font=SANS_B(18), fill=RED)
y += 24
y = text_block(draw, MX, y,
               wrap(draw, "Russia's biggest strike of the war — "
                    "missiles land in Poland", SERIF_B(40), W - 2 * MX),
               SERIF_B(40), leading=45)
y += 4
lead_scene(draw, MX, y, W - 2 * MX, 88)
y += 88 + 8
y = text_block(draw, MX, y,
               wrap(draw,
                    "More than 400 drones and 110 missiles hit Ukraine "
                    "overnight; at least eight were killed in Kyiv. Warsaw "
                    "says two missiles and a suspected drone came down on "
                    "Polish soil — PM Tusk calls it a deliberate provocation.",
                    SERIF(19), W - 2 * MX),
               SERIF(19), leading=24)
y += 10

# Markets strip
draw.rectangle([MX, y, W - MX, y + 38], fill=INK)
draw.text((W // 2, y + 9),
          "MARKETS   S&P 500 −3.70%  ·  Nasdaq −5.28%  ·  Nikkei −5.06%  ·  "
          "DAX −2.60%  ·  Gold $3,515",
          font=SANS_B(16), fill=(255, 255, 255), anchor="ma")
y += 38 + 10

# Story grid: 2 columns x 3 rows
CARDS = [
    ("MARKETS", "AI rout drags Wall Street into correction",
     "The S&P 500 and the Dow fall into correction as AI shares slide; "
     "the Nasdaq erases all its 2026 gains.", icon_chart),
    ("THE HAGUE", "Court: Myanmar guilty of genocide",
     "The International Court of Justice finds Myanmar responsible for "
     "genocide against the Rohingya.", icon_scales),
    ("ANTALYA", "Climate talks deadlocked",
     "COP31 runs past its deadline as nearly 200 nations fail to agree "
     "on fossil fuels.", icon_globe),
    ("BRUSSELS", "UK and EU sign biggest post-Brexit deals",
     "PM Burnham seals three agreements: food trade, carbon markets and "
     "youth mobility.", icon_flags),
    ("HEALTH", "Pill makes tumours vanish in trial",
     "Daraxonrasib leaves pancreatic cancer undetectable on scans in one "
     "in 12 patients.", icon_pill),
    ("EUROPE", "Gen Z takes to the streets",
     "Protests spread across 25 European countries.", icon_crowd),
]
cw = (W - 2 * MX - 20) // 2
ch = 132
for i, (kick, head, deck, icon) in enumerate(CARDS):
    cx = MX + (i % 2) * (cw + 20)
    cy = y + (i // 2) * (ch + 10)
    draw.rectangle([cx, cy, cx + cw, cy + ch], outline=INK, width=1)
    draw.line([(cx, cy + 28), (cx + cw, cy + 28)], fill=GREY, width=1)
    draw.text((cx + 10, cy + 5), kick, font=SANS_B(14), fill=RED)
    icon(draw, cx + 8, cy + 36, 118, ch - 44)
    tx = cx + 136
    tw = cw - 146
    ty = text_block(draw, tx, cy + 36,
                    wrap(draw, head, SERIF_B(19), tw), SERIF_B(19), leading=22)
    deck_lines = wrap(draw, deck, SANS(14), tw)
    max_deck = (cy + ch - 6 - (ty + 2)) // 17
    text_block(draw, tx, ty + 2, deck_lines[:max_deck], SANS(14), leading=17)
y += 3 * ch + 2 * 10 + 8

# Also-today band
rule(draw, MX, W - MX, y, width=2)
y += 6
draw.text((MX, y), "ALSO TODAY", font=SANS_B(15), fill=RED)
y += 22
y = text_block(draw, MX, y,
               wrap(draw,
                    "FBI crime database hacked amid US outages  •  Houthis fire "
                    "on Riyadh — three missiles intercepted  •  Peru hit by a "
                    "6.9 earthquake  •  GTA VI sets a $3.8bn first-day record  •  "
                    "Bitcoin slides toward $62,000 as $2bn of crypto is liquidated",
                    SANS(15), W - 2 * MX),
               SANS(15), leading=19)
rule(draw, MX, W - MX, H - 26, width=1)
draw.text((W // 2, H - 22),
          "Saturday 21 November 2026  ·  Every story first reported on this day",
          font=SANS(12), fill=GREY, anchor="ma")

print("layout: also-band ends at y =", y, " (page height", H, ")")
assert y <= H - 26, "layout overflow: also-band ends at %d" % y

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", os.path.getsize("entry.png"), "bytes", img.size)
