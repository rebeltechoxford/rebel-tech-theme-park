"""
REBEL TECH WORLD / Gateway Sign v0.1
Original procedural 3D scenery pilot for Planet Coaster 1's Thememaker's Toolkit.

Run with Blender 3.6+:
    blender --background --python blender/create_gateway.py

Outputs under build/ (not committed):
  source/rt_world_gateway.blend
  tmt/rt_world_gateway/rt_world_gateway.fbx
  tmt/rt_world_gateway/*.png
  tmt/rt_world_gateway.zip
  tmt/rt_world_gateway_preview.png
  tmt/rt_world_gateway_manifest.json

This output is an UNVALIDATED TMT candidate until Frontier's converter accepts it.
"""
import json
import math
import zipfile
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
EXPORT = BUILD / "tmt" / "rt_world_gateway"
EXPORT.mkdir(parents=True, exist_ok=True)
(BUILD / "source").mkdir(parents=True, exist_ok=True)

COLORS = {
    "RTNavy": (0.03, 0.07, 0.16, 1.0),
    "RTRed": (0.70, 0.055, 0.08, 1.0),
    "RTWhite": (0.90, 0.96, 1.00, 1.0),
    "RTSteel": (0.30, 0.36, 0.46, 1.0),
    "RTCyan": (0.04, 0.56, 0.82, 1.0),
}

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
materials = {}

for name, rgba in COLORS.items():
    image = bpy.data.images.new(name + "_BC", width=64, height=64, alpha=True)
    image.pixels[:] = list(rgba) * (64 * 64)
    image.filepath_raw = str(EXPORT / (name + "_BC.png"))
    image.file_format = "PNG"
    image.save()
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = image
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.38
    materials[name] = mat


def finish(obj, material, name):
    obj.name = name
    obj.data.materials.clear()
    obj.data.materials.append(materials[material])
    obj.color = COLORS[material]
    return obj


def box(name, xyz, dims, material, bucket):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz)
    obj = bpy.context.object
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bucket.append(finish(obj, material, name))
    return obj


def disk(name, xyz, radius, thickness, material, vertices, bucket):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=thickness,
        location=xyz, rotation=(math.pi / 2, 0, 0),
    )
    obj = bpy.context.object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bucket.append(finish(obj, material, name))
    return obj


def lettering(name, value, xyz, size, material, bucket):
    bpy.ops.object.text_add(location=xyz, rotation=(math.pi / 2, 0, 0))
    obj = bpy.context.object
    obj.data.body = value
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.006
    obj.data.bevel_depth = 0.001
    obj.data.resolution_u = 6
    obj.data.bevel_resolution = 1
    bpy.ops.object.convert(target="MESH")
    obj = bpy.context.object
    bucket.append(finish(obj, material, name))
    return obj


