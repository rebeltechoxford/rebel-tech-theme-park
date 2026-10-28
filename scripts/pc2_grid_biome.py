"""THE GRID biome — repaints the Temperate biome's terrain as the Rebel Tech grid (RT red/blue lines on gloss black).
Writes replacement PNGs (same names cobra-tools extracted) into ./inject, then
`python scripts/pc2_grid_biome.py install` backs up and injects into the game's Temperate.ovl.
`python scripts/pc2_grid_biome.py restore` puts the original biome back.
"""
import os, re, sys, shutil, subprocess, hashlib
from PIL import Image, ImageDraw, ImageFilter

here = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'grid-biome')  # work dir (gitignored)
src = os.path.join(here, '..', 'biome-research', 'Temperate')
inj = os.path.join(here, 'inject')
game = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\Win64\ovldata\Content0\Biomes\Temperate'
backup = os.path.join(here, '..', 'backups', 'pc2', 'temperate-biome-original')
world = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\Win64\ovldata\Content0\Worlds\TemperateWorld'
src_world = os.path.join(here, '..', 'biome-research', 'vx')
inj_world = os.path.join(here, 'inject-world')
backup_world = os.path.join(here, '..', 'backups', 'pc2', 'temperate-world-original')
skirts = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\TerrainSkirts\TemperateSandbox'
backup_skirt = os.path.join(here, '..', 'backups', 'pc2', 'temperate-sandbox-skirt-original')
SKIRT_LEVEL = 32786  # baked u16 height at the sandbox park centre
PARK_HEIGHT = 51.203907  # ground level of the sandbox play area
cobra = r'D:\RebelTechWorld\tools\cobra-tools\ovl_tool_cmd.py'
py = r'D:\RebelTechWorld\tools\cobra-venv\Scripts\python.exe'

BLACK, NAVY, BLUE, RED, WHITE = (9, 11, 16), (6, 26, 51), (36, 76, 255), (225, 6, 22), (255, 255, 255)
LINE_BLUE, LINE_RED = (40, 90, 255), (255, 20, 40)  # RT blue/red, lifted a touch so the lines read on gloss black
N = 1024
LINES = int(os.environ.get('GRID_LINES', 4))  # grid cells per texture repeat


def grid(bg, cols, lines=LINES, minor=8, major=14, ss=4, seed=3):  # seed 3: one red line in four across, two down
    """Tileable neon grid: gaussian halo, coloured line, white-hot core. Each line takes a colour from cols at
    random (both axes); edge lines are half on each side so repeats join into full lines, and the halo is
    blurred on a 3x3 tiling so it wraps. Where lines of two colours cross, the glow mixes."""
    import numpy as np
    rng = np.random.default_rng(seed); s = N * ss; step = s / lines
    pick = {ax: [int(rng.integers(len(cols))) for _ in range(lines)] for ax in 'vh'}
    for ax in 'vh': pick[ax].append(pick[ax][0])  # the seam line is one line split over two tiles
    masks = [Image.new('L', (s, s), 0) for _ in cols]
    for i in range(lines + 1):
        p = round(i * step); ww = (major if i in (0, lines) else minor) * ss
        ImageDraw.Draw(masks[pick['v'][i]]).rectangle([p - ww / 2, 0, p + ww / 2, s], fill=255)
        ImageDraw.Draw(masks[pick['h'][i]]).rectangle([0, p - ww / 2, s, p + ww / 2], fill=255)
    lines_, glows = [], []
    for mask in masks:
        line = np.asarray(mask.resize((N, N), Image.LANCZOS), np.float32) / 255
        tiled = Image.fromarray((np.tile(line, (3, 3)) * 255).astype(np.uint8))
        halo = sum(w * np.asarray(tiled.filter(ImageFilter.GaussianBlur(r)), np.float32)[N:2 * N, N:2 * N] / 255 for r, w in ((3, 1.2), (10, 1.0), (24, .7)))
        lines_.append(line); glows.append(np.clip(np.maximum(line, halo), 0, 1))
    a = np.maximum.reduce(glows)[..., None]
    col = sum(g[..., None] * np.array(c, np.float32) for g, c in zip(glows, cols)) / (sum(glows)[..., None] + 1e-6)
    core = np.clip(np.maximum.reduce(lines_) * 1.6 - .6, 0, 1)[..., None]  # centre of each line runs white-hot
    rgb = np.array(bg) + (col - np.array(bg)) * a
    rgb = rgb + (255 - rgb) * core * .6
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def solid(c): return Image.new('RGB', (N, N), c)


