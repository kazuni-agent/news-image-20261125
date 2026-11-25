#!/usr/bin/env python3
"""The Day in Full v6 - 25 November 2026. Original layout, denser coverage."""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 240, 225)
INK = (26, 24, 22)
NAVY = (24, 34, 58)
CORAL = (193, 39, 45)
TEAL = (14, 122, 122)
AMBER = (199, 124, 22)
VIOLET = (112, 84, 168)
GREEN = (70, 150, 80)
GREY = (92, 86, 76)
LINE = (205, 194, 172)
CARD = (255, 253, 247)
SKY = (186, 220, 240)
NIGHT = (18, 30, 58)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
FS = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FSI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

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

def para(x, y, s, font, maxw, fill=INK, lh=None, max_lines=4):
    lh = lh or int(font.size * 1.18)
    for i, ln in enumerate(wrap(s, font, maxw)[:max_lines]):
        text(x, y + i * lh, ln, font, fill)
    return y + min(len(wrap(s, font, maxw)), max_lines) * lh

def card(x, y, w, h, accent=None):
    d.rounded_rectangle([x+3, y+4, x+w+3, y+h+4], 8, fill=(214, 221, 230))
    d.rounded_rectangle([x, y, x+w, y+h], 8, fill=CARD, outline=LINE, width=1)
    if accent:
        d.rounded_rectangle([x, y, x+7, y+h], 3, fill=accent)

def tag(x, y, label, color):
    ft = f(FB, 10)
    wdt = tw(label, ft) + 10
    d.rounded_rectangle([x, y, x+wdt, y+15], 3, outline=color, width=1)
    text(x+5, y+2, label, ft, color)
    return x + wdt

def badge(x, y, n, color=NAVY):
    d.ellipse([x, y, x+20, y+20], fill=color)
    text(x+10, y+3, str(n), f(FB, 12), (255, 255, 255), "ma")

# ---------- header ----------
d.rectangle([0, 0, W, 30], fill=NAVY)
text(24, 7, "THE DAY IN FULL", f(FB, 14), (255, 255, 255))
text(1000, 8, "33 STORIES · 7 REGIONS · ALL DATED WEDNESDAY 25 NOVEMBER 2026", f(FB, 12), (255, 255, 255), "ra")
text(24, 40, "Wednesday 25 November 2026", f(FS, 50), INK)
text(26, 98, "Pakistan's first astronaut flies  ·  Asia's chip stocks plunge  ·  Hostages freed in Cartagena", f(FSI, 17), CORAL)
d.line([24, 122, 1000, 122], fill=LINE, width=1)

# UTC timeline
text(24, 129, "THE DAY IN UTC", f(FB, 11), NAVY)
tl = [("00:18", "Shenzhou-24 lifts off"), ("ASIA CLOSE", "Kospi −6.2%"), ("MORNING", "Hormuz mine claim"), ("EARLY", "Cartagena hostages freed")]
x = 130
for t, s in tl:
    text(x, 129, t, f(FB, 11), CORAL)
    text(x + tw(t, f(FB, 11)) + 6, 129, s, f(FR, 11), INK)
    x += tw(t, f(FB, 11)) + tw(s, f(FR, 11)) + 30

# region strip
regions = [("ASIA 11", (14, 122, 122)), ("MIDDLE EAST 4", (193, 39, 45)), ("EUROPE 5", (44, 90, 160)),
           ("AMERICAS 4", (70, 150, 80)), ("AFRICA 2", (199, 124, 22)), ("OCEANIA 2", (112, 84, 168)), ("GLOBAL 3", (70, 70, 70))]
rx = 24
for label, col in regions:
    wdt = int(tw(label, f(FB, 10))) + 16
    d.rounded_rectangle([rx, 148, rx + wdt, 166], 3, fill=col)
    text(rx + wdt / 2, 151, label, f(FB, 10), (255, 255, 255), "ma")
    rx += wdt + 6
d.line([24, 172, 1000, 172], fill=LINE, width=1)

