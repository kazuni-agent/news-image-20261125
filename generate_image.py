#!/usr/bin/env python3
"""Render entry v2: premium editorial world-news graphic, 1024x1024 PNG.

Writes entry.png and entry.png.b64 (same bytes as base64 text, so the
repository stays text-only for the GitHub connector). Deterministic: fixed
fonts/layout/text, no timestamps, no randomness, no network.
"""
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (248, 245, 238)
INK = (22, 24, 28)
MUTED = (92, 96, 104)
RULE = (196, 190, 176)
ACCENT = (178, 34, 52)
PANEL = (24, 27, 33)
PANEL_TEXT = (238, 236, 228)
CARD = (255, 254, 250)

FDIR = Path("/usr/share/fonts/truetype/liberation")
SERIF_B = str(FDIR / "LiberationSerif-Bold.ttf")
SERIF_R = str(FDIR / "LiberationSerif-Regular.ttf")
SANS_B = str(FDIR / "LiberationSans-Bold.ttf")
SANS_R = str(FDIR / "LiberationSans-Regular.ttf")
SANS_I = str(FDIR / "LiberationSans-Italic.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            trial = f"{cur} {word}".strip()
            if d.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_text(d, x, y, text, fnt, fill, max_w, leading, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(d, x, y, text):
    fnt = f(SANS_B, 14)
    w = int(d.textlength(text, font=fnt)) + 18
    d.rounded_rectangle([x, y, x + w, y + 26], radius=13, outline=ACCENT, width=2)
    d.text((x + 9, y + 5), text, font=fnt, fill=INK)
    return x + w + 10


def card(d, x, y, w, h, kicker, meta, headline, body, impact):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    d.rectangle([x, y, x + w, y + 5], fill=ACCENT)
    d.text((x + 16, y + 13), kicker, font=f(SANS_B, 14), fill=ACCENT)
    meta_f = f(SANS_B, 12)
    d.text((x + w - 16 - d.textlength(meta, font=meta_f), y + 14), meta, font=meta_f, fill=MUTED)
    yy = draw_text(d, x + 16, y + 34, headline, f(SERIF_B, 22), INK, w - 32, 25, max_lines=2)
    yy = draw_text(d, x + 16, yy + 3, body, f(SANS_R, 14), (42, 45, 52), w - 32, 18, max_lines=3)
    d.text((x + 16, y + h - 22), impact, font=f(SANS_I, 13), fill=MUTED)


def market_bars(d, x, y, w):
    data = [("MSCI APAC", -2.3), ("Korea", -5.3), ("Nvidia", -5.9)]
    maxv = 6.0
    lab = f(SANS_B, 12)
    val = f(SANS_R, 12)
    for i, (name, v) in enumerate(data):
        yy = y + i * 17
        d.text((x, yy), name, font=lab, fill=INK)
        bx = x + 92
        bw = int((w - 150) * (abs(v) / maxv))
        d.rectangle([bx, yy + 3, bx + bw, yy + 13], fill=ACCENT)
        d.text((bx + bw + 6, yy), f"{v:.1f}%", font=val, fill=MUTED)


def orbit_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL)
    # Earth arc
    d.ellipse([x + 34, y + h - 118, x + w - 34, y + h + 70], outline=(120, 170, 220), width=3)
    d.ellipse([x + 58, y + h - 96, x + w - 58, y + h + 48], outline=(70, 110, 160), width=2)
    # Orbit path and station
    d.ellipse([x + 52, y + 26, x + w - 52, y + h - 40], outline=(150, 160, 175), width=2)
    sx, sy = x + w - 92, y + 58
    d.line([sx - 26, sy, sx + 26, sy], fill=PANEL_TEXT, width=4)
    d.rectangle([sx - 8, sy - 8, sx + 8, sy + 8], fill=PANEL_TEXT)
    d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=ACCENT)
    # Launch point + trajectory
    lx, ly = x + 70, y + h - 52
    d.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=ACCENT)
    d.line([lx, ly, sx - 30, sy + 16], fill=(210, 180, 90), width=3)
    d.text((x + 18, y + 14), "JIUQUAN  →  TIANGONG", font=f(SANS_B, 14), fill=PANEL_TEXT)
    d.text((sx - 34, sy + 16), "TIANGONG", font=f(SANS_B, 11), fill=PANEL_TEXT)
    d.text((lx + 10, ly - 18), "LAUNCH", font=f(SANS_B, 11), fill=PANEL_TEXT)
    d.text((x + 18, y + h - 30), "Long March-2F · Shenzhou-24", font=f(SANS_R, 13), fill=(190, 196, 205))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28
    # Masthead
    d.text((m, 20), "WORLD NEWS · REPORTED 25 NOVEMBER 2026", font=f(SANS_B, 14), fill=ACCENT)
    d.text((m, 40), "The World Today", font=f(SERIF_B, 56), fill=INK)
    d.text((W - m - d.textlength("25 NOV 2026", font=f(SERIF_B, 30)), 44), "25 NOV 2026", font=f(SERIF_B, 30), fill=INK)
    d.text((W - m - d.textlength("Wednesday", font=f(SANS_B, 15)), 82), "Wednesday", font=f(SANS_B, 15), fill=MUTED)
    d.line([m, 110, W - m, 110], fill=INK, width=3)
    d.line([m, 116, W - m, 116], fill=ACCENT, width=1)
    d.text((m, 124), "Seven developments. Event dates are shown; claims marked “says” are attributed, not independently confirmed.", font=f(SANS_R, 15), fill=MUTED)

    # Lead story
    ly, lh = 150, 204
    d.rectangle([m, ly, W - m, ly + lh], fill=CARD, outline=RULE, width=1)
    d.rectangle([m, ly, m + 6, ly + lh], fill=ACCENT)
    tx = m + 20
    d.text((tx, ly + 14), "SPACE · SCIENCE", font=f(SANS_B, 15), fill=ACCENT)
    d.text((tx + 150, ly + 15), "25 NOV · JIUQUAN, CHINA", font=f(SANS_B, 13), fill=MUTED)
    yy = draw_text(d, tx, ly + 38, "Shenzhou-24 docks with Tiangong's first foreign astronaut", f(SERIF_B, 31), INK, 600, 32, max_lines=2)
    yy = draw_text(d, tx, yy + 4, "China launched Shenzhou-24 at 00:18 UTC. Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali are the crew; Ali is the first Pakistani in orbit and first foreign astronaut to board Tiangong.", f(SANS_R, 16), (42, 45, 52), 600, 20, max_lines=3)
    cx = tx
    for c in ["00:18 UTC launch", "Docked same day", "Ali stay: 5–10 days"]:
        cx = chip(d, cx, ly + lh - 38, c)
    orbit_panel(d, 656, ly + 14, 312, lh - 28)

    # Grid stories
    gx, gy, gw, gh, gap = m, 366, 476, 160, 12
    cards = [
        ("MIDDLE EAST · CONFLICT", "25 NOV · SAUDI ARABIA", "Houthis say they hit Saudi refinery and Riyadh district",
         "The group claimed attacks on Ras Tanura refinery and Riyadh's financial district. Saudi-led forces said four drones were destroyed at Ras Tanura; 11 were wounded Tuesday.",
         "Impact: energy and capital security back in focus."),
        ("UKRAINE · GEOPOLITICS", "21–22 NOV · REPORTED 25 NOV", "Ukraine's sea-drone war reaches Libya and the Baltic",
         "Kyiv confirmed strikes on cargo ship Sparta II in the Gulf of Finland and corvette Merkury at Benghazi. Tripoli condemned being drawn into the war.",
         "Impact: Russian supply routes face wider pressure."),
        ("MARKETS · AI ECONOMY", "25 NOV · ASIA / US", "Asian stocks fall as the AI rally stumbles",
         "Tariff threats hit chip-heavy markets; Brent $90.97.",
         "Impact: AI valuations meet trade and rate risk."),
        ("ARTIFICIAL INTELLIGENCE", "25 NOV · OPENAI", "OpenAI says GPT-6 designed proteins that bound in lab tests",
         "OpenAI reports GPT-6 used reasoning and code to design proteins, with lab binding evidence across five targets. Replication is the key test.",
         "Impact: general models enter specialist biology."),
        ("CLIMATE", "REPORTED 25 NOV · ANTALYA", "COP31 ends without a deal",
         "The summit closed without agreement after splits over fossil fuels and finance, the first failure since Copenhagen in 2009.",
         "Next: COP32 in Addis Ababa."),
        ("IRAQ · ENERGY POLITICS", "24 NOV · REPORTED 25 NOV", "Baghdad orders takeover of Kurdish oilfields and crossings",
         "PM Ali al-Zaidi ordered federal control after a smuggling probe in four provinces. KRG PM Masrour Barzani called it “in no way acceptable”.",
         "Impact: the oil and autonomy dispute reopens."),
    ]
    for i, (k, meta, head, body, imp) in enumerate(cards):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        card(d, x, y, gw, gh, k, meta, head, body, imp)
        if i == 2:  # markets mini-chart inside card bottom area
            market_bars(d, x + 16, y + 84, gw - 32)

    # Brief strip
    by = 876
    d.line([m, by, W - m, by], fill=INK, width=2)
    d.text((m, by + 8), "ALSO IN BRIEF", font=f(SANS_B, 14), fill=ACCENT)
    briefs = [
        "FRANCE · 24 Nov — Sarkozy and Carla Bruni ordered to trial; first hearing 1 Apr 2027.",
        "FOOTBALL · 24 Nov — Real Madrid beat PSV 5–1; Mbappé scored twice.",
        "MALAYSIA · 24 Nov — up to six carbon-storage hubs; $41.3B investment targeted by 2050.",
        "BRITAIN · 2026 — heat-related deaths reached a record 5,258 in the summer.",
    ]
    yy = by + 28
    for b in briefs:
        d.text((m, yy), "•  " + b, font=f(SANS_R, 14), fill=(42, 45, 52))
        yy += 17

    # Footer
    d.line([m, 980, W - m, 980], fill=RULE, width=1)
    d.text((m, 988), "Sources: Reuters · Xinhua/CMSA via Reuters · OpenAI via The Neuron & Sift", font=f(SANS_R, 13), fill=MUTED)
    d.text((W - m - d.textlength("THE WORLD TODAY · 25 NOV 2026", font=f(SANS_B, 13)), 988), "THE WORLD TODAY · 25 NOV 2026", font=f(SANS_B, 13), fill=INK)

    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    data = out.read_bytes()
    (HERE / "entry.png.b64").write_text(base64.b64encode(data).decode("ascii"))
    print(f"entry.png: {len(data)} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
