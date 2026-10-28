"""THE GRID look: navy night colour grade that keeps RT red and blue saturated, stronger bloom, navy sky/haze,
invisible guest coaches, and invisible vanilla turnstiles (the RT Grand Gate scenery stands over them, so
guests are admitted through it; the turnstiles still work, only their model is shrunk to a speck).
Edits GameMain/Main.ovl (LUT, render parameters, day-night curves), the coach guest-spawner OVL and PE_MainGate.
Run with the cobra-venv Python while the game is closed:
  python pc2_grid_look.py build|install|all|restore
Originals are backed up once to build/backups/pc2/grid-look-original and restored before every install.
"""
import os, re, sys, shutil, subprocess
import numpy as np

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.join(repo, 'build', 'grid-look')
research = os.path.join(repo, 'build', 'biome-research')
backup = os.path.join(repo, 'build', 'backups', 'pc2', 'grid-look-original')
ovldata = r'D:\SteamLibrary\steamapps\common\Planet Coaster 2\Win64\ovldata'
cobra = r'D:\RebelTechWorld\tools\cobra-tools\ovl_tool_cmd.py'
py = r'D:\RebelTechWorld\tools\cobra-venv\Scripts\python.exe'
GAMEMAIN = os.path.join(ovldata, 'GameMain', 'Main.ovl')
COACH = os.path.join(ovldata, r'Content0\Environment\Scenery\Facilities\Unstaffed\Facility_GuestSpawner_Coach\Facility_GuestSpawner_Coach.ovl')
GATE = os.path.join(ovldata, r'Content0\Environment\Scenery\Facilities\Unstaffed\PE_MainGate\PE_MainGate.ovl')
TARGETS = [(GAMEMAIN, 'inject-gamemain'), (COACH, 'inject-coach'), (GATE, 'inject-maingate')]

# render parameter overrides (attribute -> value text)
VIEW = {
    'View.HighFilter.Filter.Threshold': '0.6', 'View.HighFilter.Filter.Scale': '1.2',
    'View.Bloom.BlendStrength': '0.85', 'View.Bloom.Radius': '0.75', 'View.Bloom.Saturation': '1.0',
    'View.Bloom.Weight.Band_0': '0.45', 'View.Bloom.Weight.Band_1': '0.4', 'View.Bloom.Weight.Band_2': '0.3',
    'View.Bloom.Weight.Band_3': '0.2', 'View.Bloom.Weight.Band_4': '0.12', 'View.Bloom.Weight.Band_5': '0.06',
    'View.Bloom.Tint.Band_3': '170 185 255 255', 'View.Bloom.Tint.Band_4': '120 140 255 255', 'View.Bloom.Tint.Band_5': '90 110 255 255',
    'View.Bloom.AnamorphicFlares.Tint': '70 100 255 0',
    'View.LookAdjust.Luminance.HistogramExposureAdjust': '-0.6',  # +1.9 EV over stock: rides must not read as silhouettes
    'View.GlobalIllumination.SkyIntensity': '3.0', 'View.GlobalIllumination.SunIntensity': '1.3',  # strong ambient fill
    'View.LookAdjust.ColourAdjust.Saturation': '1.2',
}
ATMOS = {
    'Atmospherics.Particles.Rayleigh.Beta': '3e-06 5e-06 2.4e-05',  # mostly blue scatter, a little red: navy-violet sky
    'Atmospherics.Fog.Albedo': '22 30 80 255',
    'Atmospherics.Lights.Moon.Scatter.Tint': '200 210 255 255',
    'Atmospherics.Lights.Sky.Intensity': '2.5', 'Atmospherics.Lights.Sky.Scatter.Intensity': '1.5',
    'Atmospherics.Clouds.Density': '0.0', 'Atmospherics.Clouds.Horizon.Density': '0.0',  # no cloud shadows blotching the grid
}
CURVES = {'Atmospherics.Sky.Albedo': ('70 90 210 255', '18 22 80 255'), 'Atmospherics.Haze.Albedo': ('80 85 190 255', '22 24 85 255')}


def set_params(xml, values):
    for name, v in values.items():
        pat = r'(<attribute_name>' + re.escape(name) + r'</attribute_name>\s*<data>\s*<data>)[^<]*'
        xml, n = re.subn(pat, lambda m: m.group(1) + v, xml)
        assert n == 1, name
    return xml


def set_curves(xml):
    for name, (day, night) in CURVES.items():
        m = re.search(r'<attribute_name>' + re.escape(name) + r'</attribute_name>.*?</samples>', xml, re.S)
        block = re.sub(r'(time="([\d.]+)".*?<data>)[^<]*', lambda s: s.group(1) + (night if float(s.group(2)) >= 1 else day), m.group(), flags=re.S)
        xml = xml[:m.start()] + block + xml[m.end():]
    return xml


