"""Hide the nature the Temperate sandbox template scatters (trees, rocks, ferns, bramble, periwinkle),
including the pieces outside the park boundary that the game will not let you select.
Trees, ferns, bramble and flowers become fully transparent; rocks turn Grid black and their models shrink to 1%.
Run with the cobra-venv Python while the game is closed:
  python pc2_hide_nature.py build|install|all|restore
Originals are backed up once per pack folder to build/backups/pc2/hide-nature-original.
"""
import os, sys, shutil, subprocess

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.join(repo, 'build', 'hide-nature')
backup = os.path.join(repo, 'build', 'backups', 'pc2', 'hide-nature-original')
nature = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\Win64\ovldata\Content0\Environment\Scenery\Nature'
cobra = r'D:\RebelTechWorld\tools\cobra-tools\ovl_tool_cmd.py'
py = r'D:\RebelTechWorld\tools\cobra-venv\Scripts\python.exe'
PACKS = [r'Rocks\NAT_Rock_Temperate\NAT_Rock_Temperate.ovl',
         r'Vegetation\NAT_Bush_Bramble\NAT_Bush_Bramble.ovl',
         r'Vegetation\NAT_Flower_Periwinkle\NAT_Flower_Periwinkle.ovl',
         r'Vegetation\NAT_Plant_Fern_Common\NAT_Plant_Fern_Common\NAT_Plant_Fern_Common.ovl',
         r'Vegetation\NAT_Plant_Fern_King\NAT_Plant_Fern_King.ovl',
         r'Vegetation\NAT_Tree_Broadleaf_Ash\NAT_Tree_Broadleaf_Ash.ovl',
         r'Vegetation\NAT_Tree_Broadleaf_Elm\NAT_Tree_Broadleaf_Elm.ovl',
         r'Vegetation\NAT_Tree_Broadleaf_Maple\Nat_Tree_Broadleaf_Maple.ovl',
         r'Vegetation\NAT_Tree_Broadleaf_Oak\NAT_Tree_Broadleaf_Oak.ovl',
         r'Vegetation\NAT_Tree_Broadleaf_Poplar_Black\NAT_Tree_Broadleaf_Poplar_Black.ovl',
         r'Rocks\Shared_Rocks\Shared_Rocks.ovl']  # rock models (shrunk: black rocks still read as mounds)


def packs():
    for p in PACKS:
        ovl = os.path.join(nature, p); yield os.path.splitext(os.path.basename(p))[0], ovl


def bak(name): return os.path.join(backup, name)


def build():
    """Cutout materials (foliage, billboards, ferns, flowers) get zero alpha; opaque bark is pointed at the
    pack's cutout material so it vanishes too. Rocks have no cutout shader, so they turn Grid black."""
    import re
    from PIL import Image
    shutil.rmtree(here, ignore_errors=True)
    for name, ovl in packs():
        src, dst = os.path.join(here, 'src', name), os.path.join(here, 'inject', name)
        pristine = os.path.join(bak(name), os.path.basename(ovl)) if os.path.isdir(bak(name)) else ovl
        subprocess.run([py, cobra, 'extract', '-g', 'Planet Coaster 2', '-o', src, pristine], capture_output=True)
        os.makedirs(dst)
        fgms = {f: open(os.path.join(src, f)).read() for f in os.listdir(src) if f.endswith('.fgm')}
        cutout = [f for f, x in fgms.items() if re.search(r'shader_name="[^"]*(Clip|Billboard)', x)]
        for f, x in fgms.items():
            if f in cutout or 'Rock' in name: continue
            if cutout:  # opaque bark/stems: reuse the pack's cutout material (same vertex format)
                donor = next((c for c in cutout if 'billboard' not in c), cutout[0])
                open(os.path.join(dst, f), 'w').write(fgms[donor])
        for png in os.listdir(src):
            if not png.endswith('.png'): continue
            im = Image.open(os.path.join(src, png))
            if 'Rock' in name and 'basecolour' in png and png.endswith('_RGB.png'):
                Image.new(im.mode, im.size, (9, 11, 16) if im.mode == 'RGB' else 9).save(os.path.join(dst, png))
            elif 'Rock' not in name and (png.endswith('popacity.png') or (png.endswith('_A.png') and ('basecolour' in png or 'diffusealpha' in png))):
                Image.new(im.mode, im.size, 0).save(os.path.join(dst, png))
            else: continue
            pair = re.sub(r'_(A|RGB)\.png$', lambda m: '_' + ('RGB' if m.group(1) == 'A' else 'A') + '.png', png)
            if pair != png and os.path.exists(os.path.join(src, pair)) and not os.path.exists(os.path.join(dst, pair)):
                shutil.copy(os.path.join(src, pair), dst)  # channel pair must travel together
            tex = re.sub(r'(_[RGBA]+)?\.png$', '.tex', png)
            if not os.path.exists(os.path.join(dst, tex)): shutil.copy(os.path.join(src, tex), dst)
        if name == 'Shared_Rocks':
            sys.path.insert(0, os.path.dirname(cobra)); argv, sys.argv = sys.argv, sys.argv[:1]
            import ovl_tool_cmd  # noqa: F401  (sets up cobra-tools logging)
            from generated.formats.ms2 import Ms2File
            sys.argv = argv
            m = Ms2File(); m.load(os.path.join(src, 'models.ms2'), read_editable=True); m.resize(0.01); m.save(os.path.join(dst, 'models.ms2'))
        print(name, len(cutout), 'cutout materials,', len(os.listdir(dst)), 'files')


def install():
    for name, ovl in packs():
        d = os.path.dirname(ovl)
        if not os.path.isdir(bak(name)):
            os.makedirs(bak(name))
            for f in os.listdir(d):
                if os.path.isfile(os.path.join(d, f)): shutil.copy2(os.path.join(d, f), bak(name))
    restore(quiet=True)
    for name, ovl in packs():
        before = os.path.getmtime(ovl)
        r = subprocess.run([py, cobra, 'inject', '-g', 'Planet Coaster 2', '-i', os.path.join(here, 'inject', name), '--in-place', '--update-aux', ovl],
                           capture_output=True, text=True)
        print(name, 'ok' if os.path.getmtime(ovl) > before else 'FAILED\n' + (r.stdout + r.stderr)[-800:])


def restore(quiet=False):
    for name, ovl in packs():
        d, b = os.path.dirname(ovl), bak(name)
        if not os.path.isdir(b): continue
        for f in os.listdir(d):
            if os.path.isfile(os.path.join(d, f)) and not os.path.exists(os.path.join(b, f)): os.remove(os.path.join(d, f))
        for f in os.listdir(b): shutil.copy2(os.path.join(b, f), d)
    if not quiet: print('restored original nature packs')


step = sys.argv[1] if len(sys.argv) > 1 else 'build'
if step in ('build', 'all'): build()
if step in ('install', 'all'): install()
if step == 'restore': restore()
