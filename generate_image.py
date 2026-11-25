#!/usr/bin/env python3
"""The World in One Day - Wednesday 25 November 2026.

Dense one-page newspaper infographic in the reference style: cream paper,
black ink, deep red and teal accents, serif headlines, stat band, lead
cards with flat illustrations, brief strip. Content: verified 25 Nov 2026
news from research-brief-v2.md. Deterministic, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
INK = (24, 22, 20)
RED = (165, 32, 28)
TEAL = (18, 105, 105)
GOLD = (176, 124, 32)
GREY = (110, 104, 94)
RULE = (60, 56, 50)
CARD = (252, 249, 240)

FD = "/usr/share/fonts/truetype/liberation/"
def f(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28  # margin
CW = W - 2 * M

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_wrap(x, y, s, font, maxw, fill=INK, leading=None, max_lines=None):
    leading = leading or int(font.size * 1.22)
    lines = wrap(s, font, maxw)
    if max_lines: lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def rule(x0, y, x1, wdt=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)

# ---- masthead ----
d.text((M, 24), "THE WORLD IN ONE DAY", font=f(SANS_B, 19), fill=INK)
r = "WEDNESDAY · 25 NOVEMBER 2026"
d.text((W - M - text_w(r, f(SANS_B, 19)), 24), r, font=f(SANS_B, 19), fill=RED)
rule(M, 52, W - M, 3)
title = "Wednesday 25 November 2026"
tf = f(SERIF_B, 54)
d.text(((W - text_w(title, tf)) / 2, 58), title, font=tf, fill=INK)
sub = "Pakistan's first astronaut flies to Tiangong  ◆  Asia's chip stocks slide  ◆  Drones over Ras Tanura"
sf = f(SERIF_I, 19)
d.text(((W - text_w(sub, sf)) / 2, 120), sub, font=sf, fill=(70, 64, 56))
# region strip
regions = [("ASIA", (176, 124, 32)), ("MIDDLE EAST", (165, 32, 28)), ("EUROPE", (18, 105, 105)),
           ("AMERICAS", (70, 100, 160)), ("AFRICA", (120, 130, 60)), ("GLOBAL", (90, 70, 120))]
rx = M
for name, col in regions:
    rw_ = CW / len(regions)
    d.rectangle([rx, 142, rx + rw_ - 3, 160], fill=col)
    rf = f(SANS_B, 12)
    d.text((rx + (rw_ - 3 - text_w(name, rf)) / 2, 145), name, font=rf, fill=(250, 248, 240))
    rx += rw_
rule(M, 166, W - M, 2)

# ---- timeline strip ----
ty = 174
d.rectangle([M, ty, W - M, ty + 30], fill=INK)
tl = "THE DAY IN UTC   00:18 Shenzhou-24 lifts off   ·   Asia markets slide   ·   Houthis claim Ras Tanura attack   ·   COP31 closes with no deal"
tlf = f(SANS_B, 15)
d.text(((W - text_w(tl, tlf)) / 2, ty + 7), tl, font=tlf, fill=PAPER)

# ---- stat band ----
stats = [
    ("1st", "foreign astronaut to board Tiangong"),
    ("−5.3%", "Korean shares, intraday low"),
    ("4", "drones downed at Ras Tanura, coalition says"),
    ("11", "wounded in Riyadh tower strike"),
    ("5", "protein targets bound in lab, OpenAI says"),
    ("0", "headline deal at COP31"),
]
sy = 214
sw = CW / len(stats)
for i, (num, lab) in enumerate(stats):
    x = M + i * sw
    if i: d.line([(x, sy + 2), (x, sy + 62)], fill=(200, 192, 172), width=1)
    d.text((x + 8, sy), num, font=f(SERIF_B, 34), fill=RED)
    draw_wrap(x + 8, sy + 42, lab, f(SANS, 12), sw - 14, fill=(70, 64, 56), leading=15)
rule(M, sy + 78, W - M, 2)

# ---- lead cards ----
def rocket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 36, 58))
    for sx, sy2 in [(18, 14), (64, 34), (120, 12), (210, 20), (262, 44), (288, 14)]:
        d.ellipse([x + sx, y + sy2, x + sx + 3, y + sy2 + 3], fill=(240, 238, 220))
    # Earth curve (kept inside the art box)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(52, 110, 140))
    d.arc([x + 6, y + h - 52, x + w - 6, y + h + 24], start=180, end=360, fill=(120, 190, 220), width=2)
    # orbit arc to station
    d.arc([x + 60, y + 8, x + w - 30, y + h - 6], start=200, end=340, fill=(150, 200, 230), width=2)
    sx, sy2 = x + w - 52, y + 22
    d.rectangle([sx - 8, sy2 - 4, sx + 8, sy2 + 4], fill=(235, 232, 222))
    d.rectangle([sx - 26, sy2 - 3, sx - 10, sy2 + 3], fill=(90, 150, 200))
    d.rectangle([sx + 10, sy2 - 3, sx + 26, sy2 + 3], fill=(90, 150, 200))
    # launch tower + rocket + smoke
    cx = x + 86
    d.line([(cx + 22, y + h - 20), (cx + 22, y + 30)], fill=(170, 166, 154), width=3)
    d.line([(cx + 22, y + 44), (cx + 8, y + 44)], fill=(170, 166, 154), width=2)
    d.polygon([(cx - 10, y + h - 30), (cx + 10, y + h - 30), (cx + 6, y + 36), (cx, y + 18), (cx - 6, y + 36)], fill=(238, 236, 226))
    d.ellipse([cx - 4, y + 42, cx + 4, y + 50], fill=TEAL)
    d.polygon([(cx - 10, y + h - 30), (cx - 20, y + h - 14), (cx - 4, y + h - 18)], fill=RED)
    d.polygon([(cx + 10, y + h - 30), (cx + 20, y + h - 14), (cx + 4, y + h - 18)], fill=RED)
    d.polygon([(cx - 5, y + h - 28), (cx + 5, y + h - 28), (cx, y + h - 8)], fill=(245, 180, 70))
    for ox, oy, r in [(-26, -14, 9), (-10, -10, 12), (8, -12, 10), (24, -14, 8)]:
        d.ellipse([cx + ox - r, y + h + oy - r, cx + ox + r, y + h + oy + r], fill=(210, 206, 194))

def chart(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 30, 34))
    # chip
    cx, cy = x + 62, y + 52
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(52, 60, 68), outline=(150, 200, 230), width=2)
    for i in range(-2, 3):
        d.line([(cx + i * 10, cy - 34), (cx + i * 10, cy - 26)], fill=(150, 200, 230), width=2)
        d.line([(cx + i * 10, cy + 26), (cx + i * 10, cy + 34)], fill=(150, 200, 230), width=2)
        d.line([(cx - 34, cy + i * 10), (cx - 26, cy + i * 10)], fill=(150, 200, 230), width=2)
        d.line([(cx + 26, cy + i * 10), (cx + 34, cy + i * 10)], fill=(150, 200, 230), width=2)
    d.line([(cx - 16, cy - 24), (cx - 4, cy - 6), (cx - 12, cy + 8), (cx + 2, cy + 24)], fill=(235, 90, 80), width=3)
    # candlesticks falling
    candles = [(150, 26, 44), (178, 34, 54), (206, 44, 62), (234, 58, 76), (262, 70, 88)]
    for ox, top, bot in candles:
        d.line([(x + ox, y + top - 8), (x + ox, y + bot + 8)], fill=(235, 90, 80), width=2)
        d.rectangle([x + ox - 7, y + top, x + ox + 7, y + bot], fill=(200, 60, 50))
    d.line([(x + 140, y + 22), (x + 272, y + 86)], fill=(245, 180, 70), width=2)
    d.text((x + 12, y + h - 22), "KOSPI −5.3%   TAIEX −5.1%   NVIDIA −5.9%", font=f(SANS_B, 13), fill=(240, 238, 220))

def refinery(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 204, 172))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(150, 120, 84))
    # storage tanks
    for tx, tr in [(28, 20), (86, 15)]:
        d.ellipse([x + tx, y + h - 24 - tr * 2, x + tx + tr * 2, y + h - 24], fill=(120, 112, 98))
        d.rectangle([x + tx, y + h - 24 - tr, x + tx + tr * 2, y + h - 24], fill=(120, 112, 98))
    # flare stack + tower
    d.rectangle([x + 150, y + 30, x + 162, y + h - 24], fill=(90, 84, 76))
    d.polygon([(x + 152, y + 30), (x + 160, y + 30), (x + 156, y + 16)], fill=(245, 180, 70))
    d.rectangle([x + 190, y + h - 56, x + 240, y + h - 24], fill=(110, 100, 86))
    d.line([(x + 162, y + h - 44), (x + 190, y + h - 44)], fill=(90, 84, 76), width=3)
    # drone + dashed path + interception burst
    dx, dy = x + 262, y + 26
    for i in range(4):
        d.line([(x + 196 + i * 14, y + 40 - i * 3), (x + 204 + i * 14, y + 38 - i * 3)], fill=RED, width=2)
    d.line([(dx - 11, dy - 5), (dx + 11, dy + 5)], fill=INK, width=2)
    d.line([(dx - 11, dy + 5), (dx + 11, dy - 5)], fill=INK, width=2)
    d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=INK)
    bx, by = x + 232, y + 44
    for ang in [(0, -10), (8, -6), (10, 2), (6, 9), (-2, 10), (-9, 4), (-8, -6)]:
        d.line([(bx, by), (bx + ang[0], by + ang[1])], fill=(245, 150, 50), width=2)
    d.text((x + 12, y + h - 20), "4 DRONES DOWNED · COALITION SAYS", font=f(SANS_B, 11), fill=(240, 238, 220))

leads = [
    dict(art=rocket, loc="JIUQUAN, CHINA · SPACE", tag="CONFIRMED", tagc=TEAL,
         head="Shenzhou-24 flies a Pakistani to Tiangong",
         body="Muhammad Zeeshan Ali is the first foreign astronaut to board China's station; the Long March-2F lifted off at 00:18 UTC.",
         src="REUTERS"),
    dict(art=chart, loc="ASIA-PACIFIC · MARKETS", tag="CONFIRMED", tagc=TEAL,
         head="Asia's chip stocks slide as AI rally stumbles",
         body="MSCI Asia-Pacific ex-Japan fell 2.3%; Korean shares dropped as much as 5.3% and Taiwan 5.1% as tariff threats hit tech valuations.",
         src="REUTERS"),
    dict(art=refinery, loc="RAS TANURA, SAUDI ARABIA", tag="CLAIM", tagc=RED,
         head="Houthis say they hit a Saudi refinery",
         body="The Saudi-led coalition says four drones were destroyed at Ras Tanura; 11 people were wounded in Tuesday's Riyadh tower strike.",
         src="REUTERS"),
]
ly = 292
lh = 268
lw = (CW - 16) / 3
for i, c in enumerate(leads):
    x = M + i * (lw + 8)
    d.rectangle([x + 4, ly + 4, x + lw + 4, ly + lh + 4], fill=(222, 214, 192))
    d.rectangle([x, ly, x + lw, ly + lh], fill=CARD, outline=(205, 196, 175), width=1)
    c["art"](x + 6, ly + 6, lw - 12, 96)
    d.ellipse([x + 10, ly + 10, x + 34, ly + 34], fill=RED)
    nf = f(SANS_B, 15)
    d.text((x + 22 - text_w(str(i + 1), nf) / 2, ly + 14), str(i + 1), font=nf, fill=(250, 248, 240))
    d.text((x + 10, ly + 108), c["loc"], font=f(SANS_B, 12), fill=GREY)
    twd = text_w(c["tag"], f(SANS_B, 12)) + 12
    d.rectangle([x + lw - twd - 8, ly + 105, x + lw - 8, ly + 123], outline=c["tagc"], width=1)
    d.text((x + lw - twd - 2, ly + 108), c["tag"], font=f(SANS_B, 12), fill=c["tagc"])
    y2 = draw_wrap(x + 10, ly + 128, c["head"], f(SERIF_B, 24), lw - 20, leading=28)
    y2 = draw_wrap(x + 10, y2 + 4, c["body"], f(SANS, 14), lw - 20, fill=(50, 46, 40), leading=19)
    d.text((x + 10, ly + lh - 24), c["src"], font=f(SANS_B, 12), fill=GREY)

# ---- second row ----
def sea_drone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 74, 92))
    for i in range(5):
        yy = y + 10 + i * 9
        d.line([(x + 8 + (i % 2) * 14, yy), (x + 60 + (i % 2) * 14, yy)], fill=(120, 170, 190), width=2)
    d.polygon([(x + 120, y + h - 12), (x + 170, y + h - 12), (x + 160, y + h - 22), (x + 128, y + h - 22)], fill=(200, 60, 50))
    d.rectangle([x + 140, y + h - 30, x + 150, y + h - 22], fill=(230, 228, 218))
    d.polygon([(x + 30, y + h - 14), (x + 62, y + h - 14), (x + 46, y + h - 24)], fill=(240, 238, 220))
    d.line([(x + 46, y + h - 24), (x + 46, y + h - 34)], fill=(240, 238, 220), width=2)

def cop_globe(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 214))
    cx, cy, r = x + w // 2, y + h // 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=TEAL, width=2)
    d.polygon([(cx + 14, cy - 16), (cx + 30, cy - 22), (cx + 28, cy - 6)], fill=(90, 150, 80))
    d.line([(cx - 26, cy + 14), (cx + 26, cy - 14)], fill=RED, width=3)

def oil_pump(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 210, 178))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(150, 120, 84))
    cx = x + w // 2
    d.polygon([(cx - 26, y + h - 12), (cx + 26, y + h - 12), (cx, y + 16)], outline=INK, width=3)
    d.line([(cx - 44, y + 18), (cx + 40, y + 10)], fill=INK, width=4)
    d.polygon([(cx + 40, y + 10), (cx + 52, y + 16), (cx + 40, y + 22)], fill=INK)
    d.line([(cx - 44, y + 18), (cx - 44, y + h - 18)], fill=INK, width=3)
    d.ellipse([cx - 6, y + 12, cx + 6, y + 24], fill=RED)

def protein(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 40, 58))
    import math
    pts = []
    for i in range(13):
        px = x + 26 + i * ((w - 52) / 12)
        py = y + h / 2 + 14 * math.sin(i * 1.1)
        pts.append((px, py))
    d.line(pts, fill=(150, 200, 230), width=3)
    for i, (px, py) in enumerate(pts):
        c = (240, 170, 60) if i % 3 == 0 else (200, 220, 240)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=c)

cards = [
    ("UKRAINE · REPORTED 25 NOV", "Sea-drone war reaches Libya and the Baltic",
     "Kyiv confirms strikes on Sparta II (21 Nov) and corvette Merkury in Benghazi (22 Nov); Tripoli objects."),
    ("ANTALYA, TÜRKIYE · CLIMATE", "COP31 ends without a deal",
     "First climate summit since Copenhagen 2009 to close with no headline agreement; focus shifts to COP32."),
    ("IRAQ · REPORTED 25 NOV", "Baghdad orders takeover of Kurdish oilfields",
     "Federal control ordered for crossings and fields in four provinces after a smuggling probe; Erbil rejects it."),
    ("AI RESEARCH · 25 NOV", "GPT-6 proteins bound in lab tests",
     "General models designed the proteins, by OpenAI's account."),
]
ry = ly + lh + 12
rh = 190
rw = (CW - 24) / 4
arts = [sea_drone, cop_globe, oil_pump, protein]
for i, (loc, head, body) in enumerate(cards):
    x = M + i * (rw + 8)
    d.rectangle([x + 3, ry + 3, x + rw + 3, ry + rh + 3], fill=(222, 214, 192))
    d.rectangle([x, ry, x + rw, ry + rh], fill=CARD, outline=(205, 196, 175), width=1)
    d.rectangle([x, ry, x + rw, ry + 5], fill=TEAL if i % 2 == 0 else RED)
    arts[i](x + 6, ry + 9, rw - 12, 46)
    d.ellipse([x + 9, ry + 12, x + 29, ry + 32], fill=RED)
    nf = f(SANS_B, 13)
    d.text((x + 19 - text_w(str(i + 4), nf) / 2, ry + 15), str(i + 4), font=nf, fill=(250, 248, 240))
    y2 = draw_wrap(x + 9, ry + 60, loc, f(SANS_B, 11), rw - 18, fill=GREY, leading=14)
    y2 = draw_wrap(x + 9, y2 + 2, head, f(SERIF_B, 18), rw - 18, leading=22)
    draw_wrap(x + 9, y2 + 3, body, f(SANS, 12), rw - 18, fill=(50, 46, 40), leading=16)
    d.text((x + 9, ry + rh - 20), "OPENAI REPORT" if i == 3 else "REUTERS", font=f(SANS_B, 11), fill=GREY)

# ---- map strip ----
my = ry + rh + 12
mh = 78
d.rectangle([M, my, W - M, my + mh], fill=CARD, outline=(205, 196, 175), width=1)
d.text((M + 10, my + 8), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=INK)
d.text((M + 10, my + 26), "pins = story numbers", font=f(SANS, 11), fill=GREY)
# rough continent shapes (relative coords in map area)
mx0, mx1 = M + 190, W - M - 12
mw = mx1 - mx0
def mp(fx, fy):
    return (mx0 + fx * mw, my + 6 + fy * (mh - 12))
continents = [
    [(0.02, 0.30), (0.10, 0.12), (0.22, 0.16), (0.24, 0.34), (0.18, 0.48), (0.12, 0.44), (0.06, 0.50)],
    [(0.20, 0.56), (0.28, 0.60), (0.27, 0.80), (0.22, 0.92), (0.19, 0.74)],
    [(0.44, 0.20), (0.52, 0.14), (0.56, 0.28), (0.50, 0.36), (0.45, 0.32)],
    [(0.47, 0.44), (0.56, 0.42), (0.59, 0.62), (0.53, 0.86), (0.48, 0.66)],
    [(0.58, 0.18), (0.78, 0.12), (0.88, 0.26), (0.82, 0.44), (0.70, 0.50), (0.62, 0.40), (0.58, 0.30)],
    [(0.80, 0.62), (0.90, 0.60), (0.92, 0.76), (0.83, 0.78)],
]
for poly in continents:
    d.polygon([mp(fx, fy) for fx, fy in poly], fill=(206, 196, 172))
pins = [(1, 0.74, 0.34), (2, 0.83, 0.42), (3, 0.605, 0.46), (4, 0.50, 0.26), (5, 0.545, 0.30), (6, 0.575, 0.34), (7, 0.13, 0.34)]
for num, fx, fy in pins:
    px, py = mp(fx, fy)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
    nf = f(SANS_B, 11)
    d.text((px - text_w(str(num), nf) / 2, py - 6), str(num), font=nf, fill=(250, 248, 240))

# ---- brief strip ----
by = my + mh + 12
d.text((M, by), "ALSO ON WEDNESDAY 25 NOVEMBER", font=f(SANS_B, 15), fill=INK)
rule(M, by + 24, W - M, 2)
brief = [
    "FRANCE — Sarkozy trial ordered; hearing 1 Apr 2027",
    "FOOTBALL — Real Madrid 5–1 PSV; Mbappé ×2",
    "MALAYSIA — six carbon hubs; $41.3B by 2050",
    "BRITAIN — record 5,258 heat deaths",
]
def brief_icon(i, x, y):
    if i == 0:  # scales of justice
        d.line([(x + 9, y), (x + 9, y + 16)], fill=INK, width=2)
        d.line([(x + 1, y + 3), (x + 17, y + 3)], fill=INK, width=2)
        d.polygon([(x + 1, y + 3), (x + 5, y + 3), (x + 3, y + 9)], fill=GOLD)
        d.polygon([(x + 13, y + 3), (x + 17, y + 3), (x + 15, y + 9)], fill=GOLD)
    elif i == 1:  # football
        d.ellipse([x + 1, y + 1, x + 17, y + 17], outline=INK, width=2)
        d.polygon([(x + 9, y + 5), (x + 13, y + 8), (x + 11, y + 13), (x + 7, y + 13), (x + 5, y + 8)], fill=INK)
    elif i == 2:  # factory + leaf
        d.rectangle([x + 1, y + 8, x + 17, y + 17], fill=(120, 110, 96))
        d.rectangle([x + 3, y + 3, x + 6, y + 8], fill=(120, 110, 96))
        d.polygon([(x + 11, y + 1), (x + 17, y + 3), (x + 12, y + 7)], fill=(90, 150, 80))
    else:  # sun
        d.ellipse([x + 4, y + 4, x + 14, y + 14], fill=(240, 170, 60))
        for dx, dy in [(9, 0), (9, 18), (0, 9), (18, 9), (2, 2), (16, 2), (2, 16), (16, 16)]:
            d.line([(x + 9, y + 9), (x + dx, y + dy)], fill=(240, 170, 60), width=2)

colw = (CW - 24) / 4
for i, b in enumerate(brief):
    x = M + i * (colw + 8)
    y = by + 30
    d.text((x, y), str(i + 8), font=f(SERIF_B, 18), fill=RED)
    brief_icon(i, x + 24, y + 1)
    draw_wrap(x, y + 24, b, f(SANS, 12), colw - 4, fill=(50, 46, 40), leading=16)

# ---- footer ----
fy = H - 44
rule(M, fy - 10, W - M, 2)
d.text((M, fy), "Sources: Reuters (space, markets, Middle East, COP31, Iraq, Malaysia). Claims are attributed; dates shown per story.", font=f(SANS, 12), fill=GREY)
foot = "DRAWN BY AN AI AGENT FOR MAKE.FUN · ONE DAY, ONE PAGE"
d.text((M, fy + 18), foot, font=f(SANS_B, 12), fill=INK)
r2 = "25 NOVEMBER 2026"
d.text((W - M - text_w(r2, f(SANS_B, 12)), fy + 18), r2, font=f(SANS_B, 12), fill=RED)

img.save("entry.png")
print("saved")
