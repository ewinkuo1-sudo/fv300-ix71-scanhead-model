import bpy, math, json, csv
from pathlib import Path
from mathutils import Vector, Matrix
R=Path(__file__).resolve().parent
P=json.loads((R/'parameters.json').read_text(encoding='utf-8-sig'))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):bpy.data.collections.remove(c)
sc=bpy.context.scene
sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=.001;sc.unit_settings.length_unit='MILLIMETERS'
sc['scope']='FV300 + IX71FVSF-2 main assembly, blockout round 1. No table/peripherals.'
sc['dimension_status']='IX71 catalog dimensions are nominal reference only, not measurement of this specimen.'
sc['scanner_dimensions']='ESTIMATED from photos; independent editable parameters.'
groups={}
for name in ['01_IX71_Frame','02_IX71_Stage','03_IX71_Nosepiece','04_IX71_Binocular','05_IX71_Illumination','06_IX71_Controls','07_Side_connection_EST','08_FV300_Reused_Interior','09_FV300_Housing_EST','10_FV300_Lid_EST','90_References','99_Cameras']:
    c=bpy.data.collections.new(name);sc.collection.children.link(c);groups[name]=c
white=(.72,.73,.69,1);gray=(.44,.47,.48,1);dark=(.065,.078,.089,1);glass=(.11,.16,.17,1)
COL='01_IX71_Frame';parts=[]
src='Olympus IX71/IX81 brochure M1539E-0909B printed p28; user 153139/153147/153221'
def attach(o,name,col,status='EST shape; catalog/photo constrained placement'):
    o.name=name;o.color=col
    for c in list(o.users_collection):c.objects.unlink(o)
    groups[COL].objects.link(o)
    o['evidence']=src;o['certainty']=status
    parts.append(o);return o
def box(name,loc,dim,col=white,b=2,status='EST shape; catalog/photo constrained placement'):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);attach(o,name,col,status)
    if b:bevel(o,b)
    return o
def bevel(o,b):
    m=o.modifiers.new('Editable edge rounding EST','BEVEL');m.width=b;m.segments=3
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
def cyl(name,a,b,r,col=dark,inner=0):
    a=Vector(a);b=Vector(b);d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y')
    attach(o,name,col)
    for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
    if inner:
        subtract(o,cyl('_cut',a-d.normalized(),b+d.normalized(),inner))
    return o
def subtract(o,cutter):
    if cutter in parts:parts.remove(cutter)
    bpy.context.view_layer.objects.active=o
    m=o.modifiers.new('Through opening','BOOLEAN');m.object=cutter
    bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
def prism(name,yz,width,col=white,b=3):
    verts=[(x,y,z) for x in [-width/2,width/2] for y,z in yz];n=len(yz)
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);groups[COL].objects.link(o);attach(o,name,col)
    bevel(o,b);return o
# Body coordinate frame: X operator's right, Y rear, Z up; XY optical axis is (0,0).
L=P['ix71_base_length_mm'];W=P['ix71_front_body_width_mm'];ST=P['stage_height_mm']
for i,(x,y) in enumerate([(-49,-177),(49,-177),(-126,177),(126,177)]):
    cyl('IX01_Foot_'+str(i),(x,y,0),(x,y,13),13)
