#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page as a 1024x1024 PNG.

Fresh build for make.fun competition news-image-20261125.
Deterministic: fixed text, fixed geometry, no clock, no randomness.
Run:  python3 draw.py   -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (16, 34, 64)
RED = (178, 34, 34)
GOLD = (176, 132, 30)
TEAL = (14, 92, 92)
GREY = (96, 96, 96)
LINE = (120, 110, 95)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_ship(d, x, y, s, color):
    # Simple warship silhouette: hull, deck, mast, waves.
    d.polygon([(x, y + 26 * s), (x + 78 * s, y + 26 * s),
               (x + 66 * s, y + 40 * s), (x + 12 * s, y + 40 * s)],
              fill=color)
    d.rectangle([x + 26 * s, y + 12 * s, x + 52 * s, y + 26 * s], fill=color)
    d.line([(x + 39 * s, y + 12 * s), (x + 39 * s, y - 2 * s)],
           fill=color, width=max(2, int(3 * s)))
    d.line([(x + 2 * s, y + 48 * s), (x + 76 * s, y + 48 * s)],
           fill=color, width=max(2, int(2 * s)))


def draw_tower(d, x, y, s, color):
    # Skyscraper with a spire and lit windows.
    d.rectangle([x + 22 * s, y + 8 * s, x + 56 * s, y + 52 * s], fill=color)
    d.polygon([(x + 33 * s, y + 8 * s), (x + 45 * s, y + 8 * s),
               (x + 39 * s, y - 8 * s)], fill=color)
    for wy in (16, 26, 36):
        for wx in (28, 38, 48):
            d.rectangle([x + wx * s, y + wy * s,
                         x + (wx + 4) * s, y + (wy + 4) * s],
                        fill=PAPER)


def draw_medal(d, x, y, s, color):
    # Ribbon + round medal with a star.
    d.polygon([(x + 26 * s, y), (x + 38 * s, y),
               (x + 46 * s, y + 24 * s), (x + 32 * s, y + 24 * s)],
              fill=RED)
    d.polygon([(x + 52 * s, y), (x + 40 * s, y),
               (x + 32 * s, y + 24 * s), (x + 46 * s, y + 24 * s)],
              fill=(140, 20, 20))
    d.ellipse([x + 14 * s, y + 20 * s, x + 64 * s, y + 70 * s],
              fill=color, outline=GOLD, width=max(2, int(3 * s)))
    d.text((x + 31 * s, y + 30 * s), "*", font=font(SANS_B, int(34 * s)),
           fill=PAPER)


def draw_lock(d, x, y, s, color):
    # Padlock: shackle arc + body.
    d.arc([x + 20 * s, y + 2 * s, x + 58 * s, y + 34 * s],
          start=180, end=0, fill=color, width=max(3, int(5 * s)))
    d.rounded_rectangle([x + 10 * s, y + 24 * s, x + 68 * s, y + 62 * s],
                        radius=int(6 * s), fill=color)
    d.ellipse([x + 33 * s, y + 36 * s, x + 45 * s, y + 48 * s], fill=PAPER)
    d.rectangle([x + 37 * s, y + 44 * s, x + 41 * s, y + 54 * s], fill=PAPER)


def draw_satellite(d, x, y, s, color):
    # Satellite body, solar panels, dish.
    d.rectangle([x + 30 * s, y + 22 * s, x + 50 * s, y + 42 * s], fill=color)
    d.rectangle([x + 4 * s, y + 28 * s, x + 28 * s, y + 36 * s],
                fill=TEAL, outline=color, width=max(1, int(2 * s)))
    d.rectangle([x + 52 * s, y + 28 * s, x + 76 * s, y + 36 * s],
                fill=TEAL, outline=color, width=max(1, int(2 * s)))
    d.line([(x + 40 * s, y + 22 * s), (x + 52 * s, y + 10 * s)],
           fill=color, width=max(2, int(3 * s)))
    d.ellipse([x + 48 * s, y + 4 * s, x + 60 * s, y + 16 * s],
              outline=color, width=max(2, int(3 * s)))
    for dx, dy in ((12, 52), (66, 12), (70, 52)):
        d.ellipse([x + dx * s, y + dy * s, x + (dx + 4) * s, y + (dy + 4) * s],
                  fill=GOLD)


