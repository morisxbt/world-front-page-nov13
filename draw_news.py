from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = "#f4f0e6"
INK = "#191b1d"
RED = "#a52c27"
BLUE = "#334c5c"
MUTED = "#55514b"
SERIF = "/usr/share/fonts/truetype/sand-box/google/Playfair Display/PlayfairDisplay-VariableFont_wght.ttf"
SANS = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def font(path, size):
    return ImageFont.truetype(path, size)


def fitted(text, path, size, max_size, width, height):
    for px in range(size, max_size - 1, -1):
        f = font(path, px)
        box = d.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= width and box[3] - box[1] <= height:
            return f
    return font(path, max_size)


def label(text, xy, f, fill=INK):
    # Measure before placement; shrink only if a label would cross the page edge.
    box = d.textbbox((0, 0), text, font=f)
    max_w, max_h = W - xy[0] - 26, H - xy[1] - 20
    while (box[2] - box[0] > max_w or box[3] - box[1] > max_h) and f.size > 9:
        f = font(SANS, f.size - 1)
        box = d.textbbox((0, 0), text, font=f)
    d.text((xy[0] - box[0], xy[1] - box[1]), text, font=f, fill=fill)


def wrap_words(text, f, width):
    rows, row = [], ""
    for word in text.split():
        candidate = (row + " " + word).strip()
        box = d.textbbox((0, 0), candidate, font=f)
        if row and box[2] - box[0] > width:
            rows.append(row)
            row = word
        else:
            row = candidate
    if row:
        rows.append(row)
    return rows


def line(points, fill=INK, width=2):
    d.line(points, fill=fill, width=width, joint="curve")


def icon(kind, box):
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    if kind == "chip":
        d.rounded_rectangle((cx-29, cy-29, cx+29, cy+29), radius=6, outline=BLUE, width=4)
        d.rectangle((cx-15, cy-15, cx+15, cy+15), fill=RED)
        for off in (-18, 0, 18):
            line([(cx-39,cy+off),(cx-29,cy+off)], BLUE, 3); line([(cx+29,cy+off),(cx+39,cy+off)], BLUE, 3)
            line([(cx+off,cy-39),(cx+off,cy-29)], BLUE, 3); line([(cx+off,cy+29),(cx+off,cy+39)], BLUE, 3)
    elif kind == "smog":
        d.ellipse((cx-31,cy-30,cx+8,cy+4), fill="#ded8cc", outline=BLUE, width=2)
        d.ellipse((cx-8,cy-37,cx+30,cy+4), fill="#ded8cc", outline=BLUE, width=2)
        for bx, bw, bh in ((cx-32,13,24),(cx-16,15,34),(cx+2,13,27),(cx+17,13,20)):
            d.rectangle((bx,cy+8-bh,bx+bw,cy+8), fill="#d4cec2", outline=BLUE, width=2)
        label("AQI", (cx-17,cy+11), font(SANS, 12), RED)
    elif kind == "oil":
        # Radar dish and sweep for the Bahrain radar story.
        line([(cx-3,cy+17),(cx-3,cy+34)], BLUE, 4)
        line([(cx-21,cy+35),(cx+16,cy+35)], BLUE, 4)
        d.arc((cx-31,cy-28,cx+31,cy+34), 205, 335, fill=BLUE, width=4)
        d.arc((cx-22,cy-20,cx+22,cy+24), 205, 335, fill=BLUE, width=3)
        line([(cx,cy+2),(cx+25,cy-22)], RED, 4)
        d.ellipse((cx-5,cy-4,cx+5,cy+6), fill=RED)
    elif kind == "winter":
        # Tent silhouette, with two small snowflakes above it.
        d.polygon([(cx-31,cy+24),(cx,cy-13),(cx+31,cy+24)], outline=BLUE)
        line([(cx,cy-12),(cx,cy+24)], RED, 3)
        line([(cx-19,cy+24),(cx-19,cy+2)], BLUE, 2)
        for sx, sy in ((cx-22,cy-29),(cx+22,cy-26)):
            line([(sx-6,sy),(sx+6,sy)], BLUE, 2)
            line([(sx,sy-6),(sx,sy+6)], BLUE, 2)
            line([(sx-4,sy-4),(sx+4,sy+4)], BLUE, 2)
    elif kind == "talks":
        d.rounded_rectangle((cx-39,cy-26,cx+8,cy+8), radius=7, outline=BLUE, width=3)
        d.rounded_rectangle((cx-7,cy-5,cx+39,cy+28), radius=7, outline=RED, width=3)
        line([(cx-24,cy-12),(cx-6,cy-12)], BLUE, 2); line([(cx+7,cy+8),(cx+24,cy+8)], RED, 2)
    elif kind == "outage":
        d.rounded_rectangle((cx-36,cy-25,cx+36,cy+19), radius=5, outline=BLUE, width=3)
        line([(cx-20,cy+30),(cx+20,cy+30)], BLUE, 3); line([(cx,cy+19),(cx,cy+30)], BLUE, 3)
        line([(cx-16,cy-13),(cx+16,cy+7)], RED, 5)
        line([(cx+16,cy-13),(cx-16,cy+7)], RED, 5)
    elif kind == "defence":
        flag_y, fw, fh, gap = cy-25, 12, 25, 3
        flag_defs = (("#c62828","#ffffff","#c62828"), ("#2868a8","#f1c40f","#2868a8"),
                     ("#2868a8","#ffffff","#c62828"), ("#ffffff","#2868a8","#ffffff"),
                     ("#2868a8","#ffffff","#c62828"))
        for idx, (field, cross, border) in enumerate(flag_defs):
            fx = cx - (5*fw+4*gap)/2 + idx*(fw+gap)
            d.rectangle((fx,flag_y,fx+fw,flag_y+fh), fill=field, outline=border, width=1)
            line([(fx+4,flag_y),(fx+4,flag_y+fh)], cross, 3)
            line([(fx,flag_y+9),(fx+fw,flag_y+9)], cross, 3)