# terrain paint layers: layer 0 (temperateterrain) is the default ground. Every layer the sandbox
# template or auto-paint uses is the same RT grid (lines randomly red or blue), so the floor is uniform everywhere.
RT_GRID = grid(BLACK, (LINE_BLUE, LINE_BLUE, LINE_RED))  # two blue lines to every red, on average
LAYERS = {n: RT_GRID for n in ['temperateterrain'] + [f'temperateterrain_{i}' for i in range(1, 16)]
          + ['temperateterrainskirt_1', 'temperateterrainskirt_2']}  # cliff/slope layers too: no brown rock faces
LAYERS['temperateterrainskirt_3'] = RT_GRID  # auto-paint uses this layer too; solid black wiped the grid


def build():
    shutil.rmtree(inj, ignore_errors=True); os.makedirs(inj)
    for name, rgb in LAYERS.items():
        if not os.path.exists(os.path.join(src, name + '.pdiffusearray.png')): continue  # layer shares another's textures
        img = rgb.convert('RGBA'); img.putalpha(128); img.save(os.path.join(inj, name + '.pdiffusearray.png'))  # flat blend height
        # gloss black: G = roughness (lower is shinier), R = cavity (255 = none); B, A kept as shipped
        g = os.path.join(src, name + '.pcavityroughnessdielectricarray_G.png')
        if os.path.exists(g):
            for ch in 'BA': shutil.copy(g.replace('_G.png', f'_{ch}.png'), inj)
            Image.new('L', (N, N), 255).save(g.replace(src, inj).replace('_G.png', '_R.png'))
            Image.new('L', (N, N), 55).save(os.path.join(inj, os.path.basename(g)))
        # no rocky bumps: flat gradient (RG), constant height (B) and occlusion (A) in the parallax/normal map
        h = os.path.join(src, name + '.pgradheightarray_RG.png')
        if os.path.exists(h):
            Image.new('RGB', (N, N), (128, 128, 0)).save(os.path.join(inj, os.path.basename(h)))
            Image.new('L', (N, N), 128).save(os.path.join(inj, name + '.pgradheightarray_B.png'))
            Image.new('L', (N, N), 255).save(os.path.join(inj, name + '.pgradheightarray_A.png'))
    # flat neutral macro tint so the grid isn't blotched by the grass/dirt macro map
    for f in os.listdir(src):
        if f.endswith('pmacrodiffuse.png') and f.startswith('temperateterrain'):
            Image.new('RGBA', Image.open(os.path.join(src, f)).size, (128, 128, 128, 0)).save(os.path.join(inj, f))
    # smooth glass: no grass/dirt bumps in the detail normal
    for f in os.listdir(src):
        if f.endswith('pdetailnormaltexture_RG.png'):
            Image.new('RGB', Image.open(os.path.join(src, f)).size, (128, 128, 0)).save(os.path.join(inj, f))
    # no grass or flowers: fully transparent detail cards
    for f in os.listdir(src):
        if 'grass' in f or 'flower' in f:
            if f.endswith('popacitytexture.png') or f.endswith('pbasecolourtexture_A.png'):
                im = Image.open(os.path.join(src, f)); Image.new(im.mode, im.size, 0).save(os.path.join(inj, f))
            if f.endswith('pbasecolourtexture_RGB.png'):
                shutil.copy(os.path.join(src, f), inj)  # channel pair must travel together
    # terrain detail scatter (grass cards, pebbles): shrink every detail model to 1% so none of it shows
    sys.path.insert(0, os.path.dirname(cobra)); argv, sys.argv = sys.argv, sys.argv[:1]
    import ovl_tool_cmd  # noqa: F401  (sets up cobra-tools logging)
    from generated.formats.ms2 import Ms2File
    sys.argv = argv
    m = Ms2File(); m.load(os.path.join(src, 'models.ms2'), read_editable=True); m.resize(0.01); m.save(os.path.join(inj, 'models.ms2'))
    # cobra-tools only injects PNGs alongside their .tex header
    for f in os.listdir(inj):
        if not f.endswith('.png'): continue
        tex = re.sub(r'(_[RGBA]+)?\.png$', '.tex', f)
        if not os.path.exists(os.path.join(inj, tex)): shutil.copy(os.path.join(src, tex), inj)
    print('built', len(os.listdir(inj)), 'files in', inj)