def draw_cricket(d, x, y, s, color):
    # Cricket bat leaning on a ball, with stumps behind.
    for sx in (14, 26, 38):
        d.line([(x + sx * s, y + 4 * s), (x + sx * s, y + 34 * s)],
               fill=color, width=max(2, int(3 * s)))
    d.line([(x + 12 * s, y + 4 * s), (x + 42 * s, y + 4 * s)],
           fill=color, width=max(2, int(3 * s)))
    d.rounded_rectangle([x + 46 * s, y + 18 * s, x + 62 * s, y + 56 * s],
                        radius=int(6 * s), fill=color)
    d.line([(x + 52 * s, y + 18 * s), (x + 52 * s, y + 6 * s)],
           fill=color, width=max(2, int(4 * s)))
    d.ellipse([x + 58 * s, y + 52 * s, x + 74 * s, y + 68 * s],
              fill=PAPER, outline=color, width=max(2, int(2 * s)))


def draw_scales(d, x, y, s, color):
    # Scales of justice: pillar, beam, two pans.
    d.line([(x + 40 * s, y + 4 * s), (x + 40 * s, y + 66 * s)],
           fill=color, width=max(3, int(4 * s)))
    d.line([(x + 8 * s, y + 12 * s), (x + 72 * s, y + 12 * s)],
           fill=color, width=max(3, int(4 * s)))
    for cx in (14, 66):
        d.line([(x + cx * s, y + 12 * s), (x + cx * s, y + 30 * s)],
               fill=color, width=max(2, int(2 * s)))
        d.polygon([(x + (cx - 12) * s, y + 30 * s),
                   (x + (cx + 12) * s, y + 30 * s),
                   (x + cx * s, y + 44 * s)], fill=color)
    d.rectangle([x + 28 * s, y + 66 * s, x + 52 * s, y + 72 * s], fill=color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((mx, 14), "THE WORLD TODAY", font=font(SERIF_B, 62), fill=PAPER)
    d.text((mx, 86), "WEDNESDAY  ·  25 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=(214, 196, 140))
    d.text((W - mx - 318, 88), "ONE PAGE  ·  SEVEN STORIES",
           font=font(SANS, 15), fill=(190, 200, 215))

    # ---------- Lead story: Huawei ----------
    y = 140
    d.text((mx, y), "LEAD  ·  UNITED STATES  ·  LAW & TECH",
           font=font(SANS_B, 16), fill=RED)
    y += 30
    d.text((mx, y), "HUAWEI GUILTY ON", font=font(SERIF_B, 46), fill=INK)
    y += 52
    d.text((mx, y), "10 OF 12 COUNTS", font=font(SERIF_B, 46), fill=INK)
    y += 62
    y = para(d, mx, y,
             "A Brooklyn jury convicted the Chinese telecom giant of bank and "
             "wire fraud, sanctions violations and stealing US trade secrets "
             "after a 12-week trial.",
             font(SANS, 19), 560, 26)
    y += 10
    d.text((mx, y), "Case opened in 2018  ·  Sentencing 14 September 2027",
           font=font(SANS_B, 16), fill=NAVY)

    # Lead art: scales of justice + verdict chips, right column.
    draw_scales(d, 660, 170, 1.0, NAVY)
    d.rounded_rectangle([648, 268, 988, 306], radius=8, fill=RED)
    d.text((668, 278), "GUILTY: 10 COUNTS", font=font(SANS_B, 17), fill=PAPER)
    d.rounded_rectangle([648, 314, 988, 352], radius=8, fill=TEAL)
    d.text((668, 324), "NOT GUILTY: RACKETEERING", font=font(SANS_B, 17),
           fill=PAPER)
    d.text((648, 362), "Sources: Reuters, US Dept. of Justice",
           font=font(SANS, 13), fill=GREY)

    rule(d, mx, 402, W - mx, 2)

    # ---------- Six-story grid ----------
    stories = [
        ("WAR  ·  LIBYA & THE BALTIC",
         "Ukraine sinks Russian warship off Libya",
         "Seven sea drones sank the corvette Merkury in Benghazi and hit "
         "the cargo ship MV Angara, Zelenskyy said. Days earlier a drone "
         "set fire to the Sparta II in the Gulf of Finland.",
         draw_ship, NAVY),
        ("MIDDLE EAST  ·  SAUDI ARABIA",
         "Houthi drone hits Riyadh tower, 11 hurt",
         "A drone struck the PIF Tower in Riyadh on Tuesday, wounding 11 "
         "people, Saudi civil defence said - the second hit on the tower "
         "in less than a week.",
         draw_tower, RED),
        ("UNITED STATES  ·  POLITICS",
         "Trump gives Giuliani the Medal of Freedom",
         "In a private Oval Office ceremony, Trump awarded the nation's "
         "highest civilian honour to the 82-year-old former New York mayor, "
         "disbarred over his 2020 election challenges.",
         draw_medal, GOLD),
        ("CYBER  ·  WASHINGTON",
         "CIA and spy chief's office hit by breach",
         "The CIA and the Office of the Director of National Intelligence "
         "found a breach exposing some unclassified material, a source told "
         "Reuters. The New York Times first reported it.",
         draw_lock, TEAL),
        ("DEFENCE  ·  SPACE",
         "NATO vows space defence over 'nuclear satellite'",
         "Secretary General Rutte pledged to defend 'every inch of NATO "
         "territory, including space' after German media reported Russia is "
         "preparing a nuclear-armed satellite, 'Sputnik-S'.",
         draw_satellite, NAVY),
        ("SPORT  ·  CRICKET",
         "England crush Australia by eight wickets",
         "Chasing 185 in the second T20I, England raced to 188 for 2 in "
         "13.1 overs. Aneurin Donald smashed 85 off 32 balls as the "
         "five-match series levelled at 1-1.",
         draw_cricket, RED),
    ]

    gx, gy = mx, 420
    cw, ch = 476, 158
    for i, (kicker, head, deck, glyph, gcolor) in enumerate(stories):
        x = gx + (i % 2) * (cw + 0)
        y0 = gy + (i // 2) * ch
        if i % 2 == 1:
            x = gx + cw
        d.text((x, y0), kicker, font=font(SANS_B, 13), fill=gcolor)
        y1 = para(d, x, y0 + 20, head, font(SANS_B, 21), 380, 25)
        para(d, x, y1 + 2, deck, font(SANS, 14), 380, 19)
        glyph(d, x + 396, y0 + 52, 0.85, gcolor)
        if i % 2 == 0:
            d.line([(x + cw - 4, y0 + 4), (x + cw - 4, y0 + ch - 16)],
                   fill=LINE, width=1)
        if i // 2 < 2:
            d.line([(x, y0 + ch - 8), (x + cw - 12, y0 + ch - 8)],
                   fill=LINE, width=1)

    # ---------- Footer: also today ----------
    fy = 906
    rule(d, mx, fy, W - mx, 2)
    d.text((mx, fy + 12), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    also = [
        "SEOUL: Education minister Choi Kyo-jin quit over AI-cheating chaos "
        "in the college entrance exam; 111 device cases were caught.",
        "MARKETS: Dell raised its outlook on booming AI server demand, "
        "while Nvidia shares slid about 7% as US lawmakers pressed Huawei answers.",
        "PARIS: Former president Sarkozy was ordered to stand trial in a "
        "corruption case involving him and his wife, Carla Bruni.",
        "KYIV: A new analysis puts Russian soldiers killed in the Ukraine "
        "war above 700,000, RFE/RL reported.",
    ]
    y = fy + 36
    for item in also:
        d.text((mx, y), "\u2022", font=font(SANS_B, 14), fill=RED)
        y = para(d, mx + 16, y, item, font(SANS, 13), 936, 18)
        y += 2
    rule(d, mx, 1000, W - mx, 1, color=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