# stat band
stats = [("1st", "Pakistani in orbit"), ("−6.2%", "Kospi at Asia close"), ("11", "hurt in Riyadh tower strike"),
         ("47,000", "women killed in 2025, UN"), ("+36%", "Bangladesh garment wage"), ("ALL", "Cartagena hostages freed")]
sx = 24
for i, (n, s) in enumerate(stats):
    wdt = 162
    text(sx + wdt/2, 178, n, f(FB, 22), CORAL if i % 2 == 0 else NAVY, "ma")
    para(sx + 6, 202, s, f(FR, 10), wdt - 12, GREY, 12, 2)
    if i < 5: d.line([sx + wdt, 180, sx + wdt, 218], fill=LINE, width=1)
    sx += wdt
d.line([24, 226, 1000, 226], fill=INK, width=2)

# ---------- lead cards ----------
def lead(x, y, w, n, taglabel, tagcolor, illus, place, head, body, src):
    card(x, y, w, 238)
    illus(x + 8, y + 8, w - 16, 92)
    badge(x + 12, y + 106, n, CORAL)
    text(x + 40, y + 108, place, f(FB, 10), GREY)
    tag(x + w - 92, y + 104, taglabel, tagcolor)
    para(x + 12, y + 130, head, f(FS, 19), w - 24, INK, 22, 2)
    para(x + 12, y + 176, body, f(FR, 11), w - 24, (52, 64, 82), 14, 3)
    text(x + 12, y + 220, src, f(FB, 9), GREY)

def illus_rocket(x, y, w, h):
    d.rounded_rectangle([x, y, x+w, y+h], 6, fill=NIGHT)
    for sx_, sy_ in [(30, 14), (90, 26), (200, 12), (250, 30), (150, 8), (60, 44), (230, 52)]:
        d.ellipse([x+sx_, y+sy_, x+sx_+3, y+sy_+3], fill=(255, 255, 255))
    d.ellipse([x+w-110, y+6, x+w-8, y+64], outline=(120, 170, 220), width=2)
    d.rectangle([x+w-84, y+26, x+w-34, y+40], fill=(200, 210, 220))
    d.rectangle([x+w-96, y+30, x+w-84, y+36], fill=(90, 140, 200))
    d.rectangle([x+w-34, y+30, x+w-22, y+36], fill=(90, 140, 200))
    text(x+w-59, y+44, "TIANGONG", f(FB, 8), (160, 200, 240), "ma")
    d.rectangle([x+104, y+30, x+124, y+72], fill=(240, 244, 248))
    d.polygon([(x+104, y+30), (x+114, y+10), (x+124, y+30)], fill=CORAL)
    d.polygon([(x+104, y+62), (x+96, y+74), (x+104, y+74)], fill=CORAL)
    d.polygon([(x+124, y+62), (x+132, y+74), (x+124, y+74)], fill=CORAL)
    d.polygon([(x+107, y+72), (x+114, y+88), (x+121, y+72)], fill=AMBER)
    text(x+114, y+40, "2F", f(FB, 9), NAVY, "ma")
    d.rectangle([x, y+h-12, x+w, y+h], fill=(40, 90, 60))

def illus_market(x, y, w, h):
    d.rounded_rectangle([x, y, x+w, y+h], 6, fill=(30, 40, 60))
    pts = [(x+14+i*22, y+18+int(50*(i/8)**1.4)) for i in range(9)]
    d.line(pts, fill=CORAL, width=3)
    for px, py in pts: d.ellipse([px-2, py-2, px+2, py+2], fill=(255, 255, 255))
    text(x+12, y+6, "MSCI APAC EX-JAPAN −2.3%", f(FB, 11), (255, 255, 255))
    for i, (lab, val) in enumerate([("KOSPI", "−6.2%"), ("TAIEX", "−5.1%"), ("NIKKEI", "−2.8%"), ("NVIDIA", "−5.9%")]):
        yy = y + 22 + i * 16
        text(x+w-96, yy, lab, f(FB, 10), (200, 210, 225))
        text(x+w-12, yy, val, f(FB, 10), CORAL, "ra")

