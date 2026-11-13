"""Render a one-page world news briefing for 13 November 2026."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W = H = 1024
PAPER = "#f2eee5"
CARD = "#fffdf8"
INK = "#17232c"
MUTED = "#58656c"
RULE = "#d9d3c8"
RED = "#c63d32"
REGION = {
    "US": "#315f8a", "MIDDLE EAST": "#b66a34", "WORLD": "#6b5d91",
    "EUROPE": "#477a68", "GAZA": "#956342", "ASIA": "#b04443",
    "ECONOMY": "#96712b", "TECH": "#426d8b", "SOUTH ASIA": "#8a5f46",
    "AFRICA": "#4c795d", "CULTURE": "#855c86", "POLITICS": "#536b8e",
    "US POLITICS": "#536b8e",
    "TÜRKIYE": "#a33d37",
}
ROOT = Path(__file__).resolve().parent
FONT_HEAD = "/usr/share/fonts/truetype/sand-box/google/Oswald/Oswald-VariableFont_wght.ttf"
FONT_BODY = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def F(path, size):
    return ImageFont.truetype(path, size)


def txt(s, x, y, size, color=INK, bold=False, anchor=None):
    f = F(FONT_HEAD if bold else FONT_BODY, size)
    d.text((x, y), s, font=f, fill=color, anchor=anchor)
    return d.textbbox((x, y), s, font=f, anchor=anchor)


def fit(s, path, start, minimum, width):
    for size in range(start, minimum - 1, -1):
        f = F(path, size)
        if d.textbbox((0, 0), s, font=f)[2] <= width:
            return f
    return F(path, minimum)


def wrap(s, f, width):
    out, row = [], ""
    for word in s.split():
        test = (row + " " + word).strip()
        if row and d.textbbox((0, 0), test, font=f)[2] > width:
            out.append(row)
            row = word
        else:
            row = test
    if row:
        out.append(row)
    return out


def card(box, radius=12):
    d.rounded_rectangle(box, radius=radius, fill=CARD, outline=RULE, width=1)


def tag(label, x, y, color, size=12):
    f = F(FONT_BODY, size)
    tw = d.textbbox((0, 0), label, font=f)[2]
    d.rounded_rectangle((x, y, x + tw + 16, y + 22), radius=5, fill=color)
    d.text((x + 8, y + 4), label, font=f, fill="white")
    return tw + 16


def scene(kind, x, y, w, h):
    """Draw a scene on its own clipped canvas, then paste it into the page."""
    global im, d
    tile = Image.new("RGB", (w, h), "#e9eff2")
    page, page_draw = im, d
    im, d = tile, ImageDraw.Draw(tile)
    _scene_art(kind, 0, 0, w, h)
    im, d = page, page_draw
    page.paste(tile, (x, y))


def _scene_art(kind, x, y, w, h):
    """Vector illustration; the scene wrapper clips every mark to its box."""
    palettes = {"plane": "#e9eff2", "radar": "#e7edf0", "cloud": "#e9eff2",
                "fire": "#e7edf0", "summit": "#e8eee9", "tent": "#eee8dd",
                "ships": "#e7edf0", "chart": "#f1ecdf", "chip": "#e8edf0",
                "smog": "#ece6de"}
    d.rounded_rectangle((x, y, x + w, y + h), radius=9, fill=palettes[kind])
    cx, cy = x + w // 2, y + h // 2
    if kind == "plane":
        # Airport board with four named routes; parked aircraft and STOP marker.
        d.rounded_rectangle((x+8,y+7,x+w-8,y+57),radius=5,fill="#1d3444")
        rows=(("NEW YORK","CANCELLED"),("CHICAGO","DELAYED"),
              ("ATLANTA","CANCELLED"),("DENVER","DELAYED"))
        for i,(city,status) in enumerate(rows):
            yy=y+11+i*11
            txt(city,x+17,yy,9,"#fff4d7",True)
            txt(status,x+113,yy,9,"#f4a54a" if status=="DELAYED" else "#ff7165",True)
            if i<3:
                d.line((x+13,yy+10,x+186,yy+10),fill="#405564",width=1)
        px=x+w-91; py=y+75
        d.polygon([(px-48,py+5),(px-5,py-1),(px+15,py-20),(px+22,py-19),(px+15,py-1),(px+44,py+3),(px+48,py+8),(px+15,py+8),(px+8,py+20),(px+2,py+20),(px+1,py+8),(px-48,py+11)],fill="#385c70")
        d.ellipse((x+w-43,y+h-35,x+w-13,y+h-5),fill=RED)
        txt("STOP",x+w-28,y+h-20,9,"white",True,"mm")
    elif kind == "radar":
        # Bahrain flag, raised radar dome, and two intercepted drone paths.
        fx,fy=x+10,y+16
        d.rectangle((fx,fy,fx+41,fy+30),fill="#c43f40")
        d.rectangle((fx+15,fy,fx+41,fy+30),fill="white")
        for yy in range(fy,fy+30,6):
            d.polygon([(fx+15,yy),(fx+21,yy+3),(fx+15,yy+6)],fill="#c43f40")
        bx,by=cx+4,y+h-17
        d.rectangle((bx-48,by-5,bx+47,by+16),fill="#72828a")
        d.rectangle((bx-39,by-43,bx+38,by-5),fill="#c9d2d3")
        d.pieslice((bx-34,by-71,bx+34,by-2),180,360,fill="#fffdf8",outline="#426071",width=3)
        # Dotted trails terminate at small burst marks above the radar.
        for points in (((x+w-17,y+12),(x+w-59,y+25),(x+w-101,y+18)),
                       ((x+w-20,y+38),(x+w-71,y+49),(x+w-112,y+43))):
            for ax,ay in points:
                d.ellipse((ax-2,ay-2,ax+2,ay+2),fill=RED)
            ex,ey=points[-1]
            for dx,dy in ((-5,0),(5,0),(0,-5),(0,5)):
                d.line((ex+dx//2,ey+dy//2,ex+dx,ey+dy),fill="#e7a34d",width=2)
            d.polygon([(ex-5,ey-2),(ex+2,ey-5),(ex+5,ey+2),(ex-2,ey+5)],fill=RED)
    elif kind == "cloud":
        # Globe behind a laptop; screen shows mail failure and a Teams-like bubble.
        gx,gy=x+57,y+42
        d.ellipse((gx-40,gy-39,gx+40,gy+41),fill="#b8d0d7",outline="#507d91",width=3)
        d.arc((gx-22,gy-39,gx+22,gy+41),90,270,fill="#507d91",width=2)
        d.arc((gx-22,gy-39,gx+22,gy+41),270,90,fill="#507d91",width=2)
        d.arc((gx-39,gy-19,gx+39,gy+19),180,360,fill="#507d91",width=2)
        d.arc((gx-39,gy-19,gx+39,gy+19),0,180,fill="#507d91",width=2)
        lx,ly=x+111,y+22
        d.rounded_rectangle((lx,ly,lx+126,ly+61),radius=6,fill="#354f60",outline="#253b49",width=2)
        d.rectangle((lx+7,ly+7,lx+119,ly+51),fill="#90b2c0")
        d.rectangle((lx+24,ly+17,lx+76,ly+44),fill="white")
        d.line((lx+24,ly+17,lx+50,ly+33,lx+76,ly+17),fill="#567788",width=2)
        d.line((lx+61,ly+16,lx+79,ly+34),fill=RED,width=5)
        d.line((lx+79,ly+16,lx+61,ly+34),fill=RED,width=5)
        d.polygon([(lx+47,ly+61),(lx+145,ly+61),(lx+131,ly+68),(lx+36,ly+68)],fill="#607986")
        d.rounded_rectangle((x+w-53,y+5,x+w-14,y+37),radius=8,fill="#7652a5")
        d.polygon([(x+w-42,y+35),(x+w-47,y+44),(x+w-31,y+36)],fill="#7652a5")
        txt("T",x+w-33,y+20,16,"white",True,"mm")
    elif kind == "fire":
        # Hospital facade with orange fire glow.
        bx=x+16
        d.rectangle((bx+7,y+17,bx+70,y+h-12),fill="#d3dce0")
        for yy in (y+25,y+43,y+61):
            for xx in (bx+13,bx+32,bx+51):
                d.rectangle((xx,yy,xx+8,yy+7),fill="#6c91a1")
        d.rectangle((bx+31,y+56,bx+43,y+77),fill="#f5f0e5")
        # Flame cluster is intentionally kept inside the right half of the tile.
        fx=x+w-28
        d.polygon([(fx-19,y+h-10),(fx-14,y+41),(fx-8,y+52),(fx-2,y+33),(fx+5,y+45),(fx+10,y+h-10)],fill="#e35b35")
        d.polygon([(fx-13,y+h-10),(fx-8,y+57),(fx-3,y+65),(fx+2,y+49),(fx+7,y+h-10)],fill="#ffbe54")
    elif kind == "summit":
        d.rectangle((x+15,y+54,x+w-15,y+69),fill="#53796c")
        for xx in range(x+24,x+w-20,27):
            d.line((xx,y+35,xx,y+54),fill="#455e56",width=3)
            d.ellipse((xx-7,y+23,xx+7,y+37),fill="#455e56")
        d.rounded_rectangle((cx-44,y+15,cx+44,y+45),radius=5,fill="#fffdf8",outline="#82968c")
        txt("AI",cx,y+30,16,"#477a68",True,"mm")
    elif kind == "tent":
        for xx in range(x+15,x+w-15,26):
            d.line((xx,y+11,xx-4,y+27),fill="#9bb8c3",width=2)
        d.polygon([(x+21,y+h-10),(cx,y+18),(x+w-21,y+h-10)],fill="#ae9d83")
        d.polygon([(cx,y+18),(cx,y+h-10),(x+w-21,y+h-10)],fill="#7d867e")
        d.ellipse((x+18,y+12,x+35,y+29),fill="#fffdf8")
    elif kind == "ships":
        d.rectangle((x+10,cy+13,x+w-10,y+h-8),fill="#7da3af")
        for xx in (x+39,cx+15,x+w-48):
            d.polygon([(xx-24,cy+8),(xx+24,cy+8),(xx+14,cy+21),(xx-17,cy+21)],fill="#344d5a")
            d.rectangle((xx-6,cy-12,xx+9,cy+7),fill="#f7f1e5")
        d.line((x+25,y+18,x+60,y+18),fill=RED,width=3)
        d.line((x+w-68,y+16,x+w-26,y+16),fill=RED,width=3)
    elif kind == "chart":
        d.rectangle((x+9,y+11,x+w-9,y+h-11),fill="#fffdf8",outline="#c9c2b5",width=2)
        d.line((x+17,y+h-22,x+35,y+h-34,x+52,y+h-29,x+71,y+28),fill=RED,width=3)
        d.polygon([(x+67,y+33),(x+71,y+23),(x+77,y+31)],fill=RED)
        txt("+6.5%",x+w-11,y+14,12,"#9a6a21",True,"ra")
    elif kind == "chip":
        # Recognisable square package with pins and a separate falling indicator.
        d.rounded_rectangle((cx-28,cy-27,cx+25,cy+26),radius=4,fill="#45718a")
        d.rectangle((cx-17,cy-16,cx+14,cy+15),fill="#dce8eb")
        txt("N",cx-1,cy,13,"#45718a",True,"mm")
        for p in (-18,-6,6,18):
            d.line((cx-38,cy+p,cx-28,cy+p),fill="#45718a",width=3)
            d.line((cx+25,cy+p,cx+35,cy+p),fill="#45718a",width=3)
        for p in (-18,-6,6,18):
            d.line((cx+p,cy-37,cx+p,cy-27),fill="#45718a",width=3)
            d.line((cx+p,cy+26,cx+p,cy+36),fill="#45718a",width=3)
        ax,ay=x+w-19,y+22
        d.line((ax,ay,ax,ay+22),fill=RED,width=3)
        d.polygon([(ax-6,ay+16),(ax+6,ay+16),(ax,ay+23)],fill=RED)
    elif kind == "smog":
        d.ellipse((x+w-43,y+12,x+w-18,y+37),fill="#dfa957")
        for xx, hh in ((x+17,37),(x+42,57),(x+73,44),(x+104,64),(x+137,40)):
            d.rectangle((xx,y+h-9-hh,xx+21,y+h-9),fill="#5a5049")
        for yy in (y+37,y+51,y+65):
            d.rectangle((x+5,yy,x+w-5,yy+9),fill="#ac9884")


def lead(x, y, w, h, number, region, headline, dek, kind):
    card((x,y,x+w,y+h))
    d.ellipse((x+12,y+12,x+38,y+38),fill=RED)
    txt(str(number),x+25,y+25,14,"white",True,"mm")
    tag(region,x+47,y+14,REGION[region],11)
    scene(kind,x+12,y+45,w-24,96)
    f=fit(headline,FONT_HEAD,22,17,w-24)
    d.text((x+12,y+148),headline,font=f,fill=INK)
    df=F(FONT_BODY,13)
    lines=wrap(dek,df,w-24)
    yy=y+180
    for ln in lines[:2]:
        d.text((x+12,yy),ln,font=df,fill=MUTED)
        yy+=17


def mini(x,y,w,h,region,headline,dek,kind):
    card((x,y,x+w,y+h),9)
    scene(kind,x+8,y+8,91,h-16)
    tag(region,x+108,y+9,REGION[region],10)
    f=fit(headline,FONT_HEAD,17,13,w-124)
    d.text((x+108,y+37),headline,font=f,fill=INK)
    df=F(FONT_BODY,12)
    lines=wrap(dek,df,w-124)
    yy=y+58
    max_lines=max(1,(h-62)//15)
    for ln in lines[:max_lines]:
        d.text((x+108,yy),ln,font=df,fill=MUTED)
        yy+=15


# Header establishes the day's identity and the page's editorial hierarchy.
txt("THE WORLD'S NEWS IN ONE PICTURE",34,18,17,RED,True)
date="FRIDAY 13 NOVEMBER 2026"
f=fit(date,FONT_HEAD,45,37,930)
d.text((32,41),date,font=f,fill=INK)
txt("19 STORIES  ·  5 CONTINENTS",990,104,14,MUTED,True,"ra")
d.line((32,132,992,132),fill=INK,width=2)

g=12
lead_y, lead_h = 145, 225
lead_w=(960-2*g)//3
lead(32,lead_y,lead_w,lead_h,1,"US","FAA GROUNDS EVERY US FLIGHT",
     "A telecom outage hit all 22 air route control centers; officials see no sign of cyberattack.","plane")
lead(32+lead_w+g,lead_y,lead_w,lead_h,2,"MIDDLE EAST","IRAN CLAIMS RADAR STRIKE IN BAHRAIN",
     "Guards claim radar destroyed; CENTCOM says two drones downed, no damage.","radar")
lead(32+2*(lead_w+g),lead_y,lead_w,lead_h,3,"WORLD","MICROSOFT OUTAGE HITS 74 COUNTRIES",
     "Millions lose Outlook, Teams and Copilot in a worldwide service disruption.","cloud")

# Six compact reports: two rows, consistent icon and text columns.
txt("THE DAY, ACROSS SIX MORE FRONTS",32,386,16,INK,True)
d.line((32,410,992,410),fill=RULE,width=1)
mini_w=(960-g*2)//3
mini_h=112
items=[
    ("EUROPE","KYIV HOSPITAL BURNS","Drone debris starts fire; 30 patients and staff evacuated.","fire"),
    ("EUROPE","EU LEADERS MEET IN DUBLIN","Informal summit focuses on AI and competitiveness.","summit"),
    ("GAZA","BABY DIES IN KHAN YOUNIS","9-month-old dies of cold in a tent; 49 nations urge aid","tent"),
    ("ASIA","100+ CHINESE SHIPS","Taiwan calls unannounced drills “silent intimidation.”","ships"),
    ("ECONOMY","WHOLESALE PRICES +6.5%","Largest annual rise since 2022; Fed hike bets grow.","chart"),
    ("TECH","NVIDIA'S HUANG TO TESTIFY","Quit Thursday; to testify to House. Kress interim CEO.","chip"),
]
for i,(r,h,dek,k) in enumerate(items):
    col=i%3; row=i//3
    mini(32+col*(mini_w+g),420+row*(mini_h+7),mini_w,mini_h,r,h,dek,k)

# South Asia gets a final compact visual alongside the same-day wire list.
txt("ALSO ON 13 NOVEMBER",32,657,16,RED,True)
d.line((32,682,992,682),fill=INK,width=1)
card((32,687,271,952),10)
scene("smog",43,698,217,88)
tag("SOUTH ASIA",44,798,REGION["SOUTH ASIA"],10)
f=fit("DELHI AIR TURNS DANGEROUS",FONT_HEAD,19,15,215)
d.text((44,827),"DELHI AIR TURNS DANGEROUS",font=f,fill=INK)
small_dek="AQI 334: world's most polluted major city, overtaking Lahore."
df=F(FONT_BODY,13)
for i,ln in enumerate(wrap(small_dek,df,211)[:3]):
    d.text((44,855+i*17),ln,font=df,fill=MUTED)

also=[
    ("AFRICA","Nairobi building under construction collapses; at least 6 dead"),
    ("CULTURE","Rosalía wins Latin Grammy album of the year for Lux"),
    ("US POLITICS","Mississippi gets its first Democratic senator since 1982: Scott Colom"),
    ("MIDDLE EAST","Iran says tanker hit a mine in the Strait of Hormuz"),
    ("EUROPE","Tuscany floods displace about 100 people"),
    ("MIDDLE EAST","Saudi air defences down Houthi drones over Riyadh"),
    ("ASIA","Pakistan van plunges into river; 11 dead in Gilgit-Baltistan"),
    ("EUROPE","Paris marks 11 years since the 13 November 2015 attacks"),
    ("TÜRKIYE","Military helicopter crash in Malatya kills 4"),
]
colx=(291,647)
for i,(region,story) in enumerate(also):
    col=i//5; row=i%5
    x=colx[col]; y=689+row*52
    # A compact colored region label reserves the same first line on every row.
    d.text((x,y),region,font=F(FONT_BODY,10),fill=REGION[region])
    f=fit(story,FONT_BODY,13,12,337)
    lines=wrap(story,f,337)
    for j,ln in enumerate(lines[:2]):
        d.text((x,y+14+j*15),ln,font=f,fill=INK)

d.line((32,967,992,967),fill=INK,width=1)
footer="All stories reported 13 Nov 2026 · Sources: AP · Reuters · Al Jazeera · CNBC · Xinhua · NPR · Democracy Now! · Kyiv Independent"
ff=fit(footer,FONT_BODY,13,12,960)
d.text((512,976),footer,font=ff,fill=MUTED,anchor="mt")

im.save(ROOT / "entry.png", "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