prism('IX02_Lower_body', [(-197,13),(-197,35),(-181,165),(-156,184),(156,184),(175,145),(175,13)],W,b=5)
box('IX03_Rear_base_crossbar',(0,183,21),(290,28,20),white,5,'Catalog reference 290 mm transverse envelope; specimen unmeasured.')
# At y=197 gives catalog 394 mm base length between front/rear feet outline.
box('IX04_Rear_lower_support',(0,124,215),(132,74,75),white,3)
prism('IX05_Front_binocular_support',[(-181,164),(-174,219),(-144,264),(-105,279),(-69,277),(-67,174)],W,b=3)
# Open bay under stage: no solid block through the turret/objectives.
box('IX06_Left_upper_bay_rail',(-59,39,191),(15,166,32),white,2)
box('IX07_Right_upper_bay_rail',(59,39,191),(15,166,32),white,2)
box('IX08_Stage_rear_support',(0,136,269),(128,47,51),white,2)
box('IX09_Right_access_panel',(68.5,60,104),(3,123,104),white,4)
box('IX10_Front_control_panel',(0,-186,110),(116,4,119),white,4)
# Stage chosen as simplified manual photo stage; catalog size is baseline, not exact accessory ID.
COL='02_IX71_Stage'
stage=box('ST01_Manual_stage_main',(0,35,ST-8),(P['stage_width_mm'],P['stage_depth_mm'],16),dark,3)
subtract(stage,cyl('_stage_cut',(0,0,ST-30),(0,0,ST+10),55))
cyl('ST02_Stage_insert_ring',(0,0,ST-3),(0,0,ST+1),55,gray,inner=22)
box('ST03_X_translation_rail',(0,137,ST+4),(244,22,14),dark,2)
box('ST04_Y_translation_rail',(113,33,ST+3),(17,204,12),dark,2)
box('ST05_Stage_control_bracket',(135,93,ST-25),(25,44,46),dark,2)
cyl('ST06_Stage_control_shaft',(136,95,ST-160),(136,95,ST-35),5,gray)
cyl('ST07_Stage_coaxial_grip',(136,95,ST-78),(136,95,ST-33),14)
cyl('ST08_Stage_lower_grip',(136,95,ST-167),(136,95,ST-140),11)
COL='03_IX71_Nosepiece'
cyl('NP01_Filter_turret_lower',(0,46,184),(0,46,218),56,dark)
cyl('NP02_Filter_turret_rim',(0,46,215),(0,46,221),60,gray)
cyl('NP03_Nosepiece_disk',(0,43,236),(0,43,249),59,dark)
# Only one objective shown installed, matching visible objective in user's side photo.
cyl('NP04_Active_objective_mount',(0,0,247),(0,0,258),16,gray)
cyl('NP05_Active_objective_body',(0,0,258),(0,0,286),13,gray)
cyl('NP06_Active_objective_tip',(0,0,286),(0,0,296),9,dark)
# Empty sockets communicate six-position nominal turret without inventing six installed lenses.
for i in range(1,6):
    a=2*math.pi*i/6
    x=43*math.sin(a);y=43-43*math.cos(a)
    cyl('NP07_Empty_socket_'+str(i),(x,y,247),(x,y,251),13,gray,inner=9)
box('NP08_Filter_slider',(-39,-8,209),(31,21,10),dark,1)
COL='04_IX71_Binocular'
# Inclined head silhouette, two separately editable barrels.
prism('BI01_Observation_tube_adapter',[(-164,234),(-196,260),(-151,304),(-116,273)],104,dark,3)
axis=Vector((0,-.66,.75)).normalized()
for i,x in enumerate([-31,31]):
    a=Vector((x,-168,271))
    cyl('BI02_Prism_body_'+str(i),a,a+axis*65,25,gray)
    cyl('BI03_Eyepiece_barrel_'+str(i),a+axis*58,a+axis*120,19,dark)
    cyl('BI04_Eyepiece_rim_'+str(i),a+axis*116,a+axis*127,21,dark,inner=14)
    cyl('BI05_Eyepiece_glass_'+str(i),a+axis*120,a+axis*121,14,glass)
cyl('BI06_Interpupillary_bridge',(-31,-186,292),(31,-186,292),21,gray)
# Head raised to nominal eye height for tilted configuration; mount extends seamlessly.
for o in list(parts):
    if o.users_collection[0].name==COL:o.location.z+=P['binocular_raise_mm']
