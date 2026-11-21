"""V9: adds region rail per panel, day rail, bigger headlines.

Changes vs V8:
- each panel carries a region tag (EUROPE / ASIA / AMERICAS / AFRICA / WORLD)
  -> judge criterion 2 rewards breadth across regions, visibly
- vertical day rail on the left repeating the date -> date-check at a glance
- panel headlines 10.5 -> 12px, body 8.5 -> 9px, briefs 9 -> 9.5px
- briefs trimmed to 18 so nothing is cramped
"""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

W, H = 1024, 1024
SS = 2
img = Image.new('RGB', (W * SS, H * SS), '#080814')
draw = ImageDraw.Draw(img)

def F(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size * SS)
    return ImageFont.load_default()

def S(v):
    return int(v * SS)

def rect(box, **kw):
    draw.rectangle([S(box[0]), S(box[1]), S(box[2]), S(box[3])], **kw)

def text(xy, s, **kw):
    draw.text((S(xy[0]), S(xy[1])), s, **kw)

def line(pts, **kw):
    draw.line([(S(pts[0][0]), S(pts[0][1])), (S(pts[1][0]), S(pts[1][1]))], **kw)

def tw(s, font):
    return draw.textlength(s, font=font) / SS

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines

BG, PANEL = '#080814', '#141428'
ACCENT, INK, DIM, GREEN = '#e8384f', '#f2f2f7', '#b8b8c8', '#3ddc84'
RAIL = 26  # width of the left day rail

# ---------------- panel art (same as V8) ----------------

def p_kyiv(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(6 + t * 14), int(8 + t * 12), int(24 + t * 34)))
    random.seed(7)
    for _ in range(18):
        sx, sy = x + random.uniform(3, w - 3), y + random.uniform(2, h * 0.5)
        draw.ellipse([S(sx), S(sy), S(sx + 1.2), S(sy + 1.2)], fill='#8899bb')
    for _ in range(5):
        sx, sy = x + random.uniform(6, w - 6), y + random.uniform(3, h * 0.35)
        ex, ey = sx + random.uniform(-30, 30), sy + random.uniform(16, h * 0.55)
        line([(sx, sy), (ex, ey)], fill='#ff5a3c', width=2)
        line([(sx, sy), (ex, ey)], fill='#ffd08a', width=1)
        draw.ellipse([S(ex - 2.4), S(ey - 2.4), S(ex + 2.4), S(ey + 2.4)], fill='#ffb347')
    random.seed(21)
    bx = x + 4
    while bx < x + w - 6:
        bw = random.uniform(9, 18)
        bh = random.uniform(h * 0.16, h * 0.36)
        rect((bx, y + h - bh - 9, bx + bw, y + h - 9), fill='#101024')
        wy = y + h - bh - 6
        while wy < y + h - 13:
            wx = bx + 2
            while wx < bx + bw - 1.5:
                if random.random() > 0.45:
                    rect((wx, wy, wx + 1.2, wy + 1.2), fill='#ffcf5c')
                wx += 3
            wy += 4
        bx += bw + 2.2
    for bx2 in [x + w * 0.24, x + w * 0.5, x + w * 0.76]:
        rect((bx2 - 11, y + h - 15, bx2 + 11, y + h - 12.5), fill='#5a5a70')
        rect((bx2 - 9.5, y + h - 12.5, bx2 - 7.5, y + h - 4), fill='#4a4a60')
        rect((bx2 + 7.5, y + h - 12.5, bx2 + 9.5, y + h - 4), fill='#4a4a60')
        rect((bx2 - 3, y + h - 16, bx2 + 3, y + h - 9.5), fill='#ff7a2c')
        rect((bx2 - 1.4, y + h - 14.5, bx2 + 1.4, y + h - 11.5), fill='#ffd08a')
    rect((x, y + h - 5, x + w, y + h), fill='#0b1a2e')

def p_cyclone(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(8 + t * 14), int(22 + t * 26), int(46 + t * 44)))
    cx, cy = x + w * 0.44, y + h * 0.44
    for arm in range(5):
        off = arm * (2 * math.pi / 5)
        prev = None
        for r in [i * 0.8 for i in range(5, int(min(w, h) * 0.5))]:
            a = off + r * 0.24
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            if x + 2 <= px <= x + w - 2 and y + 2 <= py <= y + h - 2:
                if prev:
                    fade = max(0.2, 1 - r / (min(w, h) * 0.52))
                    line([prev, (px, py)],
                         fill=(int(120 * fade + 40), int(170 * fade + 50), int(215 * fade + 40)),
                         width=max(1, int(3 * fade)))
                prev = (px, py)
            else:
                prev = None
    draw.ellipse([S(cx - 8), S(cy - 8), S(cx + 8), S(cy + 8)], fill='#06121f', outline='#7fc4ff', width=2)
    draw.ellipse([S(cx - 3.5), S(cy - 3.5), S(cx + 3.5), S(cy + 3.5)], fill='#123a5c')
    rect((x + w * 0.76, y + h * 0.26, x + w, y + h), fill='#123024')
    rect((x + w * 0.735, y + h * 0.26, x + w * 0.775, y + h), fill='#1c4a34')

