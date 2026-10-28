"""Rebel Tech Grid theme park: fills the middle of THE GRID in the dream-board style
(Notion: Dream Board - Rebel Tech Grid), leaving open lots and boulevards for the owner's coasters.
  rt-park-gate        REBEL TECH THEME PARK grand gate: chevron arch crowned by the spinning RT atom, LED towers,
                      swept wings and a hex tunnel. It sits over the vanilla turnstiles (scripts/pc2_grid_look.py
                      shrinks their model out of sight), so guests are admitted through it exactly as before.
                      Origin = turnstile line; outside is -y, the tunnel runs 24 m into the park (+y).
  rt-end-of-wifi-bar  the End of WiFi Bar: skyscraper castle at the heart of the park. Mall podium with eight
                      venue bays (food, drinks, souvenirs), castle turrets, sky terraces, the sky bar and an
                      animated RT atom crown. Carries the old rt-grid-tower id.
  rt-park-center      192 x 192 m hub behind the gate: medallion plaza, RT atom monument, Rebel Tech Arcade,
                      Rebel Tech Gear, Fuel Up, Control Room, fountain lagoon and bridge, lit boulevards
  rt-park-district-a  192 x 96 m neon district: tower row, lit shopfronts, street furniture, open cross street
  rt-park-district-b  second district variant with a data-core dome
Animated through emissive scroll (make_pack.py ANIMATED): electrons orbit the atoms, data packets race along
the neon lines, beacons blink, tickers scroll, fountain jets rise and the lagoon ripples.
Modelled at real scale and exported at half size, because pieces must stay inside 96 m (a 442 m asset
crashed PC2 at startup): place them in game at 200% and guests, doors and signs come out life-size.
Helpers come from build_tron_skyline.py; textures from blender/make_city_textures.py.
Run: blender -b --factory-startup -P blender/build_grid_park.py [-- preview aerial|street|gate]
"""
import bpy, bmesh, json, sys, math, random
from mathutils import Matrix, Vector
sys.path.insert(0, r'D:\RebelTechWorld\rebel-tech-theme-park\blender')
from build_tron_skyline import (out, RED, mat, materials, link, loft, tube, rounded, ellipse, xform, armored, storefront, sign, box,
                                clear, panel, pin_uv)

EXPORT_SCALE = .5  # place at 200% in game
SIGNS = {'rebel tech': ('signs', 0), 'arcade': ('signs', 1), 'gear': ('signs', 2), 'fuel up': ('signs', 3), 'eats': ('signs', 4),
         'control room': ('signs', 5), 'theme park': ('signs', 6), 'tagline': ('signs', 7),
         'end of wifi bar': ('venues', 0), 'byte burgers': ('venues', 1), 'firewall grill': ('venues', 2), 'pixel pizza': ('venues', 3),
         '404 noodles': ('venues', 4), 'overclock coffee': ('venues', 5), 'bandwidth brews': ('venues', 6), 'cache & carry': ('venues', 7)}
BAND = {'red': 0, 'blue': 1, 'white': 2}  # colour rows of the animated textures


def park_materials():
    M = materials()
    M.update({'signs': mat('RT Signs', (0, 0, 0), 20, image='rt-signs.png'), 'venues': mat('RT Venue Signs', (0, 0, 0), 20, image='rt-signs-venues.png'),
              'medallion': mat('RT Medallion', (0, 0, 0), 10, image='rt-medallion.png'),
              'water': mat('City Water', (0, 0, 0), 3, rough=.03, metal=.6, image='city-water.png'),
              'white': mat('City White', (1, 1, 1), 25), 'canopy': mat('City Canopy', RED, 1.5, rough=.5, metal=0),
              'leaf': mat('City Foliage', (.004, .02, .012), rough=.7, metal=0),
              'orbit': mat('Atom Orbit', (0, 0, 0), 13, image='atom-orbit.png'), 'chase': mat('Data Chase', (0, 0, 0), 11, image='data-chase.png'),
              'jet': mat('Fountain Jet', (0, 0, 0), 9, image='fountain-jet.png'), 'ticker': mat('RT Ticker', (0, 0, 0), 17, image='rt-ticker.png')})
    return M


def placed(x, y, rot, fn, *a, **k):
    """Build fn at the origin (front facing -y), then move it to (x, y) turned rot radians about z."""
    before = set(bpy.data.objects); r = fn(*a, **k)
    T = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(rot, 4, 'Z')
    for o in set(bpy.data.objects) - before: o.matrix_world = T @ o.matrix_world
    return r


def strip(x, y, z, w, name, M, face=-1):
    """Sign from an RT atlas: w wide, w/4 tall, base at z, facing -y (face=1: facing +y)."""
    atlas, row = SIGNS[name]; h, v0 = w / 4, 1 - (row + 1) / 8
    xs = (x - w / 2, x + w / 2) if face < 0 else (x + w / 2, x - w / 2)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    f = bm.faces.new([bm.verts.new(p) for p in ((xs[0], y, z), (xs[1], y, z), (xs[1], y, z + h), (xs[0], y, z + h))])
    for lp, uv in zip(f.loops, ((0, v0), (1, v0), (1, v0 + 1 / 8), (0, v0 + 1 / 8))): lp[uvl].uv = uv
    me = bpy.data.meshes.new('strip'); bm.to_mesh(me); return link(me, M[atlas], 'strip')


