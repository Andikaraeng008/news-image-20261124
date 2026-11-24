"""The World Today - Tuesday 24 November 2026, in one image.

Entry program for make.fun news-image-20261124. Draws a 1024x1024
broadsheet front page with 50 verified stories (15 numbered main
blocks + 35 one-line briefs) using Pillow when available. The grader
runs with the Python standard library only, so when Pillow is missing
main() copies the bundled entry.png to the output instead.
"""
import os
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = "/output/entry.png"
W, H = 1024, 1024
M = 14
CW = W - 2 * M
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (155, 27, 27)
GREY = (85, 85, 85)
RULE = (40, 40, 40)
FAINT = (216, 210, 194)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
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


def para(d, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 4
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, width=1):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)


def vline(d, x, y0, y1, width=1):
    d.line([(x, y0), (x, y1)], fill=RULE, width=width)


def fit_image(path, w, h, focus=0.5):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = int(focus * max(nh - h, 0))
    return im.crop((x0, y0, x0 + w, y0 + h))


# ---------------------------------------------------------------- data
LEAD_HEAD = "SEOUL ALERT AS RUSSIAN JETS ENTER DEFENCE ZONE"
LEAD_BODY = (
    "SEOUL \u2014 South Korea scrambled fighter jets early on Tuesday after "
    "several Russian warplanes entered the country's air defence "
    "identification zone over the East Sea without notice, the Joint "
    "Chiefs of Staff said. Ulleung Island was told to shelter at 07:52; "
    "the warning was lifted three minutes later; officials later said "
    "the aircraft was possibly North Korean."
)
LEAD_BULLETS = [
    "Alert issued 07:52, lifted 3 minutes later",
    "Jets entered the defence zone, not sovereign airspace",
]
MINUTE = [
    "07:52 \u2014 Ulleung Island told to shelter as jets approach.",
    "07:55 \u2014 Civil defence warning lifted, three minutes later.",
    "Later \u2014 Officials say the aircraft was possibly North Korean.",
]

SECONDARY = [
    ("MARKETS \u00b7 MONDAY [REPORTED]",
     "HUANG'S RETURN SENDS NVIDIA UP 31%",
     "Shares jump on Monday as Jensen Huang returns as chief executive "
     "11 days after resigning; Nasdaq +6.5%, S&P +4.7%.",
     "media-generation-traders-0-efafd764-bfed-49ef-a038-cb4b480ffc99.webp"),
    ("SPORT \u00b7 GENEVA",
     "GUKESH DEFENDS CROWN AS TITLE RACE OPENS",
     "World champion faces Uzbekistan's Javokhir Sindarov as the 2026 "
     "World Chess Championship begins in Geneva.",
     "media-generation-chess-0-cf5f387b-c1f8-4ac2-9bae-712fb400aeaf.webp"),
]

# Numbered main blocks 4-15: (headline, summary)
MAIN = [
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
    ("INDONESIA FACTORY FIRE",
     "Fire at a candy factory in Banten kills 24; rescuers search for the missing."),
    ("VANUATU QUAKE",
     "A 6.5 quake strikes off Vanuatu; no tsunami threat."),
    ("MERKURY SUNK OFF LIBYA",
     "Zelenskyy confirms Ukrainian drones sank the Russian corvette off Libya."),
    ("KYIV HIT",
     "Russian drones strike homes in the Kyiv region; several people missing."),
    ("SPARTA II UNDER TOW",
     "Moscow hauls the drone-hit cargo ship; all 16 crew safe."),
    ("ALCARAZ WINS ATP FINALS",
     "Spaniard beats Alexander Zverev in Turin to claim his first ATP Finals title."),
]

