"""Textures for the Rebel Tech Grid city pieces (run with the cobra-venv Python: numpy + PIL).
  portal-vortex.png  RT blue/red vortex in polar space (U angle, V radius) for the spinning portal disc
  city-windows.png   blue curtain-wall glass with slim mullions and glowing floor lines (RT blue, one in four red)
  rt-logo-sign.png   Rebel Tech Grid logo (cropped from the owner's reference) on a black sign
  rt-signs.png       signage atlas: eight 4:1 strips (SIGNS below; build_grid_park.py maps sign planes to a row)
  rt-signs-venues.png  End of WiFi Bar and its eight venues, same 4:1 strip layout (VENUES below)
  atom-orbit.png     animated atom orbits: red/blue/white bands, one electron with a comet tail per orbit
  atom-orbit-base.png  the same orbit bands without the electron (base colour)
  rt-medallion.png   plaza floor medallion: RT badge inside red/blue rings and ticks
  city-water.png     lagoon water: navy with blue and red light ripples (tileable)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(repo, 'build', 'tron-grid', 'tex'); os.makedirs(out, exist_ok=True)
N = 1024
BLUE, RED, WHITE = np.array([36, 76, 255]), np.array([225, 6, 22]), np.array([255, 255, 255])

# vortex in polar space for the portal disc: U = angle (tiles), V = radius (0 centre .. 1 rim).
# Spiral arms are diagonal stripes here, so scrolling U in game spins the vortex.
v, u = np.mgrid[0:1:512j, 0:1:1024j]
lr = np.log(v + .02)
arms = (np.sin(2 * np.pi * (5 * u) + 9 * lr) * .5 + .5) ** 3
fine = (np.sin(2 * np.pi * (13 * u) + 22 * lr + 1.3) * .5 + .5) ** 6
fade = np.clip(1.15 - v, 0, 1)
core = np.clip(np.exp(-(v / .12) ** 2) * 1.2, 0, 1)
rgb = (arms * fade)[..., None] * BLUE * 1.1 + (fine * fade)[..., None] * RED * .9 + core[..., None] * WHITE
Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)).save(os.path.join(out, 'portal-vortex.png'))

# 2010s curtain wall: deep blue glass, slim mullions, a brighter LED line at every floor slab
img = np.zeros((N, N, 3), np.float32); img[:] = (6, 14, 26)
yy = np.linspace(0, 1, N)[:, None]
img += (np.clip(1 - abs(yy - .5) * 2, 0, 1) * 10)[..., None] * np.array([.3, .5, 1])  # soft sky reflection gradient
for k in range(17):  # mullions (16 per repeat)
    p = min(k * N // 16, N - 1); img[:, max(p - 1, 0):p + 2] = (22, 36, 95)
for k, c in enumerate(((50, 95, 255), (50, 95, 255), (235, 20, 40), (50, 95, 255), (50, 95, 255))):  # floor slabs (4 per repeat); first and last meet at the seam
    p = min(k * N // 4, N - 1); img[max(p - 3, 0):p + 4, :] = c
rng = np.random.default_rng(3); step = N // 16
for i in range(4):
    for j in range(16):
        if rng.random() < .18: img[i * N // 4 + 8:(i + 1) * N // 4 - 8, j * step + 3:(j + 1) * step - 3] += (14, 26, 60)
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(os.path.join(out, 'city-windows.png'))

# logo sign: crop from the reference, crush the background to black so only the badge reads
crop = Image.open(os.path.join(repo, 'build', 'references', 'rebel-tech-grid-portal-ref.jpg')).convert('RGB').crop((100, 300, 420, 585))
c = np.asarray(crop, np.float32)
sat = c.max(-1) - c.min(-1); lum = c.mean(-1)
keep = np.clip((sat - 40) / 60, 0, 1) + np.clip((lum - 150) / 60, 0, 1)
c = np.clip(c * np.clip(keep, 0, 1)[..., None] * 1.6, 0, 255)  # brighter so the badge glows like the grid
logo = Image.fromarray(c.astype(np.uint8)).resize((960, 855), Image.LANCZOS)
sign = Image.new('RGB', (N, N), (0, 0, 0)); sign.paste(logo, (32, 84))
sign.save(os.path.join(out, 'rt-logo-sign.png'))

# signage atlas: 2048 square, eight 2048x256 strips. White words bloom RT blue, red words bloom red.
FONT = r'C:\Windows\Fonts\Orbitron-Black.ttf'
SIGNS = [  # one row each: (words, size), each word (text, colour)
    ([('REBEL TECH', 'white')], 170), ([('ARCADE', 'red')], 190), ([('GEAR', 'red')], 200),
    ([('FUEL ', 'white'), ('UP', 'red')], 190), ([('EATS  //  DRINKS  //  RECHARGE', 'white')], 92),
    ([('CONTROL ROOM', 'white')], 150), ([('T H E M E   P A R K', 'white')], 120), ([('CONNECTING. INSTALLING. SOLVING.', 'white')], 84)]
FILL = {'white': (255, 255, 255), 'red': (255, 24, 40)}
GLOW = {'white': (40, 80, 255), 'red': (225, 6, 22)}


def strip(words, size):
    """One 4:1 sign: bold slanted words, white-hot fill, coloured bloom behind, on black."""
    W, H = 2048, 256; font = ImageFont.truetype(FONT, size)
    widths = [font.getlength(t) for t, _ in words]
    while sum(widths) > W * .88:
        size -= 6; font = ImageFont.truetype(FONT, size); widths = [font.getlength(t) for t, _ in words]
    fill, glow = Image.new('RGB', (W, H)), Image.new('RGB', (W, H))
    df, dg = ImageDraw.Draw(fill), ImageDraw.Draw(glow); x = (W - sum(widths)) / 2
    for (t, col), w in zip(words, widths):
        y = H / 2 - size * .62
        df.text((x, y), t, font=font, fill=FILL[col]); dg.text((x, y), t, font=font, fill=GLOW[col], stroke_width=10, stroke_fill=GLOW[col]); x += w
    skew = (1, .22, -.22 * H / 2, 0, 1, 0)  # italic slant like the dream-board lettering
    fill, glow = (im.transform((W, H), Image.AFFINE, skew, Image.BICUBIC) for im in (fill, glow))
    g = np.asarray(glow.filter(ImageFilter.GaussianBlur(14)), np.float32) * 1.3 + np.asarray(glow.filter(ImageFilter.GaussianBlur(4)), np.float32) * .6
    return np.clip(np.maximum(np.asarray(fill, np.float32), g), 0, 255)


Image.fromarray(np.concatenate([strip(w, s) for w, s in SIGNS]).astype(np.uint8)).save(os.path.join(out, 'rt-signs.png'))

# second atlas: the End of WiFi Bar and the venues stacked inside it (food, drinks, souvenirs)
VENUES = [([('END OF WIFI ', 'white'), ('BAR', 'red')], 150), ([('BYTE ', 'white'), ('BURGERS', 'red')], 150),
          ([('FIREWALL ', 'red'), ('GRILL', 'white')], 150), ([('PIXEL ', 'white'), ('PIZZA', 'red')], 160),
          ([('404 ', 'red'), ('NOODLES', 'white')], 160), ([('OVERCLOCK ', 'white'), ('COFFEE', 'red')], 130),
          ([('BANDWIDTH ', 'white'), ('BREWS', 'red')], 130), ([('CACHE ', 'white'), ('& ', 'red'), ('CARRY', 'white')], 150)]
Image.fromarray(np.concatenate([strip(w, s) for w, s in VENUES]).astype(np.uint8)).save(os.path.join(out, 'rt-signs-venues.png'))

# atom orbits: U runs once round an orbit, V wraps the tube. Bands top to bottom: red, blue, white, spare.
# atom-orbit.png (emissive) carries one white-hot electron with a comet tail; make_pack.py scrolls U so it spins.
# atom-orbit-base.png is the same ring without the electron, so nothing static shows under lighting.
u = np.linspace(0, 1, N, endpoint=False)[None, :]
d = (u - .04) % 1  # distance behind the electron head
tail = np.where(d < .5, np.exp(-d / .09), 0) * (d > 0)
head = np.exp(-(((u - .04 + .5) % 1 - .5) / .012) ** 2)
orb, base = np.zeros((N, N, 3)), np.zeros((N, N, 3))
for b, colr in enumerate((RED, BLUE, np.array([200, 215, 255]))):
    rows = slice(b * N // 4, (b + 1) * N // 4)
    line = colr * .45
    orb[rows] = (line + tail[..., None] * colr * 1.6 + head[..., None] * WHITE * 1.5)[0]
    base[rows] = line
Image.fromarray(np.clip(orb, 0, 255).astype(np.uint8)).save(os.path.join(out, 'atom-orbit.png'))
Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(os.path.join(out, 'atom-orbit-base.png'))

# the other animated materials (make_pack.py ANIMATED scrolls U): same four bands (red, blue, white, spare)
BANDS = (RED, BLUE, np.array([200, 215, 255]))
def banded(profile, floor=0.0):
    im = np.zeros((N, N, 3))
    for b, colr in enumerate(BANDS):
        im[b * N // 4:(b + 1) * N // 4] = (floor * colr + profile[..., None] * colr * 1.4 + np.clip(profile - .8, 0, 1)[..., None] * WHITE * 3)[0]
    return Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
# data-chase: three packets (bright head, short tail) per repeat racing along every neon line
dd = (u * 3) % 1
banded(np.where(dd < .3, np.exp(-dd / .05), 0), .3).save(os.path.join(out, 'data-chase.png'))
# pulse: one short flash per period; objects pin their UVs to one U (their phase), so they blink in turn
banded(np.exp(-((u - .5) / .06) ** 2) + .12).save(os.path.join(out, 'pulse.png'))
# fountain jets: broken streaks of water rising up the jet (U runs up it)
streak = sum(np.clip(np.sin(2 * np.pi * (f * u + p)) * .5 + .5, 0, 1) ** 6 for f, p in ((7, 0), (11, .3), (17, .7))) / 2
banded(streak, .15).save(os.path.join(out, 'fountain-jet.png'))
Image.new('RGB', (N, N), (4, 6, 14)).save(os.path.join(out, 'anim-base.png'))  # base colour under every scrolling light
# LED ticker: scrolling messages, one per strip row; each row tiles end to end
TICKER = [([('CONNECTING. INSTALLING. SOLVING.  ', 'white'), ('//  ', 'red')], 110),
          ([('END OF WIFI BAR  ', 'white'), ('//  ', 'red'), ('FOOD  DRINKS  SOUVENIRS  ', 'white'), ('//  ', 'red')], 96),
          ([('WELCOME TO THE GRID  ', 'white'), ('//  ', 'red'), ('REBEL TECH THEME PARK  ', 'white'), ('//  ', 'red')], 96),
          ([('SHOWTIME  ', 'red'), ('//  ', 'white'), ('CONTROL ROOM  ', 'white'), ('//  ', 'red'), ('LIVE  ', 'red')], 110)] * 2
Image.fromarray(np.concatenate([strip(w, s) for w, s in TICKER]).astype(np.uint8)).save(os.path.join(out, 'rt-ticker.png'))

# floor medallion: RT badge in the middle of red/blue rings, ticks and sweeping orbit arcs
M = 2048; med = Image.new('RGB', (M, M)); d = ImageDraw.Draw(med); c = M / 2
col = lambda a: tuple(int(x) for x in a)
for r, w, cc in ((1000, 22, BLUE), (950, 10, RED), (720, 14, BLUE), (690, 6, WHITE)):
    d.ellipse([c - r, c - r, c + r, c + r], outline=col(cc), width=w)
for k in range(72):  # tick ring between the outer rings
    a = 2 * np.pi * k / 72; r0, r1 = (860, 930) if k % 6 else (800, 935)
    d.line([c + r0 * np.cos(a), c + r0 * np.sin(a), c + r1 * np.cos(a), c + r1 * np.sin(a)], fill=col(RED if k % 6 == 0 else BLUE), width=8)
for a0 in (20, 140, 260):
    d.arc([c - 780, c - 780, c + 780, c + 780], a0, a0 + 70, fill=(255, 255, 255), width=12)
med.paste(Image.open(os.path.join(out, 'rt-badge.png')).convert('RGB').resize((1300, 1300), Image.LANCZOS), (int(c - 650), int(c - 650)))
med = np.asarray(med, np.float32)
med = np.maximum(med, np.asarray(Image.fromarray(med.astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)), np.float32) * 1.4)
Image.fromarray(np.clip(med, 0, 255).astype(np.uint8)).resize((N, N), Image.LANCZOS).save(os.path.join(out, 'rt-medallion.png'))

# lagoon water: navy with thin blue/red caustic ripples (integer frequencies so it tiles)
yy, xx = np.mgrid[0:N, 0:N] / N
w1 = np.sin(2 * np.pi * (3 * xx + 2 * yy) + 2 * np.sin(2 * np.pi * (2 * yy - xx)))
w2 = np.sin(2 * np.pi * (5 * xx - 3 * yy) + 1.5 * np.sin(2 * np.pi * (3 * xx + yy)))
water = np.array([3, 8, 26]) + np.exp(-(w1 * 6) ** 2)[..., None] * np.array([40, 90, 255]) * .8 + (np.exp(-((w2 - .3) * 7) ** 2) * .55)[..., None] * RED * .6
Image.fromarray(np.clip(water, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)).save(os.path.join(out, 'city-water.png'))
print('textures in', out)
