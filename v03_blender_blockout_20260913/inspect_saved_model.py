import bpy,json,math
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'FV300_round1.blend'))
scene=bpy.context.scene
report={'reopened_blend':True,'blender':bpy.app.version_string,'meshes':0,'curves':0,'invalid_coordinates':[],'empty_meshes':[],'views':[],'physical_dimensions_verified':False}
for o in scene.objects:
    if o.type=='MESH':
        report['meshes']+=1
        if not o.data.vertices:report['empty_meshes'].append(o.name)
        if any(not all(math.isfinite(c) for c in v.co) for v in o.data.vertices):report['invalid_coordinates'].append(o.name)
    if o.type=='CURVE':report['curves']+=1
scene.render.resolution_x=1600;scene.render.resolution_y=900
cam=bpy.data.objects['CAM_01_Overhead_reference_approx']
cam.location=(.53,-.23,19)
cam.rotation_euler=(Vector((.53,.10,.65))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=13.9
# Persist the matched camera setup to the new file only.
scene.camera=cam
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'FV300_round1.blend'))
for n,fn in [('CAM_01_Overhead_reference_approx','01_overhead'),('CAM_02_Oblique_153030_approx','02_oblique'),('CAM_03_Front_EST','03_front_EST'),('CAM_04_Right_EST','04_right_EST'),('CAM_05_Underside_EST','05_underside_EST')]:
    scene.camera=bpy.data.objects[n];scene.render.filepath=str(ROOT/(fn+'.png'))
    bpy.ops.render.render(write_still=True)
    report['views'].append(fn+'.png')
    print('RENDERED',fn,flush=True)
def pair(photo,render,out):
    a=bpy.data.images.load(str(ROOT.parent/photo),check_existing=False);a.scale(1600,900)
    b=bpy.data.images.load(str(ROOT/render),check_existing=False)
    ar=np.empty(1600*900*4,dtype=np.float32);br=ar.copy()
    a.pixels.foreach_get(ar);b.pixels.foreach_get(br)
    combo=np.concatenate([ar.reshape(900,1600,4),br.reshape(900,1600,4)],axis=1)
    im=bpy.data.images.new(out,3200,900,alpha=True);im.pixels.foreach_set(combo.ravel())
    im.filepath_raw=str(ROOT/out);im.file_format='PNG';im.save()
pair('20260910_171623.jpg','01_overhead.png','comparison_top_photo_LEFT_model_RIGHT.png')
pair('20260910_153030.jpg','02_oblique.png','comparison_oblique_photo_LEFT_model_RIGHT.png')
(ROOT/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)

