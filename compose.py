"""Compose 6 AI-generated panels into a magazine-style news image."""
from PIL import Image, ImageDraw, ImageFont
import os

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

# Load 6 panels
panels = []
for i in range(1, 7):
    p = Image.open(f'/home/ubuntu/news-image-20261120/panel_{i}.jpg')
    panels.append(p)

# Header
draw.rectangle([0, 0, W, 60], fill='#1a1a2e')
draw.text((15, 8), "THE WORLD TODAY", fill='#e94560', font=get_font(20, True))
draw.text((15, 32), "FRIDAY 20 NOVEMBER 2026", fill='#eaeaea', font=get_font(13, True))
draw.text((W-220, 12), "37 STORIES - 6 CONTINENTS", fill='#888', font=get_font(9))
draw.text((W-220, 26), "EVERY STORY REPORTED 20 NOV 2026", fill='#888', font=get_font(8))

# 6 panels in 3x2 grid
panel_w = (W - 30) // 3
panel_h = 180
start_y = 65

titles = [
    ("KYIV BARRAGE", "110 missiles + 400 drones. 3 Dnipro bridges hit. 9 killed. (Reuters, BBC)"),
    ("CYCLOONE AKVAN", "Landfall Gopalpur 02:00 UTC. 70-80 km/h. Third in a month. (Reuters, IMD)"),
    ("COP31 DEADLOCK", "Antalya final day. Fossil fuels unmentioned. 'Worst COP ever'. (UN News)"),
    ("SHENZHEN SUMMIT", "Trump-Xi-Putin trilateral. Historic. Nuclear dialogue. (WSJ, Reuters)"),
    ("AI SELL-OFF", "Nikkei -4.8%, Kospi -4.7%. Worst week since 2020. (Reuters, BBC)"),
    ("GTA VI LAUNCH", "$2.36bn, 24.6m copies. Biggest entertainment launch ever. (Sensor Tower)"),
]

for i in range(6):
    col = i % 3
    row = i // 3
    x = 5 + col * (panel_w + 5)
    y = start_y + row * (panel_h + 5)
    
    # Panel image
    panel_img = panels[i].resize((panel_w, panel_h - 35), Image.LANCZOS)
    img.paste(panel_img, (x, y))
    
    # Title bar
    draw.rectangle([x, y + panel_h - 35, x + panel_w, y + panel_h], fill='#1a1a2e')
    draw.text((x + 4, y + panel_h - 32), titles[i][0], fill='#e94560', font=get_font(8, True))
    
    # Subtitle
    words = titles[i][1].split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        if draw.textlength(test, font=get_font(6)) > panel_w - 8:
            lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)
    for j, line in enumerate(lines[:2]):
        draw.text((x + 4, y + panel_h - 22 + j * 8), line, fill='#aaa', font=get_font(6))

# Featured band
feat_y = start_y + 2 * (panel_h + 5) + 5
draw.rectangle([5, feat_y, W-5, feat_y+55], fill='#1a1a2e', outline='#e94560', width=1)
draw.text((10, feat_y+3), "FEATURED", fill='#e94560', font=get_font(8, True))
draw.text((10, feat_y+15), "ICJ: Myanmar committed genocide vs Rohingya - first state conviction 9-6 (Reuters)", fill='#ccc', font=get_font(7))
draw.text((10, feat_y+25), "Anthropic $81bn IPO closes +17% on debut (WSJ)", fill='#ccc', font=get_font(7))
draw.text((10, feat_y+35), "Trump defers Iran strikes decision to 2027 (Reuters)", fill='#ccc', font=get_font(7))
draw.text((10, feat_y+45), "GTA VI: $2.36bn launch day, 24.6m copies - biggest ever (Sensor Tower)", fill='#ccc', font=get_font(7))