def build_world():
    """Flat, treeless world skirt: park-level heightmap, straight-up normals, no skirt trees."""
    import numpy as np, imageio.v3 as iio
    shutil.rmtree(inj_world, ignore_errors=True); os.makedirs(inj_world)
    xml = open(os.path.join(src_world, 'temperateworld.voxelskirt')).read()
    xml = re.sub(r'<entity_instances>.*?</entity_instances>', '<entity_instances><data /></entity_instances>', xml, flags=re.S)
    open(os.path.join(inj_world, 'temperateworld.voxelskirt'), 'w').write(xml)
    h = iio.imread(os.path.join(src_world, 'temperateworld_height.tiff'))
    iio.imwrite(os.path.join(inj_world, 'temperateworld_height.tiff'), np.full_like(h, PARK_HEIGHT))
    Image.new('RGBA', (2048, 2048), (127, 255, 127, 255)).save(os.path.join(inj_world, 'temperateworld_normals.png'))
    shutil.copy(os.path.join(src_world, 'temperateworld_normals.tex'), inj_world)
    print('built world skirt in', inj_world)


def build_skirt():
    """Flatten the baked backdrop terrain the Temperate sandbox renders.
    Built from the shipped DefaultSandbox bake (format v0: BHMP + raw deflate; 32-byte header,
    2048x2048 little-endian u16 heights, then per-pixel material weights). Temperate's own bake is
    v2, whose height block is packed differently: rewriting it crashes the game (0xFDEAD)."""
    import zlib
    raw = open(os.path.join(skirts, '..', 'DefaultSandbox', 'DefaultSandbox.bakedHeightMap'), 'rb').read()
    assert raw[:4] == b'BHMP'
    d = bytearray(zlib.decompressobj(-15).decompress(raw[4:]))
    assert d[:4] == bytes(4), 'expected a v0 bake'
    n = 2048 * 2048
    d[32:32 + 2 * n] = SKIRT_LEVEL.to_bytes(2, 'little') * n
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    open(os.path.join(here, 'TemperateSandbox.bakedHeightMap'), 'wb').write(b'BHMP' + c.compress(bytes(d)) + c.flush())
    print('built flat sandbox skirt')


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def install():
    for d, ovl, files, bak in TARGETS:
        if not os.path.isdir(bak):
            shutil.copytree(d, bak, ignore=shutil.ignore_patterns('Art'))
            for f in os.listdir(bak): assert sha(os.path.join(bak, f)) == sha(os.path.join(d, f)), f
            print('backed up original', ovl, 'to', bak)
    if not os.path.isdir(backup_skirt):
        os.makedirs(backup_skirt); shutil.copy2(os.path.join(skirts, 'TemperateSandbox.bakedHeightMap'), backup_skirt)
    restore(quiet=True)  # always inject onto pristine files
    shutil.copy(os.path.join(here, 'TemperateSandbox.bakedHeightMap'), skirts)
    for d, ovl, files, bak in TARGETS:
        r = subprocess.run([py, cobra, 'inject', '-g', 'Planet Coaster 2', '-i', files, '--in-place', '--update-aux', os.path.join(d, ovl)],
                           capture_output=True, text=True)
        print('\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'ERROR' in l or 'SUCCESS' in l or 'Traceback' in l))


def restore(quiet=False):
    for d, ovl, files, bak in TARGETS:
        for f in os.listdir(d):
            if os.path.isfile(os.path.join(d, f)): os.remove(os.path.join(d, f))
        for f in os.listdir(bak): shutil.copy2(os.path.join(bak, f), d)
    shutil.copy2(os.path.join(backup_skirt, 'TemperateSandbox.bakedHeightMap'), skirts)
    if not quiet: print('restored original Temperate biome and world')


TARGETS = [(game, 'Temperate.ovl', inj, backup), (world, 'TemperateWorld.ovl', inj_world, backup_world)]
step = sys.argv[1] if len(sys.argv) > 1 else 'build'
if step in ('build', 'all'): build(); build_world(); build_skirt()
if step in ('install', 'all'): install()
if step == 'restore': restore()
if step == 'skirt': build_skirt(); shutil.copy(os.path.join(here, 'TemperateSandbox.bakedHeightMap'), skirts)
