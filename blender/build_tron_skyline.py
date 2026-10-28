"""Rebel Tech Grid city in the dream-board style (Notion: Dream Board - Rebel Tech Grid): dark gloss armored towers
with proud glass bays and fins, RT red and blue neon edges (no cyan), lit setbacks, RT badges and bladed crowns,
fronted by neon shopfronts. Built for the edge of the park; blender/build_grid_park.py fills the middle.
Every piece stays inside 96 m (a 442 m asset crashed PC2 at startup); scale them up in game (to 1000%).
  rt-grid-spire       single armored tower with badge and antenna
  rt-grid-skyline-a/b 96 m city blocks (tower row + shopfront row); line them up along the boundary
  rt-grid-portal      guest entry portal: animated vortex disc between two glowing logo pillars
  rt-grid-glow-floor  lines-only emissive floor that blooms over the terrain grid
Object ids in build/tron-grid/make_pack.py are unchanged, so pieces already placed pick up the new look.
The old rt-grid-tower id now carries the End of WiFi Bar from build_grid_park.py.
Textures come from blender/make_city_textures.py (build/tron-grid/tex).
Run: blender -b --factory-startup -P blender/build_tron_skyline.py [-- preview]
The helpers are shared: build_grid_park.py imports this module (the pieces only build when it is run directly).
"""
import bpy, bmesh, json, sys, math, random
from pathlib import Path
out = Path(r'D:\RebelTechWorld\rebel-tech-theme-park\build\tron-grid'); out.mkdir(parents=True, exist_ok=True)
tex = out / 'tex'
RED, BLUE = (.776, .002, .008), (.0176, .0723, 1)  # #E10616, #244CFF (linear)
GLASS_TILE = (16.0, 12.0)  # metres per window-texture repeat (across, up)


def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    for c in list(bpy.data.curves): bpy.data.curves.remove(c)


def mat(n, c, e=0, rough=.12, metal=.4, image=None):
    m = bpy.data.materials.new(n); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    if image:
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(str(tex / image), check_existing=True)
        nt.links.new(t.outputs['Color'], p.inputs['Base Color']); nt.links.new(t.outputs['Color'], p.inputs['Emission Color'])
        p.inputs['Emission Strength'].default_value = e or 1
    elif e:
        p.inputs['Emission Color'].default_value = (*c, 1); p.inputs['Emission Strength'].default_value = e
    return m


def materials():
    return {'body': mat('City Body', (.004, .006, .012), rough=.1, metal=.7),
            'glass': mat('City Glass', (0, 0, 0), 2.5, rough=.05, metal=.8, image='city-windows.png'),
            'glow': mat('City Glow', BLUE, 20), 'soft': mat('City Glow Soft', RED, 6), 'red': mat('City Red', RED, 16),
            'blue': mat('City Blue', BLUE, 22), 'badge': mat('RT Badge', (0, 0, 0), 20, image='rt-badge.png'),
            'pulse': mat('City Pulse', (0, 0, 0), 7, image='pulse.png')}  # blinking beacons (make_pack.py scrolls it)


def pin_uv(o, u, band):
    """Pin every UV of o to one point: u is its phase on a scrolling texture, band its colour row (0 red, 1 blue, 2 white)."""
    for lp in o.data.uv_layers[0].data: lp.uv = (u % 1, 1 - (band + .5) / 4)
    return o


def link(me, m, name='part'):
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o