def flat(pts, z, m, uv_box=None):
    """Horizontal face through pts at height z; UVs map uv_box (x0, y0, x1, y1) onto 0..1 (default: world/16 m)."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    f = bm.faces.new([bm.verts.new((px, py, z)) for px, py in pts])
    for lp in f.loops:
        px, py = lp.vert.co.x, lp.vert.co.y
        lp[uvl].uv = ((px - uv_box[0]) / (uv_box[2] - uv_box[0]), (py - uv_box[1]) / (uv_box[3] - uv_box[1])) if uv_box else (px / 16, py / 16)
    f.normal_update()
    if f.normal.z < 0: f.normal_flip()
    me = bpy.data.meshes.new('flat'); bm.to_mesh(me); return link(me, m, 'flat')


def ribbon(pts, r, m, band, u_of, k=6, normal=None):
    """Tube along pts with UVs for a scrolling texture: U = u_of(i, length so far), V wraps the tube in colour band."""
    P = [Vector(p) for p in pts]; n = len(P) - 1
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); v0 = 1 - (BAND[band] + 1) / 4; rings, L = [], [0.0]
    for i in range(1, n + 1): L.append(L[-1] + (P[i] - P[i - 1]).length)
    for i, p in enumerate(P):
        t = (P[min(i + 1, n)] - P[max(i - 1, 0)]).normalized()
        ref = normal or (Vector((1, 0, 0)) if abs(t.z) > .9 else Vector((0, 0, 1)))  # steady frame, no twisting
        a = ref.cross(t).normalized(); b = t.cross(a)
        rings.append([bm.verts.new(p + r * (math.cos(2 * math.pi * j / k) * a + math.sin(2 * math.pi * j / k) * b)) for j in range(k + 1)])
    for i in range(n):
        for j in range(k):
            f = bm.faces.new((rings[i][j], rings[i][j + 1], rings[i + 1][j + 1], rings[i + 1][j]))
            for lp, (ii, jj) in zip(f.loops, ((i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j))):
                lp[uvl].uv = (u_of(ii, L[ii]), v0 + .25 * jj / k)
    bm.normal_update()
    me = bpy.data.meshes.new('ribbon'); bm.to_mesh(me); return link(me, m, 'ribbon')


def chase(pts, M, band, r=.12, period=10.0):
    """Neon line with data packets racing along it (one texture repeat every `period` metres)."""
    return ribbon(pts, r, M['chase'], band, lambda i, l: l / period)


def chase_ring(x, y, z, rx, M, band, r=.15, ry=None, n=64):
    ry = ry or rx; per = 2 * math.pi * max(rx, ry) / max(1, round(2 * math.pi * max(rx, ry) / 12))  # whole repeats round the ring
    return chase([(x + rx * math.cos(2 * math.pi * i / n), y + ry * math.sin(2 * math.pi * i / n), z) for i in range(n + 1)], M, band, r, per)


def orbit(c, U, V, M, band, r=.4, n=72):
    """Animated atom orbit round centre c along cos(t)U + sin(t)V: U runs once round, so the texture's single
    electron (with its comet tail) circles the nucleus as the emissive scrolls."""
    c, U, V = Vector(c), Vector(U), Vector(V)
    return ribbon([c + math.cos(2 * math.pi * i / n) * U + math.sin(2 * math.pi * i / n) * V for i in range(n + 1)], r, M['orbit'], band,
                  lambda i, l: i / n, 8, U.cross(V).normalized())


def tilted(c, a, b, tilt, spin, M, band, r=.35):
    """Orbit of radii a x b, tilted `tilt` about x then spun `spin` about z (rings round a dome)."""
    U = (a * math.cos(spin), a * math.sin(spin), 0)
    V = (-b * math.sin(spin) * math.cos(tilt), b * math.cos(spin) * math.cos(tilt), b * math.sin(tilt))
    return orbit(c, U, V, M, band, r)


def ring(x, y, z, r, m, t=.3, n=48, ry=None):
    ry = ry or r
    tube([(x + r * math.cos(2 * math.pi * i / n), y + ry * math.sin(2 * math.pi * i / n), z) for i in range(n + 1)], t, m)


def ball(x, y, z, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=r, location=(x, y, z)); o = bpy.context.object; o.data.materials.append(m); return o


def beacon(x, y, z, M, band='red', r=.6):
    """Blinking light: its phase comes from where it stands, so neighbours blink in turn."""
    return pin_uv(ball(x, y, z, r, M['pulse']), x * .13 + y * .07 + z * .05, BAND[band])


def jet(x0, y0, x1, y1, h, M, r=.09):
    """Fountain jet: water streaks rising (U runs up the jet)."""
    return ribbon([(x0, y0, .2), (x1, y1, h)], r, M['jet'], 'white', lambda i, l: -l / 4, 5)


def ticker(cx, cy, z, w, rowv, M, h=1.6, face=-1):
    """LED ticker band facing -y: the message scrolls along it (U = metres / sign length)."""
    xs = (cx - w / 2, cx + w / 2) if face < 0 else (cx + w / 2, cx - w / 2); v0 = 1 - (rowv + 1) / 8
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    f = bm.faces.new([bm.verts.new(p) for p in ((xs[0], cy, z), (xs[1], cy, z), (xs[1], cy, z + h), (xs[0], cy, z + h))])
    for lp, uv in zip(f.loops, ((0, v0), (w / (h * 8), v0), (w / (h * 8), v0 + 1 / 8), (0, v0 + 1 / 8))): lp[uvl].uv = uv
    me = bpy.data.meshes.new('ticker'); bm.to_mesh(me); return link(me, M['ticker'], 'ticker')


def ticker_ring(cx, cy, z, R, rowv, M, h=1.6, n=48):
    """Cylindrical LED ticker facing outwards (U = metres round / sign length)."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); v0 = 1 - (rowv + 1) / 8; C = 2 * math.pi * R
    lo = [bm.verts.new((cx + R * math.cos(-2 * math.pi * i / n), cy + R * math.sin(-2 * math.pi * i / n), z)) for i in range(n + 1)]
    hi = [bm.verts.new((v.co.x, v.co.y, z + h)) for v in lo]
    for i in range(n):
        f = bm.faces.new((lo[i], lo[i + 1], hi[i + 1], hi[i]))
        for lp, (ii, top) in zip(f.loops, ((i, 0), (i + 1, 0), (i + 1, 1), (i, 1))): lp[uvl].uv = (C * ii / n / (h * 8), v0 + top / 8)
    bm.normal_update(); me = bpy.data.meshes.new('ticker'); bm.to_mesh(me); return link(me, M['ticker'], 'ticker')