def illus_tower(x, y, w, h):
    d.rounded_rectangle([x, y, x+w, y+h], 6, fill=(250, 226, 190))
    d.rectangle([x+40, y+24, x+96, y+h-10], fill=(90, 100, 116))
    for r in range(4):
        for c in range(3):
            d.rectangle([x+48+c*16, y+32+r*14, x+58+c*16, y+40+r*14], fill=(250, 220, 140))
    d.rectangle([x+150, y+44, x+196, y+h-10], fill=(120, 130, 144))
    for sx_, sy_, r in [(120, 8, 16), (140, 2, 20), (164, 10, 14)]:
        d.ellipse([x+sx_, y+sy_, x+sx_+r, y+sy_+r], fill=(70, 70, 78))
    d.polygon([(x+196, y+30), (x+238, y+18), (x+238, y+34)], fill=(60, 66, 76))
    d.line([x+214, y+24, x+206, y+16], fill=(60, 66, 76), width=2)
    d.line([x+214, y+24, x+222, y+16], fill=(60, 66, 76), width=2)
    d.rectangle([x, y+h-10, x+w, y+h], fill=(196, 168, 120))

lead(24, 234, 316, 1, "CONFIRMED", TEAL, illus_rocket, "JIUQUAN, CHINA · SPACE",
     "Shenzhou-24 lifts off with Pakistan's first astronaut",
     "Long March 2F launched at 00:18 UTC carrying Muhammad Zeeshan Ali, the first foreign visitor to Tiangong.",
     "REUTERS · XINHUA")
lead(354, 234, 316, 2, "CONFIRMED", TEAL, illus_market, "SEOUL · TAIPEI · MARKETS",
     "Asia's chip stocks plunge on AI doubts",
     "Kospi fell 6.2% and Taiwan 5.1% as the AI sell-off deepened; Nvidia slid 5.9% in New York.",
     "REUTERS · AFP")
lead(684, 234, 316, 3, "REPORTED", AMBER, illus_tower, "RIYADH, SAUDI ARABIA · WAR",
     "Houthi drone hits Riyadh tower, 11 hurt",
     "A drone struck the PIF Tower on 24 Nov, reported Wednesday; the coalition said it downed four drones over Ras Tanura.",
     "REUTERS · AL JAZEERA")

# how-sure legend
text(24, 478, "HOW SURE:", f(FB, 11), NAVY)
x = 96
for lab, col, desc in [("OFFICIAL", TEAL, "government or agency"), ("CONFIRMED", TEAL, "two or more major outlets"),
                       ("REPORTED", AMBER, "one outlet's reporting"), ("CLAIM", CORAL, "one side's word, unverified")]:
    x = tag(x, 477, lab, col) + 5
    text(x, 479, desc, f(FR, 10), GREY)
    x += tw(desc, f(FR, 10)) + 16

