#!/usr/bin/env python3
"""THE NIGHT WIRE - one picture of Monday 23 November 2026.

An original front page drawn entirely in code with Pillow.
Every panel, icon and rule below was written for this edition:
a dark masthead, a wide climate lead, two war briefs, three
short tiles and a wire ticker along the foot of the page.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAGE = (13, 20, 32)          # deep ink navy page
CARD = (246, 240, 226)       # warm paper card
CARD_DIM = (232, 224, 205)   # shaded paper for tiles
INK = (20, 30, 44)           # text on paper
CREAM = (246, 240, 226)      # text on navy
RED = (214, 69, 51)          # wire red accent
GOLD = (224, 168, 60)        # masthead gold
TEAL = (46, 127, 134)        # sea teal
SMOKE = (110, 116, 124)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
MARGIN = 36


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, fnt, fill, width, leading=1.18):
    """Draw wrapped text, return the y just below it."""
    x, y = xy
    step = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def card(draw, box, fill=CARD, radius=14, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def kicker(draw, xy, text, colour=RED):
    draw.text(xy, text, font=font(SANS_B, 21), fill=colour)
    return xy[1] + 30


# ---------------------------------------------------------------- icons
def icon_globe_crack(draw, cx, cy, r):
    """A globe split by a jagged crack, ringed by a rising thermometer."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=6)
    # two simple land masses
    draw.ellipse([cx - 52, cy - 38, cx - 6, cy + 2], fill=(96, 168, 92))
    draw.ellipse([cx + 8, cy + 16, cx + 52, cy + 52], fill=(96, 168, 92))
    # jagged crack down the middle
    pts = [(cx + 2, cy - r + 6), (cx - 12, cy - 34), (cx + 10, cy - 6),
           (cx - 10, cy + 26), (cx + 4, cy + r - 8)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    # thermometer on the right
    tx = cx + r + 26
    draw.rounded_rectangle([tx - 9, cy - 58, tx + 9, cy + 30], radius=9,
                           outline=INK, width=4)
    draw.rectangle([tx - 4, cy - 6, tx + 4, cy + 30], fill=RED)
    draw.ellipse([tx - 17, cy + 22, tx + 17, cy + 56], fill=RED)


def icon_tanker(draw, x, y, w):
    """A low tanker silhouette on wave lines, burst at the stern."""
    hull_top = y + 28
    draw.polygon([(x, hull_top), (x + w, hull_top), (x + w - 30, hull_top + 24),
                  (x + 26, hull_top + 24)], fill=(122, 52, 40))
    draw.rectangle([x + 24, hull_top - 18, x + 88, hull_top], fill=INK)
    draw.rectangle([x + w - 118, hull_top - 24, x + w - 78, hull_top],
                   fill=INK)
    draw.rectangle([x + w - 90, hull_top - 38, x + w - 83, hull_top - 24],
                   fill=SMOKE)
    # burst star at the stern
    bx, by = x + w - 6, hull_top + 12
    for dx, dy in [(0, -17), (12, -10), (16, 2), (10, 13), (0, 16),
                   (-11, 11), (-16, 0), (-10, -12)]:
        draw.line([bx, by, bx + dx, by + dy], fill=GOLD, width=5)
    draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=RED)
    # waves
    for row, off in [(hull_top + 34, 0), (hull_top + 48, 18)]:
        xx = x - 4 + off
        while xx < x + w - 14:
            draw.arc([xx, row, xx + 30, row + 12], 180, 360, fill=TEAL, width=4)
            xx += 32


