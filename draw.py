#!/usr/bin/env python3
"""Draw the front page of 23 November 2026 world news as one 1024x1024 PNG.

Original artwork drawn in code with Pillow. No photos, no downloads, no
network. Deterministic: same input always produces the same PNG bytes.
Run: python3 draw.py  ->  writes entry.png next to this script.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 231)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GREY = (90, 86, 78)
LIGHT = (233, 226, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel(draw, x, y, w, h, kicker, headline, body, head_size=30,
          body_size=19, art=None, head_lines=2):
    """A bordered news panel. art(d, x, y, w, h) draws the illustration."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    pad = 14
    cx = x + pad
    cy = y + 10
    draw.text((cx, cy), kicker, font=F_SANS_B(15), fill=RED)
    cy += 24
    hl = wrap(draw, headline, F_SERIF_B(head_size), w - 2 * pad)
    cy = text_block(draw, cx, cy, hl[:head_lines], F_SERIF_B(head_size),
                    leading=head_size + 6)
    cy += 4
    if art is not None:
        art_h = 76 if h > 200 else 64
        art(draw, x + pad, cy, w - 2 * pad, art_h)
        cy += art_h + 8
    bl = wrap(draw, body, F_SANS(body_size), w - 2 * pad)
    # Cap the body so it never spills past the panel's bottom edge.
    max_lines = max(1, (y + h - pad - cy) // (body_size + 6))
    if len(bl) > max_lines:
        bl = bl[:max_lines]
        bl[-1] = bl[-1].rstrip(".,") + "…"
    text_block(draw, cx, cy, bl, F_SANS(body_size),
               leading=body_size + 6)
    return y + h


# ---- illustrations (simple original pictograms, drawn in code) ----

def art_cop31(d, x, y, w, h):
    # A torn climate pact: a document split in two over a hot globe.
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # globe, bottom left
    cx, cy, r = x + 64, y + h // 2 + 6, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 190, 220),
              outline=BLUE, width=3)
    d.ellipse([cx - 24, cy - 16, cx - 2, cy + 6], fill=(90, 170, 90))
    d.ellipse([cx + 4, cy + 8, cx + 28, cy + 28], fill=(90, 170, 90))
    # heat waves rising from the globe
    for i, wx in enumerate([cx - 30, cx, cx + 30]):
        d.line([(wx, cy - r - 4), (wx + 6, cy - r - 16),
                (wx - 2, cy - r - 26)], fill=RED, width=3)
    # torn document, right side: two halves with a jagged gap
    dx, dy, dw, dh = x + w - 128, y + 8, 112, h - 16
    d.rectangle([dx, dy, dx + dw // 2 - 6, dy + dh], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([dx + dw // 2 + 6, dy, dx + dw, dy + dh], fill=(255, 255, 255),
                outline=INK, width=2)
    # jagged tear edges
    d.polygon([(dx + dw // 2 - 6, dy), (dx + dw // 2 + 4, dy + dh // 3),
               (dx + dw // 2 - 4, dy + 2 * dh // 3),
               (dx + dw // 2 + 6, dy + dh), (dx + dw // 2 - 6, dy + dh)],
              fill=(255, 255, 255))
    for i, ly in enumerate([dy + 14, dy + 34, dy + 54]):
        d.line([(dx + 10, ly), (dx + dw // 2 - 16, ly)], fill=GREY, width=2)
        d.line([(dx + dw // 2 + 16, ly), (dx + dw - 10, ly)], fill=GREY, width=2)
    # big red X over the gap
    gx = dx + dw // 2
    d.line([(gx - 14, dy + dh - 26), (gx + 14, dy + dh - 52)], fill=RED, width=5)
    d.line([(gx + 14, dy + dh - 26), (gx - 14, dy + dh - 52)], fill=RED, width=5)
    d.text((x + 112, y + 8), "COP31", font=F_SANS_B(19), fill=BLUE)
    d.text((x + 112, y + 34), "ANTALYA", font=F_SANS_B(19), fill=BLUE)
    d.text((x + 112, y + 60), "NO DEAL", font=F_SANS_B(18), fill=RED)


def art_gulf(d, x, y, w, h):
    # A tanker on a burning strait: sea, hull, flames and smoke.
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 232))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(31, 78, 121))
    # tanker hull
    hx, hy = x + 18, y + h - 52
    d.polygon([(hx, hy), (hx + w - 60, hy), (hx + w - 78, hy + 26),
               (hx + 8, hy + 26)], fill=(120, 40, 30))
    d.rectangle([hx + 30, hy - 22, hx + 70, hy], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([hx + 78, hy - 14, hx + 96, hy], fill=(255, 255, 255),
                outline=INK, width=2)
    # funnel with smoke
    d.rectangle([hx + w - 110, hy - 26, hx + w - 88, hy], fill=INK)
    for i, (sx, sy, sr) in enumerate([(hx + w - 108, hy - 44, 8),
                                      (hx + w - 96, hy - 58, 11),
                                      (hx + w - 80, hy - 70, 13)]):
        d.ellipse([sx, sy, sx + 2 * sr, sy + 2 * sr], fill=(90, 86, 78))
    # flames on the water ahead of the tanker
    fx = x + w - 52
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(fx, y + h - 30),
                (fx + 18 * math.cos(a), y + h - 30 + 18 * math.sin(a))],
               fill=(255, 150, 40), width=4)
    d.ellipse([fx - 9, y + h - 39, fx + 9, y + h - 21], fill=(255, 190, 60))


def art_kyiv(d, x, y, w, h):
    # A damaged apartment block at night, drone overhead, searchlight.
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    # block, left, with a broken corner
    bx, by, bw, bh = x + 10, y + 18, 110, h - 26
    d.rectangle([bx, by, bx + bw, by + bh], fill=(16, 18, 28))
    d.polygon([(bx + bw, by), (bx + bw + 16, by + 14), (bx + bw, by + 26)],
              fill=(255, 150, 40))
    for wy in range(by + 10, by + bh - 8, 16):
        for wx in [bx + 10, bx + 34, bx + 58, bx + 82]:
            d.rectangle([wx, wy, wx + 12, wy + 9], fill=(240, 200, 90))
    # rubble at the base
    d.polygon([(bx, by + bh), (bx + 40, by + bh - 14), (bx + 84, by + bh),
               (bx + 120, by + bh - 10), (bx + 150, by + bh)],
              fill=(90, 86, 78))
    # drone silhouette, top right
    dx, dy = x + w - 110, y + 10
    d.ellipse([dx, dy, dx + 56, dy + 16], fill=(220, 220, 220))
    d.line([(dx - 16, dy + 8), (dx + 72, dy + 8)], fill=(220, 220, 220),
           width=4)
    d.ellipse([dx - 16, dy, dx - 4, dy + 8], fill=(220, 220, 220))
    d.ellipse([dx + 60, dy, dx + 72, dy + 8], fill=(220, 220, 220))
    d.line([(dx + 28, dy + 16), (dx + 28, dy + 26)], fill=(220, 220, 220),
           width=3)
    # narrow searchlight beam from below
    d.polygon([(x + w - 24, y + h), (x + w - 44, y + 44),
               (x + w - 28, y + 44)], fill=(255, 240, 180))
    d.text((x + 128, y + h - 24), "DYMER, KYIV REGION",
           font=F_SANS_B(13), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    X0, X1 = M, W - M

    # --- masthead ---
    rule(d, X0, X1, 14, width=3)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_SERIF_B(62))
    d.text(((W - tw) / 2, 22), title, font=F_SERIF_B(62), fill=INK)
    rule(d, X0, X1, 104, width=2)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=F_SANS_B(38))
    d.text(((W - dw) / 2, 112), date, font=F_SANS_B(38), fill=RED)
    tag = "One day's world news — in one picture"
    tgw = d.textlength(tag, font=F_SERIF(20))
    d.text(((W - tgw) / 2, 158), tag, font=F_SERIF(20), fill=GREY)
    rule(d, X0, X1, 188, width=3)
    rule(d, X0, X1, 192, width=1)

    # --- lead story: COP31 collapses ---
    ly, lh = 202, 200
    d.rectangle([X0, ly, X1, ly + lh], outline=INK, width=2)
    d.text((X0 + 14, ly + 10), "LEAD  •  CLIMATE", font=F_SANS_B(16), fill=RED)
    head = "COP31 ends with no deal"
    hl = wrap(d, head, F_SERIF_B(40), 560)
    text_block(d, X0 + 14, ly + 36, hl, F_SERIF_B(40), leading=46)
    body = ("The Antalya summit closed with no agreement after the EU and "
            "others rejected a draft that never mentioned fossil fuels.")
    bl = wrap(d, body, F_SANS(18), 560)
    text_block(d, X0 + 14, ly + 36 + len(hl) * 46 + 8, bl, F_SANS(18),
               leading=24)
    art_cop31(d, X0 + 600, ly + 12, X1 - X0 - 614, lh - 24)

    # --- row 2: two stories ---
    ry, rh = 414, 254
    w2 = (X1 - X0 - 12) // 2
    panel(d, X0, ry, w2, rh, "WAR  •  GULF",
          "Iran hits Bahrain, tankers struck",
          "Iran struck a civilian site in Bahrain, injuring 2, as two "
          "tankers were hit in the Strait of Hormuz.",
          head_size=27, body_size=16, art=art_gulf)
    panel(d, X0 + w2 + 12, ry, w2, rh, "WAR  •  UKRAINE",
          "14 missing after drone hits flats",
          "A Russian drone hit a five-storey block in Dymer, near Kyiv; "
          "Zelenskyy pressed the US for Patriot missiles.",
          head_size=27, body_size=16, art=art_kyiv)

    # --- row 3: three stories (text only, no art: keeps them legible) ---
    ry3, rh3 = 680, 192
    w3 = (X1 - X0 - 24) // 3
    panel(d, X0, ry3, w3, rh3, "ASIA  •  INDONESIA",
          "7 bodies found, 50 missing in factory fire",
          "Rescuers searched a burned candy factory in Cikande, Banten, "
          "after Saturday's blaze.",
          head_size=23, body_size=17, art=None)
    panel(d, X0 + w3 + 12, ry3, w3, rh3, "ASIA  •  S. KOREA",
          "Minister quits over AI exam row",
          "Education chief Choi Kyo-jin resigned after AI anti-cheating "
          "rules hit the college exam.",
          head_size=23, body_size=17, art=None)
    panel(d, X0 + 2 * (w3 + 12), ry3, w3, rh3, "USA  •  TRAVEL",
          "Delta outage delays 1,000+ flights",
          "A weight-and-balance failure grounded Delta flights before "
          "Thanksgiving.",
          head_size=23, body_size=17, art=None)

    # --- footer: also today ---
    fy = 884
    rule(d, X0, X1, fy, width=3)
    d.text((X0, fy + 8), "ALSO TODAY", font=F_SANS_B(16), fill=RED)
    items = [
        ("DIPLOMACY", "Nepal PM Balendra Shah held talks with PM Modi in "
         "Delhi on his state visit."),
        ("SPORT", "India posted a record 720/9 in the Wellington Test "
         "against New Zealand."),
        ("TECH", "Nations agreed at the UN to keep negotiating curbs on "
         "lethal AI weapons."),
    ]
    col_w = (X1 - X0) // 3
    for i, (kick, txt) in enumerate(items):
        cx = X0 + i * col_w
        d.text((cx, fy + 34), kick, font=F_SANS_B(15), fill=BLUE)
        bl = wrap(d, txt, F_SANS(16), col_w - 16)
        text_block(d, cx, fy + 56, bl[:3], F_SANS(16), leading=21)
    rule(d, X0, X1, H - 16, width=2)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