# ---------- mini cards ----------
minis = [
    (4, "OFFICIAL", TEAL, "CANBERRA", "Australia and Solomons sign security treaty",
     "Canberra becomes the primary security partner; no foreign bases allowed.", "REUTERS · AP"),
    (5, "OFFICIAL", TEAL, "UNITED NATIONS", "UN: five women an hour killed by partner or kin",
     "47,000 women and girls were killed in 2025, a new UN brief says.", "UN · PINA"),
    (6, "CONFIRMED", TEAL, "NEW YORK, US", "Huawei guilty of stealing trade secrets",
     "A Brooklyn jury convicted on 10 of 12 counts; Huawei rejects the verdict.", "REUTERS · BBC"),
    (7, "OFFICIAL", TEAL, "RAS TANURA", "Saudis down Houthi drones over oil port",
     "Four drones destroyed after coalition strikes on Hodeidah.", "REUTERS"),
    (8, "REPORTED", AMBER, "BOGOR, INDONESIA", "Rescuers search flooded gold mine",
     "About 20 miners still trapped 100 m down; six bodies recovered.", "AP · AFP"),
    (9, "CONFIRMED", TEAL, "DHAKA", "Garment workers win 36% pay rise",
     "Minimum wage rises to 17,000 taka after weeks of protest.", "REUTERS · AP"),
    (10, "CLAIM", CORAL, "HORMUZ STRAIT", "Two tankers hit mines and burn, Iran says",
     "The IRGC says ships struck naval mines; no independent confirmation.", "IRGC · ARAB NEWS"),
    (11, "CONFIRMED", TEAL, "CARTAGENA", "All hostages freed in supermarket siege",
     "Forces stormed the store early Wednesday; one captor was killed.", "AP · AFP"),
]
icons = ["flag", "chart", "gavel", "drone", "mine", "shirt", "ship", "shield"]
def icon(kind, x, y, color):
    if kind == "flag":
        d.line([x, y, x, y+22], fill=color, width=2); d.polygon([(x, y), (x+16, y+4), (x, y+9)], fill=color)
    elif kind == "chart":
        for i, hh in enumerate([8, 14, 20]): d.rectangle([x+i*7, y+22-hh, x+i*7+5, y+22], fill=color)
    elif kind == "gavel":
        d.rectangle([x+2, y+4, x+16, y+9], fill=color); d.line([x+10, y+9, x+20, y+20], fill=color, width=3)
    elif kind == "drone":
        d.rectangle([x+6, y+8, x+16, y+13], fill=color)
        for dx, dy in [(2, 4), (18, 4), (2, 16), (18, 16)]: d.ellipse([x+dx, y+dy, x+dx+5, y+dy+3], outline=color)
    elif kind == "mine":
        d.polygon([(x, y+22), (x+11, y+2), (x+22, y+22)], outline=color, width=2)
        d.rectangle([x+8, y+14, x+14, y+22], fill=color)
    elif kind == "shirt":
        d.polygon([(x+6, y+2), (x+16, y+2), (x+22, y+8), (x+16, y+11), (x+16, y+22), (x+6, y+22), (x+6, y+11), (x, y+8)], fill=color)
    elif kind == "ship":
        d.polygon([(x, y+14), (x+22, y+14), (x+18, y+21), (x+4, y+21)], fill=color)
        d.rectangle([x+8, y+6, x+14, y+14], fill=color)
    else:
        d.polygon([(x+11, y), (x+21, y+4), (x+21, y+13), (x+11, y+22), (x+1, y+13), (x+1, y+4)], outline=color, width=2)