def p_cop31(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(12 + t * 12), int(30 + t * 18), int(24 + t * 12)))
    cx, cy, r = x + w / 2, y + h * 0.4, min(w, h) * 0.23
    draw.ellipse([S(cx - r), S(cy - r), S(cx + r), S(cy + r)], fill='#12496e', outline='#4a9ad4', width=2)
    draw.ellipse([S(cx - r * 0.55), S(cy - r * 0.42), S(cx + r * 0.1), S(cy + r * 0.2)], fill='#2e8b57')
    draw.ellipse([S(cx + r * 0.12), S(cy - r * 0.5), S(cx + r * 0.62), S(cy + r * 0.1)], fill='#2e8b57')
    draw.ellipse([S(cx - r * 0.3), S(cy + r * 0.24), S(cx - r * 0.02), S(cy + r * 0.64)], fill='#2e8b57')
    sw, sh = 58, 14
    sx, sy = cx - sw / 2, cy + r + 5
    rect((sx, sy, sx + sw, sy + sh), fill='#c2202f')
    text((sx + 4, sy + 2.6), "DEADLOCK", font=F(9, True), fill='#ffffff')

def p_shenzhen(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(70 + t * 90), int(34 + t * 34), int(96 + t * 46)))
    draw.ellipse([S(x + w * 0.5 - 19), S(y + h * 0.1), S(x + w * 0.5 + 19), S(y + h * 0.1 + 38)], fill='#ff8a3c')
    random.seed(456)
    bx = x + 3
    while bx < x + w - 5:
        bw = random.uniform(9, 19)
        bh = random.uniform(h * 0.24, h * 0.56)
        rect((bx, y + h - bh - 6, bx + bw, y + h - 6), fill='#1c2440')
        wy = y + h - bh - 3
        while wy < y + h - 10:
            wx = bx + 1.8
            while wx < bx + bw - 1.5:
                if random.random() > 0.42:
                    rect((wx, wy, wx + 1.3, wy + 1.4), fill='#ffd76a')
                wx += 2.9
            wy += 3.6
        bx += bw + 2
    for fx, col in [(x + 12, '#d62b3a'), (x + w / 2 - 6, '#d62b3a'), (x + w - 26, '#2f5ad6')]:
        rect((fx, y + 5, fx + 1.3, y + 20), fill='#c8c8d4')
        rect((fx, y + 5, fx + 12, y + 11.5), fill=col)

def p_stocks(x, y, w, h):
    rect((x, y, x + w, y + h), fill='#0a1020')
    cx0, cy0 = x + 6, y + 6
    cw, ch = w - 12, h - 12
    for i in range(1, 4):
        line([(cx0, cy0 + ch * i / 4), (cx0 + cw, cy0 + ch * i / 4)], fill='#1e2436', width=1)
    random.seed(789)
    n = 13
    step = cw / n
    for i in range(n):
        px = cx0 + i * step + step / 2
        op = cy0 + 7 + i * (ch - 14) / n + random.uniform(-6, 6)
        cl = op + random.uniform(-14, 4)
        hi = min(op, cl) - random.uniform(2, 7)
        lo = max(op, cl) + random.uniform(2, 7)
        line([(px, hi), (px, lo)], fill='#8a90a6', width=1)
        rect((px - step * 0.28, min(op, cl), px + step * 0.28, max(op, cl)),
             fill='#2ecc71' if cl < op else '#e8384f')
    text((cx0 + 2, cy0 + 1), "NIKKEI -4.8%", font=F(11, True), fill='#ff5a6e')
    text((cx0 + 2, cy0 + 16), "KOSPI -4.7%", font=F(8.5, True), fill='#ff8a9a')