def icon_drone_block(draw, x, y, w):
    """A five-storey block at night and a small quadcopter above it."""
    bw = int(w * 0.52)
    draw.rectangle([x, y + 14, x + bw, y + 84], fill=(38, 48, 66))
    for r in range(3):
        for c in range(4):
            wx = x + 13 + c * 28
            wy = y + 24 + r * 21
            lit = (r * 4 + c) % 3 != 0
            draw.rectangle([wx, wy, wx + 16, wy + 12],
                           fill=GOLD if lit else (90, 100, 116))
    # quadcopter
    qx, qy = x + bw + 72, y + 26
    draw.ellipse([qx - 16, qy - 8, qx + 16, qy + 8], fill=INK)
    for dx, dy in [(-30, -14), (30, -14), (-30, 14), (30, 14)]:
        draw.line([qx, qy, qx + dx, qy + dy], fill=INK, width=4)
        draw.ellipse([qx + dx - 10, qy + dy - 4, qx + dx + 10, qy + dy + 4],
                     outline=INK, width=3)
    draw.polygon([(qx - 5, qy + 8), (qx + 5, qy + 8), (qx, qy + 24)],
                 fill=RED)


def icon_flame(draw, cx, cy, s):
    """A three-tongue flame for the factory fire tile."""
    draw.polygon([(cx, cy - s), (cx + int(s * 0.55), cy + int(s * 0.3)),
                  (cx + int(s * 0.3), cy + s), (cx - int(s * 0.3), cy + s),
                  (cx - int(s * 0.55), cy + int(s * 0.3))], fill=RED)
    draw.polygon([(cx, cy - int(s * 0.45)), (cx + int(s * 0.3), cy + int(s * 0.35)),
                  (cx + int(s * 0.16), cy + s), (cx - int(s * 0.16), cy + s),
                  (cx - int(s * 0.3), cy + int(s * 0.35))], fill=GOLD)
    draw.ellipse([cx - int(s * 0.13), cy + int(s * 0.3),
                  cx + int(s * 0.13), cy + s], fill=(250, 214, 130))


def icon_cap(draw, cx, cy, s):
    """A graduation cap for the exam-row tile."""
    draw.polygon([(cx, cy - int(s * 0.35)), (cx + s, cy),
                  (cx, cy + int(s * 0.35)), (cx - s, cy)], fill=INK)
    draw.polygon([(cx - int(s * 0.5), cy + int(s * 0.18)),
                  (cx + int(s * 0.5), cy + int(s * 0.18)),
                  (cx + int(s * 0.5), cy + int(s * 0.62)),
                  (cx - int(s * 0.5), cy + int(s * 0.62))], fill=(52, 66, 84))
    draw.line([cx + s, cy, cx + s, cy + int(s * 0.66)], fill=GOLD, width=5)
    draw.ellipse([cx + s - 6, cy + int(s * 0.62), cx + s + 6,
                  cy + int(s * 0.62) + 14], fill=GOLD)


def icon_plane(draw, cx, cy, s):
    """A simple airliner seen from the front, for the outage tile."""
    draw.polygon([(cx, cy - s), (cx + 10, cy - int(s * 0.2)),
                  (cx + int(s * 0.95), cy + int(s * 0.28)),
                  (cx + int(s * 0.95), cy + int(s * 0.5)),
                  (cx + 10, cy + int(s * 0.34)), (cx + 10, cy + int(s * 0.72)),
                  (cx + int(s * 0.3), cy + s), (cx, cy + int(s * 0.82)),
                  (cx - int(s * 0.3), cy + s), (cx - 10, cy + int(s * 0.72)),
                  (cx - 10, cy + int(s * 0.34)),
                  (cx - int(s * 0.95), cy + int(s * 0.5)),
                  (cx - int(s * 0.95), cy + int(s * 0.28)),
                  (cx - 10, cy - int(s * 0.2))], fill=TEAL)


