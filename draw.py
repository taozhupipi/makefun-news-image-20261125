#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024 PNG).

Self-contained: Pillow only, no network, deterministic output.
Usage: python3 draw.py [output_path]  (default: entry.png)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (242, 237, 227)
NAVY = (28, 43, 74)
GOLD = (217, 164, 65)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 196)
INK = (26, 26, 26)
GREY = (85, 82, 74)
FOOT_GREY = (120, 114, 102)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# (tag, tag colour, headline, summary) — all verified 25 Nov 2026 reporting.
STORIES = [
    ("UKRAINE · WAR", (179, 55, 47),
     "Russia hits Ukraine's power grid",
     "Overnight strikes cut power in five regions; five killed and gas sites set ablaze."),
    ("USA · TRADE", (31, 95, 168),
     "New US tariffs on 14 partners",
     "Washington targets excess factory capacity; the steepest duties will hit China."),
    ("MIDDLE EAST · SECURITY", (180, 83, 9),
     "Houthi drone hits Riyadh tower",
     "The kingdom's tallest tower is struck a second time in a week; 11 people hurt."),
    ("PACIFIC · SECURITY", (15, 118, 110),
     "Solomons pick Australia as partner",
     "Treaty bars any foreign military base; Canberra pledges $740m over a decade."),
    ("CHINA · SPACE", (51, 65, 85),
     "First foreigner boards Tiangong",
     "Shenzhou-24 docks; Pakistani pilot Zeeshan Ali joins the station for a week."),
    ("COLOMBIA · RESCUE", (47, 125, 50),
     "Cartagena hostages freed at dawn",
     "Troops storm an Exito store at dawn; all captives freed, one gunman killed."),
    ("USA · MIGRATION", (109, 40, 217),
     "Abrego Garcia lands in Spain",
     "After a 20-month deportation fight, he flies to Madrid on a commercial flight."),
    ("SYRIA · SECURITY", (157, 44, 92),
     "IS attack kills two in Hasaka",
     "Islamic State gunmen kill two security staff and wound five in northeast Syria."),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tint(rgb, frac=0.88):
    """Mix a colour toward white for the glyph disc background."""
    return tuple(int(c + (255 - c) * frac) for c in rgb)


def draw_bolt(d, cx, cy, s, colour):
    """A lightning bolt centred on (cx, cy), spanning about s pixels."""
    pts = [(cx + 0.10 * s, cy - 0.55 * s), (cx - 0.35 * s, cy + 0.08 * s),
           (cx - 0.02 * s, cy + 0.08 * s), (cx - 0.10 * s, cy + 0.55 * s),
           (cx + 0.35 * s, cy - 0.08 * s), (cx + 0.02 * s, cy - 0.08 * s)]
    d.polygon(pts, fill=colour)


def draw_bars(d, cx, cy, s, colour):
    """Three rising bars (a tiny chart) centred on (cx, cy)."""
    bw = 0.20 * s
    for i, h in enumerate((0.45, 0.75, 1.0)):
        x0 = cx - 0.42 * s + i * 0.30 * s
        d.rectangle([x0, cy + 0.45 * s - h * s, x0 + bw, cy + 0.45 * s],
                    fill=colour)


def draw_drone(d, cx, cy, s, colour):
    """A quadcopter seen from above: body dot and four rotor dots."""
    r = 0.13 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x, y = cx + dx * 0.34 * s, cy + dy * 0.34 * s
        d.ellipse([x - 0.09 * s, y - 0.09 * s, x + 0.09 * s, y + 0.09 * s],
                  fill=colour)
        d.line([cx, cy, x, y], fill=colour, width=2)


def draw_scroll(d, cx, cy, s, colour):
    """A treaty document: folded sheet with lines and a seal."""
    d.rectangle([cx - 0.30 * s, cy - 0.42 * s, cx + 0.30 * s, cy + 0.42 * s],
                outline=colour, width=3)
    for i, y in enumerate((-0.18, 0.02, 0.22)):
        d.line([cx - 0.18 * s, cy + y * s, cx + 0.18 * s, cy + y * s],
               fill=colour, width=3)
    d.ellipse([cx + 0.18 * s, cy + 0.28 * s, cx + 0.42 * s, cy + 0.52 * s],
              fill=colour)


def draw_rocket(d, cx, cy, s, colour):
    """A small rocket pointing up-right, with a flame."""
    d.polygon([(cx + 0.30 * s, cy - 0.42 * s), (cx + 0.42 * s, cy + 0.05 * s),
               (cx + 0.05 * s, cy + 0.42 * s), (cx - 0.18 * s, cy + 0.18 * s)],
              fill=colour)
    d.polygon([(cx - 0.05 * s, cy + 0.30 * s), (cx - 0.28 * s, cy + 0.52 * s),
               (cx + 0.12 * s, cy + 0.48 * s)], fill=(217, 164, 65))


def draw_shield(d, cx, cy, s, colour):
    """A shield outline with a check mark inside."""
    pts = [(cx, cy - 0.45 * s), (cx + 0.38 * s, cy - 0.28 * s),
           (cx + 0.38 * s, cy + 0.05 * s), (cx, cy + 0.48 * s),
           (cx - 0.38 * s, cy + 0.05 * s), (cx - 0.38 * s, cy - 0.28 * s)]
    d.line(pts + [pts[0]], fill=colour, width=3, joint="curve")
    d.line([(cx - 0.20 * s, cy + 0.02 * s), (cx - 0.05 * s, cy + 0.18 * s),
            (cx + 0.24 * s, cy - 0.20 * s)], fill=colour, width=4,
           joint="curve")


def draw_plane(d, cx, cy, s, colour):
    """A paper plane flying up-right."""
    d.polygon([(cx - 0.42 * s, cy + 0.05 * s), (cx + 0.45 * s, cy - 0.35 * s),
               (cx + 0.05 * s, cy + 0.15 * s), (cx - 0.05 * s, cy + 0.42 * s)],
              fill=colour)


def draw_warn(d, cx, cy, s, colour):
    """A warning triangle with an exclamation mark."""
    d.polygon([(cx, cy - 0.48 * s), (cx + 0.48 * s, cy + 0.38 * s),
               (cx - 0.48 * s, cy + 0.38 * s)], outline=colour, width=3)
    d.line([cx, cy - 0.22 * s, cx, cy + 0.10 * s], fill=colour, width=4)
    d.ellipse([cx - 0.035 * s, cy + 0.20 * s, cx + 0.035 * s, cy + 0.27 * s],
              fill=colour)


GLYPHS = [draw_bolt, draw_bars, draw_drone, draw_scroll,
          draw_rocket, draw_shield, draw_plane, draw_warn]

def fit_headline(d, text, width):
    """Largest headline font (30 down to 24) that wraps into at most 2 lines."""
    for size in (30, 28, 26, 24):
        fnt = font(BOLD, size)
        lines = wrap(d, text, fnt, width)
        if len(lines) <= 2:
            return fnt, lines[:2]
    return font(BOLD, 24), wrap(d, text, font(BOLD, 24), width)[:2]


def draw_card(d, box, story, glyph):
    tag, colour, headline, summary = story
    x0, y0, x1, y1 = box
    pad = 18
    d.rounded_rectangle(box, radius=14, fill=CARD, outline=CARD_EDGE, width=1)

    # Tag pill, top-left.
    tag_fnt = font(BOLD, 15)
    tw = d.textlength(tag, font=tag_fnt)
    pill = (x0 + pad, y0 + 14, x0 + pad + tw + 20, y0 + 14 + 26)
    d.rounded_rectangle(pill, radius=13, fill=colour)
    d.text((pill[0] + 10, pill[1] + 5), tag, font=tag_fnt, fill=(255, 255, 255))

    # Glyph disc, top-right.
    cx, cy, r = x1 - pad - 22, y0 + 14 + 22, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=tint(colour))
    glyph(d, cx, cy, 30, colour)

    # Headline, up to two lines.
    inner_w = (x1 - x0) - 2 * pad
    head_fnt, lines = fit_headline(d, headline, inner_w)
    hy = y0 + 52
    for line in lines:
        d.text((x0 + pad, hy), line, font=head_fnt, fill=INK)
        hy += int(head_fnt.size * 1.18)

    # Summary, up to three lines.
    sum_fnt = font(REG, 19)
    slines = wrap(d, summary, sum_fnt, inner_w)[:3]
    sy = y0 + 52 + 2 * int(30 * 1.18) + 8
    for line in slines:
        d.text((x0 + pad, sy), line, font=sum_fnt, fill=GREY)
        sy += 25


