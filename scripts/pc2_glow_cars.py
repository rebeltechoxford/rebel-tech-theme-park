"""Glowing coaster trains: make each coaster car's paint channel 1 emissive in its customised colour.
Track rails use an extrusion shader with no emissive input, so trains (and our neon scenery) carry the light.
Run with the cobra-venv Python while the game is closed:
  python pc2_glow_cars.py build|install|all|restore
Originals are backed up once per car folder to build/backups/pc2/glow-cars-original.
"""
import os, re, sys, shutil, subprocess

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.join(repo, 'build', 'glow-cars')
backup = os.path.join(repo, 'build', 'backups', 'pc2', 'glow-cars-original')
cars = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\Win64\ovldata\Content0\Rides\Coasters\Cars'
cobra = r'D:\RebelTechWorld\tools\cobra-tools\ovl_tool_cmd.py'
py = r'D:\RebelTechWorld\tools\cobra-venv\Scripts\python.exe'
INTENSITY = '6.0'
SKIP = ('decal', 'rubber', 'glass', 'logo', 'wheel', 'tyre', 'tire')


def ovls():
    for car in sorted(os.listdir(cars)):
        p = os.path.join(cars, car, car + '.ovl')
        if os.path.exists(p): yield car, p


def cobra_run(*args):
    return subprocess.run([py, cobra, *args], capture_output=True, text=True)


def set_attr(xml, name, value):
    return re.sub(r'(<attribinfo name="' + name + r'"[^>]*>\s*<value>)[^<]*', lambda m: m.group(1) + value, xml)


def build():
    shutil.rmtree(here, ignore_errors=True)
    for car, ovl in ovls():
        src = os.path.join(here, 'src', car); dst = os.path.join(here, 'inject', car)
        bak = os.path.join(backup, car)
        cobra_run('extract', '-g', 'Planet Coaster 2', '--type', '.fgm', '-o', src, os.path.join(bak, car + '.ovl') if os.path.isdir(bak) else ovl)
        n = 0
        for f in os.listdir(src) if os.path.isdir(src) else ():
            xml = open(os.path.join(src, f)).read()
            if not f.endswith('.fgm') or any(s in f for s in SKIP) or 'Channel1EnableEmissive' not in xml: continue
            xml = set_attr(xml, 'pCustomisation_Channel1EnableEmissive', '1')
            xml = set_attr(xml, 'pCustomisation_EmissiveFallbackIntensity', INTENSITY)
            os.makedirs(dst, exist_ok=True); open(os.path.join(dst, f), 'w').write(xml); n += 1
        print(car, n, 'materials')


def install():
    for car, ovl in ovls():
        d, b = os.path.dirname(ovl), os.path.join(backup, car)
        if not os.path.isdir(b):
            shutil.copytree(d, b)
    restore(quiet=True)
    for car, ovl in ovls():
        folder = os.path.join(here, 'inject', car)
        if not os.path.isdir(folder): continue
        before = os.path.getmtime(ovl)
        r = cobra_run('inject', '-g', 'Planet Coaster 2', '-i', folder, '--in-place', '--update-aux', ovl)
        ok = os.path.getmtime(ovl) > before  # cobra's console output is not reliable to parse
        print(car, 'ok' if ok else 'FAILED\n' + (r.stdout + r.stderr)[-800:])


def restore(quiet=False):
    for car, ovl in ovls():
        d, b = os.path.dirname(ovl), os.path.join(backup, car)
        if not os.path.isdir(b): continue
        for f in os.listdir(d):
            if not os.path.exists(os.path.join(b, f)): os.remove(os.path.join(d, f))
        for f in os.listdir(b): shutil.copy2(os.path.join(b, f), d)
    if not quiet: print('restored original coaster cars')


step = sys.argv[1] if len(sys.argv) > 1 else 'build'
if step in ('build', 'all'): build()
if step in ('install', 'all'): install()
if step == 'restore': restore()
