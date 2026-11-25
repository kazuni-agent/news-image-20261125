#!/usr/bin/env python3
"""The Day in Full - Wednesday 25 November 2026.

Original one-page design (not based on any reference layout): cool paper,
navy ink, coral/teal/amber accents. Asymmetric grid: big date block,
lead story panel with orbit diagram, market bars, stacked right rail,
dot-matrix mini map, brief footer. Content: verified 25 Nov 2026 news.
Deterministic, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (244, 246, 248)
INK = (20, 32, 43)
NAVY = (18, 38, 58)
CORAL = (228, 87, 46)
TEAL = (15, 118, 110)
AMBER = (233, 180, 76)
GREY = (96, 110, 122)
CARD = (255, 255, 255)
LINE = (205, 214, 222)

FD = "/usr/share/fonts/truetype/liberation/"
def f(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 30
CW = W - 2 * M

def tw(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_wrap(x, y, s, font, maxw, fill=INK, leading=None):
    leading = leading or int(font.size * 1.22)
    for ln in wrap(s, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def chip(x, y, num, col):
    d.rounded_rectangle([x, y, x + 26, y + 26], radius=6, fill=col)
    nf = f(SANS_B, 15)
    d.text((x + 13 - tw(str(num), nf) / 2, y + 4), str(num), font=nf, fill=(255, 255, 255))

def card(x, y, w, h):
    d.rounded_rectangle([x + 3, y + 3, x + w + 3, y + h + 3], radius=10, fill=(226, 232, 238))
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE, width=1)

# ---------- header ----------
d.text((M, 26), "THE DAY IN FULL", font=f(SANS_B, 20), fill=INK)
d.text((M, 52), "25", font=f(SERIF_B, 92), fill=NAVY)
d.text((M + 118, 66), "NOVEMBER", font=f(SANS_B, 34), fill=CORAL)
d.text((M + 118, 106), "2026 · WEDNESDAY", font=f(SANS_B, 20), fill=GREY)
d.text((M + 118, 132), "World news of one day, on one page", font=f(SERIF_I, 18), fill=INK)
# circular badge
bx, by, br = W - M - 52, 84, 52
d.ellipse([bx - br, by - br, bx + br, by + br], fill=NAVY)
d.ellipse([bx - br + 7, by - br + 7, bx + br - 7, by + br - 7], outline=AMBER, width=2)
d.text((bx - tw("ONE DAY", f(SANS_B, 15)) / 2, by - 22), "ONE DAY", font=f(SANS_B, 15), fill=(255, 255, 255))
d.text((bx - tw("ONE PAGE", f(SANS_B, 15)) / 2, by - 2), "ONE PAGE", font=f(SANS_B, 15), fill=AMBER)
d.text((bx - tw("11 STORIES", f(SANS_B, 12)) / 2, by + 18), "11 STORIES", font=f(SANS_B, 12), fill=(200, 214, 226))
d.line([(M, 164), (W - M, 164)], fill=INK, width=3)
d.line([(M, 170), (W - M, 170)], fill=CORAL, width=2)

# ---------- lead panel (left) ----------
LX, LY, LW = M, 186, 540
LH1 = 300
card(LX, LY, LW, LH1)
# orbit diagram
ox, oy, ow, oh = LX + 14, LY + 14, LW - 28, 150
d.rounded_rectangle([ox, oy, ox + ow, oy + oh], radius=8, fill=NAVY)
for sx, sy in [(30, 20), (90, 44), (180, 16), (300, 30), (430, 18), (470, 60)]:
    d.ellipse([ox + sx, oy + sy, ox + sx + 3, oy + sy + 3], fill=(240, 238, 220))
# Earth
ex, ey, er = ox + 170, oy + 96, 46
d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(52, 110, 140))
d.arc([ex - er, ey - er, ex + er, ey + er], 20, 160, fill=(140, 200, 220), width=3)
d.ellipse([ex - 26, ey - 20, ex - 2, ey - 2], fill=(90, 160, 120))
d.ellipse([ex + 6, ey + 8, ex + 28, ey + 24], fill=(90, 160, 120))
# orbit + station (kept inside the art box)
d.ellipse([ox + 36, ey - 64, ox + ow - 36, ey + 54], outline=(150, 200, 230), width=2)
sx, sy = ex + 168, ey - 52
d.rectangle([sx - 9, sy - 5, sx + 9, sy + 5], fill=(238, 236, 226))
d.rectangle([sx - 30, sy - 4, sx - 11, sy + 4], fill=(90, 150, 200))
d.rectangle([sx + 11, sy - 4, sx + 30, sy + 4], fill=(90, 150, 200))
d.line([(ex + 40, ey - 40), (sx - 14, sy + 2)], fill=AMBER, width=2)
d.ellipse([ex + 36, ey - 44, ex + 44, ey - 36], fill=AMBER)
d.text((ox + 12, oy + oh - 24), "SHENZHOU-24 → TIANGONG · LIFTOFF 00:18 UTC", font=f(SANS_B, 13), fill=(240, 238, 220))
chip(LX + 14, LY + 178, 1, CORAL)
d.text((LX + 50, LY + 182), "SPACE · JIUQUAN, CHINA · CONFIRMED", font=f(SANS_B, 12), fill=GREY)
y = draw_wrap(LX + 14, LY + 208, "Pakistan's first astronaut reaches Tiangong", f(SERIF_B, 27), LW - 28, leading=32)
draw_wrap(LX + 14, y + 2, "Muhammad Zeeshan Ali is the first foreign astronaut to board China's space station; the Long March-2F lifted off at 00:18 UTC with a crew of three.", f(SANS, 14), LW - 28, fill=(52, 64, 76), leading=19)

# ---------- markets panel (left, below lead) ----------
MY = LY + LH1 + 14
MH = 196
card(LX, MY, LW, MH)
chip(LX + 14, MY + 12, 2, TEAL)
d.text((LX + 50, MY + 16), "MARKETS · ASIA-PACIFIC · CONFIRMED", font=f(SANS_B, 12), fill=GREY)
y = draw_wrap(LX + 14, MY + 42, "Chip stocks slide as the AI rally stumbles", f(SERIF_B, 23), LW - 28, leading=27)
bars = [("KOSPI", -5.3), ("TAIEX", -5.1), ("NVIDIA", -5.9), ("MSCI APAC ex-JP", -2.3)]
byy = y + 8
for name, val in bars:
    d.text((LX + 14, byy), name, font=f(SANS_B, 12), fill=INK)
    bw = int(abs(val) / 6.5 * 300)
    d.rounded_rectangle([LX + 150, byy + 1, LX + 150 + bw, byy + 13], radius=4, fill=CORAL)
    d.text((LX + 156 + bw, byy), f"{val:.1f}%", font=f(SANS_B, 12), fill=CORAL)
    byy += 22
d.text((LX + 14, MY + MH - 24), "Tariff threats hit tech valuations · REUTERS", font=f(SANS, 12), fill=GREY)

# ---------- right rail ----------
RX = LX + LW + 14
RW = W - M - RX
rail = [
    (3, CORAL, "MIDDLE EAST · CLAIM", "Houthis say they hit a Saudi refinery",
     "Coalition says four drones were destroyed at Ras Tanura; 11 wounded in Tuesday's Riyadh tower strike."),
    (4, TEAL, "EUROPE · REPORTED 25 NOV", "Sea-drone war reaches Libya and the Baltic",
     "Kyiv confirms strikes on Sparta II (21 Nov) and Merkury in Benghazi (22 Nov); Tripoli objects."),
    (5, TEAL, "CLIMATE · ANTALYA", "COP31 ends without a deal",
     "First climate summit since Copenhagen 2009 to close with no headline agreement."),
    (6, CORAL, "IRAQ · REPORTED 25 NOV", "Baghdad orders takeover of Kurdish oilfields",
     "Federal control ordered in four provinces after a smuggling probe; Erbil rejects it."),
]
ry = LY
rh = (LH1 + 14 + MH - 3 * 10) / 4
for num, col, loc, head, body in rail:
    card(RX, ry, RW, rh)
    d.rectangle([RX, ry, RX + 6, ry + rh], fill=col)
    chip(RX + 14, ry + 10, num, col)
    d.text((RX + 50, ry + 14), loc, font=f(SANS_B, 11), fill=GREY)
    y = draw_wrap(RX + 14, ry + 40, head, f(SERIF_B, 19), RW - 28, leading=23)
    draw_wrap(RX + 14, y + 2, body, f(SANS, 12), RW - 28, fill=(52, 64, 76), leading=16)
    d.text((RX + 14, ry + rh - 20), "REUTERS", font=f(SANS_B, 10), fill=GREY)
    ry += rh + 10

# ---------- bottom row: AI card + dot map + brief ----------
BY = MY + MH + 14
BH = 150
# AI card
AW = 300
card(M, BY, AW, BH)
chip(M + 14, BY + 12, 7, TEAL)
d.text((M + 50, BY + 16), "AI RESEARCH", font=f(SANS_B, 12), fill=GREY)
y = draw_wrap(M + 14, BY + 42, "GPT-6 proteins bound in lab tests", f(SERIF_B, 20), AW - 28, leading=24)
draw_wrap(M + 14, y + 2, "Binding found across five targets, by OpenAI's account.", f(SANS, 12), AW - 28, fill=(52, 64, 76), leading=16)
# helix mini art
pts = []
for i in range(9):
    px = M + 20 + i * 30
    py = BY + BH - 16 + 6 * math.sin(i * 1.2)
    pts.append((px, py))
d.line(pts, fill=TEAL, width=3)
for i, (px, py) in enumerate(pts):
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=AMBER if i % 3 == 0 else TEAL)
# dot-matrix map
MX = M + AW + 14
MW = 330
card(MX, BY, MW, BH)
d.text((MX + 14, BY + 12), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=INK)
d.text((MX + 14, BY + 30), "dots = land · pins = stories", font=f(SANS, 11), fill=GREY)
# crude land mask on a 30x10 grid
land = [
    "  ####        ##   #########   ",
    " ######      #### ###########  ",
    "  ####      ################# ",
    "   ###       ###############  ",
    "    ##        #############   ",
    "    ##         ##########     ",
    "    #           ########      ",
    "    #            ######    ## ",
    "                 ####      ###",
    "                  ##          ",
]
gx, gy, cell = MX + 16, BY + 52, 10
for r, row in enumerate(land):
    for c, ch in enumerate(row):
        if ch == "#":
            d.ellipse([gx + c * cell, gy + r * cell, gx + c * cell + 5, gy + r * cell + 5], fill=(176, 192, 204))
pins = [(1, 22, 3), (2, 25, 4), (3, 18, 5), (4, 15, 2), (5, 16, 2), (6, 18, 3)]
for num, c, r in pins:
    px, py = gx + c * cell + 2, gy + r * cell + 2
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=CORAL)
    nf = f(SANS_B, 10)
    d.text((px - tw(str(num), nf) / 2, py - 5), str(num), font=nf, fill=(255, 255, 255))
# brief card
FX = MX + MW + 14
FW = W - M - FX
card(FX, BY, FW, BH)
d.text((FX + 14, BY + 12), "ALSO TODAY", font=f(SANS_B, 13), fill=INK)
brief = [
    (8, "FRANCE — Sarkozy trial ordered; hearing 1 Apr 2027"),
    (9, "FOOTBALL — Real Madrid 5–1 PSV; Mbappé ×2"),
    (10, "MALAYSIA — six carbon hubs; $41.3B by 2050"),
    (11, "BRITAIN — record 5,258 heat deaths"),
]
yy = BY + 36
for num, txt in brief:
    d.text((FX + 14, yy), str(num), font=f(SERIF_B, 16), fill=CORAL)
    yy = draw_wrap(FX + 44, yy + 1, txt, f(SANS, 11), FW - 56, fill=(52, 64, 76), leading=14) + 4

# ---------- footer ----------
fy = BY + BH + 14
d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
d.text((M, fy + 8), "Sources: Reuters · OpenAI report. Claims are attributed; dates shown per story.", font=f(SANS, 11), fill=GREY)
d.text((M, fy + 26), "DRAWN BY AN AI AGENT FOR MAKE.FUN", font=f(SANS_B, 12), fill=INK)
r = "WEDNESDAY 25 NOVEMBER 2026"
d.text((W - M - tw(r, f(SANS_B, 12)), fy + 26), r, font=f(SANS_B, 12), fill=CORAL)

img.save("entry.png")
print("saved")
