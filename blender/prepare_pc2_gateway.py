"""
Prepare the original gateway as ONE self-contained Planet Coaster 2 model candidate.

Run on Raven from the cloned repository:
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python blender\prepare_pc2_gateway.py

No game files are modified. This creates offline candidate assets under build/pc2/.
The GLB still needs an actual converter/in-game test; Blender validation is NOT PC2 compatibility proof.
"""
import json
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "build" / "source" / "rt_world_gateway.blend"
OUTPUT = ROOT / "build" / "pc2"
OUTPUT.mkdir(parents=True, exist_ok=True)

if not SOURCE.is_file():
    raise FileNotFoundError(
        f"Missing original gateway source {SOURCE}. "
        "Run the PC1-era Blender geometry generator first if necessary, "
        "but do NOT upload its old PC1 TMT package for the PC2 project."
    )

bpy.ops.wm.open_mainfile(filepath=str(SOURCE))

obj = bpy.data.objects.get("RTWorldGateway_L0")
if obj is None or obj.type != "MESH":
    raise RuntimeError("No highest-detail gateway mesh named RTWorldGateway_L0 in source.")

# The original PC1 candidate had six render LODs. A general converter may treat
# each as a separate scenery item. Keep only the high-detail primary mesh.
for other in list(bpy.data.objects):
    if other != obj:
        bpy.data.objects.remove(other, do_unlink=True)

obj.name = "RebelTechWorld_Gateway"
obj.data.name = "RebelTechWorld_GatewayMesh"

# Re-anchor the scene at the midpoint of the gateway entrance on the ground.
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# Validate source mesh: triangles, UVs, bounds and texture availability.
obj.data.calc_loop_triangles()
tri_count = len(obj.data.loop_triangles)
if tri_count < 50 or tri_count > 8000:
    raise RuntimeError(f"Suspicious gateway geometry: {tri_count} triangles")
if not obj.data.uv_layers:
    raise RuntimeError("Gateway mesh has no UV layers")

world_coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
mins = [min(v[i] for v in world_coords) for i in range(3)]
maxs = [max(v[i] for v in world_coords) for i in range(3)]
dims = [round(maxs[i] - mins[i], 4) for i in range(3)]
if max(dims) > 8.1:
    raise RuntimeError(f"Unexpectedly oversized source gateway dimensions: {dims}")

missing_images = []
for image in bpy.data.images:
    if image.source == "FILE":
        # Blender may lazily unload image pixels when reopening a .blend.
        # The previous build retains the original PNGs on D:, so reload them
        # explicitly before packing and exporting the standalone candidate.
        texture = ROOT / "build" / "tmt" / "rt_world_gateway" / f"{image.name}.png"
        if not texture.is_file():
            missing_images.append(str(texture))
            continue
        image.filepath = str(texture)
        image.reload()
        if not image.has_data:
            missing_images.append(str(texture))
        else:
            image.pack()
if missing_images:
    raise RuntimeError(f"Missing or unreadable source textures: {missing_images}")

bpy.ops.file.pack_all()
blend_path = OUTPUT / "rebel_tech_world_gateway_pc2_candidate.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

glb_path = OUTPUT / "rebel_tech_world_gateway_pc2_candidate.glb"
bpy.ops.export_scene.gltf(
    filepath=str(glb_path),
    export_format="GLB",
    use_selection=True,
    export_apply=True,
    export_animations=False,
    export_cameras=False,
    export_lights=False,
    export_yup=True,
)
if not glb_path.is_file() or glb_path.stat().st_size < 1000:
    raise RuntimeError("GLB export missing or suspiciously small")

# Independent GLB round-trip check in a clean scene.
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb_path))
meshes = [x for x in bpy.data.objects if x.type == "MESH"]
if len(meshes) != 1:
    raise RuntimeError(f"Expected 1 GLB mesh, found {len(meshes)}")
loaded = meshes[0]
if not loaded.data.uv_layers:
    raise RuntimeError("GLB round-trip removed UVs")
if len(loaded.data.materials) < 1:
    raise RuntimeError("GLB round-trip has no materials")
loaded.data.calc_loop_triangles()
loaded_triangles = len(loaded.data.loop_triangles)
if loaded_triangles != tri_count:
    raise RuntimeError(
        f"Triangle count mismatch in GLB: original {tri_count}, imported {loaded_triangles}"
    )

manifest = {
    "asset": "Rebel Tech World Gateway",
    "game_target": "Planet Coaster 2",
    "status": "PASS_OFFLINE_GLTF_ROUNDTRIP; NOT tested in Planet Coaster 2",
    "source_game_format": "Planet Coaster 1 Blender geometry, repurposed",
    "blender_version": bpy.app.version_string,
    "original_triangles": tri_count,
    "glb_triangles": loaded_triangles,
    "dimensions_m": dims,
    "materials": [mat.name for mat in loaded.data.materials if mat],
    "source_blend": str(blend_path),
    "glb": str(glb_path),
    "glb_size_bytes": glb_path.stat().st_size,
}
manifest_path = OUTPUT / "gateway_pc2_manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("PC2_GATEWAY_EXPORT_PASS", json.dumps(manifest), flush=True)
