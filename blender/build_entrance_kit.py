"""
Rebel Tech World / Entrance Scenery Kit v0.1
--------------------------------------------
Generates three ORIGINAL modular decorations for possible future Planet Coaster 2 use.
NO game launch, binary patching, external assets, downloads, or mod install.

Run on Raven from the cloned GitHub workspace:
  "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python blender/build_entrance_kit.py

Outputs inside ignored build/pc2/entrance_kit/:
  rt_fiber_pylon.glb
  rt_data_core.glb
  rt_wayfinding_sign.glb
  rebel_tech_entrance_kit.blend
  entrance_kit_preview.png
  entrance_kit_manifest.json

The assets are OFFLINE Blender/GLB candidates. They are not verified in PC2.
"""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "build" / "pc2" / "entrance_kit"
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

palette = {
    "RT Navy": ((0.022, 0.052, 0.128, 1), 0.42, 0.35, 0.0),
    "RT Red": ((0.77, 0.035, 0.056, 1), 0.35, 0.30, 0.0),
    "RT White": ((0.93, 0.95, 1.0, 1), 0.1, 0.48, 0.0),
    "RT Steel": ((0.25, 0.33, 0.45, 1), 0.85, 0.26, 0.0),
    "RT Black Glass": ((0.015, 0.025, 0.06, 1), 0.2, 0.10, 0.0),
    "RT Cyan Glow": ((0.06, 0.62, 1.0, 1), 0.0, 0.3, 2.0),
}
materials={}
for name,(color,metallic,roughness,emissive) in palette.items():
    mat=bpy.data.materials.new(name)
    mat.use_nodes=True
    mat.diffuse_color=color
    bsdf=mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value=color
    bsdf.inputs["Metallic"].default_value=metallic
    bsdf.inputs["Roughness"].default_value=roughness
    if emissive:
        bsdf.inputs["Emission Color"].default_value=color
        bsdf.inputs["Emission Strength"].default_value=emissive
    materials[name]=mat


def colored(obj,name,mat,bucket):
    obj.name=name
    obj.data.materials.clear()
    obj.data.materials.append(materials[mat])
    bucket.append(obj)
    return obj

def box(bucket,name,xyz,dims,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
    obj=bpy.context.object
    obj.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return colored(obj,name,mat,bucket)

def cylinder(bucket,name,xyz,radius,depth,vertices,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=xyz)
    obj=bpy.context.object
    return colored(obj,name,mat,bucket)

def ring(bucket,name,xyz,radius,thickness,mat):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius,minor_radius=thickness,
        major_segments=32,minor_segments=8,location=xyz)
    return colored(bpy.context.object,name,mat,bucket)

def lettering(bucket,name,value,xyz,size,mat,rotation=(math.pi/2,0,0)):
    bpy.ops.object.text_add(location=xyz,rotation=rotation)
    obj=bpy.context.object
    obj.data.body=value
    obj.data.align_x="CENTER"
    obj.data.align_y="CENTER"
    obj.data.size=size
    obj.data.extrude=0.003
    obj.data.resolution_u=2
    obj.data.bevel_depth=0.0005
    obj.data.bevel_resolution=0
    bpy.ops.object.convert(target="MESH")
    return colored(bpy.context.object,name,mat,bucket)

def assemble(asset_name,parts):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts: obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.object.join()
    obj=bpy.context.object
    obj.name=asset_name
    obj.data.name=asset_name+"_Mesh"
    bpy.context.scene.cursor.location=(0,0,0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=0.025)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.data.calc_loop_triangles()
    triangles=len(obj.data.loop_triangles)
    dims=tuple(round(x,3) for x in obj.dimensions)
    mats=[m.name for m in obj.data.materials if m]
    if triangles<40 or triangles>10000:
        raise RuntimeError(f"{asset_name} triangle budget invalid: {triangles}")
    if max(dims)>8.01 or min(dims)<=0:
        raise RuntimeError(f"{asset_name} invalid 8m-conservative asset bounds: {dims}")
    if len(mats)>8 or not obj.data.uv_layers:
        raise RuntimeError(f"{asset_name} materials/UVs invalid: {mats}")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active=obj
    glb=OUT/(asset_name+".glb")
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",
                              use_selection=True,export_apply=True,
                              export_animations=False,export_cameras=False,
                              export_lights=False,export_yup=True)
    if glb.stat().st_size<1000:
        raise RuntimeError(f"{asset_name} GLB unexpectedly small")
    return obj,{"asset":asset_name,"status":"exported_not_in_game",
                "triangles":triangles,"dimensions_m":dims,
                "materials":mats,"glb_file":glb.name,
                "glb_size_bytes":glb.stat().st_size,
                "rights":"original geometry designed for Rebel Tech World"}