def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band.
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title_fnt = font(BOLD, 44)
    title = "WEDNESDAY 25 NOVEMBER 2026"
    tw = d.textlength(title, font=title_fnt)
    d.text(((W - tw) / 2, 18), title, font=title_fnt, fill=(255, 255, 255))
    sub_fnt = font(BOLD, 21)
    sub = "THE WORLD TODAY · EIGHT STORIES"
    sw = d.textlength(sub, font=sub_fnt)
    d.text(((W - sw) / 2, 76), sub, font=sub_fnt, fill=GOLD)

    # 2 x 4 grid of cards.
    gx, gy = 24, 134
    gap_x, gap_y = 16, 12
    cw = (W - 2 * gx - gap_x) // 2
    ch = (H - gy - 34 - 3 * gap_y) // 4
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (cw + gap_x)
        y0 = gy + row * (ch + gap_y)
        draw_card(d, (x0, y0, x0 + cw, y0 + ch), story, GLYPHS[i])

    # Footer with sources.
    foot_fnt = font(REG, 16)
    foot = "Sources: Reuters · AP · CNN · BBC · PM of Australia"
    fw = d.textlength(foot, font=foot_fnt)
    d.text(((W - fw) / 2, H - 26), foot, font=foot_fnt, fill=FOOT_GREY)

    img.save(out_path, "PNG")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