# Raise adapter lower support separately.
box('BI07_Head_riser',(0,-135,282),(93,60,28),white,3)
COL='05_IX71_Illumination'
# Fiber head in user's 153221; omit standard large rear halogen lamphouse.
HT=P['illumination_top_mm'];py=P['pillar_y_mm']
prism('IL01_Pillar_lower',[(py-31,184),(py-31,355),(py+27,355),(py+27,184)],65,white,3)
prism('IL02_Pillar_upper',[(py-21,348),(py-21,570),(py+27,590),(py+27,348)],55,white,3)
box('IL03_Condenser_height_rail',(0,py-25,455),(22,8,165),gray,1)
box('IL04_Condenser_carriage',(0,py-37,459),(66,26,41),dark,3)
box('IL05_Condenser_arm',(0,(py-42)/2,454),(54,py-42,18),dark,2)
cyl('IL06_Condenser_body',(0,0,420),(0,0,461),46,dark)
cyl('IL07_Condenser_turret',(0,0,406),(0,0,427),55,dark)
cyl('IL08_Condenser_lower_lens',(0,0,371),(0,0,410),28,dark)
cyl('IL09_Condenser_open_top',(0,0,461),(0,0,470),36,gray,inner=29)
cyl('IL10_Condenser_side_knob',(48,py-31,460),(73,py-31,460),19,dark)
cyl('IL11_Centering_screw_L',(-63,0,445),(-42,0,445),6,gray)
cyl('IL12_Centering_screw_R',(42,0,445),(63,0,445),6,gray)
# Dog-leg at the top extends forward over condenser optical axis.
prism('IL13_Top_forward_arm',[(py-22,546),(-8,567),(-29,587),(-29,620),(py+27,620),(py+27,560)],61,white,3)
box('IL14_Fiber_illumination_head',(0,3,HT-48),(132,117,96),white,4)
box('IL15_Filter_slider',(0,-44,HT-102),(95,35,13),white,2)
box('IL16_Filter_handle',(0,-66,HT-105),(16,15,15),dark,2)
cyl('IL17_Rear_fiber_socket',(0,61,HT-42),(0,79,HT-42),14,dark)
# Fiber route only short visible section, endpoints deliberately open.
def curve(name,pts,r,col):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3
    s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
    for bp,co in zip(s.bezier_points,pts):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);groups[COL].objects.link(o);attach(o,name,col,'EST visible fiber envelope; source equipment excluded');return o
curve('IL18_Fiber_visible_section_EST',[(0,79,HT-42),(25,132,HT-51),(56,177,510),(80,204,354)],5,gray)
COL='06_IX71_Controls'
for side in [-1,1]:
    x=side*68
    cyl('CT01_Focus_coarse_'+str(side),(x, -78,88),(side*92,-78,88),31,dark)
    cyl('CT02_Focus_fine_'+str(side),(side*92,-78,88),(side*107,-78,88),21,dark)
cyl('CT03_Front_lightpath_dial',(29,-190,155),(29,-201,155),17,dark)
box('CT04_Lightpath_lever',(36,-204,168),(8,7,28),dark,1).rotation_euler.y=math.radians(30)
cyl('CT05_Intensity_dial',(29,-196,67),(29,-204,67),14,gray)
cyl('CT06_Power_indicator',(-27,-192,48),(-27,-196,48),4,(.25,.46,.29,1))
box('CT07_Power_button',(-11,-195,48),(8,5,8),(.25,.46,.29,1),1)
# Reuse v03 geometry by append; old .blend never modified.
source=R.parent/'v03_blender_blockout_20260913'/'FV300_round1.blend'
with bpy.data.libraries.load(str(source),link=False) as (data_from,data_to):
    data_to.objects=[n for n in data_from.objects if n[:1] in ['B','C','R','E','W','P'] and not n.startswith(('CAM','REF','P01','B02','B03','B04','B05'))]
sx=P['scanhead_width_EST_mm']/10
cx,cy=P['scanhead_center_xy_EST_mm'];bottom=P['scanhead_base_z_EST_mm'];top=bottom+P['scanhead_height_EST_mm']
zoffset=top-1.455*sx
fvobjects=[]
for o in data_to.objects:
    if o is None:continue
    original_basis=o.matrix_basis.copy()
    groups['08_FV300_Reused_Interior'].objects.link(o)
    o.matrix_basis=Matrix.Translation((cx,cy,zoffset)) @ Matrix.Diagonal((sx,sx,sx,1)) @ original_basis
    o['import_expected_translation']=list(o.matrix_basis.translation)
    o.name='FV_'+o.name
    o['certainty']='v03 visible geometry retained; assembly scale and mounting elevation estimated'
    o['evidence']='v03 FV300_round1.blend; user four scanhead photos'
    parts.append(o);fvobjects.append(o)