def make_pylon():
    p=[]
    box(p,"Footing",(0,0,0.14),(1.9,1.15,0.28),"RT Steel")
    box(p,"Body",(0,0,2.83),(1.33,0.78,5.15),"RT Navy")
    box(p,"Frontglass",(0,-0.408,3.07),(1.13,0.045,3.9),"RT Black Glass")
    box(p,"Topcap",(0,0,5.55),(1.8,0.92,0.32),"RT Red")
    box(p,"BaseRed",(0,-0.4,0.58),(1.35,0.085,0.16),"RT Red")
    box(p,"LeftGlow",(-0.59,-0.45,3.02),(0.045,0.055,3.9),"RT Cyan Glow")
    box(p,"RightGlow",(0.59,-0.45,3.02),(0.045,0.055,3.9),"RT Cyan Glow")
    box(p,"Divider",(0,-0.451,4.18),(1.04,0.05,0.07),"RT Red")
    lettering(p,"BigRT","RT",(0,-0.457,4.83),0.48,"RT White")
    lettering(p,"RebelTech","REBEL TECH",(0,-0.457,3.76),0.15,"RT White")
    for i in range(11):
        z=1.11+i*0.21
        box(p,f"RackIndicator{i:02d}",(0,-0.456,z),(0.77,0.05,0.065),
            "RT Cyan Glow" if i%3==0 else "RT Steel")
    return assemble("rt_fiber_pylon",p)

def make_core():
    p=[]
    cylinder(p,"HexBase",(0,0,0.22),2.30,0.43,6,"RT Navy")
    cylinder(p,"SteelPlate",(0,0,0.49),1.95,0.12,32,"RT Steel")
    cylinder(p,"CentralGlass",(0,0,2.56),0.76,3.86,24,"RT Black Glass")
    cylinder(p,"PowerSpine",(0,0,2.58),0.30,4.15,24,"RT Red")
    cylinder(p,"Canopy",(0,0,4.58),1.27,0.27,24,"RT Navy")
    cylinder(p,"Antenna",(0,0,4.96),0.19,0.56,16,"RT Steel")
    for j,z in enumerate((1.18,2.03,2.88,3.73,4.36)):
        ring(p,f"CircuitRing{j}",(0,0,z),0.88,0.065,"RT Cyan Glow")
    for j in range(8):
        a=j*2*math.pi/8
        x,y=1.43*math.cos(a),1.43*math.sin(a)
        upright=box(p,f"VerticalRib{j}",(x,y,2.66),
                    (0.12,0.18,3.45),"RT Steel")
        upright.rotation_euler[2]=a
        segment=box(p,f"TipLight{j}",(x,y,4.29),
                    (0.14,0.20,0.21),"RT Red" if j%2 else "RT Cyan Glow")
        segment.rotation_euler[2]=a
    return assemble("rt_data_core",p)

def make_sign():
    p=[]
    box(p,"LeftLeg",(-2.08,0,1.51),(0.18,0.25,2.95),"RT Steel")
    box(p,"RightLeg",(2.08,0,1.51),(0.18,0.25,2.95),"RT Steel")
    box(p,"NavySign",(0,0,2.65),(4.5,0.27,1.02),"RT Navy")
    box(p,"RedHeader",(0,-0.158,3.12),(4.58,0.04,0.11),"RT Red")
    box(p,"CyanDivider",(0,-0.161,2.66),(0.055,0.04,0.89),"RT Cyan Glow")
    lettering(p,"SignLeft","THE CORE",(-1.08,-0.167,2.66),0.27,"RT White")
    lettering(p,"SignRight","CLANKA LABS",(1.12,-0.167,2.66),0.22,"RT White")
    lettering(p,"LeftArrow","<",(-1.96,-0.168,2.67),0.33,"RT Cyan Glow")
    lettering(p,"RightArrow",">",(2.00,-0.168,2.67),0.33,"RT Cyan Glow")
    return assemble("rt_wayfinding_sign",p)

assets=[]
for builder in (make_pylon,make_core,make_sign):
    assets.append(builder())

# Art-direction preview. Export GLBs above remained at local origin for placement.
for (obj,_),x in zip(assets,(-6.8,0,7.0)):
    obj.location.x=x

bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"rebel_tech_entrance_kit.blend"))

bpy.ops.object.camera_add(location=(14,-23,14))
cam=bpy.context.object
target=Vector((0,0,2.8))
cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.type="ORTHO"
cam.data.ortho_scale=22.5
scene=bpy.context.scene
scene.camera=cam
scene.render.engine="BLENDER_WORKBENCH"
scene.display.shading.light="STUDIO"
scene.display.shading.color_type="MATERIAL"
scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=True
scene.render.resolution_x=1500
scene.render.resolution_y=860
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.filepath=str(OUT/"entrance_kit_preview.png")
bpy.ops.render.render(write_still=True)

# Independent per-file GLB re-import, without relying on in-memory geometry.
for obj,item in assets:
    path=OUT/item["glb_file"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    if len(meshes)!=1:
        raise RuntimeError(f"{item['asset']} roundtrip produced {len(meshes)} meshes")
    m=meshes[0]
    m.data.calc_loop_triangles()
    t=len(m.data.loop_triangles)
    if t!=item["triangles"] or len(m.data.materials)<2 or not m.data.uv_layers:
        raise RuntimeError(f"{item['asset']} roundtrip differs: {t}, {len(m.data.materials)} mats")
    item["roundtrip"]="PASS_BLENDER_GLTF_ONLY"
    print("ASSET_OK",item["asset"],t,item["dimensions_m"],flush=True)

manifest={"project":"Rebel Tech World — PC2 modular entrance kit v0.1",
          "status":"BLENDER_GLTF_OFFLINE_PASS; PC2 in-game import NOT verified",
          "game_must_remain_closed":True,
          "assets":[item for _,item in assets]}
(OUT/"entrance_kit_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print("RT_ENTRANCE_KIT_PASS",json.dumps(manifest),flush=True)
