import bpy, math, json, csv
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection': bpy.data.collections.remove(c)
scene=bpy.context.scene
scene.unit_settings.system='NONE'
scene['scale_status']='Unmeasured. Outer width = 10 arbitrary units. All heights estimated.'
scene['scope']='FV300 open scanhead only. Round 1 blockout, independent rebuild.'
scene['reference_commit']='a34300bcfe74eabe824f81419d8e13f4c39ac116'
collections={}
for name in ['01_Housing','02_Bridge_and_partitions','03_Central_mechanism','04_Right_mechanisms','05_Electronics','06_Cable_envelopes_EST','07_External_ports_EST','90_Reference','99_Cameras']:
    c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
COL='01_Housing'
silver=(.52,.55,.57,1); rim=(.73,.75,.74,1); black=(.055,.066,.077,1); brass=(.45,.34,.15,1); pcb=(.13,.24,.20,1)
parts=[]
# Coordinates manually re-read from 2048-wide overhead photo. No old geometry imported.
# Image plane: left=210, right=1680, top=225, bottom=960.
# Z is arbitrary estimated elevation above hidden floor.
S=10/1470
def p(u,v,z):return ((u-945)*S,(592.5-v)*S,z)
def tag(o,name,color,note='Visible plan envelope; elevation and hidden shape estimated.'):
    o.name=name;o.color=color
    for c in list(o.users_collection):c.objects.unlink(o)
    collections[COL].objects.link(o)
    o['evidence']='20260910_171623.jpg; 153030; 153051; 153102'
    o['uncertainty']=note
    o['height_status']='ESTIMATED'
    parts.append(o)
    return o
def box(name,u,v,w,h,z,t,color=silver):
    bpy.ops.mesh.primitive_cube_add(size=1,location=p(u+w/2,v+h/2,z+t/2))
    o=bpy.context.object;o.dimensions=(w*S,h*S,t)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return tag(o,name,color)
def rod(name,a,b,r,color=black):
    a=Vector(p(*a));b=Vector(p(*b));d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r*S,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y')
    return tag(o,name,color)
def hole(o,a,b,r):
    cutter=rod('_temporary_cutter',a,b,r)
    parts.remove(cutter)
    bpy.context.view_layer.objects.active=o
    m=o.modifiers.new('Through opening','BOOLEAN');m.operation='DIFFERENCE';m.object=cutter
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
def bevel(o,width=.025):
    m=o.modifiers.new('Editable edge radius EST','BEVEL');m.width=width;m.segments=3
    m=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o
# Housing walls separate from hidden floor, editable estimated height H.
H=1.42
floor=box('H01_Base_floor_EST',210,225,1470,735,0,.10)
floor['uncertainty']='Underside unseen; flat base and thickness wholly assumed.'
for name,u,v,w,h in [('H02_Left_wall_EST',210,225,22,735),('H03_Right_wall_EST',1658,225,22,735),('H04_Rear_wall_EST',232,225,1426,20),('H05_Front_wall_EST',232,939,1426,21)]:
    o=box(name,u,v,w,h,.1,H-.1)
    if name.startswith('H03'):hole(o,(1645,528,.69),(1692,528,.69),49)
    bevel(o)
# Top flange traces distinguish lip from deep wall.
for i,(u,v,w,h) in enumerate([(210,225,1470,14),(210,945,1470,15),(210,239,14,706),(1666,239,14,706)]):
    bevel(box('H06_Rim_'+str(i+1),u,v,w,h,H,.035,rim),.014)
COL='02_Bridge_and_partitions'
# Double window bridge built as one editable slab with two boolean openings.
bridge=box('B01_Double_window_bridge',454,250,802,338,H-.015,.055,rim)
for i,(u,v,w,h) in enumerate([(510,275,430,253),(1000,276,222,234)]):
    cutter=box('_window',u,v,w,h,H-.1,.30)
    parts.remove(cutter);bevel(cutter,.06)
    bpy.context.view_layer.objects.active=cutter
    bpy.ops.object.modifier_apply(modifier=cutter.modifiers[0].name)
    bpy.context.view_layer.objects.active=bridge
    m=bridge.modifiers.new('Window '+str(i+1),'BOOLEAN');m.object=cutter
    bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
bevel(bridge,.02)
for name,u,v,w,h in [('B02_Left_bay_partition',447,250,25,687),('B03_Right_bay_partition',1227,250,31,687),('B04_Central_cross_partition',472,553,755,27),('B05_Electronic_separator',944,275,49,278)]:
    o=box(name,u,v,w,h,.10,H-.12)
    if name.startswith('B04'):
        hole(o,(648,542,.69),(648,592,.69),56)
    if name.startswith('B03'):
        hole(o,(1210,765,.63),(1271,765,.63),58)
    bevel(o,.025)
