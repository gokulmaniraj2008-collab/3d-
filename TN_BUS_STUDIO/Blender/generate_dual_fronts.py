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
  # Bevel alone avoids unsupported weighted-normal/Auto Smooth combinations on CI Blender.
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
 # Variant-specific shaped glass: mesh outline, recessed gasket and independent pane.
 def panel(name, outline, y, material):
  verts=[(x,y,z) for x,z in outline]
  mesh=bpy.data.meshes.new(name+' mesh');mesh.from_pydata(verts,[],[tuple(range(len(verts)))])
  mesh.update();obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
  obj.data.materials.append(material);return obj
 if town:
  outline=[(-1.045,2.22),(-1.075,2.29),(-1.055,2.82),(-.97,2.97),(.97,2.97),(1.055,2.82),(1.075,2.29),(1.045,2.22)]
  panel('Town shaped windscreen rubber',[(x*1.045,2.59+(z-2.59)*1.055) for x,z in outline],front-.060,rubber)
  panel('Town panoramic windscreen',outline,front-.082,glass)
  cube('Town lower air intake',(0,front-.10,2.16),(1.75,.028,.042),steel,.012)
 else:
  for side in (-1,1):
   outline=[(.045,2.19),(1.045,2.19),(1.08,2.29),(1.035,2.84),(.94,2.98),(.045,2.98)]
   outline=[(side*x,z) for x,z in outline]
   panel('Ordinary windscreen gasket '+str(side),[(x*1.035,2.585+(z-2.585)*1.05) for x,z in outline],front-.058,rubber)
   panel('Ordinary split glass '+str(side),outline,front-.081,glass)
  cube('Ordinary centre windscreen divider',(0,front-.104,2.59),(.075,.043,.82),ivory,.012)
 cube('Destination outer housing',(0,front-.045,3.055),(w-.26,.15,.29 if town else .35),paint if town else ivory,.04)
 cube('Destination recessed black display',(0,front-.131,3.055),(w-.43,.012,.19 if town else .24),rubber,.014)
 cube('Route number insert',(-.82,front-.147,3.055),(.23,.012,.14),red,.009)
 cube('Destination display lower lip',(0,front-.146,2.91),(w-.35,.04,.035),steel,.008)
 cube('Front cream belt',(0,front-.065,2.05),(w-.08,.045,.15),ivory,.025)
 if town:
  cube('Town broad central grille',(0,front-.085,1.35),(1.13,.045,.48),rubber,.055)
  for side in (-1,1):
   cube('Town recessed rectangular lamp bezel '+str(side),(side*.85,front-.105,1.30),(.50,.085,.29),steel,.032)
   cube('Town dark lamp cavity '+str(side),(side*.85,front-.154,1.30),(.45,.012,.24),rubber,.025)
   for x in (.74,.94):
    cube('Town rectangular reflector %s %s'%(side,x),(side*x,front-.167,1.30),(.165,.013,.166),steel,.017)
    cube('Town rectangular glass %s %s'%(side,x),(side*x,front-.179,1.30),(.143,.013,.143),lamp,.015)
   cube('Town corner turn signal '+str(side),(side*1.09,front-.13,1.63),(.16,.025,.12),amber,.018)
 else:
  cube('Ordinary narrower grille',(0,front-.09,1.39),(.86,.05,.43),rubber,.035)
  for side in (-1,1):
   cube('Ordinary lamp surround '+str(side),(side*.87,front-.095,1.32),(.53,.06,.33),rubber,.035)
   for x in (.75,.99):
    cyl('Ordinary circular reflector %s %s'%(side,x),(side*x,front-.143,1.33),.112,.026,steel)
    cyl('Ordinary circular lens %s %s'%(side,x),(side*x,front-.164,1.33),.092,.028,lamp)
   cube('Ordinary indicator '+str(side),(side*1.07,front-.13,1.62),(.17,.018,.11),amber,.015)
 for i in range(6):
  cube('Grille horizontal blade %d'%i,(0,front-.13,1.16+i*.075),(.95 if town else .71,.015,.012),steel)
 for s in (-1,1):
  # Diagonal articulated arm and separate rubber blade, positioned on glass face.
  def rod(name,p1,p2,r,material):
   from mathutils import Vector
   a,b=Vector(p1),Vector(p2);delta=b-a
   bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=r,depth=delta.length,location=(a+b)/2)
   o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(material)
  pivot=(s*.76,front-.13,2.23);elbow=(s*.53,front-.14,2.39);tip=(s*.14,front-.14,2.48)
  rod('Wiper articulated arm '+str(s),pivot,elbow,.012,steel)
  rod('Wiper rubber blade '+str(s),elbow,tip,.014,rubber)
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
for kind in ('Town','Ordinary'):
 build(kind)