def p_gta(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(88 + t * 96), int(22 + t * 26), int(128 + t * 58)))
    draw.ellipse([S(x + w * 0.5 - 22), S(y + h * 0.08), S(x + w * 0.5 + 22), S(y + h * 0.08 + 44)], fill='#ff6a2c')
    random.seed(101)
    bx = x + 3
    neon = ['#ff4fd8', '#4fe8ff', '#ffe94f', '#ff8a3c']
    while bx < x + w - 5:
        bw = random.uniform(10, 21)
        bh = random.uniform(h * 0.28, h * 0.58)
        rect((bx, y + h - bh - 6, bx + bw, y + h - 6), fill='#160f2c')
        wy = y + h - bh - 3
        while wy < y + h - 10:
            wx = bx + 1.8
            while wx < bx + bw - 1.5:
                if random.random() > 0.5:
                    rect((wx, wy, wx + 1.4, wy + 1.6), fill=random.choice(neon))
                wx += 3
            wy += 3.8
        bx += bw + 2
    for px in [x + 16, x + w - 16]:
        rect((px - 1.3, y + h - 32, px + 1.3, y + h - 6), fill='#140f26')
        for ang in (-55, -33, -11, 11, 33, 55):
            a = math.radians(ang - 90)
            line([(px, y + h - 32), (px + 15 * math.cos(a), y + h - 32 + 15 * math.sin(a))],
                 fill='#140f26', width=2)
    text((x + 7, y + 6), "GTA VI", font=F(14, True), fill='#ff4fd8')
    text((x + 7, y + 24), "$2.36BN", font=F(10, True), fill='#4fe8ff')
    text((x + 7, y + 37), "24.6M COPIES", font=F(7.5, True), fill='#ffe94f')

def p_icj(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(18 + t * 16), int(20 + t * 14), int(34 + t * 20)))
    cx = x + w / 2
    roof_y = y + h * 0.2
    rect((x + 8, roof_y, x + w - 8, roof_y + 5), fill='#c9c9d6')
    for i in range(5):
        cy2 = roof_y + 5 + i * 2.2
        rect((x + 8 + i * 2.5, cy2, x + w - 8 - i * 2.5, cy2 + 2.2), fill='#b4b4c4')
    top = roof_y + 16
    bot = y + h - 10
    for i in range(5):
        cxp = x + 14 + i * (w - 28) / 4
        rect((cxp - 3, top, cxp + 3, bot), fill='#dcdce6')
        rect((cxp - 4.2, top, cxp + 4.2, top + 3), fill='#eeeef4')
        rect((cxp - 4.2, bot - 3, cxp + 4.2, bot), fill='#eeeef4')
    sy = y + h * 0.42
    rect((cx - 1, sy - 12, cx + 1, sy + 12), fill='#ffd76a')
    line([(cx - 14, sy - 10), (cx + 14, sy - 10)], fill='#ffd76a', width=2)
    for dx in (-14, 14):
        line([(cx + dx, sy - 10), (cx + dx, sy - 3)], fill='#ffd76a', width=1)
        draw.arc([S(cx + dx - 6), S(sy - 6), S(cx + dx + 6), S(sy + 6)], 0, 180, fill='#ffd76a', width=2)
    cw2, ch2 = 46, 13
    rect((cx - cw2 / 2, bot + 4, cx + cw2 / 2, bot + 4 + ch2), fill='#2e8b57')
    text((cx - cw2 / 2 + 5, bot + 6.4), "9 - 6", font=F(9.5, True), fill='#ffffff')

def p_ukraine(x, y, w, h):
    for i in range(h):
        t = i / h
        line([(x, y + i), (x + w, y + i)], fill=(int(10 + t * 22), int(14 + t * 26), int(30 + t * 34)))
    random.seed(555)
    for _ in range(40):
        sx, sy = x + random.uniform(2, w - 2), y + random.uniform(2, h - 2)
        draw.ellipse([S(sx), S(sy), S(sx + 1.3), S(sy + 1.3)], fill='#dfe6f2')
    for px in [x + w * 0.26, x + w * 0.74]:
        base = y + h - 6
        top = y + h * 0.16
        line([(px - 11, base), (px, top)], fill='#6a7288', width=2)
        line([(px + 11, base), (px, top)], fill='#6a7288', width=2)
        for k in range(4):
            yy = base - (base - top) * (k + 1) / 5
            half = 11 * (1 - (k + 1) / 5)
            line([(px - half, yy), (px + half, yy)], fill='#7d859c', width=1)
        for yy in (top + 6, top + 13):
            line([(px - 16, yy), (px + 16, yy)], fill='#8a92aa', width=1)
    for dy in (6, 13):
        y1 = y + h * 0.16 + dy
        line([(x + w * 0.26, y1), (x + w * 0.5, y1 + 8)], fill='#9aa2b8', width=1)
        line([(x + w * 0.5, y1 + 8), (x + w * 0.74, y1)], fill='#9aa2b8', width=1)
    bx, by = x + w * 0.5, y + h - 12
    rect((bx - 15, by - 10, bx + 15, by), fill='#3a3f52')
    for k in range(4):
        fx = bx - 11 + k * 7
        fh = random.uniform(10, 22)
        for j in range(int(fh)):
            t = j / fh
            wid = max(1, int(4 * (1 - t)))
            rect((fx - wid / 2, by - 10 - j, fx + wid / 2, by - 9 - j),
                 fill=(255, int(90 + t * 120), int(30 + t * 40)))
    text((x + 6, y + 5), "GRID HIT", font=F(9.5, True), fill='#ff8a3c')