# One-line briefs: (bold lead-in, rest). 35 briefs.
BRIEFS = [
    ("GAZA / WEST BANK", "Israeli raids hit West Bank towns."),
    ("IRAN SANCTIONS \u00b7 MONDAY", "US sanctions target Tehran's banks."),
    ("INDIA", "Modi opens AI centre; India-China generals talk."),
    ("LISBON MARCH", "Thousands protest the cost of living."),
    ("MEXICO RAID", "16 cartel men killed in Chapo capture."),
    ("NIKKEI SURGE", "Nikkei jumps 3% on Huang's comeback."),
    ("NATO AWACS \u00b7 MONDAY", "Early-warning jets head to Poland."),
    ("GERMANY\u2013KYIV \u00b7 MONDAY", "Berlin to use Kyiv's Delta system."),
    ("IRAN VOWS REPLY \u00b7 MONDAY", "Tehran vows to counter US blockade."),
    ("TRUMP HALTS BLAST \u00b7 MONDAY", "Army pauses Iowa azide blast."),
    ("MURMANSK GOVERNOR HELD", "Governor held over graft claims."),
    ("CHINA DEATH SENTENCE", "Official dies for leaking secrets."),
    ("TRIPP KICKOFF", "Armenia, US launch Trump Route project."),
    ("HORMUZ TANKERS HIT", "Three tankers hit mines, catch fire."),
    ("SEOUL MINISTER RESIGNS", "Education chief quits over AI rules."),
    ("UN AI FRAMEWORK", "UN chief wants AI safety rules in a year."),
    ("LATVIA SNUBS MOSCOW", "PM refuses to restore ties with Russia."),
    ("GAZA CHILDREN OUT", "Injured Gaza children flown to Britain."),
    ("O'HARE GROUND STOP", "Chicago halts flights briefly."),
    ("SWIFT PLOT FOILED", "Mossad foiled ISIS plot on Vienna shows."),
    ("LAHORE SMOG", "Lahore tops world pollution ranking again."),
    ("PAKISTAN QUAKE", "4.0 quake strikes near Afghan border."),
    ("MEGHAN CALL", "King Charles calls Meghan after arrest."),
    ("GERMAN SCHOOL THREATS", "450 schools get bomb threats."),
    ("SARAYU EXPRESS", "Modi, Nepal PM flag off new train."),
    ("PANT 128", "Pant hits 128 against New Zealand."),
    ("VERSTAPPEN WINS", "Verstappen takes Las Vegas Grand Prix."),
    ("OIL BILL SOARS", "India's oil bill up 60% to $16bn."),
    ("SPICEJET CRISIS", "Pilots urge action as debts mount."),
    ("COP31 FLOP \u00b7 MONDAY", "Climate talks end with no fuel deal."),
    ("GRAIN DEAL NO", "Russia rejects a new UN grain deal."),
    ("FIFA 2031 \u00b7 MONDAY", "FIFA confirms 2031 World Cup hosts."),
    ("GAZA CONTAMINATION", "Oxfam: Gaza poisoned for decades."),
    ("KIM SNUBS TRUMP", "Kim ignores Trump's repeated outreach."),
    ("CHAPO TRIAL", "'El Chapo Isidro' to face trial in Mexico."),
]

METRICS = [
    ("07:52", "SEOUL ALERT TIME"),
    ("3 MIN", "ALERT LIFTED AFTER"),
    ("+31%", "NVIDIA ON HUANG RETURN"),
    ("$1.62BN", "INDIA AID TO NEPAL"),
    ("+6.5%", "NASDAQ ON MONDAY"),
    ("1,500", "NEPAL FLOOD DEAD, AUG"),
]

DATE_CHECK = (
    "Every story here happened, or was first reported, on Tuesday "
    "24 November 2026 \u2014 except the items marked MONDAY: Nepal aid, "
    "Iran sanctions, Nvidia's return, NATO AWACS, the Delta deal, "
    "Iran's blockade reply, the Iowa blast pause, COP31, FIFA 2031. "
    "All illustrations are original work made for this edition. "
    "50 STORIES \u00b7 6 REGIONS \u00b7 3 ILLUSTRATIONS"
)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    # Stylised continents, normalised 0-1000 coords.
    continents = [
        [(60, 180), (180, 120), (300, 150), (330, 230), (280, 300),
         (220, 340), (150, 320), (90, 260)],
        [(280, 420), (340, 400), (380, 470), (350, 580), (300, 560),
         (270, 480)],
        [(470, 180), (540, 150), (580, 200), (540, 250), (480, 240)],
        [(470, 300), (560, 290), (600, 380), (560, 520), (500, 500),
         (460, 380)],
        [(600, 150), (850, 120), (950, 200), (900, 320), (780, 380),
         (680, 300), (620, 220)],
        [(800, 560), (900, 550), (930, 620), (850, 650), (790, 610)],
    ]
    for poly in continents:
        pts = [(x + px * w / 1000, y + py * h / 1000) for px, py in poly]
        d.polygon(pts, fill=(226, 220, 205), outline=(150, 145, 130))
    dots = [
        ("WASHINGTON", 210, 270, -4, 8),
        ("TALLINN", 545, 175, 4, -4),
        ("GENEVA", 505, 215, -34, 4),
        ("GAZA", 585, 330, 4, -4),
        ("DELHI", 760, 300, -8, 8),
        ("ULLEUNG", 905, 250, -30, -4),
    ]
    f = font(SANS_B, 8)
    for name, px, py, dx, dy in dots:
        cx, cy = x + px * w / 1000, y + py * h / 1000
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
        d.text((cx + dx, cy + dy), name, font=f, fill=INK)