def scene(kind, x, y, w, h, color):
    bg = {"flag": (186, 220, 240), "chart": (44, 36, 64), "gavel": (238, 226, 200), "drone": (250, 226, 190),
          "mine": (120, 92, 64), "shirt": (214, 240, 220), "ship": (186, 220, 240), "shield": (230, 238, 248)}[kind]
    d.rounded_rectangle([x, y, x + w, y + h], 4, fill=bg)
    cx = x + w // 2
    if kind == "flag":
        d.rectangle([cx - 30, y + 6, cx + 30, y + h - 6], fill=(255, 255, 255), outline=color)
        d.line([cx - 22, y + 12, cx + 22, y + 12], fill=color, width=2)
        d.line([cx - 22, y + 18, cx + 14, y + 18], fill=(150, 150, 150), width=2)
        d.ellipse([cx + 12, y + h - 16, cx + 24, y + h - 5], outline=CORAL, width=2)
    elif kind == "chart":
        for i, hh in enumerate([8, 14, 20, 26]):
            d.rectangle([cx - 34 + i * 18, y + h - 6 - hh, cx - 22 + i * 18, y + h - 6], fill=CORAL)
        text(cx, y + 3, "47,000", f(FB, 11), (255, 255, 255), "ma")
    elif kind == "gavel":
        d.rectangle([cx - 16, y + 8, cx + 16, y + 16], fill=(90, 60, 30))
        d.line([cx + 6, y + 16, cx + 26, y + h - 6], fill=(90, 60, 30), width=4)
        d.line([cx - 30, y + h - 5, cx + 30, y + h - 5], fill=(90, 60, 30), width=3)
    elif kind == "drone":
        d.rectangle([cx - 10, y + 10, cx + 10, y + 17], fill=(50, 54, 62))
        for dx, dy in [(-26, 6), (18, 6), (-26, 20), (18, 20)]:
            d.ellipse([cx + dx, y + dy, cx + dx + 10, y + dy + 4], outline=(50, 54, 62), width=2)
        d.rectangle([x + 8, y + h - 12, x + 40, y + h - 4], fill=(120, 130, 144))
        d.rectangle([x + w - 40, y + h - 12, x + w - 8, y + h - 4], fill=(120, 130, 144))
    elif kind == "mine":
        d.polygon([(x + 6, y + h - 4), (cx, y + 6), (x + w - 6, y + h - 4)], fill=(96, 74, 50))
        d.rectangle([cx - 7, y + h - 16, cx + 7, y + h - 4], fill=(40, 30, 20))
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(90, 150, 200))
    elif kind == "shirt":
        d.polygon([(cx - 12, y + 6), (cx + 12, y + 6), (cx + 24, y + 13), (cx + 12, y + 17), (cx + 12, y + h - 6), (cx - 12, y + h - 6), (cx - 12, y + 17), (cx - 24, y + 13)], fill=color)
        for i in range(3):
            d.ellipse([cx + 26 + i * 12, y + h - 14 - i * 4, cx + 36 + i * 12, y + h - 5 - i * 4], fill=AMBER, outline=(160, 110, 20))
    elif kind == "ship":
        d.polygon([(cx - 34, y + 16), (cx + 34, y + 16), (cx + 24, y + h - 8), (cx - 24, y + h - 8)], fill=(60, 66, 76))
        d.rectangle([cx - 8, y + 6, cx + 8, y + 16], fill=(200, 60, 50))
        d.polygon([(cx + 14, y + 4), (cx + 24, y + 12), (cx + 8, y + 12)], fill=AMBER)
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(90, 150, 200))
    else:
        d.rectangle([cx - 34, y + 8, cx + 34, y + h - 8], fill=(255, 255, 255), outline=(150, 160, 170))
        d.polygon([(cx - 34, y + 8), (cx, y + 1), (cx + 34, y + 8)], fill=CORAL)
        d.polygon([(cx, y + 12), (cx + 9, y + 15), (cx + 9, y + 22), (cx, y + h - 10), (cx - 9, y + 22), (cx - 9, y + 15)], fill=TEAL)