def prism(profile, y0, y1, m):
    """Closed x-z profile extruded from y0 to y1 (walls, arches without holes)."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    a = [bm.verts.new((x, y0, z)) for x, z in profile]; b = [bm.verts.new((x, y1, z)) for x, z in profile]; n = len(profile)
    faces = [bm.faces.new(list(reversed(a))), bm.faces.new(b)] + [bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i])) for i in range(n)]
    for f in faces:
        for lp in f.loops: lp[uvl].uv = ((lp.vert.co.x + lp.vert.co.y) / 16, lp.vert.co.z / 12)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); me = bpy.data.meshes.new('prism'); bm.to_mesh(me); return link(me, m, 'prism')


def arch(outer, inner, y0, y1, m):
    """Thick open arch: x-z outlines outer/inner (same count, bottom-left round to bottom-right) extruded y0..y1."""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    O0, O1, I0, I1 = ([bm.verts.new((x, y, z)) for x, z in pts] for pts, y in ((outer, y0), (outer, y1), (inner, y0), (inner, y1)))
    faces = []
    for i in range(len(outer) - 1):
        faces += [bm.faces.new((O0[i], O0[i + 1], I0[i + 1], I0[i])), bm.faces.new((O1[i], I1[i], I1[i + 1], O1[i + 1])),
                  bm.faces.new((O0[i], O1[i], O1[i + 1], O0[i + 1])), bm.faces.new((I0[i], I0[i + 1], I1[i + 1], I1[i]))]
    for e in (0, -1): faces.append(bm.faces.new((O0[e], I0[e], I1[e], O1[e])))
    for f in faces:
        for lp in f.loops: lp[uvl].uv = ((lp.vert.co.x + lp.vert.co.y) / 16, lp.vert.co.z / 12)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); me = bpy.data.meshes.new('arch'); bm.to_mesh(me); return link(me, m, 'arch')


def chev(w, side, top, tw):
    """Chevron-hex arch outline (dream-board gate): straight legs, angled shoulders, flat top."""
    return [(-w, 0), (-w, side), (-tw, top), (tw, top), (w, side), (w, 0)]


def inset(pts, d):
    """Shrink a chevron outline by d (legs in, top down) for neon lines just inside its edge."""
    return [(x - math.copysign(d, x), z if z == 0 else z - d) for x, z in pts]


# ---------------------------------------------------------------- street furniture
def streetlight(M):
    """Pure white streetlight (owner brief): slim dark pole, arm over the walk (+y), lit head, glowing collar."""
    box(0, 0, 0, .3, .3, 7.5, M['body']); box(0, 0, 0, .6, .6, .5, M['body'])
    box(0, .9, 7.3, .25, 2, .25, M['body']); box(0, 1.6, 7.0, .7, 1.2, .3, M['white'])
    ring(0, 0, .55, .4, M['blue'], .07, 12)


def banner(x, y, M, rot=0.0):
    """Tall pole with a round RT badge banner both sides and red/blue light bars."""
    box(x, y, 0, .25, .25, 10, M['body'])
    placed(x, y, rot, lambda: (sign(.9, -.15, 5, 2.4, M['badge']), sign(.9, .15, 5, 2.4, M['badge'], back=True),
                               box(.9, 0, 7.4, 2.6, .12, .25, M['red']), box(.9, 0, 4.8, 2.6, .12, .2, M['blue'])))


def tree(x, y, M, rnd):
    """Dark stylised tree in a hex planter with a lit rim (no grass, per the owner brief)."""
    loft([(0, xform(ellipse(3, 3, 6), x, y)), (.6, xform(ellipse(3, 3, 6), x, y))], M['body'])
    ring(x, y, .62, 1.55, M[rnd.choice(('blue', 'red'))], .06, 6)
    box(x, y, .6, .3, .3, 2.6, M['body'])
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(1.8, 2.6), location=(x, y, 4.2))
    o = bpy.context.object; o.scale.z = 1.25; bpy.ops.object.transform_apply(scale=True); o.data.materials.append(M['leaf'])


def umbrella(x, y, M):
    box(x, y, 0, .12, .12, 2.6, M['body']); ball(x, y, .75, .55, M['body'])
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=1.8, radius2=.1, depth=.7, location=(x, y, 2.75))
    bpy.context.object.data.materials.append(M['canopy'])


def lane(x0, y0, x1, y1, M, step=14, rnd=None):
    """Streetlights both sides of a walk, banners and trees between them, packet-chase kerb lines."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    for k in range(int(L // step) + 1):
        px, py = x0 + ux * k * step, y0 + uy * k * step
        for s in (-1, 1):
            placed(px + s * nx * 7, py + s * ny * 7, math.atan2(s * nx, -s * ny), streetlight, M)  # arm reaches over the walk
            if k % 2 and rnd: tree(px + s * nx * 9.5 + ux * step / 2, py + s * ny * 9.5 + uy * step / 2, M, rnd)
            elif rnd: banner(px + s * nx * 8.5 + ux * step / 2, py + s * ny * 8.5 + uy * step / 2, M, math.atan2(uy, ux))
    for s, band in ((-1, 'blue'), (1, 'red')):
        chase([(x0 + s * nx * 6, y0 + s * ny * 6, .08), (x1 + s * nx * 6, y1 + s * ny * 6, .08)], M, band, .1)