def loft(rings, m, cap=True):
    """Side surface through closed rings [(z, [(x, y), ...]), ...] (same point count), world-scaled facade UVs."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); n = len(rings[0][1])
    vs = [[bm.verts.new((x, y, z)) for x, y in pts] for z, pts in rings]
    for k in range(len(rings) - 1):
        z0, z1 = rings[k][0], rings[k + 1][0]; d = 0.0
        for i in range(n):
            j = (i + 1) % n
            f = bm.faces.new((vs[k][i], vs[k][j], vs[k + 1][j], vs[k + 1][i]))
            seg = (vs[k][j].co - vs[k][i].co).length
            for lp, (u, v) in zip(f.loops, ((d, z0), (d + seg, z0), (d + seg, z1), (d, z1))):
                lp[uvl].uv = (u / GLASS_TILE[0], v / GLASS_TILE[1])
            d += seg
    if cap:
        bm.faces.new(list(reversed(vs[0]))); bm.faces.new(vs[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('loft'); bm.to_mesh(me); return link(me, m)


def tube(points, r, m):
    """Glowing line along a 3D polyline (curve with a round bevel, converted to mesh)."""
    cu = bpy.data.curves.new('tube', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 1
    sp = cu.splines.new('POLY'); sp.points.add(len(points) - 1)
    for p, (x, y, z) in zip(sp.points, points): p.co = (x, y, z, 1)
    o = bpy.data.objects.new('tube', cu); bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.convert(target='MESH'); o.select_set(False)
    o.data.materials.append(m); return o


def rounded(w, d, r, seg=3):
    """Rounded-rectangle profile (counter-clockwise), corner radius r."""
    pts = []
    for cx, cy, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
        for s in range(seg + 1):
            a = math.radians(a0 + 90 * s / seg); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ellipse(w, d, n=24): return [(w / 2 * math.cos(2 * math.pi * i / n), d / 2 * math.sin(2 * math.pi * i / n)) for i in range(n)]


def tri(r, n=8):
    """Rounded triangle profile (Shanghai-tower style)."""
    pts = []
    for k in range(3):
        a0 = math.radians(90 + 120 * k)
        for s in range(n):
            a = a0 - math.radians(60) + math.radians(120) * s / n
            rr = r * (1 - .18 * math.cos(3 * (a - a0)) ** 2)
            pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def xform(pts, x, y, s=1.0, rot=0.0):
    c, sn = math.cos(rot), math.sin(rot)
    return [(x + s * (px * c - py * sn), y + s * (px * sn + py * c)) for px, py in pts]


def tower(x, y, h, profile, M, twist=0.0, taper=1.0, steps=12, spine=0, bands=True, crown=True):
    """Generic modern tower: profile lofted up h metres, twisting `twist` radians and scaling to `taper` at the top.
    `spine` glowing lines, evenly spaced round the profile, follow the twist; LED floor bands and a crown."""
    rings = [(h * k / steps, xform(profile, x, y, 1 - (1 - taper) * k / steps, twist * k / steps)) for k in range(steps + 1)]
    loft(rings, M['glass'])
    for i in (round(k * len(profile) / spine) % len(profile) for k in range(spine)):
        tube([(px[i][0], px[i][1], z) for z, px in rings], .35, M['glow'])
    if bands:
        for k in range(2, steps, 3):
            z, pts = rings[k]; grow = xform(profile, x, y, (1 - (1 - taper) * k / steps) * 1.03, twist * k / steps)
            loft([(z, grow), (z + .45, grow)], M['soft'], cap=False)
    if crown:
        z, pts = rings[-1]; inner = xform(profile, x, y, taper * .7, twist)
        loft([(z, pts), (z + 3, inner)], M['body'])
        tube([(px, py, z + .2) for px, py in pts] + [(pts[0][0], pts[0][1], z + .2)], .45, M['glow'])
    return rings[-1][0] + (3 if crown else 0)


def slant(x, y, w, d, h, cut, M, flip=1):
    """Slant-top tower: rounded slab with a diagonal roof; the cut edge glows."""
    base = rounded(w, d, min(w, d) * .2)
    top = [(x + px, y + py, h - cut * (.5 + flip * px / w)) for px, py in base]  # roof slopes across local x
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    lo = [bm.verts.new((px, py, 0)) for px, py in xform(base, x, y)]; hi = [bm.verts.new(p) for p in top]; n = len(lo); d0 = 0.0
    for i in range(n):
        j = (i + 1) % n; f = bm.faces.new((lo[i], lo[j], hi[j], hi[i])); seg = (lo[j].co - lo[i].co).length
        for lp, (u, v) in zip(f.loops, ((d0, 0), (d0 + seg, 0), (d0 + seg, hi[j].co.z), (d0, hi[i].co.z))):
            lp[uvl].uv = (u / GLASS_TILE[0], v / GLASS_TILE[1])
        d0 += seg
    bm.faces.new(list(reversed(lo))); bm.faces.new(hi); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new('slant'); bm.to_mesh(me); link(me, M['glass'])
    tube(top + [top[0]], .4, M['glow'])
    for px, py in xform([(w / 2, d / 2), (-w / 2, d / 2), (-w / 2, -d / 2), (w / 2, -d / 2)], x, y, .985):
        tube([(px, py, 0), (px, py, h - cut * (.5 + flip * (px - x) / w))], .2, M['soft'])


def shard(x, y, w, h, M):
    """Shard: four leaning glass sails that taper to a split glowing tip."""
    pts = [(w / 2, 0), (0, w / 2), (-w / 2, 0), (0, -w / 2)]
    rings = [(h * k / 6, xform(pts, x + .04 * w * k / 6, y, 1 - .9 * k / 6, .25 * k / 6)) for k in range(7)]
    loft(rings, M['glass'])
    for i in range(4): tube([(r[1][i][0], r[1][i][1], r[0]) for r in rings], .3, M['glow'])
    tube([(x + .04 * w, y, h), (x + .04 * w, y, h + 6)], .25, M['glow'])


def podium(x, y, w, d, h, M):
    loft([(0, rounded(w, d, 3)), (h, rounded(w, d, 3))], M['body'])
    p = [(px + x, py + y) for px, py in rounded(w + .4, d + .4, 3)]
    for z in (.3, h - .3): tube([(px, py, z) for px, py in p] + [(p[0][0], p[0][1], z)], .25, M['glow'])


def join(name):
    bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join(); o = bpy.context.object; o.name = name
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.export_scene.gltf(filepath=str(out / (name + '.glb')), export_format='GLB', use_selection=True)
    return {'name': name, 'dims_m': [round(v, 2) for v in o.dimensions], 'tris': sum(len(p.vertices) - 2 for p in o.data.polygons),
            'materials': [m.name for m in o.data.materials]}  # make_pack.py lists exactly these


def panel(x, y, z, w, h, face, m, inset=0.0):
    """Flat facade panel (world-UV'd via loft) on the front (face=-1, -y) or back (face=1) of a block."""
    pts = [(x - w / 2, y + face * inset), (x + w / 2, y + face * inset), (x + w / 2, y + face * (inset + .05)), (x - w / 2, y + face * (inset + .05))]
    return loft([(z, pts), (z + h, pts)], m)


def armored(x, y, w, d, h, M, rnd, logo=False, neon=None):
    """Dream-board tower: dark chamfered core with proud glass bays, facade fins, red/blue neon edges,
    lit setback cornices, an RT badge on the front and a bladed crown with a beacon."""
    neon = neon or rnd.choice(('blue', 'red', 'blue'))
    tiers = rnd.choice((2, 3, 3)); z = 0.0
    for k in range(tiers):
        f = 1 - .15 * k; ww, dd = w * f, d * f
        th = h * (.55 if k == 0 else .45 / (tiers - 1))
        prof = xform(rounded(ww, dd, min(ww, dd) * .14, 1), x, y)
        loft([(z, prof), (z + th, prof)], M['body'])
        for face in (-1, 1):  # glass bays on front and back with slim vertical fins over them
            panel(x, y + face * dd / 2, z + 1.2, ww * .72, th - 2.4, face, M['glass'], .15)
            for i in range(1, 6):
                box(x - ww * .36 + ww * .72 * i / 6, y + face * (dd / 2 + .45), z + 1.2, .25, .6, th - 2.4, M['body'])
        for side in (-1, 1):  # narrower glass bays on the sides
            sx = x + side * (ww / 2 + .15)
            pts = [(sx, y - dd * .3), (sx, y + dd * .3), (sx + side * .05, y + dd * .3), (sx + side * .05, y - dd * .3)]
            loft([(z + 1.2, pts), (z + th - 1.2, pts)], M['glass'])
        for cx, cy in ((ww / 2, dd / 2), (-ww / 2, dd / 2), (ww / 2, -dd / 2), (-ww / 2, -dd / 2)):  # neon on the chamfers
            tube([(x + cx * .97, y + cy * .97, z), (x + cx * .97, y + cy * .97, z + th)], .28, M[neon if cy < 0 else 'blue'])
        ring = xform(rounded(ww + .6, dd + .6, min(ww, dd) * .14, 1), x, y)
        tube([(px, py, z + th - .3) for px, py in ring] + [(ring[0][0], ring[0][1], z + th - .3)], .3, M['blue'])
        if k == 0:
            tube([(px, py, 1.0) for px, py in ring] + [(ring[0][0], ring[0][1], 1.0)], .25, M['red'])
            if logo:
                s = min(ww * .55, th * .3, 18); sign(x, y - dd / 2 - .9, z + th - s - 3, s, M['badge'])
        z += th
    cw, cd = w * (1 - .15 * tiers), d * (1 - .15 * tiers)
    for side in (-1, 1):  # crown blades
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + side * cw * .22, y, z + cw * .35), rotation=(0, side * .35, 0))
        o = bpy.context.object; o.dimensions = (cw * .12, cd * .8, cw * .8)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True); o.data.materials.append(M['body'])
        tube([(x + side * cw * .22, y - cd * .4, z), (x + side * cw * .5, y - cd * .4, z + cw * .7)], .2, M[neon])
    tube([(x, y, z), (x, y, z + rnd.uniform(6, 16))], .25, M['blue'])
    pin_uv(box(x, y, z + 5, .9, .9, .7, M['pulse']), x * .37 + y * .11, 0)  # aircraft beacon, blinking out of step with its neighbours
    return z


