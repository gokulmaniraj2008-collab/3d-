"""Phase 6 front-first comparative prototypes. Run blender -b --python generate_dual_fronts.py.
These are distinct TNSTC-inspired design studies, not certified replicas of a particular vehicle.
X width, negative Y front, Z up. Original simulator assets remain untouched.
"""
import bpy, math, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","Shared_Assets","Front_Studies"))
os.makedirs(ROOT,exist_ok=True)
def mat(name,rgb,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Metallic'].default_value=metal
 return m
def cube(name,loc,dim,m,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:
  mod=o.modifiers.new('Soft stamped panel edge','BEVEL');mod.width=bevel;mod.segments=3
  o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o
def cyl(name,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc,rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=name;o.data.materials.append(m);return o
def build(kind):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 town=kind=='Town'
 paint=mat('Town green' if town else 'Ordinary dark green',(.12,.36,.19) if town else (.08,.28,.17))
 ivory=mat('Ivory cream',(.82,.78,.61));glass=mat('Tinted windscreen',(.055,.115,.145))
 rubber=mat('Black seals and grille',(.025,.029,.027));steel=mat('Satin metal',(.57,.59,.57),.5)
 lamp=mat('Headlamp lens',(.93,.94,.82));amber=mat('Indicator amber',(1,.40,.02));red=mat('Route marking',(.72,.09,.055))
 w=2.43 if town else 2.49; front=-2.35 if town else -2.50
 cube('Full width body shell',(0,0,1.48),(w,4.65 if town else 4.95,1.58),paint,.10)
 cube('Roof cap',(0,.03,3.12),(w+.05,4.65 if town else 4.95,.19),ivory,.08)
 for s in (-1,1):
  cube('A pillar %s'%s,(s*(w/2-.11),front+.04,2.59),(.16,.17,.91),ivory,.035)
  cube('Mirror bracket %s'%s,(s*(w/2+.17),front-.13,2.45),(.39,.045,.055),steel)
  cube('Mirror casing %s'%s,(s*(w/2+.34),front-.13,2.44),(.20,.13,.39),rubber,.04)
  cube('Mirror reflector %s'%s,(s*(w/2+.34),front-.207,2.44),(.155,.012,.33),steel)
  cube('Wheel arch side %s'%s,(s*(w/2+.018),-.65,.85),(.025,.91,.075),rubber)
 cube('Windscreen gasket',(0,front-.025,2.59),(w-.22,.035,.79 if town else .83),rubber,.04)
 cube('Wide town windscreen' if town else 'Ordinary windscreen',(0,front-.049,2.59),(w-.31,.019,.71 if town else .75),glass,.035)
 if not town:
  cube('Ordinary split windscreen centre',(0,front-.07,2.59),(.048,.03,.76),ivory)
 else:
  cube('Town windscreen lower vent',(0,front-.069,2.18),(1.82,.025,.038),steel)
 cube('Destination housing',(0,front-.048,3.015),(w-.28,.095,.25 if town else .30),paint if town else rubber,.03)
 cube('Destination display',(0,front-.103,3.02),(w-.43,.012,.15 if town else .19),rubber)
 cube('Route number panel',(-.79,front-.12,3.02),(.23,.013,.12),red)
 cube('Front cream belt',(0,front-.065,2.05),(w-.08,.045,.15),ivory,.025)
 if town:
  cube('Town broad central grille',(0,front-.085,1.35),(1.13,.045,.48),rubber,.055)
  for s in (-1,1):
   cube('Town rectangular twin lamp housing',(s*.85,front-.09,1.30),(.47,.06,.25),rubber,.04)
   for x in (.74,.94):cube('Town rectangular headlamp %s %s'%(s,x),(s*x,front-.133,1.30),(.145,.015,.145),lamp,.015)
   cube('Town corner turn signal %s'%s,(s*1.09,front-.12,1.63),(.16,.018,.12),amber,.018)
 else:
  cube('Ordinary narrower grille',(0,front-.09,1.39),(.86,.05,.43),rubber,.035)
  for s in (-1,1):
   cube('Ordinary lamp surround %s'%s,(s*.87,front-.095,1.32),(.53,.06,.33),rubber,.035)
   for x in (.75,.99):cyl('Ordinary circular lamp %s %s'%(s,x),(s*x,front-.14,1.33),.095,.026,lamp)
   cube('Ordinary indicator %s'%s,(s*1.07,front-.13,1.62),(.17,.018,.11),amber,.015)
 for i in range(6):
  cube('Grille horizontal blade %d'%i,(0,front-.13,1.16+i*.075),(.95 if town else .71,.015,.012),steel)
 for s in (-1,1):
  cube('Wiper arm %s'%s,(s*.48,front-.093,2.31),(.78,.018,.025),rubber)
  cube('Bumper reflector %s'%s,(s*.99,front-.19,.84),(.14,.02,.055),amber)
 cube('Stamped front bumper',(0,front-.16,.81),(w+.12,.20,.19),steel,.055)
 cube('Number plate mount',(0,front-.273,.83),(.44,.014,.105),rubber)
 cube('Roof marker',(0,front-.075,3.20),(.43,.07,.045),amber)
 # Both studies export independent front geometry; no demo bus overwrite.
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.context.scene.objects:
  if o.type=='MESH':o.select_set(True)
 bpy.context.view_layer.objects.active=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 out=os.path.join(ROOT,'TNSTC_'+kind+'_Front.glb')
 bpy.ops.export_scene.gltf(filepath=out,export_format='GLB',use_selection=True)
 print('EXPORTED',out,os.path.getsize(out))
for kind in ('Town','Ordinary'):build(kind)
