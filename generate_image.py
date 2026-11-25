#!/usr/bin/env python3
"""Render the 25 November 2026 world-news infographic (1024x1024 PNG).

Run:  python3 generate_image.py
Writes entry.png (the image the entry ships) and entry.png.b64 (the same
bytes as one base64 text file, so the repository stays text-only and can be
pushed through the GitHub connector, which accepts UTF-8 files only).
Deterministic: fixed fonts, fixed layout, no timestamps, no randomness.
"""
import base64
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
CREAM = (247, 243, 233)
NAVY = (16, 36, 62)
GOLD = (242, 193, 78)
INK = (24, 28, 36)
MUTED = (74, 82, 96)
CARD_BG = (255, 255, 255)
CARD_BORDER = (216, 210, 192)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
BOLD = str(FONT_DIR / "LiberationSans-Bold.ttf")
REG = str(FONT_DIR / "LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        cur = ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


STORIES = [
    {
        "num": "1",
        "color": (108, 74, 182),
        "kicker": "SPACE",
        "date": "25 NOV 2026  ·  JIUQUAN, CHINA",
        "headline": "Shenzhou-24 launches for Tiangong",
        "body": "China launches Shenzhou-24 at 00:18 UTC. Crew Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first Pakistani, and first foreign astronaut, to visit Tiangong.",
    },
    {
        "num": "2",
        "color": (29, 111, 184),
        "kicker": "UKRAINE",
        "date": "REPORTED 25 NOV  ·  GULF OF FINLAND",
        "headline": "Zelenskyy confirms drone strike on Russian ship",
        "body": "Ukraine hit the cargo ship Sparta II in the Gulf of Finland on Saturday, Kyiv says. Norway urges caution in the busy waterway.",
    },
    {
        "num": "3",
        "color": (176, 58, 46),
        "kicker": "LIBYA",
        "date": "REPORTED 25 NOV  ·  LIBYA",
        "headline": "Russian warship sunk in Libyan port",
        "body": "Ukraine says it sank a Russian naval vessel in a Libyan port on Sunday, raising the stakes for Libya's frozen conflict.",
    },
    {
        "num": "4",
        "color": (198, 122, 18),
        "kicker": "RIYADH",
        "date": "25 NOV 2026  ·  RIYADH, SAUDI ARABIA",
        "headline": "Houthis strike Riyadh's tallest tower",
        "body": "A missile hits the capital's tallest tower on Tuesday — the second strike in under a week. Saudi Civil Defense: 11 people wounded.",
    },
    {
        "num": "5",
        "color": (46, 125, 91),
        "kicker": "IRAQ",
        "date": "REPORTED 25 NOV  ·  IRAQ",
        "headline": "Baghdad moves to take over Kurdish oilfields",
        "body": "PM Ali al-Zaidi orders federal control of oilfields in Diyala, Kirkuk, Salahuddin and Nineveh after a smuggling probe. KRG PM Masrour Barzani rejects the move.",
    },
    {
        "num": "6",
        "color": (55, 71, 79),
        "kicker": "EUROPE",
        "date": "REPORTED 25 NOV  ·  FRANCE & SPAIN",
        "headline": "Sarkozy ordered to trial; Real Madrid win 5–1",
        "body": "France orders ex-president Nicolas Sarkozy and Carla Bruni to trial for corruption; pre-trial hearing 1 Apr 2027. Real Madrid beat PSV 5–1 — Mbappé scored twice.",
    },
]


def draw_card(draw, x, y, w, h, story):
    color = story["color"]
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD_BG,
                           outline=CARD_BORDER, width=2)
    draw.rectangle([x, y + 10, x + 10, y + h - 10], fill=color)
    # Number badge.
    badge_cx, badge_cy, badge_r = x + w - 34, y + 34, 22
    draw.ellipse([badge_cx - badge_r, badge_cy - badge_r,
                  badge_cx + badge_r, badge_cy + badge_r], fill=color)
    num_font = font(BOLD, 26)
    tw = draw.textlength(story["num"], font=num_font)
    draw.text((badge_cx - tw / 2, badge_cy - 15), story["num"],
              font=num_font, fill=(255, 255, 255))
    # Kicker + date.
    kicker_font = font(BOLD, 19)
    draw.text((x + 26, y + 16), story["kicker"], font=kicker_font, fill=color)
    date_font = font(BOLD, 15)
    draw.text((x + 26, y + 42), story["date"], font=date_font, fill=MUTED)
    # Headline, up to 2 lines.
    head_font = font(BOLD, 26)
    head_lines = wrap(draw, story["headline"], head_font, w - 52)[:2]
    hy = y + 68
    for line in head_lines:
        draw.text((x + 26, hy), line, font=head_font, fill=INK)
        hy += 30
    # Body.
    body_font = font(REG, 19)
    body_lines = wrap(draw, story["body"], body_font, w - 52)
    by = hy + 6
    for line in body_lines:
        draw.text((x + 26, by), line, font=body_font, fill=(38, 44, 54))
        by += 24


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # Header band.
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw.rectangle([0, 148, W, 154], fill=GOLD)
    draw.text((24, 18), "WORLD NEWS", font=font(BOLD, 68), fill=(255, 255, 255))
    draw.text((24, 96), "Wednesday, 25 November 2026",
              font=font(BOLD, 34), fill=GOLD)
    # Big date block on the right of the header.
    draw.text((W - 24 - draw.textlength("25 NOV", font=font(BOLD, 44)),
               26), "25 NOV", font=font(BOLD, 44), fill=(255, 255, 255))
    draw.text((W - 24 - draw.textlength("2026", font=font(BOLD, 30)),
               78), "2026", font=font(BOLD, 30), fill=(200, 210, 225))
    # Subheader.
    sub = "Six stories that defined the day — events that happened, or were first reported, on 25 November 2026."
    draw.text((24, 164), sub, font=font(REG, 21), fill=MUTED)
    # Cards: 2 columns x 3 rows.
    margin, gap = 24, 16
    card_w = (W - 2 * margin - gap) // 2
    card_h = 238
    top = 200
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw_card(draw, x, y, card_w, card_h, story)
    # Footer band.
    draw.rectangle([0, 952, W, H], fill=NAVY)
    foot = "Sources: Reuters World News Summary, 25 November 2026. All six stories happened, or were first reported, on that day."
    foot_font = font(REG, 18)
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, 970), foot, font=foot_font, fill=(220, 228, 240))
    draw.text(((W - draw.textlength("WORLD NEWS  ·  25 NOVEMBER 2026", font=font(BOLD, 16))) / 2, 996),
              "WORLD NEWS  ·  25 NOVEMBER 2026", font=font(BOLD, 16), fill=GOLD)
    png_path = HERE / "entry.png"
    img.save(png_path, format="PNG", optimize=True)
    data = png_path.read_bytes()
    (HERE / "entry.png.b64").write_text(base64.b64encode(data).decode("ascii"))
    print(f"entry.png: {len(data)} bytes, {img.size[0]}x{img.size[1]}")
    print(f"entry.png.b64: {len(base64.b64encode(data))} chars")


if __name__ == "__main__":
    main()