# Whole FV300 group can be selected/transformed together.
empty=bpy.data.objects.new('FV300_ASSEMBLY_ROOT_EST',None);groups['09_FV300_Housing_EST'].objects.link(empty)
empty['width_EST_mm']=P['scanhead_width_EST_mm'];empty['height_EST_mm']=P['scanhead_height_EST_mm']
for o in fvobjects:
    m=o.matrix_basis.copy();o.parent=empty;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=m
COL='09_FV300_Housing_EST'
sw=P['scanhead_width_EST_mm'];sd=sw*.5;t=5
housing=[]
housing.append(box('FV_H01_Floor_EST',(cx,cy,bottom+3),(sw,sd,6),white,3))
housing.append(box('FV_H02_Left_wall_EST',(cx-sw/2+2.5,cy,(bottom+top)/2),(5,sd,top-bottom),white,2))
right=box('FV_H03_Right_wall_EST',(cx+sw/2-2.5,cy,(bottom+top)/2),(5,sd,top-bottom),white,2);housing.append(right)
housing.append(box('FV_H04_Rear_wall_EST',(cx,cy+sd/2-2.5,(bottom+top)/2),(sw-10,5,top-bottom),white,2))
housing.append(box('FV_H05_Front_wall_EST',(cx,cy-sd/2+2.5,(bottom+top)/2),(sw-10,5,top-bottom),white,2))
port_y=cy+(592.5-528)*(10/1470)*sx;port_z=zoffset+.69*sx
subtract(right,cyl('_port',(cx+sw/2-10,port_y,port_z),(cx+sw/2+10,port_y,port_z),24))
# Main partitions reach upper rim; hidden lower construction explicitly assumed.
for i,(u,v,w,h) in enumerate([(447,250,25,687),(1227,250,31,687),(472,553,755,27),(944,275,49,278)]):
    x=cx+((u+w/2)-945)*(10/1470)*sx;y=cy+(592.5-(v+h/2))*(10/1470)*sx
    housing.append(box('FV_H06_Partition_EST_'+str(i),(x,y,(bottom+top)/2),(w*sw/1470,h*sw/1470,top-bottom-3),gray,1))
for i,(x,y) in enumerate([(cx-sw/2+20,cy-sd/2+20),(cx+sw/2-20,cy-sd/2+20),(cx-sw/2+20,cy+sd/2-20),(cx+sw/2-20,cy+sd/2-20)]):
    housing.append(cyl('FV_H07_Foot_EST_'+str(i),(x,y,0),(x,y,bottom),12,dark))
for o in housing:
    m=o.matrix_world.copy();o.parent=empty;o.matrix_world=m
COL='10_FV300_Lid_EST'
lid=box('FV_LID_Removable_EST',(cx,cy,top+2),(sw,sd,4),white,3,'Photo/brochure visible cover; dimensions estimated.')
m=lid.matrix_world.copy();lid.parent=empty;lid.matrix_world=m
COL='07_Side_connection_EST'
# Joining tube axis is constrained by reused scanner port and IX71 side face.
x0=cx+sw/2
cyl('CN01_Scanner_collar_EST',(x0-1,port_y,port_z),(x0+14,port_y,port_z),29,dark,inner=23)
cyl('CN02_Side_coupling_tube_EST',(x0+12,port_y,port_z),(-70,port_y,port_z),23,dark,inner=18)
cyl('CN03_IX71_port_flange_EST',(-77,port_y,port_z),(-66,port_y,port_z),29,dark,inner=18)
# Visible second lower camera adapter in user front photo, different from scan connection.
cyl('CN04_Lower_camera_adapter_EST',(-69,-93,86),(-155,-93,86),28,gray)
cyl('CN05_Lower_camera_front_EST',(-155,-93,86),(-185,-93,86),24,dark)
# Nominal anchors stored explicitly for meaningful post-save checks.
sc['nominal_stage_z_mm']=ST;sc['nominal_base_length_mm']=L;sc['nominal_front_body_width_mm']=W
sc['connection_axis_y_EST_mm']=port_y;sc['connection_axis_z_EST_mm']=port_z
for o in parts:
    if o.type in ['MESH','CURVE']:
        # Flat diffuse colors for portability; no material polish.
        key='MAT_'+str(tuple(round(v,3) for v in o.color))
        mat=bpy.data.materials.get(key) or bpy.data.materials.new(key)
        mat.diffuse_color=o.color;o.data.materials.clear();o.data.materials.append(mat)
