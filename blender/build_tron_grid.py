"""Rebel Tech Grid v3 — Tron-style floor. Glossy black slab, glowing RT-blue minor
lines every 4 m, brighter major lines every 16 m, lit top edge on the skirt.
Edge lines are half width so neighbouring tiles join into full-width lines.
Run: blender -b --factory-startup -P blender/build_tron_grid.py [-- preview]
"""
import bpy, json, sys, math
from pathlib import Path
out = Path(r'D:\RebelTechWorld\rebel-tech-theme-park\build\tron-grid'); out.mkdir(parents=True, exist_ok=True)
SKIRT, MINOR, MAJOR = 4.0, 4.0, 16.0
BLUE, RED, WHITE = (.0176, .0723, 1), (.776, .002, .008), (1, 1, 1)  # #244CFF, #E10616 (linear)

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(n, c, e=0, rough=.08, metal=.3):
    m = bpy.data.materials.new(n); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    if e: p.inputs['Emission Color'].default_value = (*c, 1); p.inputs['Emission Strength'].default_value = e
    return m

def box(x, y, z, w, d, h, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z)); o = bpy.context.object; o.dimensions = (w, d, h)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(m)

def tile(name, size, col):
    clear()
    floor = mat('Tron Floor', (.0015, .0018, .0025))
    minor = mat('Grid Minor', col, 6); major = mat('Grid Major', tuple(.35 + .65 * v for v in col), 14)
    box(0, 0, -SKIRT / 2, size, size, SKIRT, floor)
    half, n = size / 2, int(round(size / MINOR))
    for i in range(n + 1):
        a = -half + i * MINOR
        is_major = abs((a + half) % MAJOR) < 1e-6
        w = .16 if is_major else .06
        edge = i in (0, n)
        if edge: w /= 2; a += w / 2 if i == 0 else -w / 2
        m = major if is_major else minor
        box(a, 0, .01, w, size, .02, m); box(0, a, .01, size, w, .02, m)
    # glowing lip around the top of the skirt so tile edges read as light, not raw walls
    for s in (-1, 1):
        box(s * (half + .02), 0, -.15, .04, size + .08, .3, minor); box(0, s * (half + .02), -.15, size + .08, .04, .3, minor)
    bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.join(); o = bpy.context.object; o.name = name
    bpy.ops.export_scene.gltf(filepath=str(out / (name + '.glb')), export_format='GLB', use_selection=True)
    return {'name': name, 'dims_m': [round(v, 3) for v in o.dimensions], 'tris': sum(len(p.vertices) - 2 for p in o.data.polygons)}

def preview(name):
    bpy.ops.import_scene.gltf(filepath=str(out / (name + '.glb')))
    for dx, dy in ((96, 0), (0, 96), (96, 96)):
        src = bpy.context.selected_objects[0]; d = src.copy(); d.data = src.data; d.location = (dx, dy, 0); bpy.context.collection.objects.link(d)
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    w = bpy.data.worlds.new('Night'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (.002, .004, .012, 1); sc.world = w
    cam = bpy.data.cameras.new('Cam'); co = bpy.data.objects.new('Cam', cam); bpy.context.collection.objects.link(co); sc.camera = co
    co.location = (-40, -60, 14); co.rotation_euler = (math.radians(78), 0, math.radians(-38)); cam.lens = 24
    sc.view_settings.view_transform = 'AgX'
    sc.use_nodes = True; nt = sc.node_tree; rl = nt.nodes['Render Layers']; comp = nt.nodes['Composite']
    g = nt.nodes.new('CompositorNodeGlare'); g.glare_type = 'FOG_GLOW'  # bloom approximation of the in-game glow
    nt.links.new(rl.outputs['Image'], g.inputs['Image']); nt.links.new(g.outputs['Image'], comp.inputs['Image'])
    sc.render.filepath = str(out / 'tron-grid-preview.png'); bpy.ops.render.render(write_still=True)

manifest = [tile('rt-tron-grid-96m-blue', 96, BLUE), tile('rt-tron-grid-16m-blue', 16, BLUE), tile('rt-tron-grid-16m-red', 16, RED)]
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2)); print('TRON_GRID', json.dumps(manifest))
if 'preview' in sys.argv:
    clear(); preview('rt-tron-grid-96m-blue'); print('PREVIEW_DONE')