# ---------------------------------------------------------------- page
def build_image():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([MARGIN, 26, W - MARGIN, 31], fill=GOLD)
    title = "THE NIGHT WIRE"
    tf = font(SERIF, 68)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 44), title, font=tf, fill=CREAM)
    sub = "MONDAY  ·  23 NOVEMBER 2026  ·  ONE DAY, ONE PICTURE"
    sf = font(SANS_B, 25)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 130), sub, font=sf, fill=GOLD)
    d.rectangle([MARGIN, 168, W - MARGIN, 173], fill=RED)

    # --- lead: COP31 ----------------------------------------------------
    top = 190
    card(d, [MARGIN, top, W - MARGIN, top + 222])
    x = MARGIN + 28
    y = kicker(d, (x, top + 18), "LEAD  ·  CLIMATE — ANTALYA, TÜRKIYE")
    y = block(d, (x, y + 2), "COP31 closes with no deal on fossil fuels",
              font(SERIF, 38), INK, 600, leading=1.1)
    block(d, (x, y + 8),
          "The Antalya summit ended without agreement after the EU and "
          "others rejected a draft text that never mentioned fossil fuels.",
          font(SANS, 21), INK, 600, leading=1.2)
    icon_globe_crack(d, 800, top + 110, 62)

    # --- two war briefs --------------------------------------------------
    top2 = top + 238
    half = (W - 2 * MARGIN - 20) // 2
    card(d, [MARGIN, top2, MARGIN + half, top2 + 252])
    card(d, [MARGIN + half + 20, top2, W - MARGIN, top2 + 252])
    x = MARGIN + 24
    y = kicker(d, (x, top2 + 16), "WAR  ·  THE GULF")
    y = block(d, (x, y), "Iran hits Bahrain; two tankers struck",
              font(SERIF, 28), INK, half - 48, leading=1.12)
    icon_tanker(d, x, y + 4, half - 60)
    block(d, (x, top2 + 204),
          "A civilian site in Bahrain was hit, injuring 2; two tankers "
          "struck in the Strait of Hormuz.", font(SANS, 18), INK,
          half - 48, leading=1.2)
    x = MARGIN + half + 44
    y = kicker(d, (x, top2 + 16), "WAR  ·  UKRAINE")
    y = block(d, (x, y), "14 missing after drone hits Kyiv flats",
              font(SERIF, 28), INK, half - 48, leading=1.12)
    icon_drone_block(d, x, y + 8, half - 60)
    block(d, (x, top2 + 204),
          "A Russian drone hit a block in Dymer, near Kyiv; Zelenskyy "
          "pressed the US for Patriots.",
          font(SANS, 18), INK, half - 48, leading=1.2)

    # --- three short tiles ----------------------------------------------
    top3 = top2 + 268
    third = (W - 2 * MARGIN - 40) // 3
    tiles = [
        ("ASIA  ·  INDONESIA", "7 bodies found, 50 missing in factory fire",
         "Rescuers searched a burned candy factory in Cikande, Banten, "
         "after Saturday's blaze.", icon_flame),
        ("ASIA  ·  S. KOREA", "Minister quits over AI exam row",
         "Education chief Choi Kyo-jin resigned after AI anti-cheating "
         "rules hit the college entrance exam.", icon_cap),
        ("USA  ·  TRAVEL", "Delta outage delays 1,000+ flights",
         "A weight-and-balance failure grounded Delta flights across the "
         "US before Thanksgiving.", icon_plane),
    ]
    for i, (kick, head, body, icon) in enumerate(tiles):
        bx = MARGIN + i * (third + 20)
        card(d, [bx, top3, bx + third, top3 + 190], fill=CARD_DIM)
        y = kicker(d, (bx + 20, top3 + 14), kick)
        icon(d, bx + third - 26, top3 + 28, 13)
        y = block(d, (bx + 20, y), head, font(SERIF, 24), INK,
                  third - 40, leading=1.12)
        block(d, (bx + 20, y + 6), body, font(SANS, 17), INK,
              third - 40, leading=1.2)

    # --- wire ticker ------------------------------------------------------
    top4 = top3 + 206
    d.rectangle([MARGIN, top4, W - MARGIN, top4 + 5], fill=GOLD)
    y = kicker(d, (MARGIN, top4 + 14), "ALSO ON THE WIRE", colour=GOLD)
    items = [
        "DIPLOMACY — Nepal PM Balendra Shah held talks with PM Modi in Delhi.",
        "SPORT — India posted a record 720/9 in the Wellington Test vs New Zealand.",
        "TECH — UN talks continue on curbs for lethal AI weapons.",
    ]
    for it in items:
        y = block(d, (MARGIN, y), "▸  " + it, font(SANS, 20), CREAM,
                  W - 2 * MARGIN, leading=1.15) + 5
    return img


if __name__ == "__main__":
    build_image().save("entry.png")
    print("wrote entry.png")
