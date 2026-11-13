from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = "#f4f0e6"
INK = "#191b1d"
RED = "#a52c27"
BLUE = "#334c5c"
MUTED = "#6f6a61"
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
        d.ellipse((cx-23,cy-30,cx+23,cy+16), outline=RED, width=3)
        for yy in (cy-3, cy+9, cy+21): line([(cx-38,yy),(cx+38,yy)], BLUE, 4)
    elif kind == "oil":
        d.polygon([(cx,cy-37),(cx-24,cy+2),(cx-20,cy+24),(cx,cy+36),(cx+20,cy+24),(cx+24,cy+2)], fill=RED)
        line([(cx-43,cy+32),(cx+43,cy+32)], BLUE, 3)
    elif kind == "winter":
        line([(cx,cy-34),(cx,cy+34)], BLUE, 3); line([(cx-30,cy-17),(cx+30,cy+17)], BLUE, 3); line([(cx-30,cy+17),(cx+30,cy-17)], BLUE, 3)
        d.ellipse((cx-5,cy-5,cx+5,cy+5), fill=RED)
    elif kind == "talks":
        d.rounded_rectangle((cx-39,cy-26,cx+8,cy+8), radius=7, outline=BLUE, width=3)
        d.rounded_rectangle((cx-7,cy-5,cx+39,cy+28), radius=7, outline=RED, width=3)
        line([(cx-24,cy-12),(cx-6,cy-12)], BLUE, 2); line([(cx+7,cy+8),(cx+24,cy+8)], RED, 2)
    elif kind == "outage":
        d.rounded_rectangle((cx-35,cy-27,cx+35,cy+24), radius=5, outline=BLUE, width=3)
        line([(cx-20,cy+34),(cx+20,cy+34)], BLUE, 3); line([(cx,cy+24),(cx,cy+34)], BLUE, 3)
        line([(cx-27,cy-14),(cx+27,cy+12)], RED, 4)
    elif kind == "defence":
        d.polygon([(cx,cy-38),(cx+32,cy-22),(cx+27,cy+12),(cx,cy+37),(cx-27,cy+12),(cx-32,cy-22)], outline=BLUE, fill=None)
        line([(cx-14,cy),(cx-3,cy+12),(cx+17,cy-12)], RED, 4)


def card(x, y, w, h, kind, headline, kicker):
    d.rectangle((x, y, x+w, y+h), outline="#c9c1b3", width=2)
    icon(kind, (x+9, y+13, 67, h-25))
    label(kicker.upper(), (x+84, y+14), font(SANS, 11), RED)
    f = fitted(headline, SANS, 20, 11, w-99, h-44)
    label(headline, (x+84, y+34), f)


# Refined page layout and editorial treatment.
d.rectangle((24, 18, 1000, 1006), outline="#b8ae9e", width=2)
label("THE WORLD TODAY", (48, 30), font(SERIF, 43))
label("FRIDAY 13 NOVEMBER 2026", (50, 82), font(SANS, 17), RED)
label("A DAY OF SHOCKS", (790, 50), font(SANS, 13), MUTED)
line([(48, 117), (976, 117)], INK, 3)

# Lead story: a vacated chair, severed corporate authority, and a sharp market fall.
d.rounded_rectangle((48, 136, 976, 482), radius=4, fill="#e9e4d9", outline="#c9c1b3", width=2)
label("TECH / MARKETS", (68, 153), font(SANS, 13), RED)
label("NVIDIA CHIEF RESIGNS", (68, 175), fitted("NVIDIA CHIEF RESIGNS", SERIF, 43, 34, 570, 58))
label("Jensen Huang steps down amid scandals", (69, 234), font(SANS, 20), INK)
label("Colette Kress named interim CEO; Huang to face House lawmakers", (69, 266), fitted("Colette Kress named interim CEO; Huang to face House lawmakers", SANS, 15, 11, 570, 24), MUTED)
label("NEARLY $2 TRILLION", (69, 317), font(SANS, 19), RED)
label("in market value lost since early October", (69, 345), font(SANS, 14), INK)
# Chair icon constructed from clean geometric strokes.
d.ellipse((731, 158, 933, 359), fill="#f4f0e6", outline="#c9c1b3", width=2)
d.rounded_rectangle((798, 197, 868, 274), radius=12, outline=BLUE, width=6)
line([(798, 262), (783, 300), (881, 300), (868, 262)], BLUE, 6)
line([(800, 306), (796, 333)], BLUE, 6); line([(865, 306), (869, 333)], BLUE, 6)
d.rectangle((817, 217, 850, 250), fill=RED)
label("N", (821, 214), font(SANS, 23), PAPER)
# Downward stock line.
line([(711, 384),(757,369),(797,377),(835,397),(872,402),(925,443)], RED, 6)
d.polygon([(925,443),(904,437),(918,423)], fill=RED)
label("NVDA", (710, 414), font(SANS, 12), BLUE)
line([(68, 397), (678,397)], "#c9c1b3", 1)
label("ALLEGATIONS REPORTED; NO FINDINGS SHOWN", (69, 414), font(SANS, 11), MUTED)

label("WORLD IN BRIEF", (48, 503), font(SERIF, 24))
label("CONFLICT · CITIES · POWER · TECHNOLOGY", (620, 511), font(SANS, 12), MUTED)
line([(48, 536), (976, 536)], INK, 2)

cards = [
    (48,550,"oil","Iran says Bahrain radar destroyed","GULF / IRAN"),
    (360,550,"talks","Ukraine talks yield swap, no deal","UKRAINE / RUSSIA"),
    (672,550,"winter","Gaza infant dies in winter cold","GAZA"),
    (48,654,"outage","Microsoft outage hits 74 nations","GLOBAL TECH"),
    (360,654,"smog","Delhi smog tops world rankings","INDIA / AIR"),
    (672,654,"defence","Nordics draft shared defence pact","EUROPE"),
]
for x,y,kind,headline,kicker in cards:
    card(x,y,304,91,kind,headline,kicker)

# Compact ticker carries additional breadth without competing with lead.
d.rectangle((48, 776, 976, 952), fill="#e9e4d9", outline="#c9c1b3", width=2)
label("ALSO TODAY", (65, 789), font(SANS, 12), RED)
line([(65, 812),(959,812)], "#c9c1b3", 1)
ticker = [
    "US MIDTERMS: Mississippi's first Democratic senator since 1982; Van Hollen challenges Schumer",
    "NYC: Brooklyn collapse kills 8; 100 sites ordered inspected",
    "INDIA: 23 killed in Assam bus-truck crash near Kaziranga",
    "INDONESIA: Prabowo accepts Gibran resignation",
    "HORMUZ TANKERS ATTACKED · HOUTHIS CLAIM SAUDI OIL STRIKES · TRUMP: NO IRAN DEAL",
]
for i, txt in enumerate(ticker):
    yy = 824 + i*24
    d.ellipse((67, yy+6, 74, yy+13), fill=RED if i in (0, 4) else BLUE)
    f = fitted(txt, SANS, 13, 10, 865, 20)
    label(txt, (85, yy), f)

line([(48, 970), (976, 970)], INK, 2)
label("WORLD DESK", (50, 979), font(SANS, 11), RED)
label("13 NOVEMBER 2026", (818, 979), font(SANS, 11), MUTED)

im.save("entry.png", "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