# ---------------------------------------------------------------- feature pieces (built at the origin, front -y)
def atom(M, C=15, R=12.5, plinth=True, badge=14):
    """RT atom: double-sided round RT badge as the nucleus inside three spinning electron orbits."""
    if plinth:
        for z0, z1, r in ((0, 1.2, 9), (1.2, 2.6, 6.5), (2.6, 4.2, 4)):
            loft([(z0, ellipse(2 * r, 2 * r, 32)), (z1, ellipse(2 * r - .6, 2 * r - .6, 32))], M['body'])
            chase_ring(0, 0, z1 - .05, r - .25, M, 'blue' if r != 6.5 else 'red', .16)
        tube([(0, 0, 4.2), (0, 0, C - badge / 2)], .5, M['blue'])
    sign(0, -.1, C - badge / 2, badge, M['badge']); sign(0, .1, C - badge / 2, badge, M['badge'], back=True)
    for k, band in enumerate(('red', 'blue', 'white')):  # in the badge plane, 60 degrees apart, a little depth
        a = math.radians(60 * k + 30)
        orbit((0, 0, C), (R * math.cos(a), 0, R * math.sin(a)), (-R * .37 * math.sin(a), R * .18, R * .37 * math.cos(a)), M, band, R * .034)


def gate(M, rnd):
    """REBEL TECH THEME PARK gate, after the dream board: chevron arch with neon outlines and the spinning
    RT atom on top, LED screen towers, swept neon wings, and a hex tunnel leading guests into the park."""
    outer, inner = chev(17, 22, 32, 11), chev(9.5, 12, 16, 6)
    arch(outer, inner, -4, 4, M['body'])
    for fy, face in ((-4.1, -1), (4.1, 1)):  # neon outlines on both faces: red outside, white and blue inside
        tube([(x, fy, z) for x, z in inset(outer, .5)], .3, M['red'])
        tube([(x, fy, z) for x, z in inset(outer, 1.4)], .16, M['blue'])
        tube([(x, fy, z) for x, z in inset(inner, -.5)], .3, M['white'])
        strip(0, fy, 20.6, 24, 'rebel tech', M, face); strip(0, fy, 17.3, 11, 'theme park', M, face)
    for s in (-1, 1):  # glass light panels on the arch legs
        for fy, face in ((-4.06, -1), (4.06, 1)): panel(s * 13.2, fy - face * .01, 2, 4.6, 16, face, M['glass'], 0)
    # the atom crowning the arch, on a hex plate
    loft([(30, xform(ellipse(14, 4, 6), 0, 0)), (31.5, xform(ellipse(12, 3, 6), 0, 0))], M['body'])
    placed(0, 0, 0, atom, M, 39, 10.5, False, 12)
    for s in (-1, 1):  # LED towers
        px = s * 24.5
        loft([(0, xform(rounded(10, 10, 2, 1), px, 0)), (40, xform(rounded(8, 8, 1.6, 1), px, 0))], M['body'])
        for fy, face in ((-5, -1), (5, 1)):
            panel(px, fy * .97, 3, 6, 30, face, M['glass'], .05); sign(px, fy * .97 + face * .15, 20, 7, M['badge'], back=face > 0)
            ticker(px, fy * .97 + face * .12, 5, 5.6, 2, M, 1.4, face)
        for cx, cy in ((5, 5), (-5, 5), (5, -5), (-5, -5)):
            chase([(px + cx * .96, cy * .96, 0), (px + cx * .78, cy * .78, 40)], M, 'red' if cx * s > 0 else 'blue', .22, 12)
        for k in (-1, 1):  # bladed crown
            bpy.ops.mesh.primitive_cube_add(size=1, location=(px + k * 2, 0, 43), rotation=(0, k * .35, 0))
            o = bpy.context.object; o.dimensions = (1.2, 6, 8); bpy.ops.object.transform_apply(rotation=True, scale=True); o.data.materials.append(M['body'])
        tube([(px, 0, 40), (px, 0, 50)], .25, M['blue']); beacon(px, 0, 50.4, M)
    for s in (-1, 1):  # swept wings: walls falling away from the towers with angled light bands
        x0, x1 = s * 29.5, s * 54
        prism([(x0, 0), (x1, 0), (x1, 6), (x0, 15)], -2.5, 2.5, M['body'])
        for fy, face in ((-2.6, -1), (2.6, 1)):
            for k, band in enumerate(('red', 'blue', 'red')):
                chase([(x0, fy, 13.5 - 3 * k), (x1, fy, 5 - 1.4 * k)], M, band, .2, 9)
            ticker((x0 + x1) / 2, fy, .6, abs(x1 - x0) - 4, 2, M, 1.2, face)
        for k in range(3): banner(x0 + s * (5 + 8 * k), -7, M, 0)
    # tunnel into the park: hex frames, glowing ceiling, packet lines on the floor
    for k, y in enumerate((8, 12, 16, 20, 24)):
        arch(chev(11.5, 13.5, 18.5, 7.2), inset(chev(11.5, 13.5, 18.5, 7.2), 1.2), y - .5, y + .5, M['body'])
        tube([(x, y - .6, z) for x, z in inset(chev(11.5, 13.5, 18.5, 7.2), 1.5)], .22, M[('white', 'blue', 'red')[k % 3]])
    roof = inset(chev(11.5, 13.5, 18.5, 7.2), 1.0)[1:5]
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    for (xa, za), (xb, zb) in zip(roof, roof[1:]):
        f = bm.faces.new([bm.verts.new(p) for p in ((xa, 4, za), (xa, 24.5, za), (xb, 24.5, zb), (xb, 4, zb))])
        for lp in f.loops: lp[uvl].uv = ((lp.vert.co.x + lp.vert.co.z) / 16, lp.vert.co.y / 12)
    bm.normal_update(); me = bpy.data.meshes.new('ceiling'); bm.to_mesh(me); link(me, M['glass'], 'ceiling')
    for x, band in ((-8, 'blue'), (-3, 'white'), (3, 'white'), (8, 'red')):
        chase([(x, -14, .08), (x, 26, .08)], M, band, .1, 6)


