import bpy, json
from pathlib import Path
out=Path(r'D:\RebelTechWorld\rebel-tech-theme-park\build\blank-grid-surfaces');out.mkdir(parents=True,exist_ok=True)
def mat(name,col,emit=0,rough=.22):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.45
 if emit:p.inputs['Emission Color'].default_value=(*col,1);p.inputs['Emission Strength'].default_value=emit
 return m
def box(name,loc,scale,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
manifest=[]
for name,col in [('grid-floor',(1,1,1)),('guest-blue',(0.0176,.0723,1)),('queue-red',(.776,.002,.008))]:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 black=mat(name+'-obsidian',(.0027,.0033,.0052));light=mat(name+'-light',col,3);body=mat(name+'-surface',col if name!='grid-floor' else (.0027,.0033,.0052),0,.18)
 box(name,(0,0,-.06),(12,12,.12),body)
 for axis in (0,1):
  for n in range(-6,7,3):
   loc=[0,0,.006];loc[axis]=n;size=[12,.035,.012] if axis==1 else [.035,12,.012];box('lit-grid-line',loc,size,light)
 bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(name+'.blend')));bpy.ops.export_scene.gltf(filepath=str(out/(name+'.glb')),export_format='GLB',use_selection=True)
 manifest.append({'name':name,'size_m':[12,12],'grid_pitch_m':3,'line_width_m':.035,'status':'OFFLINE_MODEL_ONLY_NOT_INSTALLED_IN_PC2'})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('GRID_SURFACES_EXPORTED_NOT_PC2_INSTALLED')