def grade(c):
    """Rebel Grid grade: greys and dull colours pulled toward navy; saturated RT red and blue left alone;
    the brightest whites stay white (pure white streetlights); a little navy lifted into the blacks."""
    lum = c @ np.array([.2126, .7152, .0722])
    navy = np.clip(lum[:, None] * np.array([.62, .74, 1.35]), 0, 1)
    sat = c.max(1) - c.min(1)
    s = (.55 * (1 - np.clip(sat * 2.5, 0, 1)) * (1 - lum ** 3))[:, None]
    out = c * (1 - s) + navy * s + ((1 - lum) ** 4)[:, None] * np.array([.004, .006, .025])
    return np.clip(out, 0, 1)


def build():
    gm = os.path.join(here, 'inject-gamemain'); src = os.path.join(research, 'gamemain')
    shutil.rmtree(gm, ignore_errors=True); os.makedirs(gm)
    lines = open(os.path.join(src, 'gametemperate.cube')).read().splitlines()
    head = [l for l in lines if not re.match(r'^[\d.\-e ]+$', l) or not l.strip()]
    vals = np.array([[float(x) for x in l.split()] for l in lines if re.match(r'^[\d.\-e]+ [\d.\-e]+ [\d.\-e]+$', l)])
    assert len(vals) == 32 ** 3
    open(os.path.join(gm, 'gametemperate.cube'), 'w').write('\n'.join(head + [f'{r:.6f} {g:.6f} {b:.6f}' for r, g, b in grade(vals)]) + '\n')
    shutil.copy(os.path.join(src, 'gametemperate.lut'), gm)
    for f, values in (('renderparameters_view.renderparameters', VIEW), ('renderparameters_atmospherics.renderparameters', ATMOS)):
        open(os.path.join(gm, f), 'w').write(set_params(open(os.path.join(src, f)).read(), values))
    f = 'renderparametercurves_daytonight.renderparametercurves'
    open(os.path.join(gm, f), 'w').write(set_curves(open(os.path.join(src, f)).read()))
    # coaches: shrink the mesh to a speck so arriving buses are invisible
    sys.path.insert(0, os.path.dirname(cobra)); sys.argv = sys.argv[:1]
    import ovl_tool_cmd  # noqa: F401  (sets up cobra-tools logging)
    from generated.formats.ms2 import Ms2File
    co = os.path.join(here, 'inject-coach'); shutil.rmtree(co, ignore_errors=True); os.makedirs(co)
    m = Ms2File(); m.load(os.path.join(research, 'coach', 'facility_guestspawner_coach_.ms2'), read_editable=True)
    m.resize(0.01); m.save(os.path.join(co, 'facility_guestspawner_coach_.ms2'))
    # vanilla turnstiles: shrink the gate and turnstile models to a speck; admission, queueing and the
    # turnstile animations keep running, guests just appear to walk through the RT Grand Gate tunnel
    src = os.path.join(research, 'maingate')
    if not os.path.exists(os.path.join(src, 'models.ms2')):
        pristine = os.path.join(bak(GATE), 'PE_MainGate.ovl') if os.path.isdir(bak(GATE)) else GATE
        subprocess.run([py, cobra, 'extract', '-g', 'Planet Coaster 2', '--type', '.ms2', '-o', src, pristine], capture_output=True)
    mg = os.path.join(here, 'inject-maingate'); shutil.rmtree(mg, ignore_errors=True); os.makedirs(mg)
    m = Ms2File(); m.load(os.path.join(src, 'models.ms2'), read_editable=True)
    m.resize(0.01); m.save(os.path.join(mg, 'models.ms2'))
    print('built grid look in', here)


def bak(ovl): return os.path.join(backup, os.path.basename(os.path.dirname(ovl)))


def install():
    for ovl, _ in TARGETS:  # whole folder: inject also rewrites the .ovs/.aux side files
        d, b = os.path.dirname(ovl), bak(ovl)
        if not os.path.isdir(b):
            os.makedirs(b)
            for f in os.listdir(d):
                if os.path.isfile(os.path.join(d, f)): shutil.copy2(os.path.join(d, f), b)
    restore(quiet=True)
    for ovl, folder in TARGETS:
        r = subprocess.run([py, cobra, 'inject', '-g', 'Planet Coaster 2', '-i', os.path.join(here, folder), '--in-place', '--update-aux', ovl],
                           capture_output=True, text=True)
        print(os.path.basename(ovl), '\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'ERROR' in l or 'SUCCESS' in l or 'Traceback' in l))


def restore(quiet=False):
    for ovl, _ in TARGETS:
        d, b = os.path.dirname(ovl), bak(ovl)
        if not os.path.isdir(b): continue
        for f in os.listdir(d):
            if os.path.isfile(os.path.join(d, f)) and not os.path.exists(os.path.join(b, f)): os.remove(os.path.join(d, f))
        for f in os.listdir(b): shutil.copy2(os.path.join(b, f), d)
    if not quiet: print('restored original GameMain and coach OVLs')


step = sys.argv[1] if len(sys.argv) > 1 else 'build'
if step in ('build', 'all'): build()
if step in ('install', 'all'): install()
if step == 'restore': restore()
