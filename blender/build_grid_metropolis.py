import bpy,random,json
from pathlib import Path
random.seed(42)
out=Path(r'D:\RebelTechWorld\rebel-tech-theme-park\build\blank-grid-surfaces');out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(n,c,e=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.26;p.inputs['Metallic'].default_value=.5;p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=e;return m
def box(n,x,y,z,w,d,h,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,z));o=bpy.context.object;o.name=n;o.dimensions=(w,d,h);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
black=mat('Obsidian',(.0027,.0033,.0052));navy=mat('Navy',(.0018,.0103,.033));white=mat('White',(.92,.92,.92),.4);blue=mat('RT Blue',(.0176,.0723,1),3);red=mat('RT Red',(.776,.002,.008),3)
for i in range(32):
 x=(i-15.5)*14;y=random.uniform(-18,18);h=random.uniform(24,100);w=random.uniform(7,12);d=random.uniform(8,16)
 box('Tower',x,y,h/2,w,d,h,black if i%2 else navy)
 box('Edge',x-w/2+.1,y-d/2-.04,h/2,.18,.1,h,blue if i%2 else red)
 for z in range(4,int(h)-2,5):
  box('Window strip',x,y-d/2-.08,z,w*.65,.1,.15,white)
bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();bpy.context.object.name='RT Dark Metropolis Backdrop'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'dark-metropolis.blend'));bpy.ops.export_scene.gltf(filepath=str(out/'dark-metropolis.glb'),export_format='GLB',use_selection=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
box('White grid slab',0,0,-.06,48,48,.12,white)
for a in range(-24,25,3):
 box('Dark joint',a,0,.002,.04,48,.006,navy);box('Dark joint',0,a,.002,48,.04,.006,navy)
bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();bpy.context.object.name='RT White Grid Ground 48m'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'white-grid-ground.blend'));bpy.ops.export_scene.gltf(filepath=str(out/'white-grid-ground.glb'),export_format='GLB',use_selection=True)
print('ORIGINAL_WHITE_GRID_AND_METROPOLIS_EXPORTED_NOT_INSTALLED')
