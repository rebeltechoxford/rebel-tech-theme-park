"""Original Rebel Grid prototypes: mobile workshop, branded shells, white lamp, paving.
Run in Blender 4.5+: blender --background --python blender/build_rebel_grid_kit.py
OFFLINE ONLY. GLB is not a native Planet Coaster 2 blueprint. No game files modified.
"""
from pathlib import Path
import json, math
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build'/'pc2'/'rebel-grid'/'models'
MEDIA=ROOT/'build'/'pc2'/'rebel-grid'/'media'
SOURCE=ROOT/'assets'/'branding'/'grid-v1'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def linear(v):
    return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4

def material(name,hexcode,metallic=0.0,rough=.4,emit=0.0):
    rgb=tuple(linear(int(hexcode[i:i+2],16)/255) for i in (0,2,4))
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metallic;p.inputs['Roughness'].default_value=rough
    if emit:p.inputs['Emission Color'].default_value=(*rgb,1);p.inputs['Emission Strength'].default_value=emit
    return m

M={
 'black':material('RT Obsidian','090B10',.3),
 'navy':material('RT Navy','061A33',.55),
 'red':material('RT Signal Red','E10616',.35),
 'blue':material('RT Electric Blue NOT Cyan','244CFF',.3,emit=2),
 'white':material('RT White Paint','FFFFFF',.25),
 'steel':material('RT Graphite Alloy','58616F',.85),
 'glass':material('RT Dark Glass','101B28',.3,.12),
 'rubber':material('RT Rubber','121318',0,.8),
 'light':material('RT Pure White Luminaire','FFFFFF',0,.3,5)
}

def texture(name,path):
    if not path.is_file():raise FileNotFoundError(path)
    im=bpy.data.images.load(str(path),check_existing=True)
    if max(im.size)>1024:im.scale(1024,round(im.size[1]*1024/im.size[0]))
    im.pack()
    m=bpy.data.materials.new(name);m.use_nodes=True
    t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=im
    p=m.node_tree.nodes.get('Principled BSDF');m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color'])
    p.inputs['Roughness'].default_value=.35
    return m

M['logo']=texture('Owner Original RT Circle',SOURCE/'rt-circle-original.png')
for code in ('FOOD','CAFE','TOILETS','SHOP','RESTAURANT','SERVICE','GATE'):
    M[code]=texture('Owner RT Grid '+code,MEDIA/('RT_GRID_'+code+'.png'))

def finish(obj,name,mat,parts):
    obj.name=name;obj.data.materials.append(M[mat]);parts.append(obj);return obj