def end_of_wifi_bar(M, rnd):
    """End of WiFi Bar: skyscraper castle. Podium mall with eight venue bays, four castle turrets with
    crenellations and spires, a three-tier glass keep with sky terraces, the sky bar and an RT atom crown."""
    P = 72; prof = rounded(P, P, 6, 2)
    loft([(0, prof), (16, prof)], M['body'])
    edge = xform(prof, 0, 0, 1.006)
    for z, m in ((.4, 'red'), (8.2, 'blue'), (15.8, 'red')): tube([(x, y, z) for x, y in edge + edge[:1]], .22, M[m])
    bays = [('byte burgers', 'firewall grill'), ('pixel pizza', '404 noodles'), ('overclock coffee', 'bandwidth brews'), ('cache & carry', 'gear')]
    for f, names in enumerate(bays):
        def face(names=names, front=(f == 0)):
            for b, name in zip((-1, 1), names):
                x = b * 20; panel(x, -P / 2, .4, 22, 6.4, -1, M['glass'], .1); panel(x, -P / 2, 9, 26, 6, -1, M['glass'], .1)
                tube([(x - 11.5, -P / 2 - .3, 0), (x - 11.5, -P / 2 - .3, 7), (x + 11.5, -P / 2 - .3, 7), (x + 11.5, -P / 2 - .3, 0)], .2, M['white'])
                if name == 'gear': strip(x, -P / 2 - .35, 10.4, 12, 'rebel tech', M); strip(x, -P / 2 - .35, 7.3, 9, 'gear', M)
                else: strip(x, -P / 2 - .35, 7.4, 18, name, M)
            if front:  # main doors under the big sign, chevron portal in neon
                panel(0, -P / 2, .3, 10, 12, -1, M['glass'], .12)
                tube([(x, -P / 2 - .4, z) for x, z in chev(6, 10, 14, 3.5)], .3, M['red'])
                box(0, -P / 2 - .6, 16, 34, 1.2, 8.5, M['body']); strip(0, -P / 2 - 1.25, 16.5, 30, 'end of wifi bar', M)
        placed(0, 0, f * math.pi / 2, face)
    ticker_ring(0, 0, 17, 23.5, 1, M, 2.0, 72)  # LED ticker round the foot of the keep, above the podium roof garden
    for k in range(48):  # crenellated parapet on the podium roof
        a = 2 * math.pi * k / 48; r = P / 2 * 1.02
        if k % 2 == 0: box(r * math.cos(a), r * math.sin(a), 16, 2.2, 2.2, 1.6, M['body'])
    for cx, cy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):  # castle turrets
        tx, ty, R, H = cx * (P / 2 - 1), cy * (P / 2 - 1), 7.5, 66
        loft([(0, xform(ellipse(2 * R, 2 * R, 24), tx, ty)), (H, xform(ellipse(2 * R, 2 * R, 24), tx, ty))], M['body'])
        for z in range(20, H - 4, 9):  # glass slit bands
            loft([(z, xform(ellipse(2 * R + .2, 2 * R + .2, 24), tx, ty)), (z + 3.5, xform(ellipse(2 * R + .2, 2 * R + .2, 24), tx, ty))], M['glass'], cap=False)
        for k in range(12):
            a = 2 * math.pi * k / 12
            if k % 2 == 0: box(tx + (R - .6) * math.cos(a), ty + (R - .6) * math.sin(a), H, 2, 2, 2.4, M['body'])
        loft([(H, xform(ellipse(2 * R - 1, 2 * R - 1, 24), tx, ty)), (H + 22, xform(ellipse(.4, .4, 24), tx, ty))], M['body'])
        for k in range(4):  # neon ribs up the spire, packets climbing the turret
            a = 2 * math.pi * k / 4 + math.pi / 4
            tube([(tx + (R - .5) * math.cos(a), ty + (R - .5) * math.sin(a), H + .2), (tx + .2 * math.cos(a), ty + .2 * math.sin(a), H + 22)], .18, M['red' if k % 2 else 'blue'])
        a = math.atan2(cy, cx)
        chase([(tx + (R + .1) * math.cos(a), ty + (R + .1) * math.sin(a), 0), (tx + (R + .1) * math.cos(a), ty + (R + .1) * math.sin(a), H)], M, 'red' if cx > 0 else 'blue', .25, 14)
        beacon(tx, ty, H + 22.6, M, 'red', .7)
        # light bridge from turret top to the keep
        tube([(tx, ty, 58), (cx * 20, cy * 20, 62)], .25, M['blue']); box((tx + cx * 20) / 2, (ty + cy * 20) / 2, 57.5, 3, 3, .6, M['body'])
    z = 16
    for w, h, band in ((40, 54, 'blue'), (32, 50, 'red'), (24, 22, 'white')):  # keep tiers with sky terraces
        kp = rounded(w, w, 4, 1)
        loft([(z, kp), (z + h, kp)], M['glass'])
        for x, y in ((w / 2, w / 2), (-w / 2, w / 2), (w / 2, -w / 2), (-w / 2, -w / 2)):
            chase([(x * 1.0, y * 1.0, z), (x * 1.0, y * 1.0, z + h)], M, band, .3, 16)
        for side in range(4):
            def fins(w=w, z=z, h=h):
                for i in range(1, 6): box(-w / 2 + w * i / 6, -w / 2 - .3, z, .35, .6, h, M['body'])
            placed(0, 0, side * math.pi / 2, fins)
        z += h
        tp = rounded(w + 6, w + 6, 4, 1); loft([(z, tp), (z + 1, tp)], M['body'])
        tube([(x, y, z + 1.2) for x, y in tp + tp[:1]], .2, M['white'])
    # the sky bar: lit glass lantern at the top of tier two with END OF WIFI BAR on all four faces
    for side in range(4):
        placed(0, 0, side * math.pi / 2, lambda: (box(0, -16.6, 116.5, 26, .8, 6.5, M['body']), strip(0, -17.05, 116.8, 24, 'end of wifi bar', M)))
    for k in (-1, 1):  # bladed crown
        bpy.ops.mesh.primitive_cube_add(size=1, location=(k * 6, 0, z + 9), rotation=(0, k * .3, 0))
        o = bpy.context.object; o.dimensions = (3, 18, 18); bpy.ops.object.transform_apply(rotation=True, scale=True); o.data.materials.append(M['body'])
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, k * 6, z + 9), rotation=(-k * .3, 0, 0))
        o = bpy.context.object; o.dimensions = (18, 3, 18); bpy.ops.object.transform_apply(rotation=True, scale=True); o.data.materials.append(M['body'])
    before = set(bpy.data.objects); atom(M, 0, 13, False, 15)
    for o in set(bpy.data.objects) - before: o.location.z += z + 22  # RT atom crown, spinning above the castle
    tube([(0, 0, z + 34), (0, 0, z + 46)], .3, M['blue']); beacon(0, 0, z + 46.6, M, 'red', .8)
    for s in (-1, 1): beacon(s * 13, 0, z + 18, M, 'blue', .5); beacon(0, s * 13, z + 18, M, 'white', .5)
    for k in range(10):  # entrance plaza: lights and banners leading to the doors
        x = -27 + 6 * k
        if k in (4, 5): continue
        if k % 2: placed(x, -P / 2 - 10, 0, streetlight, M)
        else: banner(x, -P / 2 - 8, M)