def card(x, y, w, h, kind, headline, kicker, subline):
    d.rectangle((x, y, x+w, y+h), outline="#c9c1b3", width=2)
    icon(kind, (x+11, y+11, 57, 54))
    label(kicker.upper(), (x+77, y+10), font(SANS, 16), RED)
    title_lines = headline.split("\n")
    for idx, title in enumerate(title_lines):
        label(title, (x+77, y+32+idx*25), font(SANS, 22), INK)
    summary_font = font(SANS, 16)
    for idx, summary in enumerate(wrap_words(subline, summary_font, w-24)[:2]):
        label(summary, (x+12, y+85+idx*18), summary_font, INK)


# Refined page layout and editorial treatment.
d.rectangle((24, 18, 1000, 1006), outline="#b8ae9e", width=2)
label("THE WORLD TODAY", (48, 30), font(SERIF, 43))
label("FRIDAY 13 NOVEMBER 2026", (50, 82), font(SANS, 19), RED)
label("A DAY OF SHOCKS", (790, 50), font(SANS, 13), MUTED)
line([(48, 117), (976, 117)], RED, 2)

# Lead story: a vacated chair, severed corporate authority, and a sharp market fall.
d.rounded_rectangle((48, 136, 976, 482), radius=4, fill="#e9e4d9", outline="#c9c1b3", width=2)
label("TECH / MARKETS", (68, 153), font(SANS, 13), RED)
label("NVIDIA CHIEF", (68, 173), font(SERIF, 48), INK)
label("RESIGNS", (68, 221), font(SERIF, 48), INK)
label("Jensen Huang steps down amid scandals", (69, 275), font(SANS, 21), INK)
label("Colette Kress named interim CEO; Huang to face House lawmakers", (69, 307), font(SANS, 17), INK)
label("NEARLY $2 TRILLION", (69, 350), font(SANS, 21), RED)
label("in market value lost since early October", (69, 380), font(SANS, 17), INK)
# Chair icon constructed from clean geometric strokes.
d.ellipse((731, 158, 933, 359), fill="#f4f0e6", outline="#c9c1b3", width=2)
d.rounded_rectangle((798, 197, 868, 274), radius=12, outline=BLUE, width=6)
line([(798, 262), (783, 300), (881, 300), (868, 262)], BLUE, 6)
line([(800, 306), (796, 333)], BLUE, 6); line([(865, 306), (869, 333)], BLUE, 6)
d.rectangle((817, 217, 850, 250), fill=RED)
label("N", (821, 214), font(SANS, 23), PAPER)
# Properly framed falling market line uses the open right side of the lead.
label("−$2T", (755, 367), font(SANS, 25), RED)
line([(731, 445),(944,445)], BLUE, 2)
line([(731, 410),(731,445)], BLUE, 2)
line([(741, 402),(778,397),(808,407),(838,416),(868,421),(899,435),(929,439)], RED, 5)
d.polygon([(929,439),(912,428),(916,443)], fill=RED)
label("NVDA", (737, 421), font(SANS, 16), BLUE)
line([(68, 425), (678,425)], "#c9c1b3", 1)
label("ALLEGATIONS REPORTED; NO FINDINGS SHOWN", (69, 436), font(SANS, 16), INK)