def storefront(x, y, w, d, h, M, face=-1):
    """Low podium building: glass shopfront, red-over-blue neon fascia, RT badges at each end."""
    prof = xform(rounded(w, d, 1.2, 1), x, y)
    loft([(0, prof), (h, prof)], M['body'])
    panel(x, y + face * d / 2, .3, w * .8, h * .55, face, M['glass'], .1)
    for zz, m in ((h * .62, 'red'), (h * .72, 'blue')):
        tube([(x - w / 2, y + face * (d / 2 + .3), zz), (x + w / 2, y + face * (d / 2 + .3), zz)], .22, M[m])
    for s in (-1, 1):
        sign(x + s * (w / 2 - h * .25), y + face * (d / 2 + .35), h * .2, h * .4, M['badge'], back=face > 0)
    tube([(px, py, h) for px, py in prof] + [(prof[0][0], prof[0][1], h)], .2, M['blue'])


def needle():
    clear(); M = materials(); rnd = random.Random(9)
    z = armored(0, 0, 14, 14, 78, M, rnd, logo=True, neon='red')
    tube([(0, 0, z), (0, 0, 95)], .3, M['blue'])
    return join('rt-grid-spire')


def skyline(name, seed):
    """96 m city block: a back row of armored towers and a front row of neon shopfronts."""
    clear(); M = materials(); rnd = random.Random(seed)
    x, k = -46.0, 0
    while x < 44:
        w = min(rnd.choice((12, 14, 16, 18)), 46 - x)
        if w < 8: break
        armored(x + w / 2, 4 + rnd.uniform(-2, 2), w - 2, rnd.uniform(11, 15), rnd.uniform(40, 82), M, rnd, logo=(k % 2 == 0))
        x += w; k += 1
    x = -46.0
    while x < 40:
        w = min(rnd.choice((14, 18, 22)), 46 - x)
        storefront(x + w / 2, -9, w - 2, 7, rnd.uniform(6, 9), M); x += w
    tube([(-48, -13.5, .2), (48, -13.5, .2)], .25, M['blue'])
    return join(name)