def arcade(M):
    """REBEL TECH ARCADE: chamfered hall, glass front glowing from the game floor, stacked neon sign, badge pylon."""
    prof = rounded(32, 20, 3.5, 1); edge = xform(prof, 0, 0, 1.01)
    loft([(0, prof), (14, prof)], M['body'])
    panel(0, -10, .3, 24, 6.2, -1, M['glass'], .1)
    strip(1, -10.25, 10.2, 17, 'rebel tech', M); strip(1, -10.25, 6.6, 15, 'arcade', M)
    chase([(x, y, .4) for x, y in edge + edge[:1]], M, 'red', .22, 8); tube([(x, y, 13.6) for x, y in edge + edge[:1]], .22, M['blue'])
    tube([(-9, -10.4, 0), (-11, -10.4, 6.5), (-6, -10.4, 6.8)], .3, M['red']); tube([(9, -10.4, 0), (11, -10.4, 6.5), (6, -10.4, 6.8)], .3, M['blue'])
    box(-17.5, -6, 0, 4.5, 4.5, 20, M['body']); sign(-17.5, -8.3, 13, 4, M['badge'])
    chase([(-15.2, -8.3, 0), (-15.2, -8.3, 20)], M, 'blue', .2, 6); chase([(-19.8, -8.3, 0), (-19.8, -8.3, 20)], M, 'red', .2, 6)
    beacon(-17.5, -6, 20.6, M, 'blue')
    for k in range(3): box(-6 + 6 * k, 3, 14, 3, 3, 1.4, M['body']); box(-6 + 6 * k, 1.4, 14.5, 2.4, .1, .4, M['blue'])


def gear_shop(M):
    """REBEL TECH GEAR: low store with display windows and a hexagonal RT badge tower on the roof."""
    prof = rounded(28, 16, 2, 1)
    loft([(0, prof), (11, prof)], M['body'])
    panel(0, -8, .3, 22, 5, -1, M['glass'], .1)
    strip(-2, -8.25, 8.3, 12, 'rebel tech', M); strip(-2, -8.25, 5.6, 9, 'gear', M)
    tube([(px, py, 10.8) for px, py in prof] + [(prof[0][0], prof[0][1], 10.8)], .2, M['red'])
    ticker(0, -8.2, 5.25, 26, 0, M, .7)
    hexp = xform(ellipse(8, 8, 6), 9, 0, 1, math.pi / 6)
    loft([(11, hexp), (19, hexp)], M['body']); sign(9, -3.6, 12, 6, M['badge'])
    chase([(px, py, 19) for px, py in hexp + hexp[:1]], M, 'blue', .2, 6)
    tube([(px, py, 11.2) for px, py in hexp] + [(hexp[0][0], hexp[0][1], 11.2)], .2, M['red'])


def fuel_up(M, rnd):
    """FUEL UP food pavilion: glass drum under stacked orbit roof discs, front sign, red parasols outside."""
    loft([(0, ellipse(26, 26, 32)), (5, ellipse(26, 26, 32))], M['glass'])
    for z0, z1, r, band in ((5, 6.2, 16, 'red'), (6.2, 7.6, 11.5, 'blue'), (7.6, 8.8, 7, 'red')):
        loft([(z0, ellipse(2 * r, 2 * r, 40)), (z1, ellipse(2 * r - 1, 2 * r - 1, 40))], M['body'])
        chase_ring(0, 0, z0 + .05, r + .1, M, band, .22)
    tube([(0, 0, 8.8), (0, 0, 13)], .2, M['blue']); beacon(0, 0, 13.3, M, 'white', .8)
    for k in range(10):
        a = 2 * math.pi * k / 10; box(12.5 * math.cos(a), 12.5 * math.sin(a), 0, .5, .5, 5, M['body'])
    box(0, -16.4, 7.4, 17, .6, 5, M['body']); strip(0, -16.8, 8.2, 15.5, 'fuel up', M); strip(0, -16.8, 7.5, 13, 'eats', M)
    for k in range(7): umbrella(-15 + 5 * k, -22 - 2.5 * (k % 2), M)


