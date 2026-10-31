"""Procedural, stylized Tamil Nadu green-and-cream bus. Blender 3.x/4.x."""
import bpy, math, os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def material(name, rgb, metallic=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metallic
    return m
green=material('Transport green',(.12,.34,.18))
cream=material('Cream paint',(.83,.79,.63))
glass=material('Dark windows',(.04,.09,.12))
black=material('Rubber / grille',(.025,.025,.025))
silver=material('Metal',(.55,.55,.52),.65)
white=material('Headlamps',(.95,.92,.8))
amber=material('Signals',(.95,.4,.02))
def box(name, loc, dimensions, mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    return o
def disc(name,loc,r,depth,mat,rot):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc,rotation=rot)
    o=bpy.context.object;o.name=name;o.data.materials.append(mat);return o
# X width, Y length, Z height. Front at negative Y.
box('Green lower shell',(0,0,1.43),(2.42,10.3,1.55),green)
box('Cream upper shell',(0,0,2.55),(2.42,10.3,.72),cream)
box('Roof',(0,0,3.04),(2.48,10.4,.22),cream)
box('Cream waist band',(0,0,2.08),(2.45,10.32,.17),cream)
box('Undercarriage',(0,0,.75),(2,10,.18),black)
for side in (-1,1):
    for i in range(8):
        y=-4.42+i*1.22
        box('Side glass %s %s'%(side,i),(side*1.225,y,2.55),(.025,1.04,.52),glass)
    box('Mirror stalk %s'%side,(side*1.38,-5.16,2.5),(.33,.06,.05),silver)
    box('Mirror %s'%side,(side*1.54,-5.17,2.5),(.18,.10,.32),black)
    for y in (-3.55,3.1):
        for offset in ((0,.18) if y>0 else (0,)):
            x=side*(1.14-offset)
            disc('Tyre %s %s %s'%(side,y,offset),(x,y,.58),.55,.18,black,(0,math.pi/2,0))
            disc('Hub %s %s %s'%(side,y,offset),(side*(abs(x)+.10),y,.58),.24,.025,silver,(0,math.pi/2,0))
box('Front windscreen',(0,-5.175,2.56),(2.06,.045,.56),glass)
box('Destination board',(0,-5.18,2.94),(1.92,.05,.18),green)
box('Front grille',(0,-5.185,1.28),(1.45,.06,.46),black)
for i in range(5):
    box('Grille slat %s'%i,(0,-5.23,1.11+i*.08),(1.36,.025,.015),silver)
for side in (-1,1):
    for j in range(2):
        disc('Headlight %s %s'%(side,j),(side*(.78+j*.18),-5.25,1.17),.07,.03,white,(math.pi/2,0,0))
    box('Indicator %s'%side,(side*1.03,-5.24,1.48),(.16,.035,.10),amber)
box('Front bumper',(0,-5.28,.79),(2.5,.19,.17),silver)
box('Rear bumper',(0,5.28,.79),(2.5,.19,.17),silver)
# Camera / light are not part of exported model.
bpy.ops.object.camera_add(location=(11,-16,9))
cam=bpy.context.object; direction=Vector((0,0,1.5))-cam.location
cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(0,-5,9))
bpy.context.object.data.energy=2200;bpy.context.object.data.size=8
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.cycles.use_denoising=False
for layer in scene.view_layers:
    layer.cycles.use_denoising=False
scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
out=os.path.abspath(os.environ.get('BUS_OUTPUT','TN_BUS_STUDIO/Shared_Assets'))
os.makedirs(out,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'TN_Bus.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in scene.objects:
    if obj.type=='MESH': obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(out,'TN_Bus.glb'),export_format='GLB',use_selection=True)
scene.render.filepath=os.path.join(out,'TN_Bus_preview.png')
bpy.ops.render.render(write_still=True)
print('Generated TN Bus artifacts in',out)
