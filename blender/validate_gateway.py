"""
Offline validation for Rebel Tech World Gateway FBX and TMT ZIP.
Use Blender 3.6+:
    blender --background --python blender/validate_gateway.py
Not a substitute for Frontier's online Thememaker's Toolkit conversion.
"""
import json
import re
import zipfile
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "build" / "tmt"
FBX = DIR / "rt_world_gateway" / "rt_world_gateway.fbx"
ZIP = DIR / "rt_world_gateway.zip"
REPORT = DIR / "rt_world_gateway_validation.json"

errors, warnings = [], []
if not FBX.is_file() or not ZIP.is_file():
    raise SystemExit("Missing generated asset. Run blender/create_gateway.py first.")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=str(FBX), use_image_search=False)
objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
by_lod = {}
for o in objects:
    match = re.fullmatch(r"RTWorldGateway_L([0-5])", o.name)
    if not match:
        errors.append("Unexpected FBX mesh: " + o.name)
        continue
    level = int(match.group(1))
    if level in by_lod:
        errors.append("Duplicate LOD " + str(level))
    by_lod[level] = o

lod_triangles = []
bounds = []
materials = set()
for level in range(6):
    obj = by_lod.get(level)
    if obj is None:
        errors.append("Missing expected level _L%d" % level)
        lod_triangles.append(None)
        continue
    tris = sum(max(1, len(face.vertices) - 2) for face in obj.data.polygons)
    lod_triangles.append(tris)
    if tris <= 0:
        errors.append("LOD %d has no triangles" % level)
    if not obj.data.uv_layers:
        errors.append("LOD %d has no UVs" % level)
    for slot in obj.material_slots:
        if slot.material:
            materials.add(slot.material.name)
    if len(obj.material_slots) == 0:
        errors.append("LOD %d missing materials" % level)
    bounds.extend(obj.matrix_world @ Vector(c) for c in obj.bound_box)

if lod_triangles[0] and lod_triangles[0] > 8000:
    errors.append("LOD0 exceeds 8,000 triangles")
if all(x is not None for x in lod_triangles):
    if any(a <= b for a, b in zip(lod_triangles, lod_triangles[1:])):
        errors.append("Triangle counts must decrease at each LOD")
if len(materials) > 8:
    errors.append("More than eight materials")
if bounds:
    dimensions = [
        max(v[i] for v in bounds) - min(v[i] for v in bounds)
        for i in range(3)
    ]
    if max(dimensions) > 8.0001:
        errors.append("Bounds exceed 8 metres: " + str(dimensions))
else:
    dimensions = []

with zipfile.ZipFile(ZIP, "r") as f:
    members = f.namelist()
    if f.testzip() is not None:
        errors.append("ZIP member failed integrity test")
    if not any(x.lower().endswith(".fbx") for x in members):
        errors.append("ZIP missing FBX")
    if "icon.png" not in members:
        errors.append("ZIP missing icon.png")
    if not any(x.endswith("_BC.png") for x in members):
        errors.append("ZIP missing base-color PNG")
    for member in members:
        if "/" in member or "\\" in member:
            errors.append("ZIP contains nested path " + member)
    zip_bytes = ZIP.stat().st_size

# Frontier's legacy docs list Blender 2.79 among explicitly tested releases.
warnings.append(
    "Blender %s is newer than the explicitly tested 2.79; "
    "Frontier's conversion remains unverified." % bpy.app.version_string
)
report = {
    "status": "PASS_OFFLINE" if not errors else "FAIL_OFFLINE",
    "note": "Checks FBX round-trip and ZIP structure only, not Frontier acceptance",
    "blender_version": bpy.app.version_string,
    "lod_triangles": lod_triangles,
    "bounds_m": [round(x, 3) for x in dimensions],
    "material_count": len(materials),
    "materials": sorted(materials),
    "zip_members": members,
    "zip_bytes": zip_bytes,
    "errors": errors,
    "warnings": warnings,
}
REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("OFFLINE_VALIDATION", json.dumps(report), flush=True)
if errors:
    raise RuntimeError("; ".join(errors))