def box(parts,name,pos,size,mat,bevel=.0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        b=o.modifiers.new('Manufactured edge','BEVEL');b.width=bevel;b.segments=2
        bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
    return finish(o,name,mat,parts)

def cylinder(parts,name,pos,radius,depth,mat,axis='Z',vertices=24):
    rot=(math.pi/2,0,0) if axis=='Y' else (0,0,0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=pos,rotation=rot)
    return finish(bpy.context.object,name,mat,parts)

def mesh(parts,name,verts,faces,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
    return finish(o,name,mat,parts)

def panel(parts,name,x,y,z,w,h,mat):
    # Front faces negative Y, UVs retain the owner artwork's aspect ratio.
    o=mesh(parts,name,[(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)],[(0,1,2,3)],mat)
    uv=o.data.uv_layers.new(name='UVMap')
    for i,v in enumerate(((0,0),(1,0),(1,1),(0,1))):uv.data[i].uv=v
    return o

def text(parts,name,value,pos,size,mat):
    bpy.ops.object.text_add(location=pos,rotation=(math.pi/2,0,0))
    o=bpy.context.object;o.data.body=value;o.data.size=size;o.data.extrude=.0015;o.data.resolution_u=3
    bpy.ops.object.convert(target='MESH');return finish(bpy.context.object,name,mat,parts)

records=[];objects=[]
def export_asset(name,parts):
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
    bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    o.data.calc_loop_triangles();tri=len(o.data.loop_triangles)
    if tri>30000:raise RuntimeError(f'Prototype triangle budget exceeded: {name}: {tri}')
    path=OUT/(name+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_apply=True,export_animations=False,export_cameras=False,export_lights=False)
    records.append({'name':name,'triangles':tri,'dimensions_m':[round(v,3) for v in o.dimensions], 'file':path.name,'bytes':path.stat().st_size,'status':'OFFLINE_EXPORTED_NOT_IMPORTED_IN_PC2'})
    objects.append(o);return o

# High-roof long wheelbase workshop van. Original simplified geometry, not an exact licensed vehicle model.
p=[]
box(p,'Chassis',(-.05,0,.51),(6.9,1.92,.28),'black',.07)
box(p,'High roof cargo',(-.58,0,1.90),(5.58,2.08,2.25),'white',.15)
box(p,'Navy lower wrap',(-.58,0,.97),(5.6,2.1,.5),'navy',.05)
box(p,'Roof cap',(-.58,0,3.04),(5.35,2,.11),'navy',.05)
verts=[(1.72,-1,.82),(3.30,-.89,.82),(3.30,.89,.82),(1.72,1,.82),
       (1.72,-1,2.97),(2.66,-.91,2.48),(2.66,.91,2.48),(1.72,1,2.97)]
mesh(p,'Sloping cabin',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)],'navy')
box(p,'Hood',(2.81,0,1.31),(1.17,1.91,.40),'navy',.12)
mesh(p,'Windscreen',[(2.63,-.84,2.39),(2.63,.84,2.39),(3.15,.85,1.59),(3.15,-.85,1.59)],[(0,1,2,3)],'glass')
box(p,'Front grille',(3.4,0,1.07),(.07,1.15,.35),'black',.03)
for y in (-.79,.79):box(p,'White headlamp',(3.39,y,1.35),(.06,.32,.14),'light',.025)
for x in (-2.12,1.98):
 for y in (-1.06,1.06):
    cylinder(p,'All-terrain tire',(x,y,.54),.50,.26,'rubber','Y',32)
    cylinder(p,'Black alloy wheel',(x,y*1.13,.54),.31,.03,'black','Y',24)
    cylinder(p,'Wheel center',(x,y*1.15,.54),.09,.035,'steel','Y',16)
for y in (-1.06,1.06):
    box(p,'Side running board',(-.7,y,.62),(4.22,.18,.11),'black',.03)
    box(p,'Roof rail',(-.65,y*.85,3.20),(5.5,.06,.12),'black',.015)
    box(p,'Rear red taillight',(-3.40,y*.84,1.31),(.05,.10,.66),'red',.02)
    # Original circle mark on both side panels; the far-side orientation is rotated.
    o=panel(p,'RT original logo',-.95,y*1.015,2.0,1.05,1.05,'logo')
    if y>0:
        # Same image stays readable from the positive-Y side.
        for vert in o.data.vertices:vert.co.x=-1.9-vert.co.x
    box(p,'White side scene light',(-.3,y,2.96),(2.9,.05,.035),'light')
# Near-side diagonal red wrap and blue service stripe.
mesh(p,'Red wrap slash',[(-2.91,-1.063,.72),(-2.57,-1.063,.72),(-2.07,-1.063,2.96),(-2.4,-1.063,2.96)],[(0,1,2,3)],'red')
text(p,'Van brand','REBEL TECH',(-.20,-1.083,2.23),.30,'navy')
text(p,'Van role','MOBILE SOLUTIONS',(-.2,-1.084,1.89),.12,'navy')
text(p,'Van phone','(662) 281-2970',(-.2,-1.084,1.55),.14,'white')
for x in (-2.55,-.8,1.1):box(p,'Roof cross bar',(x,0,3.2),(.07,1.84,.08),'black')
box(p,'Roof solar panel',(-1.35,0,3.31),(1.72,1.28,.045),'glass',.015)
box(p,'Roof terminal',(.88,0,3.37),(.58,.38,.06),'white',.02)
box(p,'Awning cassette',(-.8,-1.17,2.94),(4.65,.16,.14),'black',.04)
van=export_asset('rt_mobile_workshop_van',p)

# Reusable pure-white streetlight; Blender emission is not a PC2 functional light.
p=[];box(p,'Lamp foot',(0,0,.06),(.6,.6,.12),'steel',.04)
box(p,'Lamp mast',(0,0,2.6),(.12,.12,5.1),'navy',.018)
box(p,'Lamp arm',(.46,0,5.1),(1.05,.10,.12),'black',.02)
box(p,'Luminaire',(.89,0,5.04),(.72,.42,.15),'steel',.03)
box(p,'PURE WHITE diffuser',(.89,0,4.957),(.64,.36,.016),'light')
lamp=export_asset('rt_pure_white_streetlight',p)