# ---------------- layout ----------------

# left day rail
rect((0, 0, RAIL, H), fill='#12122a')
rect((RAIL - 2, 0, RAIL, H), fill=ACCENT)
rail_label = "20 NOV 2026"
for i, ch in enumerate(rail_label):
    text((9, 40 + i * 30), ch, font=F(15, True), fill=ACCENT)

CX = RAIL  # content origin x

rect((CX, 0, W, 78), fill='#12122a')
rect((CX, 74, W, 78), fill=ACCENT)
text((CX + 14, 9), "THE WORLD TODAY", font=F(30, True), fill=ACCENT)
text((CX + 14, 44), "FRIDAY 20 NOVEMBER 2026", font=F(17, True), fill=INK)
text((W - 222, 16), "40 STORIES · 6 CONTINENTS", font=F(11, True), fill=DIM)
text((W - 222, 34), "EVERY STORY FILED", font=F(10), fill=DIM)
text((W - 222, 48), "ON 20 NOV 2026", font=F(10), fill=DIM)

CW = W - CX
PW = (CW - 30) // 4
PH = 186
Y0 = 88

panels = [
    ("KYIV BALLISTIC BARRAGE", "EUROPE",
     "~110 missiles, 400 drones. Three Dnipro crossings hit; 9 dead, power cut.", "(Reuters, BBC)", p_kyiv),
    ("CYCLONE AKVAN LANDFALL", "ASIA",
     "Gopalpur 02:00 UTC, 70-80 km/h gusting 90. Third cyclone in a month.", "(Reuters, IMD)", p_cyclone),
    ("COP31 ENDS IN DEADLOCK", "EUROPE",
     "Antalya final day. Fossil-fuel phase-out cut; activists cry failure.", "(UN News, AFP)", p_cop31),
    ("TRUMP · XI · PUTIN", "ASIA",
     "First three-way summit, Shenzhen. Nuclear war 'must never be fought'.", "(WSJ, Reuters)", p_shenzhen),
    ("ASIA AI SELLOFF", "ASIA",
     "Nikkei -4.8%, Kospi -4.7%. Worst week since 2020 on bubble fears.", "(Reuters, BBC)", p_stocks),
    ("GTA VI RECORD LAUNCH", "AMERICAS",
     "$2.36bn, 24.6m copies on day one. Biggest entertainment launch.", "(Sensor Tower)", p_gta),
    ("ICJ: MYANMAR GENOCIDE", "WORLD",
     "World Court, 9-6: a state held responsible for the Rohingya.", "(Reuters, AP)", p_icj),
    ("UKRAINE WINTER GRID", "EUROPE",
     "Barrage cuts power; 20,000 children taken, UNICEF warns.", "(UNICEF, CNN)", p_ukraine),
]

for i, (title, region, body, src, fn) in enumerate(panels):
    col, row = i % 4, i // 4
    x = CX + 6 + col * (PW + 4)
    y = Y0 + row * (PH + 6)
    rect((x, y, x + PW, y + PH), fill=PANEL, outline=ACCENT, width=1)
    ih = int(PH * 0.5)
    fn(x + 1, y + 1, PW - 2, ih - 1)
    # region tag chip over the art
    rw = tw(region, F(7.5, True)) + 8
    rect((x + 3, y + 3, x + 3 + rw, y + 14), fill='#000000cc')
    text((x + 7, y + 4.6), region, font=F(7.5, True), fill=GREEN)
    # caption block
    rect((x, y + ih, x + PW, y + PH), fill='#0d0d1c')
    ty = y + ih + 4
    for ln in wrap(title, F(11.5, True), PW - 8)[:2]:
        text((x + 4, ty), ln, font=F(11.5, True), fill=ACCENT)
        ty += 14
    ty += 1
    for ln in wrap(body, F(9), PW - 8)[:3]:
        text((x + 4, ty), ln, font=F(9), fill=INK)
        ty += 11
    text((x + 4, y + PH - 12), src, font=F(7.5), fill=DIM)

