"""Procedural, stylized Tamil Nadu green-and-cream bus. Blender 3.x/4.x."""
import bpy, math, os
from bus_config import load_config
CONFIG = load_config()
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def material(name, rgb, metallic=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metallic
    return m
green=material('Transport green',CONFIG['body_color'])
cream=material('Cream paint',CONFIG['roof_color'])
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
# Open upper cabin rather than opaque upper cube.
for side in (-1,1):
    box('Upper roof rail %s'%side,(side*1.17,0,2.89),(.13,10.25,.19),cream)
    for i in range(9):
        box('Window pillar %s %s'%(side,i),(side*1.18,-4.96+i*1.24,2.53),(.10,.09,.66),cream)
box('Front upper fascia',(0,-5.10,2.91),(2.38,.15,.26),cream)
box('Rear upper fascia',(0,5.10,2.58),(2.38,.15,.72),cream)
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
# Phase 2: passenger cabin, driver cockpit and exterior fixtures.
seat=material('Seat upholstery blue',CONFIG['seat_color'])
seat_frame=material('Seat frame',(.19,.20,.19),.35)
floor_mat=material('Non slip floor',(.23,.22,.19))
red=material('Tail lamp red',(.7,.035,.025))
yellow=material('Handrail yellow',(.85,.64,.07),.35)
board=material('Destination board dark',(.055,.075,.045))
box('Passenger cabin floor',(0,0,1.24),(2.17,9.75,.09),floor_mat)
box('Centre aisle',(0,.25,1.295),(.48,8.8,.012),black)
for row in range(CONFIG['seat_rows']):
    y=-3.40+row*1.16
    for side in (-1,1):
        x=side*.76
        box('Seat cushion %s %s'%(row,side),(x,y,1.73),(.76,.65,.16),seat)
        box('Seat back %s %s'%(row,side),(x,y+.27,2.04),(.76,.13,.68),seat)
        for leg in (-.23,.23):
            box('Seat support %s %s %s'%(row,side,leg),(x+leg,y,1.47),(.055,.055,.45),seat_frame)
box('Driver seat cushion',(-.70,-4.55,1.72),(.68,.62,.17),seat)
box('Driver seat back',(-.70,-4.25,2.03),(.68,.12,.64),seat)
box('Dashboard',(0,-4.91,1.99),(2.12,.39,.24),black)
disc('Steering wheel',(-.68,-4.60,2.28),.24,.055,black,(math.pi/2,0,0))
box('Fare box',(.68,-4.43,1.73),(.32,.28,.68),seat_frame)
for side in (-1,1):
    box('Overhead grab rail %s'%side,(side*.63,.15,2.79),(.035,8.9,.035),yellow)
    for y in (-3.1,-.8,1.5,3.8):
        box('Grab pole %s %s'%(side,y),(side*.63,y,2.12),(.035,.035,1.38),yellow)
    box('Side skirt trim %s'%side,(side*1.237,.2,1.03),(.028,9.6,.065),silver)
    for i in range(8):
        y=-4.42+i*1.22
        box('Window top trim %s %s'%(side,i),(side*1.246,y,2.83),(.018,1.05,.024),silver)
        box('Window bottom trim %s %s'%(side,i),(side*1.246,y,2.27),(.018,1.05,.024),silver)
    box('Entry door outline %s'%side,(side*1.253,-2.55,1.75),(.024,1.0,1.65),silver)
    box('Entry door split %s'%side,(side*1.268,-2.55,1.75),(.028,.026,1.58),black)
    box('Entry handle %s'%side,(side*1.282,-2.26,1.64),(.035,.055,.21),silver)
    box('Rear side marker %s'%side,(side*1.26,4.52,1.24),(.035,.16,.09),amber)
box('Destination sign face',(0,-5.216,2.94),(1.76,.024,.135),board)
# Convert destination text to a mesh so GLB exporters can include it.
bpy.ops.object.text_add(location=(-.82,-5.245,2.902), rotation=(math.pi/2,0,0))
sign=bpy.context.object
sign.name='Destination text'
sign.data.body=CONFIG['destination']
sign.data.size=.105
sign.data.extrude=.001
sign.data.materials.append(white)
bpy.ops.object.convert(target='MESH')
box('Registration plate front',(0,-5.39,.91),(.50,.025,.13),white)
box('Rear window',(0,5.20,2.55),(1.95,.028,.50),glass)
box('Rear registration plate',(0,5.40,.91),(.50,.025,.13),white)
for side in (-1,1):
    box('Rear tail lamp %s'%side,(side*1.03,5.23,1.35),(.18,.035,.36),red)
    box('Rear indicator %s'%side,(side*1.03,5.25,1.63),(.18,.035,.11),amber)
    box('Front fog lamp %s'%side,(side*.98,-5.30,.85),(.16,.035,.075),white)
for y in (-2.8,.1,2.9)[:CONFIG['roof_vents']]:
    box('Roof vent %s'%y,(0,y,3.19),(.62,.72,.085),silver)
for side in (-1,1):
    box('Rain gutter %s'%side,(side*1.245,0,3.075),(.045,10.35,.035),silver)
# Camera / light are not part of exported model.
bpy.ops.object.camera_add(location=(11,-16,9))
cam=bpy.context.object; direction=Vector((0,0,1.5))-cam.location
cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(0,-5,9))
bpy.context.object.data.energy=2200;bpy.context.object.data.size=8
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=CONFIG['preview_samples']
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
