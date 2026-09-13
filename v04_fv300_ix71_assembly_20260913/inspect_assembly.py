import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'FV300_IX71_round1.blend'))
sc=bpy.context.scene
checks={'reopened_saved_blend':True,'blender_version':bpy.app.version_string,'invalid_meshes':[],'views':[]}
for o in sc.objects:
    if o.type=='MESH' and (not o.data.vertices or any(not all(math.isfinite(v) for v in pt.co) for pt in o.data.vertices)):
        checks['invalid_meshes'].append(o.name)
bpy.context.view_layer.update()
def zmax(name):
    o=sc.objects[name]
    return max((o.matrix_world @ vert.co).z for vert in o.data.vertices)
checks['stage_top_mm']=zmax('ST01_Manual_stage_main')
checks['active_objective_tip_mm']=zmax('NP06_Active_objective_tip')
checks['objective_to_stage_clearance_mm']=checks['stage_top_mm']-checks['active_objective_tip_mm']
checks['import_translation_errors']=[]
for o in sc.objects:
    if 'import_expected_translation' in o:
        err=(o.matrix_world.translation-Vector(o['import_expected_translation'])).length
        if err>0.001:checks['import_translation_errors'].append([o.name,err])
checks['connector_axis_offset_mm']=abs(sc.objects['CN02_Side_coupling_tube_EST'].location.z-sc.objects['CN03_IX71_port_flange_EST'].location.z)
assert not checks['import_translation_errors'],checks['import_translation_errors']
assert checks['objective_to_stage_clearance_mm']>0
checks['stage_hole_radius_mm']=55
checks['optical_axis_xy_mm']=[0,0]
checks['scanner_dimensions_measured']=False
checks['physical_assembly_verified']=False
cl=sc.view_layers['01_Closed_assembly']
for cam,fn,open_lid,body_only in [
('CAM01_Assembly_front_left','01_assembly_closed',False,False),
('CAM01_Assembly_front_left','02_assembly_open',True,False),
('CAM02_Front','03_front',False,False),
('CAM03_Right_side','04_right_side',False,False),
('CAM04_Top','05_top_open',True,False),
('CAM05_Rear_right','06_rear',False,False),
('CAM06_Photo153139_front_detail','07_photo153139_front_detail',False,False),
('CAM07_Photo153147_side_detail','08_photo153147_side_detail',False,False),
('CAM08_Photo153221_illumination','09_photo153221_illumination',False,False),
('CAM09_IX71_side_nominal','10_ix71_nominal_side',False,True)]:
    sc.camera=bpy.data.objects[cam]
    cl.layer_collection.children['10_FV300_Lid_EST'].exclude=open_lid or body_only
    for cn in ['08_FV300_Reused_Interior','09_FV300_Housing_EST','07_Side_connection_EST']:
        cl.layer_collection.children[cn].exclude=body_only
    sc.render.filepath=str(R/(fn+'.png'))
    if cam=='CAM09_IX71_side_nominal':
        sc.render.resolution_x=900;sc.render.resolution_y=1000;sc.camera.data.ortho_scale=700
    elif cam in ['CAM06_Photo153139_front_detail','CAM07_Photo153147_side_detail','CAM08_Photo153221_illumination']:
        sc.render.resolution_x=900;sc.render.resolution_y=1400
    else:sc.render.resolution_x=1600;sc.render.resolution_y=1100
    bpy.ops.render.render(write_still=True)
    checks['views'].append(fn+'.png')
    print('RENDERED',fn,flush=True)
(R/'inspection.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks),flush=True)