COL='90_References'
for fn in ['20260910_153139.jpg','20260910_153147.jpg','20260910_153221.jpg']:
    im=bpy.data.images.load(str(R.parent/fn));im.pack()
    o=bpy.data.objects.new('REF_'+fn,None);groups[COL].objects.link(o)
    o.empty_display_type='IMAGE';o.data=im;o.empty_display_size=400;o.hide_render=True;o.hide_viewport=True
# Two explicit layers, default closed; open layer omits only the removable lid.
sc.view_layers[0].name='01_Closed_assembly'
op=sc.view_layers.new('02_Open_scanhead')
op.layer_collection.children['10_FV300_Lid_EST'].exclude=True
op.use=False
sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=1600;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG'
sh=sc.display.shading;sh.light='STUDIO';sh.studio_light='paint.sl';sh.color_type='OBJECT'
sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_specular_highlight=False
sh.background_type='WORLD';sc.world.color=(.83,.84,.85)
sc.view_settings.view_transform='Standard'
def cam(name,loc,target,scale):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);groups['99_Cameras'].objects.link(o)
    o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;d.clip_end=10000;d.clip_start=1
    return o
hero=cam('CAM01_Assembly_front_left',(-1150,-1650,1000),(-205,15,325),1280)
cam('CAM02_Front',(-205,-1800,340),(-205,0,340),1040)
cam('CAM03_Right_side',(1700,0,340),(0,0,340),1070)
cam('CAM04_Top',(-205,0,2200),(-205,0,0),1000)
cam('CAM05_Rear_right',(950,1250,860),(-185,10,315),1100)
cam('CAM06_Photo153139_front_detail',(0,-1100,620),(0,-95,205),540)
cam('CAM07_Photo153147_side_detail',(1000,-400,230),(0,25,230),460)
cam('CAM08_Photo153221_illumination',(0,-150,530),(0,0,510),370)
cam('CAM09_IX71_side_nominal',(1700,0,333.5),(0,0,333.5),770)
sc.camera=hero
bpy.ops.object.select_all(action='DESELECT')
sc['review_stop']='Round 1 assembly blockout. Await proportions before detail work.'
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.shading.color_type='OBJECT';a.spaces.active.overlay.show_overlays=False
            rg=a.spaces.active.region_3d;rg.view_distance=1100;rg.view_location=Vector((-205,15,325));rg.view_rotation=hero.rotation_euler.to_quaternion();rg.view_perspective='ORTHO'
with (R/'parts.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['name','collection','evidence','certainty'])
    for o in parts:w.writerow([o.name,o.users_collection[0].name,o.get('evidence',''),o.get('certainty','')])
notes=bpy.data.texts.new('READ_ME_FIRST')
notes.write('FV300 + IX71FVSF-2 assembly blockout. Catalog dimensions are reference only.\nUse view layers 01_Closed_assembly / 02_Open_scanhead.\nparameters.json controls estimated scanner width/position and nominal IX71 anchors.\nScanner interior copied from v03; uniform scale preserves component shapes, hidden support not reconstructed.\nOnly one objective is instantiated from the visible photo; remaining sockets are placeholders.\nReference lamp shown as fiber-coupled head from actual photos, not the standard halogen housing.\n')
bpy.context.preferences.filepaths.save_version=0
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'FV300_IX71_round1.blend'))
(R/'assembly_manifest.json').write_text(json.dumps({'objects':len(parts),'reused_v03_objects':len(fvobjects),'parameters':P,'connection_axis':[port_y,port_z]},indent=2),encoding='utf-8')
print('ASSEMBLY SAVED',len(parts),'parts, reused',len(fvobjects),flush=True)