def make_lod(level):
    parts = []
    # 7.6m wide x 5.6m tall: within the Toolkit's 8m bounding-box limit.
    box("LeftPost", (-3.40, 0.0, 2.0), (0.60, 0.75, 4.0), "RTNavy", parts)
    box("RightPost", (3.40, 0.0, 2.0), (0.60, 0.75, 4.0), "RTNavy", parts)
    box("Lintel", (0.0, 0.0, 4.18), (7.55, 0.75, 0.66), "RTNavy", parts)
    if level < 5:
        box("LetteringBacker", (0, -0.402, 4.19), (6.05, 0.08, 0.51), "RTSteel", parts)
    if level < 4:
        disk("RoundEmblem", (0, -0.10, 5.00), 0.54, 0.16, "RTRed",
             (64, 48, 32, 16)[level], parts)
    if level < 3:
        box("PillarRedLeft", (-3.40, -0.41, 3.18), (0.35, 0.055, 0.31), "RTRed", parts)
        box("PillarRedRight", (3.40, -0.41, 3.18), (0.35, 0.055, 0.31), "RTRed", parts)
        lettering("SignText", "REBEL TECH WORLD", (0, -0.467, 4.18),
                  0.42, "RTWhite", parts)
        lettering("EmblemText", "RT", (0, -0.203, 5.00),
                  0.37, "RTWhite", parts)
    if level < 2:
        box("CanopyGlow", (0, -0.43, 3.84), (5.5, 0.08, 0.06), "RTCyan", parts)
        box("LeftRail", (-3.40, -0.46, 2.06), (0.10, 0.05, 2.2), "RTCyan", parts)
        box("RightRail", (3.40, -0.46, 2.06), (0.10, 0.05, 2.2), "RTCyan", parts)
    if level == 0:
        for i in range(10):
            box("Pixel_%02d" % i, (-2.48 + i * 0.55, -0.46, 4.53),
                (0.19, 0.05, 0.05), "RTRed" if i % 2 else "RTCyan", parts)
        disk("EmblemTrim", (0, -0.20, 5.00), 0.46, 0.03, "RTSteel", 48, parts)
        lettering("EmblemTextFront", "RT", (0, -0.238, 5.00), 0.36, "RTWhite", parts)

    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    merged = bpy.context.object
    merged.name = "RTWorldGateway_L%d" % level

    # All geometry gets explicit UV coordinates even for flat-color materials.
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=0.02)
    bpy.ops.object.mode_set(mode="OBJECT")
    merged.hide_render = level != 0
    tris = sum(max(1, len(poly.vertices) - 2) for poly in merged.data.polygons)
    return merged, tris


LODS = [make_lod(i) for i in range(6)]
counts = [x[1] for x in LODS]
print("LOD_TRIANGLE_COUNTS", counts, flush=True)
if counts[0] > 8000:
    raise RuntimeError("Highest detail level exceeds 8,000 triangles: %d" % counts[0])
if any(a <= b for a, b in zip(counts, counts[1:])):
    raise RuntimeError("LOD triangle counts must decrease strictly: %s" % counts)

# Do not include cameras, lights, or rendered backgrounds in FBX.
bpy.ops.object.select_all(action="DESELECT")
for obj, _ in LODS:
    obj.select_set(True)
bpy.context.view_layer.objects.active = LODS[0][0]
fbx_path = EXPORT / "rt_world_gateway.fbx"
bpy.ops.export_scene.fbx(
    filepath=str(fbx_path),
    use_selection=True,
    object_types={"MESH"},
    axis_forward="Y",
    axis_up="Z",
    apply_unit_scale=True,
    bake_anim=False,
    path_mode="STRIP",
    add_leaf_bones=False,
)

# Source file is a repeatable editing and debugging artifact.
for level, (obj, _) in enumerate(LODS):
    obj.hide_set(level > 0)
bpy.ops.wm.save_as_mainfile(filepath=str(BUILD / "source" / "rt_world_gateway.blend"))

# Produce screenshots of LOD0 for review and the Toolkit upload.
bpy.ops.object.camera_add(location=(8.2, -12, 8.3))
camera = bpy.context.object
direction = Vector((0, 0, 2.55)) - camera.location
camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 10.4
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.render.image_settings.file_format = "PNG"
scene.render.resolution_percentage = 100
scene.render.resolution_x = 1200
scene.render.resolution_y = 750
scene.render.filepath = str(BUILD / "tmt" / "rt_world_gateway_preview.png")
bpy.ops.render.render(write_still=True)
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.filepath = str(EXPORT / "icon.png")
bpy.ops.render.render(write_still=True)

zip_path = BUILD / "tmt" / "rt_world_gateway.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as package:
    for path in sorted(EXPORT.iterdir()):
        if path.suffix.lower() in {".fbx", ".png"}:
            package.write(path, path.name)
manifest = {
    "name": "Rebel Tech World Gateway",
    "blender_version": bpy.app.version_string,
    "status": "exported but NOT tested in Frontier Thememaker's Toolkit",
    "lod_triangles": counts,
    "fbx": str(fbx_path),
    "zip": str(zip_path),
    "toolkit_preview": str(BUILD / "tmt" / "rt_world_gateway_preview.png"),
}
(BUILD / "tmt" / "rt_world_gateway_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf8")
print("ASSET_BUILD_SUCCESS", json.dumps(manifest), flush=True)