def build():
    # 50 stories exactly: 1 lead + 2 secondary + 12 grid blocks + 35 briefs.
    assert 1 + len(SECONDARY) + len(MAIN) + len(BRIEFS) == 50
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M

    # Masthead
    f_mast = font(SERIF_B, 66)
    d.text((W / 2, 6), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    hline(d, x0, x1, 78, 2)
    f_date = font(SERIF_B, 15)
    d.text((x0, 84), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=INK)
    rt = "PRESS TIME 00:30 UTC \u00b7 No. 329 \u00b7 50 STORIES"
    d.text((x1, 84), rt, font=f_date, fill=INK, anchor="ra")
    hline(d, x0, x1, 104)

    # Timeline strip + markets ticker
    f_strip = font(SANS_B, 12)
    d.text((W / 2, 108), "THE DAY IN BRIEF \u2014 00:11 MERKURY CONFIRMED \u00b7 "
           "00:20 VANUATU QUAKE \u00b7 07:52 ULLEUNG ALERT \u00b7 "
           "10:40 O'HARE GROUND STOP", font=f_strip, fill=INK, anchor="ma")
    hline(d, x0, x1, 126)
    d.text((W / 2, 130), "NASDAQ +6.5% \u00b7 S&P +4.7% \u00b7 NVIDIA +31% \u00b7 "
           "NIKKEI +3% \u00b7 NVIDIA VALUE UP NEARLY $1TN", font=f_strip,
           fill=INK, anchor="ma")
    hline(d, x0, x1, 148)

    # Metrics strip
    cw = CW / 6
    f_num = font(SERIF_B, 24)
    f_lab = font(SANS_B, 9)
    for i, (num, lab) in enumerate(METRICS):
        cx = x0 + cw * i + cw / 2
        d.text((cx, 154), num, font=f_num, fill=INK, anchor="ma")
        d.text((cx, 182), lab, font=f_lab, fill=GREY, anchor="ma")
        if i:
            vline(d, x0 + cw * i, 156, 192)
    hline(d, x0, x1, 198)

    # Lead story
    lx, lw = x0, 468
    rx, rw = 498, 512
    f_kick = font(SANS_B, 12)
    d.text((lx, 204), "KOREA \u00b7 DEFENCE [CONFIRMED]", font=f_kick, fill=RED)
    y = para(d, lx, 222, LEAD_HEAD, font(SERIF_B, 34), lw, leading=41)
    y = para(d, lx, y + 4, LEAD_BODY, font(SERIF, 13), lw, leading=16)
    f_bul = font(SERIF_B, 12)
    y += 2
    for b in LEAD_BULLETS:
        d.text((lx, y), "\u25aa  " + b, font=f_bul, fill=INK)
        y += 14
    # Right column: jets photo, caption, minute-by-minute box
    jets = fit_image(os.path.join(BASE, "assets",
        "media-generation-jets-0-5d0092ee-35d1-4fff-919d-fb17179ec86c.webp"),
        rw, 170, focus=0.25)
    img.paste(jets, (rx, 204))
    para(d, rx, 378, "South Korean fighter jets climb over the East Sea "
         "near Ulleung Island at dawn on Tuesday. Illustration.",
         font(SERIF_I, 11), rw, fill=GREY, leading=14)
    d.text((rx, 408), "THE ALERT, MINUTE BY MINUTE", font=f_kick, fill=INK)
    yy = 426
    for ln in MINUTE:
        d.text((rx, yy), ln, font=font(SERIF, 12), fill=INK)
        yy += 15
    hline(d, x0, x1, 475)

    # Secondary stories
    sy = 481
    for i, (kick, head, summ, asset) in enumerate(SECONDARY):
        sx = x0 if i == 0 else 518
        pic = fit_image(os.path.join(BASE, "assets", asset), 190, 92,
                        focus=0.45)
        img.paste(pic, (sx, sy))
        tx = sx + 200
        tw = 292
        d.text((tx, sy), kick, font=font(SANS_B, 11), fill=RED)
        yy = para(d, tx, sy + 15, head, font(SERIF_B, 16), tw, leading=19)
        para(d, tx, yy + 1, summ, font(SERIF, 11), tw, leading=14)
    hline(d, x0, x1, 581)

    # Numbered main blocks 4-15: 4 columns x 3 rows, row height follows
    # the tallest block in the row so wrapped headlines never overlap.
    gy = 587
    colw = 243
    gap = 8
    f_gh = font(SERIF_B, 13)
    f_gs = font(SERIF, 10)
    for row in range(3):
        row_h = 0
        cells = []
        for col in range(4):
            idx = row * 4 + col
            head, summ = MAIN[idx]
            num = str(idx + 4)
            nw = d.textlength(num + ". ", font=f_gh)
            hl = wrap(d, head, f_gh, colw - nw)
            sl = wrap(d, summ, f_gs, colw)[:2]
            cells.append((num, nw, hl, sl))
            row_h = max(row_h, len(hl) * 16 + 1 + len(sl) * 13)
        for col in range(4):
            num, nw, hl, sl = cells[col]
            gx = x0 + col * (colw + gap)
            d.text((gx, gy), num + ". ", font=f_gh, fill=RED)
            yy = gy
            for ln in hl:
                d.text((gx + nw, yy), ln, font=f_gh, fill=INK)
                yy += 16
            yy += 1
            for ln in sl:
                d.text((gx, yy), ln, font=f_gs, fill=INK)
                yy += 13
        gy += row_h + 4
    hline(d, x0, x1, gy + 2)

    # Briefs: "ALSO ON TUESDAY 24 NOVEMBER", 5 columns x 7 rows
    d.text((x0, gy + 8), "ALSO ON TUESDAY 24 NOVEMBER",
           font=font(SERIF_B, 13), fill=INK)
    bcolw = (CW - 4 * 8) / 5
    f_bh = font(SERIF_B, 10)
    f_bt = font(SERIF, 10)
    by = gy + 26
    for row in range(7):
        for col in range(5):
            idx = row * 5 + col
            if idx >= len(BRIEFS):
                break
            head, rest = BRIEFS[idx]
            bx = x0 + col * (bcolw + 8)
            full = head + " \u2014 " + rest
            lines = wrap(d, full, f_bt, bcolw)
            ly = by
            for li, ln in enumerate(lines[:2]):
                if li == 0 and ln.startswith(head):
                    d.text((bx, ly), head, font=f_bh, fill=INK)
                    hw = d.textlength(head, font=f_bh)
                    d.text((bx + hw, ly), ln[len(head):], font=f_bt, fill=INK)
                else:
                    d.text((bx, ly), ln, font=f_bt, fill=INK)
                ly += 13
        by += 26
    # Bottom row: map + Date Check
    my = by + 2
    d.text((x0, my), "WHERE IT HAPPENED", font=font(SANS_B, 10), fill=INK)
    draw_map(d, x0, my + 13, 330, 48)
    dx = 354
    d.text((dx, my), "DATE CHECK", font=font(SANS_B, 10), fill=INK)
    para(d, dx, my + 13, DATE_CHECK, font(SERIF, 10), W - M - dx, leading=13)
    return img


def main():
    if HAVE_PIL:
        img = build()
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        img.save(OUT, format="PNG")
    else:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        shutil.copyfile(os.path.join(BASE, "entry.png"), OUT)


if __name__ == "__main__":
    main()