o=box('B06_Left_dark_baffle',300,355,7,515,.12,1.04,black)
hole(o,(290,642,.59),(316,642,.59),20)
COL='03_Central_mechanism'
box('C01_Cast_support_main',525,716,190,112,.1,.72)
box('C02_Cast_support_step',685,686,43,167,.1,.89)
rod('C03_Rear_barrel',(650,584,.79),(650,699,.79),56)
rod('C04_Rear_barrel_rim',(650,580,.79),(650,593,.79),61)
rod('C05_Front_barrel',(650,818,.56),(650,866,.56),52)
rod('C06_Brass_guide',(755,603,.95),(755,701,.95),21,brass)
# Broad horizontal pierced plate, plus separate folded returns and open end.
plate=box('C07_Pierced_long_plate',786,608,137,321,.89,.075,black)
hole(plate,(842,778,.83),(842,778,1.04),21)
bevel(plate,.016)
box('C08_Long_plate_left_return',786,608,8,321,.22,.67,black)
box('C09_Long_plate_right_return',915,608,8,321,.22,.67,black)
box('C10_Left_folded_cover_top',715,699,63,230,.76,.05,black)
box('C11_Left_folded_cover_return',715,699,7,230,.20,.56,black)
# Short channel behind long plate: open rather than solid slab.
box('C12_Rear_channel_side',929,607,8,105,.30,.83,black)
box('C13_Rear_channel_end',930,705,132,7,.30,.83,black)
box('C14_Rear_channel_floor_EST',930,607,132,105,.30,.05,black)
box('C15_Wheel_support',931,752,42,134,.1,.42)
rod('C16_Upright_wheel_axis_X',(969,813,.62),(1016,813,.62),79)
rod('C17_Wheel_face',(1016,813,.62),(1024,813,.62),71,silver)
rod('C18_Transverse_brass_shaft',(920,813,.62),(1080,813,.62),7,brass)
rod('C19_Bevel_drive_envelope_EST',(1068,813,.62),(1087,813,.62),19)
rod('C20_Longitudinal_drive_envelope_EST',(1100,831,.54),(1100,849,.54),20)
rod('C21_Longitudinal_sleeve',(1100,849,.54),(1100,926,.54),18,brass)
box('C22_Actuator_support',1033,622,92,73,.13,.12)
rod('C23_Upper_actuator',(1057,653,.41),(1118,653,.41),24)
box('C24_Actuator_vertical_board',1131,611,7,120,.12,.71,pcb)
box('C25_Transverse_link',937,700,180,11,.28,.04,brass)
COL='04_Right_mechanisms'
bevel(box('R01_Upper_mount_plate',1270,392,194,190,.10,.09,(.29,.29,.25,1)))
rod('R02_Upper_cylinder_Y',(1425,423,.42),(1425,479,.42),30,silver)
rod('R03_Upper_cylinder_X',(1268,530,.39),(1345,530,.39),27)
box('R04_Upper_clamp_Y',1392,463,65,51,.20,.31,black)
box('R05_Upper_clamp_X',1337,505,65,50,.20,.27,black)
o=box('R06_Angled_connector',1351,474,52,23,.43,.10,black);o.rotation_euler.z=math.radians(35)
bevel(box('R07_Slider_base',1370,614,224,104,.1,.13,black))
for i,v in enumerate([620,699]):
    box('R08_Slider_rail_'+str(i),1385,v,184,10,.23,.065)
for name,u,v,w,h in [('R09_Frame_left',1482,635,12,59),('R10_Frame_right',1549,635,12,59),('R11_Frame_rear',1494,635,55,10),('R12_Frame_front',1494,684,55,10)]:
    box(name,u,v,w,h,.29,.30,black)
rod('R13_Diagonal_plate_edge',(1388,684,.45),(1453,624,.45),10,silver)
o=box('R14_Diagonal_plate',1400,637,65,42,.39,.065,black);o.rotation_euler.z=math.radians(43)
# Key correction: vertical Z spindle, not the horizontal X shaft in v0.2.
box('R15_Vertical_adjuster_block',1570,627,51,58,.24,.34)
rod('R16_Vertical_adjustment_spindle',(1596,652,.56),(1596,652,1.68),8,silver)
rod('R17_Slider_round_knob',(1499,652,.40),(1515,652,.40),14,brass)
rod('R18_Lower_silver_barrel',(1460,753,.39),(1460,866,.39),27,silver)
rod('R19_Lower_cross_pin',(1417,783,.39),(1517,783,.39),11,silver)
rod('R20_Lower_brass_barrel',(1318,812,.32),(1318,864,.32),31,brass)
rod('R21_Lower_black_barrel',(1318,864,.32),(1318,918,.32),39)
o=box('R22_Pierced_brass_flag',1291,746,51,67,.37,.075,brass)
hole(o,(1317,778,.33),(1317,778,.49),18)
COL='05_Electronics'
box('E01_Metal_module',1008,291,87,215,.1,1.10)
box('E02_Upright_electronics_board',1152,287,12,227,.13,1.08,pcb)
for i,v in enumerate([326,380,440]):
    box('E03_Board_component_'+str(i),1110,v,39,37,.35,.50,black)
