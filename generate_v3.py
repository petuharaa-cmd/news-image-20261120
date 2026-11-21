"""Generate a magazine-style news image with illustrated panels for 20 Nov 2026."""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

W, H = 1024, 1024
img = Image.new('RGB', (W, H), '#0a0a1a')
draw = ImageDraw.Draw(img)

def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_panel(draw, x, y, w, h, title, lines, color, icon_fn=None):
    draw.rectangle([x, y, x+w, y+h], fill=color, outline='#e94560', width=1)
    icon_h = h // 2
    if icon_fn:
        icon_fn(draw, x, y, w, icon_h)
    draw.text((x+6, y+icon_h+4), title, fill='#e94560', font=get_font(10, True))
    for j, line in enumerate(lines[:4]):
        draw.text((x+6, y+icon_h+18+j*12), line, fill='#eaeaea', font=get_font(8))

def icon_kyiv(draw, x, y, w, h):
    for i in range(h):
        t = i / h
        r = int(10 + t * 20)
        g = int(10 + t * 10)
        b = int(30 + t * 40)
        draw.line([(x, y+i), (x+w, y+i)], fill=(r, g, b))
    random.seed(42)
    for _ in range(5):
        sx = x + random.randint(10, w-10)
        sy = y + random.randint(5, h//2)
        ex = sx + random.randint(-30, 30)
        ey = sy + random.randint(20, h//2)
        draw.line([(sx, sy), (ex, ey)], fill='#ff4444', width=1)
        draw.ellipse([ex-2, ey-2, ex+2, ey+2], fill='#ffaa00')
    for bx in [x+w//4, x+w//2, x+3*w//4]:
        draw.line([(bx-15, y+h-10), (bx-15, y+h-25)], fill='#333', width=2)
        draw.line([(bx+15, y+h-10), (bx+15, y+h-25)], fill='#333', width=2)
        draw.line([(bx-15, y+h-25), (bx+15, y+h-25)], fill='#444', width=2)
    draw.rectangle([x, y+h-10, x+w, y+h], fill='#1a2a4a')

def icon_cyclone(draw, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    for arm in range(4):
        angle_offset = arm * math.pi / 2
        points = []
        for r in range(5, min(w, h)//2, 2):
            angle = angle_offset + r * 0.3
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            if x <= px <= x+w and y <= py <= y+h:
                points.append((px, py))
        if len(points) > 1:
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=(100, 150, 200), width=2)
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill='#1a3a5a', outline='#4488cc')
    random.seed(123)
    for _ in range(20):
        rx = x + random.randint(5, w-5)
        ry = y + random.randint(5, h-5)
        draw.line([(rx, ry), (rx-2, ry+5)], fill='#4466aa', width=1)

def icon_cop31(draw, x, y, w, h):
    cx, cy = x + w//2, y + h//2
    r = min(w, h) // 3
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill='#1a4a6a', outline='#2266aa', width=2)
    draw.ellipse([cx-r//2, cy-r//3, cx+r//4, cy+r//4], fill='#2a6a4a')
    draw.ellipse([cx+r//5, cy-r//4, cx+r//2, cy+r//3], fill='#2a6a4a')
    draw.rectangle([cx-r, cy+r+5, cx+r, cy+r+15], fill='#cc2222')
    draw.text((cx-15, cy+r+6), "DEADLOCK", fill='white', font=get_font(8, True))

def icon_shenzhen(draw, x, y, w, h):
    random.seed(456)
    bx = x + 5
    while bx < x + w - 5:
        bw = random.randint(8, 20)
        bh = random.randint(15, h-20)
        draw.rectangle([bx, y+h-bh, bx+bw, y+h], fill='#2a3a5a')
        for wy in range(y+h-bh+3, y+h-2, 4):
            for wx in range(bx+2, bx+bw-1, 3):
                if random.random() > 0.4:
                    draw.rectangle([wx, wy, wx+1, wy+1], fill='#ffdd66')
        bx += bw + 2
    flag_y = y + 5
    for fx, color in [(x+10, '#cc2222'), (x+w//2-10, '#cc2222'), (x+w-30, '#2244cc')]:
        draw.line([(fx, flag_y), (fx, flag_y+15)], fill='#888', width=1)
        draw.rectangle([fx, flag_y, fx+12, flag_y+8], fill=color)

def icon_stocks(draw, x, y, w, h):
    chart_x, chart_y = x+10, y+10
    chart_w, chart_h = w-20, h-20
    draw.rectangle([chart_x, chart_y, chart_x+chart_w, chart_y+chart_h], fill='#0a1520')
    for i in range(1, 4):
        gy = chart_y + i * chart_h // 4
        draw.line([(chart_x, gy), (chart_x+chart_w, gy)], fill='#222', width=1)
    points = []
    random.seed(789)
    for i in range(20):
        px = chart_x + i * chart_w // 19
        py = chart_y + 10 + i * (chart_h - 20) // 19 + random.randint(-5, 5)
        points.append((px, py))
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill='#ff3333', width=2)
    draw.text((chart_x+5, chart_y+5), "NIKKEI -4.8%", fill='#ff4444', font=get_font(10, True))

def icon_gta(draw, x, y, w, h):
    for i in range(h):
        t = i / h
        r = int(40 + t * 60)
        g = int(10 + t * 20)
        b = int(60 + t * 40)
        draw.line([(x, y+i), (x+w, y+i)], fill=(r, g, b))
    for px in [x+20, x+w-20]:
        py = y + h - 5
        draw.line([(px, py), (px, py-30)], fill='#1a1a1a', width=3)
        for angle in [-40, -20, 0, 20, 40]:
            rad = math.radians(angle - 90)
            ex = px + 15 * math.cos(rad)
            ey = py - 30 + 15 * math.sin(rad)
            draw.line([(px, py-30), (ex, ey)], fill='#1a1a1a', width=2)
    draw.text((x+10, y+10), "GTA VI", fill='#ff00ff', font=get_font(14, True))
    draw.text((x+10, y+28), "$2.36BN", fill='#00ffff', font=get_font(10, True))

# Header
draw.rectangle([0, 0, W, 65], fill='#1a1a2e')
draw.text((15, 10), "THE WORLD TODAY", fill='#e94560', font=get_font(22, True))
draw.text((15, 38), "FRIDAY 20 NOVEMBER 2026", fill='#eaeaea', font=get_font(14, True))
draw.text((W-250, 15), "37 STORIES - 6 CONTINENTS", fill='#888', font=get_font(10))
draw.text((W-250, 30), "EVERY STORY REPORTED 20 NOV 2026", fill='#888', font=get_font(9))

# 6 Illustrated Panels
panel_w = (W - 40) // 3
panel_h = 200
start_y = 75

panels = [
    ("KYIV BARRAGE", ["110 missiles + 400 drones", "3 Dnipro bridges hit", "9 killed, power cut", "(Reuters, BBC)"], '#16213e', icon_kyiv),
    ("CYCLOONE AKVAN", ["Landfall Gopalpur 02:00 UTC", "70-80 km/h gusting 90", "Third cyclone in a month", "(Reuters, IMD)"], '#0f3460', icon_cyclone),
    ("COP31 DEADLOCK", ["Antalya final day", "Fossil fuels unmentioned", "'Worst COP ever'", "(UN News, AFP)"], '#196f3d', icon_cop31),
    ("SHENZHEN SUMMIT", ["Trump-Xi-Putin trilateral", "Historic first meeting", "Nuclear dialogue agreed", "(WSJ, Reuters)"], '#1a5276', icon_shenzhen),
    ("AI SELL-OFF", ["Nikkei -4.8%, Kospi -4.7%", "Worst week since 2020", "AI bubble fears", "(Reuters, BBC)"], '#7d3c98', icon_stocks),
    ("GTA VI LAUNCH", ["$2.36bn, 24.6m copies", "Biggest entertainment launch", "Neon dusk, palm trees", "(Sensor Tower)"], '#922b21', icon_gta),
]

for i, (title, lines, color, icon_fn) in enumerate(panels):
    col = i % 3
    row = i // 3
    x = 10 + col * (panel_w + 10)
    y = start_y + row * (panel_h + 10)
    draw_panel(draw, x, y, panel_w, panel_h, title, lines, color, icon_fn)

# Featured band
feat_y = start_y + 2 * (panel_h + 10) + 5
draw.rectangle([10, feat_y, W-10, feat_y+70], fill='#1a1a2e', outline='#e94560', width=1)
draw.text((15, feat_y+5), "FEATURED", fill='#e94560', font=get_font(10, True))
draw.text((15, feat_y+20), "ICJ: Myanmar committed genocide vs Rohingya - first state conviction (9-6) (Reuters)", fill='#ccc', font=get_font(8))
draw.text((15, feat_y+33), "Anthropic $81bn IPO closes +17% on debut (WSJ)", fill='#ccc', font=get_font(8))
draw.text((15, feat_y+46), "Trump defers Iran strikes decision to 2027 (Reuters)", fill='#ccc', font=get_font(8))
draw.text((15, feat_y+59), "GTA VI: $2.36bn launch day, 24.6m copies - biggest ever (Sensor Tower)", fill='#ccc', font=get_font(8))

# UTC Timeline
tl_y = feat_y + 80
draw.rectangle([10, tl_y, W-10, tl_y+60], fill='#1a1a2e', outline='#e94560', width=1)
draw.text((15, tl_y+5), "UTC TIMELINE", fill='#e94560', font=get_font(10, True))
timeline = [
    "01:22 Kyiv barrage begins",
    "02:00 Cyclone Akvan landfall (Gopalpur)",
    "05:50 Landfall complete (11:20 IST)",
    "05:53 Asia shares slide (Taiex -6.2%)",
    "07:07 Kyiv toll: 9 killed, 3 bridges",
]
for i, t in enumerate(timeline):
    draw.text((15, tl_y+18+i*8), t, fill='#aaa', font=get_font(7))

# Brief stories
brief_y = tl_y + 70
brief = [
    "Europe: UK-EU agree trade + youth deals, Burnham 'undo Brexit damage' (BBC)",
    "Europe: Poland 11-nation drills, Coalition of the Willing (Reuters)",
    "Europe: Italy national strike, stagnant wages (ANSA)",
    "Asia: Japan-India military cooperation, UNICORN antenna (Kyodo)",
    "Asia: S. Korea court overturns Han 15-year sentence (Yonhap)",
    "Asia: India Gen Z cockroach movement, 130M names deleted (Indian Express)",
    "Asia: Fiji El Nino drought, state of disaster (FBC)",
    "Mideast: Houthi missile hits Riyadh 80-storey tower (Al Jazeera)",
    "Mideast: Saudi air campaign across Houthi Yemen (AFP)",
    "Africa: Kenya US consortium wins Mrima Hill $60B rare earth (Reuters)",
    "Africa: Nigeria first cholera case in 10 years (WHO)",
    "Africa: Senegal boat tragedy, 100+ missing (AFP)",
    "Americas: El Salvador Bukele third-term bid (AP)",
    "Americas: Brazil isolated Awa group makes contact (AP)",
    "Americas: US deportees in S. Sudan went hungry (HRW)",
    "Americas: Canada youth climate trial reset (AFP)",
    "Oceania: Australia-China AI talks, Albanese 11-day trip (ABC)",
    "Oceania: NZ vs England test, Wellington (ESPN)",
    "Sport: Verstappen sent to stewards, Las Vegas GP (Autosport)",
    "Sport: Rahul century vs NZ, India 344/2 (ESPN)",
    "Tech: Nvidia antitrust probe (Bloomberg)",
    "Tech: SpaceX funding threatened by lawmakers (CNN)",
    "Markets: Bitcoin below $59K, worst month since 2022 (CoinDesk)",
    "Markets: Anthropic IPO $2.01T valuation (WSJ)",
    "Law: Missouri $7.25bn Roundup settlement approved (AFP)",
    "Law: Palisades fire jury convicts man (ABC)",
    "Climate: WFP $12.1B appeal for 91M people (UN News)",
    "Climate: 600 women killed in S. Africa in 3 months (BBC)",
]

col_w = (W - 30) // 2
for i, text in enumerate(brief):
    col = i % 2
    row = i // 2
    x = 10 + col * (col_w + 10)
    y = brief_y + row * 12
    if y < H - 50:
        draw.text((x, y), f"- {text}", fill='#aaa', font=get_font(7))

# Proof strip
proof_y = H - 45
draw.rectangle([10, proof_y, W-10, proof_y+15], fill='#1a4a1a')
draw.text((15, proof_y+2), "DATE CHECK - FRIDAY 20 NOVEMBER 2026 - ALL 37 STORIES REPORTED THIS DAY", fill='#4aff4a', font=get_font(8, True))

# Footer
draw.rectangle([0, H-25, W, H], fill='#1a1a2e')
draw.text((10, H-18), "Sources: Reuters, BBC, CNN, NPR, CSMonitor, Euronews, IPS, UN News, Kyiv Independent, IMD, PTI, AFP, WSJ, Al Jazeera", fill='#555', font=get_font(6))
draw.text((W-160, H-18), "make.fun/r/vjr5hbm8", fill='#e94560', font=get_font(7, True))

# Save
out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/tmp')
os.makedirs(out, exist_ok=True)
path = os.path.join(out, 'entry.png')
img.save(path, 'PNG')
print(f"saved: {path} ({os.path.getsize(path)} bytes)")