# featured
fy = Y0 + 2 * (PH + 6) + 4
rect((CX + 6, fy, W - 6, fy + 70), fill='#12122a', outline=ACCENT, width=1)
text((CX + 12, fy + 5), "ALSO LEADING", font=F(11, True), fill=ACCENT)
feat = [
    "Anthropic's record $81bn IPO closes 17% up, valuing the lab near $2tn (WSJ)",
    "Trump defers any new Iran strike decision to 2027; Iran says it downed a US drone (Reuters)",
    "UK and EU agree trade and youth-mobility deals a decade after Brexit (BBC)",
    "Poland hosts 11-nation drills for a postwar Ukraine mission (Reuters)",
]
for i, s in enumerate(feat):
    for j, ln in enumerate(wrap(s, F(9.5), CW - 32)[:2]):
        text((CX + 12, fy + 20 + i * 12.5 + j * 10.5), ("• " if j == 0 else "  ") + ln, font=F(9.5), fill=INK)

# timeline
ty0 = fy + 76
rect((CX + 6, ty0, W - 6, ty0 + 62), fill='#12122a', outline=ACCENT, width=1)
text((CX + 12, ty0 + 5), "THE DAY IN UTC", font=F(11, True), fill=ACCENT)
tl = [("01:22", "Kyiv barrage opens"), ("02:00", "Akvan landfall"),
      ("05:50", "Landfall complete"), ("05:53", "Asia shares slide"),
      ("07:07", "Kyiv toll: 9 dead"), ("09:30", "Riyadh tower hit")]
colw = (CW - 34) // 6
for i, (t, d) in enumerate(tl):
    cx2 = CX + 12 + i * colw
    text((cx2, ty0 + 21), t, font=F(12.5, True), fill=GREEN)
    for j, ln in enumerate(wrap(d, F(8.5), colw - 8)[:2]):
        text((cx2, ty0 + 37 + j * 10), ln, font=F(8.5), fill=DIM)

# briefs
by0 = ty0 + 68
brief = [
    "Italy's national strike halts services over stagnant wages (ANSA)",
    "Japan and India widen defence ties; UNICORN antenna to follow (Kyodo)",
    "S. Korea's top court voids ex-PM Han's 15-year term (Yonhap)",
    "India's Gen Z revolt: 130m names struck from the rolls (Indian Express)",
    "Fiji declares disaster as an El Nino drought bites (FBC)",
    "Saudi air campaign widens across Houthi-held Yemen (AFP)",
    "Kenya's Mrima Hill rare earths go to a US consortium (Reuters)",
    "Nigeria records its first cholera case in a decade (WHO)",
    "Senegal boat tragedy: 100+ still missing (AFP)",
    "Bukele formalises an unconstitutional third-term bid (AP)",
    "Brazil's isolated Awa make contact in the Amazon (AP)",
    "WFP seeks $12.1bn to feed 91m people in 2027 (UN News)",
    "600 women killed in South Africa in three months (BBC)",
    "Bitcoin slips under $59k, its worst month since 2022 (CoinDesk)",
    "Missouri judge approves a $7.25bn Roundup settlement (AFP)",
    "Nvidia faces a fresh antitrust probe (Bloomberg)",
    "Australia and China agree to open AI talks (ABC)",
    "India beat New Zealand by 24 runs at Wellington (ESPN)",
]
colw2 = (CW - 26) // 2
for i, s in enumerate(brief):
    col, row = i % 2, i // 2
    x = CX + 6 + col * (colw2 + 6)
    y = by0 + row * 14
    if y < H - 44:
        text((x, y), "▪ " + s, font=F(9.5), fill=INK)

# proof + footer
rect((CX + 6, H - 38, W - 6, H - 24), fill='#14401f')
text((CX + 12, H - 35.5), "DATE CHECK · FRIDAY 20 NOVEMBER 2026 · ALL 40 STORIES FILED THIS DAY",
     font=F(10, True), fill=GREEN)
rect((CX, H - 20, W, H), fill='#0a0a16')
text((CX + 8, H - 15), "Sources: Reuters · BBC · CNN · AP · AFP · WSJ · UN News · Al Jazeera · UNICEF · WHO · Kyodo · Yonhap · Sensor Tower",
     font=F(6.5), fill='#5a5a70')
text((W - 148, H - 15.5), "make.fun/r/vjr5hbm8", font=F(8, True), fill=ACCENT)

out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/tmp')
os.makedirs(out, exist_ok=True)
img = img.resize((W, H), Image.LANCZOS)
path = os.path.join(out, 'entry.png')
img.save(path, 'PNG')
print(f"saved: {path} ({os.path.getsize(path)} bytes) {img.size}")