box('E04_Left_connector_board',525,504,140,17,.21,.09,pcb)
COL='06_Cable_envelopes_EST'
def cable(name,pts,r,color):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r*S;cu.bevel_resolution=3
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for b,co in zip(sp.bezier_points,pts):
        b.co=p(*co);b.handle_left_type='AUTO';b.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);collections[COL].objects.link(o)
    tag(o,name,color,'Visible cable envelope only; hidden routing and endpoints not reconstructed.')
    return o
cable('W01_Right_outer_loop_EST',[(1300,419,.55),(1390,343,.93),(1466,282,1.17),(1365,266,1.20),(1268,288,1.10)],8,black)
cable('W02_Right_inner_loop_EST',[(1312,468,.48),(1360,391,.69),(1435,304,1.05),(1355,287,1.09),(1270,318,.93)],6,(.30,.33,.33,1))
cable('W03_Left_cable_loop_EST',[(558,472,.44),(603,346,1.01),(713,307,1.10),(828,334,1.17),(929,284,1.27)],6,(.57,.55,.47,1))
cable('W04_Left_inner_cable_EST',[(689,485,.33),(680,397,.86),(774,384,1.00),(871,329,1.12),(929,291,1.22)],6,(.63,.61,.54,1))
cable('W05_Left_high_bundle_EST',[(576,435,.76),(635,351,1.17),(759,319,1.28),(932,275,1.37)],6,(.18,.21,.26,1))
cable('W06_Right_board_bundle_EST',[(1118,289,1.18),(1140,398,1.08),(1143,507,.89),(1133,597,.53)],5,(.28,.22,.18,1))
COL='07_External_ports_EST'
rod('P01_Right_external_port_EST',(1667,528,.69),(1860,528,.69),86)
rod('P02_Front_external_port_EST',(1100,951,.54),(1100,1045,.54),78)
rod('P03_Front_adjuster_EST',(855,951,.53),(855,1010,.53),11)
rod('P04_Front_adjuster_EST',(777,951,.51),(777,1040,.51),7,brass)
# Packed reference empties excluded from viewport by default, available for editing.
COL='90_Reference'
for i,fn in enumerate(['20260910_171623.jpg','20260910_153030.jpg','20260910_153051.jpg','20260910_153102.jpg']):
    im=bpy.data.images.load(str(ROOT.parent/fn));im.pack()
    o=bpy.data.objects.new('REF_'+fn,None);collections[COL].objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.empty_display_size=10;o.location=(0,0,-.05-i*.01);o.hide_render=True;o.hide_viewport=True
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.world.color=(.8,.8,.8)
sh=scene.display.shading;sh.light='STUDIO';sh.studio_light='paint.sl'
sh.color_type='OBJECT';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH'
sh.curvature_ridge_factor=1.25;sh.curvature_valley_factor=1.1
sh.background_type='WORLD';sh.show_specular_highlight=False
scene.view_settings.view_transform='Standard'
def camera(name,loc,target,scale,typ='ORTHO'):
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);collections['99_Cameras'].objects.link(o)
    o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    data.type=typ;data.ortho_scale=scale;data.lens=48;data.clip_end=200
    return o
top=camera('CAM_01_Overhead_reference_approx',(0,-.32,19),(0,0,.65),13.8)
camera('CAM_02_Oblique_153030_approx',(0,-9.6,16),(0,0,.65),13.8)
camera('CAM_03_Front_EST',(0,-17,5.9),(0,0,.65),13.5)
camera('CAM_04_Right_EST',(14,-7,10),(0,0,.65),13.5)
camera('CAM_05_Underside_EST',(0,-8,-13),(0,0,.65),13.5)
scene.camera=top
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active=bridge;bridge.select_set(True)
for scr in bpy.data.screens:
    for a in scr.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_perspective='CAMERA'
            a.spaces.active.overlay.show_overlays=False
            a.spaces.active.shading.color_type='OBJECT'
notes="""FV300 round 1 - editable Blender blockout
No old geometry imported. Width 10 arbitrary units, no millimetre claim.
Four packed scanhead photographs. IX71 context photos not modeled.
Key correction: R16 is a vertical spindle based on 153051.
C07-C14 are separate folded/open-channel parts, not solid blocks.
Visible XY silhouettes traced from overhead image; all elevations estimated.
Housing H01 unseen base, housing depth, hidden surfaces and all port lengths estimated.
Camera matching is approximate, not calibrated. No invented optical path.
Stop here for user's proportion review before adding detail.
"""
t=bpy.data.texts.new('READ_ME_FIRST');t.write(notes)
with (ROOT/'parts.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['name','collection','evidence','uncertainty'])
    for o in parts:w.writerow([o.name,o.users_collection[0].name,o['evidence'],o['uncertainty']])
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'FV300_round1.blend'))
print('SAVED',len(parts),'parts',flush=True)

