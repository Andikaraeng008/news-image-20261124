"""The World Today - Tuesday 24 November 2026 (dense v2).

Entry program for make.fun news-image-20261124. Writes one 1024x1024 PNG
of the day's world news to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).

Standard library only in the grader: when Pillow is missing, the
pre-rendered entry.png shipped in this repository is copied to the output.
When Pillow is present the page is composed from the bundled illustrations.
"""
import os
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (143, 29, 29)
GREY = (96, 92, 84)
LINE = (120, 115, 105)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill=INK, lh=None):
    if lh is None:
        lh = int(fnt.size * 1.32)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_font(d, text, path, start, width):
    size = start
    while size > 10:
        f = font(path, size)
        if d.textlength(text, font=f) <= width:
            return f
        size -= 2
    return font(path, 10)


def hline(d, x0, x1, y, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(d, x, y0, y1, width=1, fill=LINE):
    d.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---- simplified world map (lon, lat polygons) ----
NA = [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-85, 76),
      (-80, 73), (-70, 62), (-60, 55), (-55, 50), (-60, 45), (-68, 44),
      (-75, 38), (-76, 34), (-81, 31), (-84, 30), (-90, 29), (-97, 26),
      (-103, 22), (-97, 16), (-90, 14), (-83, 10), (-79, 9), (-86, 13),
      (-92, 15), (-98, 17), (-105, 20), (-112, 25), (-118, 32), (-124, 40),
      (-125, 48), (-135, 58), (-150, 60), (-162, 58), (-168, 65)]
SA = [(-79, 9), (-77, 4), (-75, -2), (-70, -5), (-62, -8), (-52, -5),
      (-42, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -33),
      (-62, -38), (-68, -45), (-70, -52), (-72, -54), (-74, -48), (-73, -38),
      (-72, -28), (-70, -18), (-76, -12), (-80, -6), (-81, 0), (-80, 5)]
AF = [(-17, 15), (-16, 21), (-10, 28), (-6, 33), (0, 36), (10, 37),
      (20, 32), (30, 31), (34, 28), (38, 22), (43, 12), (51, 11),
      (48, 2), (41, -4), (40, -12), (36, -18), (32, -26), (28, -33),
      (20, -35), (16, -32), (13, -22), (12, -12), (13, -5), (9, 4),
      (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)]
EU = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (0, 48),
      (3, 50), (6, 53), (8, 55), (8, 58), (12, 58), (18, 60), (20, 62),
      (25, 65), (28, 70), (32, 70), (35, 68), (40, 66), (42, 62),
      (40, 58), (35, 55), (30, 52), (28, 48), (26, 45), (23, 42),
      (22, 38), (20, 36), (15, 38), (12, 38), (8, 38), (3, 37),
      (-2, 36), (-6, 36), (-9, 37)]
AS = [(28, 70), (35, 68), (40, 66), (45, 68), (55, 70), (65, 72),
      (75, 73), (90, 75), (105, 77), (120, 73), (135, 72), (150, 70),
      (162, 68), (175, 65), (170, 62), (162, 60), (158, 55), (150, 58),
      (142, 55), (140, 48), (138, 42), (132, 38), (128, 35), (126, 40),
      (122, 38), (120, 32), (118, 28), (112, 22), (108, 18), (105, 10),
      (102, 8), (98, 12), (96, 16), (94, 20), (91, 22), (88, 22),
      (85, 20), (82, 16), (80, 10), (78, 8), (76, 12), (74, 18),
      (72, 20), (70, 23), (66, 25), (62, 25), (58, 27), (55, 28),
      (52, 29), (50, 30), (48, 30), (45, 32), (43, 35), (40, 37),
      (38, 40), (36, 42), (33, 44), (30, 46), (30, 50), (28, 55),
      (30, 60), (30, 65), (28, 68)]
AU = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
      (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
      (145, -38), (149, -37), (151, -34), (153, -30), (153, -27),
      (150, -23), (147, -19), (143, -15), (141, -13), (139, -15),
      (136, -15), (135, -12), (132, -11), (130, -13), (127, -14),
      (124, -17), (121, -20), (117, -20), (114, -22)]