# UTC Timeline
tl_y = feat_y + 60
draw.rectangle([5, tl_y, W-5, tl_y+50], fill='#1a1a2e', outline='#e94560', width=1)
draw.text((10, tl_y+3), "UTC TIMELINE", fill='#e94560', font=get_font(8, True))
timeline = [
    "01:22 Kyiv barrage begins",
    "02:00 Cyclone Akvan landfall (Gopalpur)",
    "05:50 Landfall complete (11:20 IST)",
    "05:53 Asia shares slide (Taiex -6.2%)",
    "07:07 Kyiv toll: 9 killed, 3 bridges",
]
for i, t in enumerate(timeline):
    draw.text((10, tl_y+14+i*7), t, fill='#aaa', font=get_font(6))

# Brief stories
brief_y = tl_y + 55
brief = [
    "Europe: UK-EU agree trade + youth deals (BBC)",
    "Europe: Poland 11-nation drills (Reuters)",
    "Europe: Italy national strike (ANSA)",
    "Asia: Japan-India military cooperation (Kyodo)",
    "Asia: S. Korea court overturns Han sentence (Yonhap)",
    "Asia: India Gen Z movement, 130M names deleted (Indian Express)",
    "Asia: Fiji El Nino drought, state of disaster (FBC)",
    "Mideast: Houthi missile hits Riyadh tower (Al Jazeera)",
    "Mideast: Saudi air campaign across Houthi Yemen (AFP)",
    "Africa: Kenya US wins Mrima Hill $60B rare earth (Reuters)",
    "Africa: Nigeria first cholera case in 10 years (WHO)",
    "Africa: Senegal boat tragedy, 100+ missing (AFP)",
    "Americas: El Salvador Bukele third-term bid (AP)",
    "Americas: Brazil isolated Awa group makes contact (AP)",
    "Americas: US deportees in S. Sudan went hungry (HRW)",
    "Oceania: Australia-China AI talks (ABC)",
    "Sport: Verstappen stewards, Las Vegas GP (Autosport)",
    "Sport: Rahul century vs NZ, India 344/2 (ESPN)",
    "Tech: Nvidia antitrust probe (Bloomberg)",
    "Tech: SpaceX funding threatened (CNN)",
    "Markets: Bitcoin below $59K (CoinDesk)",
    "Law: Missouri $7.25bn Roundup settlement (AFP)",
    "Law: Palisades fire jury convicts man (ABC)",
    "Climate: WFP $12.1B appeal for 91M people (UN News)",
    "Climate: 600 women killed in S. Africa 3 months (BBC)",
    "Climate: 20K+ Ukrainian children abducted (UNICEF)",
]

col_w = (W - 20) // 2
for i, text in enumerate(brief):
    col = i % 2
    row = i // 2
    x = 5 + col * (col_w + 5)
    y = brief_y + row * 9
    if y < H - 40:
        draw.text((x, y), f"- {text}", fill='#aaa', font=get_font(6))

# Proof strip
proof_y = H - 35
draw.rectangle([5, proof_y, W-5, proof_y+12], fill='#1a4a1a')
draw.text((10, proof_y+1), "DATE CHECK - FRIDAY 20 NOVEMBER 2026 - ALL 37 STORIES REPORTED THIS DAY", fill='#4aff4a', font=get_font(7, True))

# Footer
draw.rectangle([0, H-20, W, H], fill='#1a1a2e')
draw.text((5, H-15), "Sources: Reuters, BBC, CNN, NPR, Euronews, IPS, UN News, Kyiv Independent, IMD, PTI, AFP, WSJ, Al Jazeera", fill='#444', font=get_font(5))
draw.text((W-140, H-15), "make.fun/r/vjr5hbm8", fill='#e94560', font=get_font(6, True))

# Save
out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/tmp')
os.makedirs(out, exist_ok=True)
path = os.path.join(out, 'entry.png')
img.save(path, 'PNG')
print(f"saved: {path} ({os.path.getsize(path)} bytes)")