def control_room(M):
    """CONTROL ROOM show building: drum with badge screens, a lit dome and two orbit rings carrying lights."""
    loft([(0, ellipse(26, 26, 36)), (11, ellipse(26, 26, 36))], M['body'])
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * .5
        placed(13.1 * math.cos(a), 13.1 * math.sin(a), a + math.pi / 2, lambda: (sign(0, -.05, 3.5, 4.5, M['badge']), box(0, .05, 2.8, 5.4, .1, .25, M['blue'])))
    chase_ring(0, 0, .4, 13.2, M, 'red', .22); ticker_ring(0, 0, 9, 13.15, 3, M, 1.4)
    rings = [(11 + 9 * math.sin(math.pi / 2 * k / 6), ellipse(24 * math.cos(math.pi / 2 * k / 6) + .5, 24 * math.cos(math.pi / 2 * k / 6) + .5, 36)) for k in range(7)]
    loft(rings, M['glass'])
    tilted((0, 0, 14), 19, 15, .45, .3, M, 'red'); tilted((0, 0, 14), 19, 15, -.45, -.5, M, 'blue')
    box(0, -13.4, 11, 18, .6, 4.5, M['body']); strip(0, -13.8, 11.4, 16, 'control room', M)
    tube([(0, 0, 20), (0, 0, 26)], .25, M['blue']); beacon(0, 0, 26.4, M)


def lagoon(M, rnd, w=84, d=44):
    """Fountain lagoon: rippling water, packet-chase rims, rising jets; a bridge carries the boulevard across."""
    flat(ellipse(w, d, 48), .15, M['water'])
    chase_ring(0, 0, .35, w / 2 + .4, M, 'red', .25, d / 2 + .4); chase_ring(0, 0, .55, w / 2 + 1.4, M, 'blue', .2, d / 2 + 1.4)
    loft([(0, ellipse(w + 1.6, d + 1.6, 48)), (.4, ellipse(w + 1.6, d + 1.6, 48))], M['body'], cap=False)
    for cx, cy in ((-26, 0), (26, 0), (-14, 9), (14, -9), (-14, -9), (14, 9)):
        ring(cx, cy, .3, 2.4, M['blue'], .12, 16)
        for j in range(9):
            a = 2 * math.pi * j / 9; r = 0 if j == 0 else 1.6; h = rnd.uniform(6, 10) if j == 0 else rnd.uniform(2.5, 5)
            jet(cx + r * math.cos(a), cy + r * math.sin(a), cx + r * 1.4 * math.cos(a), cy + r * 1.4 * math.sin(a), h, M, .12 if j == 0 else .08)
    box(0, 0, .9, 12, d + 8, .5, M['body'])
    for s in (-1, 1):
        box(s * 5.8, 0, 1.4, .2, d + 8, 1.1, M['body']); chase([(s * 5.9, -d / 2 - 4, 2.5), (s * 5.9, d / 2 + 4, 2.5)], M, 'blue' if s < 0 else 'red', .1, 8)
        for k in range(-2, 3): box(s * 5.8, k * 10, 0, .8, .8, .9, M['body'])


# ---------------------------------------------------------------- the pieces
def export(name):
    """Join everything, shrink to EXPORT_SCALE about the origin, export GLB (place at 200% in game)."""
    bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join(); o = bpy.context.object; o.name = name
    bpy.context.scene.cursor.location = (0, 0, 0); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    o.scale = (EXPORT_SCALE,) * 3; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.export_scene.gltf(filepath=str(out / (name + '.glb')), export_format='GLB', use_selection=True)
    return {'name': name, 'dims_m': [round(v, 2) for v in o.dimensions], 'game_scale_pct': round(100 / EXPORT_SCALE),
            'tris': sum(len(p.vertices) - 2 for p in o.data.polygons), 'materials': [m.name for m in o.data.materials]}


def gate_piece():
    clear(); M = park_materials(); gate(M, random.Random(3)); return export('rt-park-gate')


def wifi_piece():
    clear(); M = park_materials(); end_of_wifi_bar(M, random.Random(21)); return export('rt-end-of-wifi-bar')


def center():
    """Hub behind the gate: its -y edge meets the end of the gate tunnel; the End of WiFi Bar stands past its +y edge."""
    clear(); M = park_materials(); rnd = random.Random(11)
    flat(xform(ellipse(30, 30, 48), 0, -62), .05, M['medallion'], (-15, -77, 15, -47))  # entry plaza floor medallion
    chase_ring(0, -62, .1, 16, M, 'blue', .15); chase_ring(0, -62, .1, 17.2, M, 'red', .1)
    for k in range(6):  # white lights round the medallion plaza
        a = 2 * math.pi * k / 6; placed(19 * math.cos(a), -62 + 19 * math.sin(a), a + math.pi / 2, streetlight, M)
    placed(-40, -64, math.pi / 2, arcade, M)  # faces +x, onto the plaza
    placed(40, -64, -math.pi / 2, gear_shop, M)
    chase_ring(0, -10, .08, 26, M, 'blue', .2); chase_ring(0, -10, .08, 28, M, 'red', .14); chase_ring(0, -10, .08, 15, M, 'white', .12)
    placed(0, -10, 0, atom, M)
    for k in range(8):  # ring of small fountains round the hub
        a = 2 * math.pi * (k + .5) / 8; fx, fy = 21 * math.cos(a), -10 + 21 * math.sin(a)
        ring(fx, fy, .25, 1.6, M['blue'], .1, 12)
        for j in range(5): jet(fx, fy, fx + .6 * math.cos(j), fy + .6 * math.sin(j), rnd.uniform(2.5, 4.5), M, .08)
    placed(60, 22, -math.pi / 2, fuel_up, M, rnd)  # north of the cross boulevard, beside the lagoon
    placed(-58, 24, math.pi / 2, control_room, M)
    placed(0, 50, 0, lagoon, M, rnd)
    lane(0, -96, 0, -80, M, 14); lane(0, -44, 0, -38, M, 13); lane(0, 20, 0, 22, M, 13)
    lane(-90, -10, -34, -10, M, 14, rnd); lane(34, -10, 90, -10, M, 14, rnd)
    lane(0, 78, 0, 92, M, 14, rnd)
    for s in (-1, 1):  # waterfront towers either side of the lagoon, clear of the bridge
        placed(s * 62, 52, 0, armored, 0, 0, 16, 14, rnd.uniform(34, 46), M, rnd, logo=True)
        placed(s * 62, 82, 0, armored, 0, 0, 14, 12, rnd.uniform(24, 36), M, rnd, logo=True)
        placed(s * 70, -62, -s * math.pi / 2, storefront, 0, 0, 22, 8, 8, M)
    for x, y in ((-30, -36), (30, -36), (-30, 16), (30, 16)):  # corner trees framing the hub
        tree(x, y, M, rnd)
    return export('rt-park-center')


