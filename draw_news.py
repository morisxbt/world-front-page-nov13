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
        # Three large airport-board rows over a detailed parked airliner and runway.
        d.rounded_rectangle((x+8,y+2,x+w-8,y+59),radius=6,fill="#1d3444")
        rows=(("NEW YORK","CANCELLED"),("CHICAGO","DELAYED"),
              ("ATLANTA","CANCELLED"))
        for i,(city,status) in enumerate(rows):
            yy=y+8+i*15
            txt(city,x+20,yy,13,"#fff4d7",True)
            txt(status,x+134,yy,13,"#f4b54a" if status=="DELAYED" else "#ff7165",True)
            if i<len(rows)-1:
                d.line((x+15,yy+14,x+w-16,yy+14),fill="#405564",width=1)
        # Runway with dashed centreline; broad swept wings, fuselage, tail and windows.
        ry=y+h-12
        d.polygon([(x+71,ry-4),(x+w-12,ry-4),(x+w-3,ry+13),(x+60,ry+13)],fill="#c2c9c8")
        for dash in range(x+84,x+w-18,20):
            d.line((dash,ry+4,dash+8,ry+4),fill="#fffdf8",width=2)
        px=x+w-87; py=y+h-19
        d.polygon([(px-51,py-4),(px-8,py-7),(px+3,py-30),(px+11,py-30),(px+9,py-7),(px+26,py-7),(px+42,py-21),(px+48,py-20),(px+41,py-5),(px+59,py-3),(px+59,py+3),(px+11,py+5),(px+8,py+18),(px+2,py+18),(px+1,py+5),(px-51,py+3)],fill="#385c70")
        d.line((px-42,py-1,px+42,py-1),fill="#6e8996",width=2)
        for wx in range(px-29,px+27,10):
            d.ellipse((wx,py-2,wx+4,py+1),fill="#e6e5d9")
        d.ellipse((px-16,py+7,px-10,py+13),fill="#263b48")
        d.ellipse((px+22,py+7,px+28,py+13),fill="#263b48")
        d.ellipse((x+16,y+h-43,x+42,y+h-17),fill=RED)
        d.line((x+29,y+h-17,x+29,ry+2),fill="#667883",width=2)
        txt("STOP",x+29,y+h-30,8,"white",True,"mm")
    elif kind == "radar":
        # Bahrain flag, raised radar dome, and two intercepted drone paths.
        fx,fy=x+10,y+16
        d.rectangle((fx,fy,fx+41,fy+30),fill="#c43f40")
        d.rectangle((fx+15,fy,fx+41,fy+30),fill="white")
        for yy in range(fy,fy+30,6):
            d.polygon([(fx+15,yy),(fx+21,yy+3),(fx+15,yy+6)],fill="#c43f40")
        bx,by=cx+4,y+h-23
        # Elevated lattice tower and crisp white radome.
        d.rectangle((bx-39,by-33,bx+38,by-5),fill="#bac7ca")
        d.pieslice((bx-34,by-64,bx+34,by+3),180,360,fill="#fffdf8",outline="#426071",width=3)
        d.line((bx-39,by-5,bx-50,by+21),fill="#657b84",width=3)
        d.line((bx+38,by-5,bx+50,by+21),fill="#657b84",width=3)
        d.line((bx-50,by+21,bx+50,by+21),fill="#657b84",width=3)
        for yy in (by+1,by+9,by+17):
            d.line((bx-47,yy,bx+47,yy-8),fill="#81949a",width=2)
            d.line((bx+47,yy,bx-47,yy-8),fill="#81949a",width=2)
        # Dotted trails terminate at small burst marks above the radar.
        for points in (((x+w-17,y+12),(x+w-59,y+25),(x+w-101,y+18)),
                       ((x+w-20,y+38),(x+w-71,y+49),(x+w-112,y+43))):
            dx0,dy0=points[0]
            d.line((dx0-8,dy0,dx0+8,dy0),fill="#526977",width=2)
            d.line((dx0,dy0-5,dx0,dy0+5),fill="#526977",width=2)
            d.ellipse((dx0-3,dy0-3,dx0+3,dy0+3),fill="#405968")
            for ax,ay in points:
                d.ellipse((ax-2,ay-2,ax+2,ay+2),fill=RED)
            ex,ey=points[-1]
            for dx,dy in ((-5,0),(5,0),(0,-5),(0,5)):
                d.line((ex+dx//2,ey+dy//2,ex+dx,ey+dy),fill="#e7a34d",width=2)
            d.polygon([(ex-5,ey-2),(ex+2,ey-5),(ex+5,ey+2),(ex-2,ey+5)],fill=RED)
    elif kind == "cloud":
        # Globe behind a laptop; screen shows mail failure and a Teams-like bubble.
        gx,gy=x+57,y+42
        d.ellipse((gx-44,gy-43,gx+44,gy+45),fill="#d8e7e9")
        d.ellipse((gx-39,gy-39,gx+39,gy+41),fill="#a9c8d1",outline="#507d91",width=3)
        d.arc((gx-22,gy-39,gx+22,gy+41),90,270,fill="#507d91",width=2)
        d.arc((gx-22,gy-39,gx+22,gy+41),270,90,fill="#507d91",width=2)
        d.arc((gx-39,gy-19,gx+39,gy+19),180,360,fill="#507d91",width=2)
        d.arc((gx-39,gy-19,gx+39,gy+19),0,180,fill="#507d91",width=2)
        lx,ly=x+111,y+22
        d.rounded_rectangle((lx+3,ly+4,lx+130,ly+65),radius=7,fill="#263c49")
        d.rounded_rectangle((lx,ly,lx+126,ly+61),radius=6,fill="#354f60",outline="#253b49",width=2)
        d.rectangle((lx+7,ly+7,lx+119,ly+51),fill="#a9c6cf")
        d.rectangle((lx+7,ly+40,lx+119,ly+51),fill="#7fa3b1")
        d.rectangle((lx+24,ly+17,lx+76,ly+44),fill="white")
        d.line((lx+24,ly+17,lx+50,ly+33,lx+76,ly+17),fill="#567788",width=2)
        d.line((lx+61,ly+16,lx+79,ly+34),fill=RED,width=5)
        d.line((lx+79,ly+16,lx+61,ly+34),fill=RED,width=5)
        d.polygon([(lx+47,ly+61),(lx+145,ly+61),(lx+131,ly+68),(lx+36,ly+68)],fill="#607986")
        d.rounded_rectangle((x+w-53,y+5,x+w-14,y+37),radius=8,fill="#7652a5")
        d.polygon([(x+w-42,y+35),(x+w-47,y+44),(x+w-31,y+36)],fill="#7652a5")
        txt("T",x+w-33,y+20,16,"white",True,"mm")
    elif kind == "fire":
        # Three-tone hospital block, red cross, and fire through an upper window.
        d.rectangle((x+13,y+29,x+73,y+h-10),fill="#cad5d9")
        d.rectangle((x+19,y+34,x+31,y+h-10),fill="#e3e9e8")
        d.rectangle((x+34,y+37,x+69,y+h-10),fill="#b6c5ca")
        for yy in (y+48,y+65,y+82):
            for xx in (x+21,x+41,x+57):
                d.rectangle((xx,yy,xx+8,yy+7),fill="#65889a")
                d.line((xx+4,yy,xx+4,yy+7),fill="#dce6e7",width=1)
        d.rectangle((x+31,y+13,x+53,y+35),fill="#fffdf8")
        d.rectangle((x+38,y+16,x+46,y+32),fill=RED)
        d.rectangle((x+34,y+20,x+50,y+28),fill=RED)
        # A bright window and a contained pair of flame tongues.
        d.rectangle((x+56,y+47,x+69,y+62),fill="#ffd37a")
        fx=x+67
        d.polygon([(fx-13,y+70),(fx-11,y+53),(fx-5,y+61),(fx,y+44),(fx+6,y+56),(fx+9,y+70)],fill="#d94e36")
        d.polygon([(fx-7,y+70),(fx-4,y+60),(fx,y+65),(fx+4,y+54),(fx+7,y+70)],fill="#ffbd52")
    elif kind == "summit":
        # Twelve gold stars encircle an AI placard above a round summit table.
        sx,sy=cx,y+38
        for n in range(12):
            import math
            a=math.radians(n*30-90)
            px=sx+math.cos(a)*29; py=sy+math.sin(a)*27
            d.ellipse((px-2.2,py-2.2,px+2.2,py+2.2),fill="#d8a73e")
        d.rounded_rectangle((cx-20,y+26,cx+20,y+49),radius=4,fill="#fffdf8",outline="#82968c",width=2)
        txt("AI",cx,y+38,13,"#477a68",True,"mm")
        d.ellipse((x+14,y+61,x+w-14,y+79),fill="#53796c")
        d.ellipse((x+19,y+62,x+w-19,y+73),fill="#79a08e")
        d.line((cx-22,y+75,cx-27,y+90),fill="#455e56",width=3)
        d.line((cx+22,y+75,cx+27,y+90),fill="#455e56",width=3)
    elif kind == "tent":
        # Rainy shelter, open flap and a small heart-marked baby blanket.
        for xx in range(x+10,x+w-8,18):
            d.line((xx,y+8,xx-5,y+19),fill="#92b3c1",width=2)
            d.ellipse((xx-2,y+18,xx+1,y+21),fill="#92b3c1")
        d.polygon([(x+8,y+h-8),(cx,y+26),(x+w-8,y+h-8)],fill="#b7a48a")
        d.polygon([(cx,y+26),(cx,y+h-8),(x+w-8,y+h-8)],fill="#827c70")
        d.polygon([(cx,y+39),(cx-19,y+h-8),(cx+5,y+h-8)],fill="#534f4a")
        d.rounded_rectangle((cx+11,y+59,cx+39,y+76),radius=3,fill="#e7d9bf")
        d.polygon([(cx+19,y+64),(cx+23,y+60),(cx+27,y+64),(cx+31,y+60),(cx+35,y+64),(cx+27,y+72)],fill=RED)
    elif kind == "ships":
        d.rectangle((x+5,y+43,x+w-5,y+h-7),fill="#91afba")
        # Island in the centre, surrounded by three grey patrol ships.
        d.polygon([(cx-17,y+40),(cx-7,y+30),(cx+8,y+33),(cx+20,y+42),(cx+12,y+48),(cx-9,y+47)],fill="#91a184",outline="#677d72")
        for xx,yy,scale in ((x+22,y+57,0),(x+w-24,y+57,0),(cx,y+79,1)):
            hull=[(xx-18,yy),(xx+18,yy),(xx+12,yy+8),(xx-13,yy+8)]
            d.polygon(hull,fill="#4d5d65",outline="#35454d")
            d.rectangle((xx-5,yy-8,xx+7,yy),fill="#d5d9d6")
            d.line((xx,yy-8,xx,yy-15),fill="#4d5d65",width=2)
    elif kind == "chart":
        d.rounded_rectangle((x+7,y+9,x+w-7,y+h-9),radius=4,fill="#fffdf8",outline="#c9c2b5",width=2)
        for yy in (y+36,y+57,y+78):
            d.line((x+14,yy,x+w-14,yy),fill="#e5e1d8",width=1)
        d.line((x+13,y+h-20,x+32,y+h-36,x+50,y+h-31,x+76,y+34),fill="#bf4037",width=4)
        d.polygon([(x+70,y+39),(x+76,y+28),(x+81,y+38)],fill="#bf4037")
        d.rounded_rectangle((x+12,y+13,x+67,y+31),radius=4,fill="#f3e4b9")
        txt("+6.5%",x+39,y+22,12,"#946820",True,"mm")
    elif kind == "chip":
        # Recognisable square package with pins and a separate falling indicator.
        d.rounded_rectangle((cx-28,cy-27,cx+25,cy+26),radius=4,fill="#34795d")
        d.rectangle((cx-17,cy-16,cx+14,cy+15),fill="#dce8eb")
        d.rectangle((cx-13,cy-12,cx+10,cy+11),fill="#a7cbb4")
        txt("N",cx-1,cy,13,"#34795d",True,"mm")
        for p in (-18,-6,6,18):
            d.line((cx-38,cy+p,cx-28,cy+p),fill="#34795d",width=3)
            d.line((cx+25,cy+p,cx+35,cy+p),fill="#34795d",width=3)
        for p in (-18,-6,6,18):
            d.line((cx+p,cy-37,cx+p,cy-27),fill="#34795d",width=3)
            d.line((cx+p,cy+26,cx+p,cy+36),fill="#34795d",width=3)
        ax,ay=x+w-10,y+8
        d.line((ax,ay,ax,ay+20),fill=RED,width=3)
        d.polygon([(ax-6,ay+14),(ax+6,ay+14),(ax,ay+21)],fill=RED)
    elif kind == "smog":
        d.ellipse((x+w-43,y+12,x+w-18,y+37),fill="#dfa957")
        for xx, hh in ((x+17,37),(x+42,57),(x+73,44),(x+104,64),(x+137,40)):
            d.rectangle((xx,y+h-9-hh,xx+21,y+h-9),fill="#5a5049")
            d.rectangle((xx+4,y+h-9-hh+12,xx+8,y+h-9-hh+17),fill="#b49c7e")
            d.rectangle((xx+13,y+h-9-hh+23,xx+17,y+h-9-hh+28),fill="#b49c7e")
        for yy in (y+37,y+51,y+65):
            d.rectangle((x+5,yy,x+w-5,yy+9),fill="#ac9884")
        if w>100:
            d.rounded_rectangle((x+8,y+7,x+81,y+29),radius=5,fill="#44535a")
            txt("AQI 334",x+44,y+18,12,"white",True,"mm")


def lead(x, y, w, h, number, region, headline, dek, kind):
    card((x,y,x+w,y+h))
    d.ellipse((x+12,y+12,x+38,y+38),fill=RED)
    txt(str(number),x+25,y+25,14,"white",True,"mm")
    tag(region,x+47,y+14,REGION[region],11)
    scene(kind,x+12,y+43,w-24,110)
    f=fit(headline,FONT_HEAD,22,17,w-24)
    d.text((x+12,y+162),headline,font=f,fill=INK)
    df=F(FONT_BODY,13)
    lines=wrap(dek,df,w-24)
    yy=y+193
    for ln in lines[:2]:
        d.text((x+12,yy),ln,font=df,fill=MUTED)
        yy+=17


def mini(x,y,w,h,region,headline,dek,kind):
    card((x,y,x+w,y+h),9)
    scene(kind,x+8,y+8,91,h-16)
    tag(region,x+108,y+9,REGION[region],10)
    f=fit(headline,FONT_HEAD,17,13,w-124)
    d.text((x+108,y+37),headline,font=f,fill=INK)
    df=F(FONT_BODY,13)
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
lead_y, lead_h = 145, 239
lead_w=(960-2*g)//3
lead(32,lead_y,lead_w,lead_h,1,"US","FAA GROUNDS EVERY US FLIGHT",
     "A telecom outage hit all 22 air route control centers; officials see no sign of cyberattack.","plane")
lead(32+lead_w+g,lead_y,lead_w,lead_h,2,"MIDDLE EAST","IRAN CLAIMS RADAR STRIKE IN BAHRAIN",
     "Guards claim radar destroyed; CENTCOM says two drones downed, no damage.","radar")
lead(32+2*(lead_w+g),lead_y,lead_w,lead_h,3,"WORLD","MICROSOFT OUTAGE HITS 74 COUNTRIES",
     "Millions lose Outlook, Teams and Copilot in a worldwide service disruption.","cloud")

# Six compact reports: two rows, consistent icon and text columns.
txt("THE DAY, ACROSS SIX MORE FRONTS",32,400,16,INK,True)
d.line((32,424,992,424),fill=RULE,width=1)
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
    mini(32+col*(mini_w+g),432+row*(mini_h+7),mini_w,mini_h,r,h,dek,k)

# South Asia gets a final compact visual alongside the same-day wire list.
txt("ALSO ON 13 NOVEMBER",32,668,16,RED,True)
d.line((32,693,992,693),fill=INK,width=1)
card((32,698,271,963),10)
scene("smog",43,709,217,88)
tag("SOUTH ASIA",44,809,REGION["SOUTH ASIA"],10)
f=fit("DELHI AIR TURNS DANGEROUS",FONT_HEAD,19,15,215)
d.text((44,838),"DELHI AIR TURNS DANGEROUS",font=f,fill=INK)
small_dek="AQI 334: world's most polluted major city, overtaking Lahore."
df=F(FONT_BODY,13)
for i,ln in enumerate(wrap(small_dek,df,211)[:3]):
    d.text((44,866+i*17),ln,font=df,fill=MUTED)

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
    x=colx[col]; y=698+row*56
    # A compact colored region label reserves the same first line on every row.
    d.text((x,y),region,font=F(FONT_BODY,13),fill=REGION[region])
    f=fit(story,FONT_BODY,13,13,337)
    lines=wrap(story,f,337)
    for j,ln in enumerate(lines[:2]):
        d.text((x,y+17+j*15),ln,font=f,fill=INK)

d.line((32,978,992,978),fill=INK,width=1)
footer="All stories reported 13 Nov 2026 · Sources: AP · Reuters · Al Jazeera · CNBC · Xinhua · NPR · Democracy Now! · Kyiv Independent"
ff=fit(footer,FONT_BODY,13,12,960)
d.text((512,986),footer,font=ff,fill=MUTED,anchor="mt")

im.save(ROOT / "entry.png", "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