label("WORLD IN BRIEF", (48, 493), font(SERIF, 26))
label("CONFLICT · CITIES · POWER · TECHNOLOGY", (620, 501), font(SANS, 16), INK)
line([(48, 529), (976, 529)], INK, 2)

cards = [
    (48,541,"oil","IRAN: BAHRAIN\nRADAR DESTROYED","GULF / IRAN","IRGC says retaliation for U.S. strike; tankers hit in Hormuz"),
    (360,541,"talks","ABU DHABI TALKS\nSWAP ANNOUNCED","UKRAINE / RUSSIA","Abu Dhabi talks end; largest prisoner swap of the war"),
    (672,541,"winter","GAZA INFANT DIES\nIN WINTER COLD","GAZA","49 nations urge Israel to let tents and fuel in"),
    (48,676,"outage","MICROSOFT DOWN\nIN 74 NATIONS","GLOBAL TECH","Outlook, Teams and Copilot down for millions"),
    (360,676,"smog","DELHI AIR TOPS\nWORLD RANKINGS","INDIA / AIR","AQI 334: Delhi overtakes Lahore as most polluted"),
    (672,676,"defence","NORDIC DEFENCE\nPACT DRAFTED","EUROPE","Denmark, Finland, Iceland, Norway, Sweden"),
]
for x,y,kind,headline,kicker,subline in cards:
    card(x,y,304,135,kind,headline,kicker,subline)

# Compact ticker carries additional breadth without competing with lead.
d.rectangle((48, 811, 976, 952), fill="#e9e4d9", outline="#c9c1b3", width=2)
label("ALSO TODAY", (65, 817), font(SANS, 16), RED)
line([(65, 840),(959,840)], "#c9c1b3", 1)
ticker = [
    "US MIDTERMS: Mississippi's first Democratic senator since 1982; Van Hollen challenges Schumer",
    "NYC: Brooklyn collapse kills 8; 100 sites ordered inspected",
    "INDIA: 23 killed in Assam bus-truck crash near Kaziranga",
    "INDONESIA: Prabowo accepts Gibran resignation",
    "HORMUZ TANKERS ATTACKED · HOUTHIS CLAIM SAUDI OIL STRIKES · TRUMP: NO IRAN DEAL",
]
for i, txt in enumerate(ticker):
    yy = 843 + i*21
    d.ellipse((67, yy+6, 74, yy+13), fill=RED if i in (0, 4) else BLUE)
    f = fitted(txt, SANS, 16, 16, 865, 20)
    label(txt, (85, yy), f)

line([(48, 970), (976, 970)], INK, 2)
label("WORLD DESK", (50, 979), font(SANS, 16), RED)
label("13 NOVEMBER 2026", (818, 979), font(SANS, 16), MUTED)

im.save("entry.png", "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