def district(name, seed, dome=False):
    """192 x 96 m: a back row of towers, lit shopfronts and kiosks along a lit street, open cross street at x = 0."""
    clear(); M = park_materials(); rnd = random.Random(seed)
    for side in (-1, 1):
        x = 14.0
        while x < 92:
            w = rnd.choice((14, 16, 18, 20))
            if x + w > 96: break
            placed(side * (x + w / 2), rnd.uniform(26, 34), 0, armored, 0, 0, w - 2, rnd.uniform(12, 16), rnd.uniform(28, 72), M, rnd, logo=rnd.random() < .6)
            x += w
        x = 14.0
        while x < 90:
            w = rnd.choice((16, 20, 24))
            if x + w > 96: break
            h = rnd.uniform(7, 11); placed(side * (x + w / 2), 6, 0, storefront, 0, 0, w - 2, 9, h, M)
            if rnd.random() < .6:  # rooftop sign standing on the front edge
                sw = min(w - 6, 12); box(side * (x + w / 2), 2.2, h, sw * .9, .3, .5, M['body'])
                strip(side * (x + w / 2), 1.95, h + .4, sw, rnd.choice(('rebel tech', 'rebel tech', 'tagline')), M)
            else:
                ticker(side * (x + w / 2), 1.3, h * .5, w - 6, rnd.choice((0, 2)), M, .9)
            x += w
    lane(-92, -10, -16, -10, M, 14, rnd); lane(16, -10, 92, -10, M, 14, rnd)
    lane(0, -44, 0, -40, M, 12)
    if dome:  # small data-core plaza at the cross street: medallion floor and a glass dome inside spinning orbits
        flat(xform(ellipse(22, 22, 40), 0, -25), .05, M['medallion'], (-11, -36, 11, -14))
        chase_ring(0, -25, .1, 11.6, M, 'red', .14)
        rings = [(9 * math.sin(math.pi / 2 * k / 6), ellipse(14 * math.cos(math.pi / 2 * k / 6) + .4, 14 * math.cos(math.pi / 2 * k / 6) + .4, 32)) for k in range(7)]
        before = set(bpy.data.objects); loft(rings, M['glass'])
        for o in set(bpy.data.objects) - before: o.location = (0, 28, 0)
        tilted((0, 28, 6), 11, 9, .5, .4, M, 'red', .3); tilted((0, 28, 6), 11, 9, -.5, -.4, M, 'blue', .3); tilted((0, 28, 6), 12, 10, 1.2, 1.4, M, 'white', .25)
    else:
        placed(0, 30, 0, atom, M)
    for k in range(-2, 3):  # kiosks with parasols on the street corners
        if k: umbrella(k * 34 + 6, -25, M); umbrella(k * 34 - 6, -25, M)
    return export(name)


if __name__ == '__main__':
    manifest = [gate_piece(), wifi_piece(), center(), district('rt-park-district-a', 31), district('rt-park-district-b', 57, dome=True)]
    (out / 'park-manifest.json').write_text(json.dumps(manifest, indent=2)); print('GRID_PARK', json.dumps(manifest))

if __name__ == '__main__' and 'preview' in sys.argv:
    view = sys.argv[sys.argv.index('preview') + 1] if len(sys.argv) > sys.argv.index('preview') + 1 else 'aerial'
    clear()
    # park layout the in-game placement follows: gate tunnel -> hub -> End of WiFi Bar, districts either side
    for n, x, y in (('rt-park-gate', 0, -120), ('rt-park-center', 0, 0), ('rt-end-of-wifi-bar', 0, 150),
                    ('rt-park-district-a', -150, 60), ('rt-park-district-b', 150, 60)):
        bpy.ops.import_scene.gltf(filepath=str(out / (n + '.glb'))); o = bpy.context.selected_objects[0]
        o.location = (x, y, 0); o.scale = (2, 2, 2)
        if 'district' in n: o.rotation_euler.z = -math.pi / 2 if x < 0 else math.pi / 2
    bpy.ops.mesh.primitive_plane_add(size=1600); bpy.context.object.data.materials.append(mat('Floor', (.002, .003, .006), rough=.2))
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE_NEXT'; sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    w = bpy.data.worlds.new('Sky'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.004, .006, .02, 1); sc.world = w
    cam = bpy.data.cameras.new('Cam'); co = bpy.data.objects.new('Cam', cam); bpy.context.collection.objects.link(co); sc.camera = co
    co.location, co.rotation_euler, cam.lens = {'aerial': ((0, -330, 190), (math.radians(60), 0, 0), 28),
                                                 'gate': ((0, -175, 14), (math.radians(84), 0, 0), 24),
                                                 'street': ((0, -60, 9), (math.radians(86), 0, 0), 22)}[view]
    sun = bpy.data.lights.new('Moon', 'SUN'); sun.energy = .6; so = bpy.data.objects.new('Moon', sun); bpy.context.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(30))
    sc.view_settings.view_transform = 'AgX'
    sc.use_nodes = True; nt = sc.node_tree; rl = nt.nodes['Render Layers']; comp = nt.nodes['Composite']
    g = nt.nodes.new('CompositorNodeGlare'); g.glare_type = 'FOG_GLOW'
    nt.links.new(rl.outputs['Image'], g.inputs['Image']); nt.links.new(g.outputs['Image'], comp.inputs['Image'])
    sc.render.filepath = str(out / f'park-preview-{view}.png'); bpy.ops.render.render(write_still=True); print('PREVIEW_DONE')
