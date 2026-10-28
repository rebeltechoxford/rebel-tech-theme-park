"""Rebel Grid base v2: deep-skirted floor tiles so uneven terrain cannot show
through, plus a dark lit floor matching the dream board. Metropolis is rebuilt
unchanged in geometry; its scale bug lived in the converter project (0.01).
Run: blender -b -P blender/build_grid_base_v2.py
"""
import bpy, json, random
from pathlib import Path
out = Path(r'D:\RebelTechWorld\rebel-tech-theme-park\build\grid-base-v2'); out.mkdir(parents=True, exist_ok=True)
SKIRT = 4.0  # metres of solid body below the walking surface

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(n, c, e=0, rough=.26, metal=.5):
    m = bpy.data.materials.new(n); m.use_nodes = True; p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    if e: p.inputs['Emission Color'].default_value = (*c, 1); p.inputs['Emission Strength'].default_value = e
    return m

def box(n, x, y, z, w, d, h, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.name = n; o.dimensions = (w, d, h)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(m)

def export(name, label):
    bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join(); o = bpy.context.object; o.name = label
    bpy.ops.export_scene.gltf(filepath=str(out / (name + '.glb')), export_format='GLB', use_selection=True)
    return {'name': name, 'dims_m': [round(v, 3) for v in o.dimensions], 'tris': sum(len(p.vertices) - 2 for p in o.data.polygons)}

def floor(name, label, size, pitch, body, line, line_w=.05):
    # top surface at z=0, solid skirt down to -SKIRT hides terrain dips at edges/gaps
    box('Slab', 0, 0, -SKIRT / 2, size, size, SKIRT, body)
    half = size / 2
    n = int(size // pitch)
    for i in range(n + 1):
        a = -half + i * pitch
        box('Line', a, 0, .004, line_w, size, .008, line); box('Line', 0, a, .004, size, line_w, .008, line)
    return export(name, label)

manifest = []
clear()
navy = mat('Navy', (.0018, .0103, .033)); white = mat('White', (.92, .92, .92), .4)
manifest.append(floor('white-grid-ground', 'RT White Grid Ground 48m', 48, 3, white, navy, .04))
clear()
manifest.append(floor('dark-grid-floor-96m', 'RT Dark Grid Floor 96m', 96, 4,
                      mat('Obsidian', (.0027, .0033, .0052), 0, .12, .6), mat('Grid Light', (1, 1, 1), 4), .06))

# Metropolis: same seeded layout as build_grid_metropolis.py
clear(); random.seed(42)
black = mat('Obsidian', (.0027, .0033, .0052)); navy = mat('Navy', (.0018, .0103, .033)); white = mat('White', (.92, .92, .92), .4)
blue = mat('RT Blue', (.0176, .0723, 1), 3); red = mat('RT Red', (.776, .002, .008), 3)
for i in range(32):
    x = (i - 15.5) * 14; y = random.uniform(-18, 18); h = random.uniform(24, 100); w = random.uniform(7, 12); d = random.uniform(8, 16)
    box('Tower', x, y, h / 2, w, d, h, black if i % 2 else navy)
    box('Edge', x - w / 2 + .1, y - d / 2 - .04, h / 2, .18, .1, h, blue if i % 2 else red)
    for z in range(4, int(h) - 2, 5):
        box('Window strip', x, y - d / 2 - .08, z, w * .65, .1, .15, white)
manifest.append(export('dark-metropolis', 'RT Dark Metropolis Backdrop'))

(out / 'manifest.json').write_text(json.dumps(manifest, indent=2)); print('GRID_BASE_V2', json.dumps(manifest))