# Large paving module, intentionally not thousands of miniature floor tiles.
p=[];box(p,'Grid paving',(0,0,-.08),(12,12,.16),'black')
box(p,'Red edge',(-5.90,0,.007),(.055,12,.014),'red')
box(p,'Blue edge',(5.90,0,.007),(.055,12,.014),'blue')
for x in (-3,0,3):box(p,'Expansion seam',(x,0,.001),(.012,12,.003),'steel')
tile=export_asset('rt_large_grid_paving_module',p)

# Open-front custom shells: real game counters/doors must be fitted and tested separately.
for i,code in enumerate(('FOOD','CAFE','TOILETS','SHOP','RESTAURANT','SERVICE')):
 p=[];width=7.2 if code=='RESTAURANT' else 5.8;height=3.6+(i%2)*.35
 box(p,'Back wall',(0,2.45,height/2),(width,.16,height),'navy',.04)
 for x in (-width/2+.08,width/2-.08):box(p,'Side wall',(x,0,height/2),(.16,5,height),'black',.04)
 box(p,'Roof',(0,0,height+.10),(width+.26,5.25,.20),'black',.06)
 for x in (-width/2+.12,width/2-.12):box(p,'Entry red frame',(x,-2.54,height/2),(.10,.12,height),'red')
 box(p,'Blue roof edge',(0,-2.64,height+.12),(width+.3,.045,.065),'blue')
 box(p,'White canopy strip',(0,-2.5,height-.08),(width-.6,.06,.035),'light')
 panel(p,'Custom branded sign',0,-2.57,height-.28,2.4,2.4*720/1280,code)
 # Keep the lower front opening clear for the functional game facility.
 o=export_asset('rt_shell_'+code.lower(),p)
 o.location=(i*8-20,10,0)

# Stage three instances of the shared original van for the overview source scene.
van.location=(-9,-6,0)
for idx,x in enumerate((0,9),2):
 copy=van.copy();copy.data=van.data;bpy.context.collection.objects.link(copy)
 copy.name=f'RT van display instance {idx}';copy.location=(x,-6,0)
 # Three placements remain proposed, not in-game objects.
lamp.location=(-15,-1,0);tile.location=(0,-4,-.01)
scene=bpy.context.scene
if scene.world is None:
    scene.world=bpy.data.worlds.new('Rebel Grid Preview World')
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.035,.035,.035,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
for x in (-12,10):
 bpy.ops.object.light_add(type='AREA',location=(x,-10,15));light=bpy.context.object
 light.data.energy=2200;light.data.shape='DISK';light.data.size=12
 light.rotation_euler=(Vector((0,2,1))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(25,-34,25));cam=bpy.context.object
cam.rotation_euler=(Vector((0,2,1.7))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=56;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=12
scene.render.resolution_x=1500;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'rebel_grid_offline_kit.png')
bpy.ops.file.pack_all();blend=OUT/'rebel_grid_original_kit.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.render.render(write_still=True)

# Verify every independent exported asset imports into a fresh Blender scene.
for record in records:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(OUT/record['file']))
 meshes=[o for o in bpy.data.objects if o.type=='MESH']
 if not meshes:raise RuntimeError('GLB roundtrip contains no geometry')
 count=0
 for o in meshes:o.data.calc_loop_triangles();count+=len(o.data.loop_triangles)
 if count!=record['triangles']:raise RuntimeError('Roundtrip triangle mismatch '+record['name'])
 record['blender_roundtrip']='PASS';print('GRID_ASSET_PASS',record['name'],count,flush=True)
manifest={'status':'OFFLINE_BLENDER_GLTF_PASS_NOT_NATIVE_PC2_CONTENT','assets':records,'van_instances_in_preview':3,'actual_vans_placed_in_pc2':0,'light_color':'#FFFFFF','accent_blue':'#244CFF','accent_red':'#E10616'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('REBEL_GRID_KIT_PASS',json.dumps(manifest),flush=True)