def disc(x, y, z, R, m, rings=10, seg=72):
    """Vertical disc facing -y, both sides, polar UVs: U = angle (0..1 around), V = radius. Scrolling U spins it."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    for side in (-1, 1):
        grid = [[bm.verts.new((x + R * (k / rings) * math.cos(2 * math.pi * i / seg), y + side * .05, z + R * (k / rings) * math.sin(2 * math.pi * i / seg)))
                 for i in range(seg + 1)] for k in range(1, rings + 1)]
        centre = bm.verts.new((x, y + side * .05, z))
        def put(f, uvs):
            if side > 0: f.normal_flip()
            for lp, uv in zip(f.loops, uvs if side < 0 else list(reversed(uvs))): lp[uvl].uv = uv
        for i in range(seg):
            put(bm.faces.new((centre, grid[0][i], grid[0][i + 1])), ((i / seg + .5 / seg, 0), (i / seg, 1 / rings), ((i + 1) / seg, 1 / rings)))
            for k in range(rings - 1):
                put(bm.faces.new((grid[k][i], grid[k + 1][i], grid[k + 1][i + 1], grid[k][i + 1])),
                    ((i / seg, (k + 1) / rings), (i / seg, (k + 2) / rings), ((i + 1) / seg, (k + 2) / rings), ((i + 1) / seg, (k + 1) / rings)))
    me = bpy.data.meshes.new('disc'); bm.to_mesh(me); return link(me, m, 'disc')


def sign(x, y, z, s, m, back=False):
    """Logo facing -y (or +y when back), s square, base at z. The RT badge is cut to its circle (a round
    plate, no black square and no alpha needed); other logos stay square planes."""
    if m.name == 'RT Badge':
        bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); R = .43 * s; n = 40; flip = -1 if back else 1
        f = bm.faces.new([bm.verts.new((x + flip * R * math.cos(2 * math.pi * k / n), y, z + s / 2 + R * math.sin(2 * math.pi * k / n))) for k in range(n)])
        for k, lp in enumerate(f.loops):
            lp[uvl].uv = (.5 + R * math.cos(2 * math.pi * k / n) / s, .5 + R * math.sin(2 * math.pi * k / n) / s)
        me = bpy.data.meshes.new('badge'); bm.to_mesh(me); return link(me, m, 'badge')
    bpy.ops.mesh.primitive_plane_add(size=s, location=(x, y, z + s / 2), rotation=(math.pi / 2, 0, math.pi if back else 0))
    o = bpy.context.object; bpy.ops.object.transform_apply(location=False, rotation=True, scale=True); o.data.materials.append(m); return o


def box(x, y, z, w, d, h, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + h / 2)); o = bpy.context.object; o.dimensions = (w, d, h)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(m); return o


def portal():
    clear(); M = materials()
    M['vortex'] = mat('Portal Vortex', (0, 0, 0), 8, image='portal-vortex.png'); M['logo'] = mat('RT Logo', (0, 0, 0), 30, image='rt-logo-sign.png')
    podium(0, 0, 62, 18, .6, M)
    C = 14.5
    ring = [(17 * math.cos(2 * math.pi * i / 72), 17 * math.sin(2 * math.pi * i / 72)) for i in range(72)]
    for r, m, t in ((15.2, M['body'], 1.6), (13.4, M['glow'], .5), (16.9, M['soft'], .3)):
        pts = [(r * math.cos(2 * math.pi * i / 72), 0, C + r * math.sin(2 * math.pi * i / 72)) for i in range(73)]
        for dy in ((0,) if r < 16 else (-1.7, 1.7)): tube([(px, dy, pz) for px, _, pz in pts], t, m)
    del ring
    for k in range(16):
        a = 2 * math.pi * k / 16
        bpy.ops.mesh.primitive_cube_add(size=1, location=(17.3 * math.cos(a), 0, C + 17.3 * math.sin(a)), rotation=(0, -a, 0))
        o = bpy.context.object; o.dimensions = (2.2, 4.2, 3.2); bpy.ops.object.transform_apply(location=False, rotation=True, scale=True); o.data.materials.append(M['body'])
    disc(0, 0, C, 13.2, M['vortex'])
    for s in (-1, 1):  # logo pillars: badge on front and back, framed in glowing lines like the grid
        px = s * 25
        loft([(.6, xform(rounded(13, 6, 1.2), px, 0)), (31.6, xform(rounded(11, 5, 1.2), px, 0))], M['body'])
        for dy in (-3.06, 3.06):
            sign(px, dy, 15, 12, M['logo'], back=dy > 0)
            fy = dy * 1.004
            tube([(px - 6.4, fy, 14.6), (px + 6.4, fy, 14.6), (px + 6.4, fy, 27.4), (px - 6.4, fy, 27.4), (px - 6.4, fy, 14.6)], .25, M['glow'])
            tube([(px - 5, fy, 3), (px + 5, fy, 3), (px + 5, fy, 12), (px - 5, fy, 12), (px - 5, fy, 3)], .15, M['soft'])
        tube([(px, 0, 31.6), (px, 0, 37)], .25, M['glow']); box(px, 0, 36.6, 1, 1, .7, M['red'])
        box(s * 18.5, 0, .6, 2.5, 4, C - 1, M['body'])
    tube([(-13, -9, .75), (13, -9, .75)], .15, M['glow'])  # threshold light-line where guests step out
    return join('rt-grid-portal')


def glow_floor():
    """Lines only, no slab: lays over the terrain grid so the floor itself blooms; each line is RT red or blue at random."""
    clear(); M = materials(); rnd = random.Random(4)
    for i in range(25):
        a = -48.0 + i * 4.0; w = .12 if i % 4 == 0 else .05
        box(a, 0, 0, w, 96, .03, M[rnd.choice(('glow', 'glow', 'red'))]); box(0, a, 0, 96, w, .03, M[rnd.choice(('glow', 'glow', 'red'))])
    return join('rt-grid-glow-floor')


if __name__ == '__main__':
    manifest = [needle(), skyline('rt-grid-skyline-a', 7), skyline('rt-grid-skyline-b', 23), portal(), glow_floor()]
    (out / 'skyline-manifest.json').write_text(json.dumps(manifest, indent=2)); print('TRON_SKYLINE', json.dumps(manifest))

if __name__ == '__main__' and 'preview' in sys.argv:
    clear()
    for n, x, y in (('rt-grid-skyline-a', -150, 60), ('rt-grid-skyline-b', 150, 60),
                    ('rt-grid-spire', -70, 70), ('rt-grid-spire', 70, 70), ('rt-grid-portal', 0, -20)):
        bpy.ops.import_scene.gltf(filepath=str(out / (n + '.glb'))); bpy.context.selected_objects[0].location = (x, y, 0)
    bpy.ops.mesh.primitive_plane_add(size=900, location=(0, 0, 0)); bpy.context.object.data.materials.append(mat('Floor', (.002, .003, .004)))
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE_NEXT'; sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    w = bpy.data.worlds.new('Sky'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.01, .05, .08, 1); sc.world = w
    cam = bpy.data.cameras.new('Cam'); co = bpy.data.objects.new('Cam', cam); bpy.context.collection.objects.link(co); sc.camera = co
    co.location = (0, -190, 24); co.rotation_euler = (math.radians(83), 0, 0); cam.lens = 30
    sun = bpy.data.lights.new('Sun', 'SUN'); sun.energy = 2; so = bpy.data.objects.new('Sun', sun); bpy.context.collection.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(30))
    sc.view_settings.view_transform = 'AgX'
    sc.use_nodes = True; nt = sc.node_tree; rl = nt.nodes['Render Layers']; comp = nt.nodes['Composite']
    g = nt.nodes.new('CompositorNodeGlare'); g.glare_type = 'FOG_GLOW'
    nt.links.new(rl.outputs['Image'], g.inputs['Image']); nt.links.new(g.outputs['Image'], comp.inputs['Image'])
    sc.render.filepath = str(out / 'skyline-preview.png'); bpy.ops.render.render(write_still=True); print('PREVIEW_DONE')