my = 492
for i, (n, lab, col, place, head, body, src) in enumerate(minis):
    cx = 24 + (i % 4) * 248
    cy = my + (i // 4) * 130
    card(cx, cy, 238, 126, col)
    scene(icons[i], cx + 12, cy + 8, 214, 30, col)
    badge(cx + 12, cy + 44, n, CORAL)
    text(cx + 38, cy + 47, place, f(FB, 8), GREY)
    tag(cx + 238 - 12 - (tw(lab, f(FB, 10)) + 10), cy + 44, lab, col)
    para(cx + 12, cy + 66, head, f(FB, 12), 214, INK, 14, 2)
    para(cx + 12, cy + 94, body, f(FR, 9), 214, (52, 64, 82), 10, 2)
    text(cx + 12, cy + 116, src, f(FB, 7), GREY)

# ---------- map + brief ----------
by = 752
card(24, by, 330, 162)
text(36, by+8, "WHERE IT HAPPENED · PINS = STORY NUMBERS", f(FB, 10), NAVY)
mx, myy, mw, mh = 36, by+28, 306, 104
d.rounded_rectangle([mx, myy, mx+mw, myy+mh], 6, fill=(214, 232, 246))
blobs = [(16, 14, 66, 30), (40, 52, 34, 36), (128, 10, 40, 22), (136, 34, 36, 40), (182, 12, 84, 30), (216, 54, 40, 24)]
for bx, byy, bw, bh in blobs:
    for yy in range(myy + byy, myy + byy + bh, 7):
        for xx in range(mx + bx, mx + bx + bw, 7):
            d.ellipse([xx, yy, xx + 3, yy + 3], fill=(96, 140, 110))
pins = [(1, 244, 30), (2, 258, 36), (3, 172, 42), (4, 282, 84), (5, 196, 66), (6, 66, 34), (7, 166, 56), (8, 252, 66), (9, 230, 46), (10, 192, 50), (11, 56, 66)]
for n, px, py in pins:
    d.ellipse([mx+px, myy+py, mx+px+13, myy+py+13], fill=CORAL, outline=(255, 255, 255))
    text(mx+px+6, myy+py+1, str(n), f(FB, 8), (255, 255, 255), "ma")

card(368, by, 632, 162)
text(380, by+8, "IN BRIEF · 22 MORE FROM 25 NOVEMBER", f(FB, 10), NAVY)
brief = [
    ("12", "PARIS Sarkozy and wife ordered to stand trial (Reuters)"),
    ("13", "MADRID Real Madrid rout PSV 5–1; Mbappé scores twice (Reuters)"),
    ("14", "KUALA LUMPUR Malaysia plans $41.3B carbon hubs by 2050 (Reuters)"),
    ("15", "LONDON Britain records 5,258 heat deaths, a record (official)"),
    ("16", "HAVANA WHO chief urges US to lift Cuba fuel blockade (WHO)"),
    ("17", "KINSHASA UNICEF links Ebola to violence vs women (UNICEF)"),
    ("18", "DAKAR Senegal regains CAN title by CAS ruling, 24 Nov (CAS)"),
    ("19", "BAGHDAD Iraq orders takeover of Kurdish oilfields (Reuters)"),
    ("20", "BLACK SEA Ukraine sea drones hit Sparta II, Merkury (reported)"),
    ("21", "SAN FRANCISCO GPT-6 proteins bind across 5 targets (OpenAI)"),
    ("22", "PANAMA Cobre Panamá copper mine may reopen (press)"),
    ("23", "SHANGHAI Party pledges loyalty as chief Chen probed (Reuters)"),
    ("24", "WASHINGTON US to unveil tariffs on China, 16 economies (WSJ)"),
    ("25", "REDMOND Microsoft declares Code Red after outage (Reuters)"),
    ("26", "LONDON Wang Yi urges Britain to back free trade (press)"),
    ("27", "KATHMANDU India backs flood-hit Nepal with $1.6B aid (press)"),
    ("28", "SEOUL Kang Kum-sil nominated first woman NIS chief (press)"),
    ("29", "SHANGHAI China stocks fall to 16-month low (Reuters)"),
    ("30", "SEOUL South Korea October retail sales rise 5.7% (data)"),
    ("31", "BEIJING China extends dual-use export suspension (MOFCOM)"),
    ("32", "SYDNEY Australia CPI jumps 4.9% in October (ABS)"),
    ("33", "LANGLEY CIA unclassified system breached (NYT)"),
]
for i, (n, s) in enumerate(brief):
    bx = 380 + (i % 2) * 316
    byy = by + 24 + (i // 2) * 12
    text(bx, byy, n, f(FB, 9), CORAL)
    text(bx + 20, byy, s, f(FR, 8), INK)

# ---------- date check + footer ----------
dy = 918
d.rounded_rectangle([24, dy, 1000, dy+52], 6, fill=(255, 255, 255), outline=CORAL, width=1)
d.rectangle([24, dy, 128, dy+52], fill=CORAL)
text(76, dy+18, "DATE CHECK", f(FB, 12), (255, 255, 255), "ma")
para(140, dy+7, "Every story here happened, or was first reported, on Wednesday 25 November 2026. Dated exceptions are tagged: the Riyadh strike, the Cartagena siege and the Senegal ruling are 24 Nov; Microsoft's outage was 12–13 Nov. Left out as earlier news: COP31's collapse (22 Nov), Nepal's quake (23 Nov).",
     f(FR, 10), 848, INK, 13, 3)
text(24, 982, "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Xinhua, WHO, UNICEF, UN, IRGC — 25 Nov 2026", f(FR, 10), GREY)
text(1000, 982, "THE DAY IN FULL · ONE PAGE", f(FB, 10), NAVY, "ra")

img.save("entry.png")
print("saved")