CONTINENTS = [NA, SA, AF, EU, AS, AU]
# (label, lon, lat, dx, dy) label offsets keep the six tags readable
PLACES = [("TALLINN", 24.7, 59.4, 4, -9),
          ("WASHINGTON", -77.0, 38.9, 4, -9),
          ("GENEVA", 6.1, 46.2, -42, 8),
          ("GAZA", 34.5, 31.5, 4, -9),
          ("DELHI", 77.2, 28.6, 4, 7),
          ("ULLEUNG", 130.9, 37.5, -46, -9)]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=LINE, width=1)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 78.0, -58.0
    for poly in CONTINENTS:
        pts = [(x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)
               for lon, lat in poly]
        d.polygon(pts, fill=(214, 208, 194), outline=(150, 144, 130))
    fnt = font(SANS_B, 8)
    for label, lon, lat, dx, dy in PLACES:
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        d.text((px + dx, py + dy), label, font=fnt, fill=INK)


def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 18
    cw = W - 2 * mx  # 988 content width

    # ---- masthead ----
    f_mast = fit_font(d, "THE WORLD TODAY", SERIF_B, 96, cw)
    tw = d.textlength("THE WORLD TODAY", font=f_mast)
    d.text(((W - tw) / 2, 6), "THE WORLD TODAY", font=f_mast, fill=INK)
    hline(d, mx, W - mx, 100, width=2)
    f_date = font(SANS_B, 13)
    d.text((mx, 106), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=INK)
    right = "PRESS TIME 00:30 UTC  ·  No. 329"
    d.text((W - mx - d.textlength(right, font=f_date), 106), right,
           font=f_date, fill=INK)
    hline(d, mx, W - mx, 126, width=1)

    # ---- markets ticker (verified figures only) ----
    f_tick = font(SANS_B, 11)
    tick = ("NASDAQ +6.5%   ·   S&P +4.7%   ·   NVIDIA +31%   ·   "
            "NIKKEI +3%   ·   NVIDIA VALUE UP NEARLY $1TN")
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 131), tick, font=f_tick, fill=INK)
    hline(d, mx, W - mx, 150, width=1)

    # ---- key metrics strip ----
    metrics = [("07:52", "SEOUL ALERT TIME"),
               ("3 MIN", "ALERT LIFTED AFTER"),
               ("+31%", "NVIDIA ON HUANG RETURN"),
               ("$1.62BN", "INDIA AID TO NEPAL"),
               ("+6.5%", "NASDAQ ON MONDAY"),
               ("1,500", "NEPAL FLOOD DEAD, AUG")]
    f_num = font(SANS_B, 23)
    f_lab = font(SANS, 8)
    cell = cw / 6.0
    for i, (num, lab) in enumerate(metrics):
        cx = mx + cell * i + cell / 2
        d.text((cx - d.textlength(num, font=f_num) / 2, 156), num,
               font=f_num, fill=INK)
        d.text((cx - d.textlength(lab, font=f_lab) / 2, 184), lab,
               font=f_lab, fill=GREY)
        if i:
            vline(d, mx + cell * i, 156, 198, width=1)
    hline(d, mx, W - mx, 202, width=1)

    # ---- lead story ----
    lx, lw = mx, 482
    y = 208
    f_kick = font(SANS_B, 12)
    d.text((lx, y), "KOREA  ·  DEFENCE", font=f_kick, fill=RED)
    tag = "[CONFIRMED]"
    d.text((lx + d.textlength("KOREA  ·  DEFENCE  ", font=f_kick), y), tag,
           font=f_kick, fill=INK)
    y = 228
    f_head = font(SERIF_B, 33)
    y = draw_lines(d, lx, y, wrap(d, "SEOUL ALERT AS RUSSIAN JETS ENTER "
                                    "DEFENCE ZONE", f_head, lw), f_head, lh=39)
    y += 4
    f_deck = font(SERIF, 13)
    y = draw_lines(d, lx, y, wrap(d, "Seoul scrambles fighters as warplanes "
                                    "enter the defence zone; the Ulleung alert "
                                    "lifts in three minutes.", f_deck, lw),
                   f_deck, lh=17)
    y += 6
    f_body = font(SANS, 11)
    body = ("SEOUL — South Korea scrambled fighter jets early on Tuesday "
            "after several Russian warplanes entered the country's air "
            "defence identification zone over the East Sea without notice, "
            "the Joint Chiefs of Staff said. Ulleung Island was told to "
            "shelter at 07:52 after an unidentified aircraft set off a "
            "civil defence alert. The warning was lifted three minutes "
            "later; officials later said the aircraft was possibly "
            "North Korean.")
    y = draw_lines(d, lx, y, wrap(d, body, f_body, lw), f_body, lh=15)
    y += 4
    f_bul = font(SANS_B, 11)
    for b in ("Alert issued 07:52, lifted 3 minutes later",
              "Jets entered the defence zone, not sovereign airspace"):
        d.text((lx, y), "■", font=f_bul, fill=RED)
        d.text((lx + 14, y), b, font=f_bul, fill=INK)
        y += 15

    # lead photo (smaller than v1) + caption + minute-by-minute box
    rx = 512
    jets = Image.open(os.path.join(BASE, "assets", "jets.jpg")).convert("RGB")
    jets = jets.resize((494, 189), Image.LANCZOS)
    img.paste(jets, (rx, 208))
    f_cap = font(SANS, 9)
    y = draw_lines(d, rx, 402, wrap(d, "South Korean fighter jets climb over "
                                      "the East Sea near Ulleung Island at "
                                      "dawn on Tuesday. Illustration.",
                                    f_cap, 494), f_cap, fill=GREY, lh=12)
    y += 6
    hline(d, rx, W - mx, y, width=1)
    y += 6
    f_th = font(SANS_B, 10)
    d.text((rx, y), "THE ALERT, MINUTE BY MINUTE", font=f_th, fill=INK)
    y += 15
    f_tl = font(SANS, 10)
    for t in ("07:52 — Ulleung Island told to shelter as jets approach.",
              "07:55 — Civil defence warning lifted, three minutes later.",
              "Later — Officials say the aircraft was possibly North Korean."):
        y = draw_lines(d, rx, y, wrap(d, t, f_tl, 494), f_tl, lh=13)

    # ---- secondary stories (small photos, text beside them) ----
    hline(d, mx, W - mx, 528, width=1)
    secondaries = [
        ("MARKETS  ·  MONDAY", " [REPORTED]", "traders.jpg",
         "HUANG'S RETURN SENDS NVIDIA UP 31%",
         "Shares jump on Monday as Jensen Huang returns as chief executive "
         "11 days after resigning; Nasdaq +6.5%, S&P +4.7%."),
        ("SPORT  ·  GENEVA", "", "chess.jpg",
         "GUKESH DEFENDS CROWN AS TITLE RACE OPENS",
         "World champion faces Uzbekistan's Javokhir Sindarov as the 2026 "
         "World Chess Championship begins in Geneva."),
    ]
    f_sk = font(SANS_B, 10)
    f_sh = font(SERIF_B, 15)
    f_ss = font(SANS, 10)
    for i, (kick, tag2, pic, head, summ) in enumerate(secondaries):
        x0 = mx + i * 501
        ph = Image.open(os.path.join(BASE, "assets", pic)).convert("RGB")
        ph = ph.resize((228, 140), Image.LANCZOS)
        img.paste(ph, (x0, 536))
        tx = x0 + 240
        d.text((tx, 536), kick, font=f_sk, fill=RED)
        if tag2:
            d.text((tx + d.textlength(kick, font=f_sk), 536), tag2,
                   font=f_sk, fill=INK)
        yy = draw_lines(d, tx, 554, wrap(d, head, f_sh, 247), f_sh, lh=18)
        draw_lines(d, tx, yy + 3, wrap(d, summ, f_ss, 247), f_ss, lh=13)
    hline(d, mx, W - mx, 686, width=1)

    # ---- six headline cards, each with a two-line summary ----
    cards = [
        ("NATO CALLS URGENT MEETING",
         "Alliance meets as a string of incidents escalates tensions with Russia."),
        ("RUSSIA WARNS ESTONIA",
         "Moscow warns of 'open war' over a plan to close land border crossings."),
        ("INDIA PLEDGES $1.62BN TO NEPAL",
         "Aid for flood rebuilding, announced Monday; $377m grant, $1.24bn credit."),
        ("STATES SUE OVER GROK IMAGES",
         "US states sue Musk firms over sexualised images made by AI chatbot Grok."),
        ("TAJIKISTAN MOVES TO QUIT ICC",
         "Dushanbe moves to leave the International Criminal Court."),
        ("DENMARK UPHOLDS 'GHETTO LAW'",
         "Top court backs evictions under the hardline housing law."),
    ]
    f_ch = font(SERIF_B, 13)
    f_cs = font(SANS, 10)
    for i, (head, summ) in enumerate(cards):
        col, row = i % 3, i // 3
        x0 = mx + col * 335
        y0 = 694 + row * 74
        yy = draw_lines(d, x0, y0, wrap(d, head, f_ch, 318), f_ch, lh=16)
        draw_lines(d, x0, yy + 2, wrap(d, summ, f_cs, 318), f_cs, lh=13)
        if col:
            vline(d, x0 - 9, y0, y0 + 66, width=1)
    hline(d, mx, W - mx, 844, width=1)

    # ---- bottom band: map | more from the world | date check ----
    f_bh = font(SANS_B, 11)
    d.text((mx, 852), "WHERE IT HAPPENED", font=f_bh, fill=INK)
    d.text((344, 852), "MORE FROM THE WORLD", font=f_bh, fill=INK)
    d.text((708, 852), "DATE CHECK", font=f_bh, fill=INK)
    draw_map(d, mx, 872, 310, 86)
    more = [
        ("GAZA / WEST BANK", "Israeli raids hit West Bank towns."),
        ("IRAN SANCTIONS · MONDAY", "US sanctions hit Tehran's banks."),
        ("INDIA", "Modi opens AI centre; India-China generals talk."),
        ("INDONESIA FACTORY FIRE", "24 dead in Banten factory blaze."),
        ("VANUATU QUAKE", "6.5 quake off Vanuatu; no tsunami threat."),
        ("MERKURY SUNK OFF LIBYA", "Zelenskyy confirms the sinking."),
    ]
    f_mt = font(SANS_B, 10)
    f_ms = font(SANS, 10)
    y = 872
    for title, summ in more:
        line = title + " — " + summ
        lines = wrap(d, line, f_ms, 340)
        yy = y
        for li, ln in enumerate(lines):
            if li == 0:
                d.text((344, yy), title, font=f_mt, fill=INK)
                rest = ln[len(title):]
                d.text((344 + d.textlength(title, font=f_mt), yy), rest,
                       font=f_ms, fill=INK)
            else:
                d.text((344, yy), ln, font=f_ms, fill=INK)
            yy += 13
        y = yy + 2
    f_dc = font(SANS, 10)
    dc = ("Every story here happened, or was first reported, on Tuesday "
          "24 November 2026 — except the items marked Monday: the Nepal "
          "aid announcement and the US Iran sanctions. All illustrations "
          "are original work made for this edition.")
    y = draw_lines(d, 708, 872, wrap(d, dc, f_dc, 298), f_dc, lh=13)
    y += 5
    d.text((708, y), "19 STORIES · 6 REGIONS · 3 ILLUSTRATIONS",
           font=font(SANS_B, 9), fill=RED)
    vline(d, 336, 852, 964, width=1)
    vline(d, 700, 852, 964, width=1)

    # ---- briefs strip ----
    hline(d, mx, W - mx, 966, width=1)
    d.text((mx, 972), "BRIEFS", font=f_bh, fill=INK)
    briefs = [
        ("KYIV HIT", "Russian drones strike homes in the Kyiv region; several missing."),
        ("LISBON MARCH", "Thousands protest the rising cost of living."),
        ("MEXICO RAID", "16 cartel associates killed in the capture of 'El Chapo Isidro'."),
        ("NIKKEI SURGE", "Nikkei jumps over 3% on Huang's Nvidia comeback."),
    ]
    f_bt = font(SANS_B, 10)
    f_bs = font(SANS, 10)
    for i, (title, summ) in enumerate(briefs):
        x0 = mx + i * 252
        yy = draw_lines(d, x0, 990, wrap(d, title + " — " + summ, f_bs, 240),
                        f_bs, lh=13)
    return img


def main():
    out = os.path.join(OUTDIR, "entry.png")
    os.makedirs(OUTDIR, exist_ok=True)
    if HAVE_PIL:
        compose().save(out, format="PNG", optimize=True, compress_level=6)
    else:
        shutil.copyfile(os.path.join(BASE, "entry.png"), out)


if __name__ == "__main__":
    main()
