import bpy, math, json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
SOURCE=R.parent/'v04_fv300_ix71_assembly_20260913'/'FV300_IX71_round1.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
sc=bpy.context.scene
sc.frame_start=1;sc.frame_end=672;sc.render.fps=24
sc.render.resolution_x=1920;sc.render.resolution_y=1080;sc.render.resolution_percentage=100
sc.render.engine='BLENDER_WORKBENCH'
sc.render.film_transparent=False
sc.display.shading.show_shadows=False
sc.view_layers['01_Closed_assembly'].use=True
sc.view_layers['01_Closed_assembly'].layer_collection.children['10_FV300_Lid_EST'].exclude=False
sc.view_layers['02_Open_scanhead'].use=False
sc.world.color=(.88,.89,.90)
# The animation is a demonstration of cover separation, not a verified opening mechanism.
sc['animation_scope']='28s camera / removable cover study. No geometry detail edits.'
sc['cover_motion_status']='Illustrative lift and lateral separation; real removal mechanism not verified.'
anim=bpy.data.collections.new('ANIMATION_Camera_and_titles');sc.collection.children.link(anim)
data=bpy.data.cameras.new('ANIM_Camera')
cam=bpy.data.objects.new('ANIM_Camera',data);anim.objects.link(cam)
data.type='ORTHO';data.clip_start=1;data.clip_end=10000
aim=bpy.data.objects.new('ANIM_Look_at',None);anim.objects.link(aim)
con=cam.constraints.new('TRACK_TO');con.target=aim;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
sc.camera=cam
lid=bpy.data.objects['FV_LID_Removable_EST'];lid.animation_data_clear()
home=lid.location.copy()
font=bpy.data.fonts.load('C:/Windows/Fonts/msjh.ttc')
font.pack()
def text_obj(name,body,color):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.align_y='TOP';cu.size=1
    ob=bpy.data.objects.new(name,cu);anim.objects.link(ob);ob.parent=cam;ob.color=(*color,1)
    return ob
title=text_obj('TITLE_FV300_IX71','FV300 ＋ IX71',(.10,.14,.18))
subtitle=text_obj('TITLE_Blockout','粗模動畫預覽',(.23,.28,.32))
note=text_obj('TITLE_Estimated','尺寸含推估｜上蓋分離為展示示意',(.26,.30,.33))
# Step labels fade via scale over phase boundaries. Chinese characters remain packed and editable.
labels=[]
for body,a,b in [('整機環繞',1,216),('聚焦掃描頭',217,312),('上蓋分離示意',313,432),('可見內構',433,504),('回到整機',505,672)]:
    ob=text_obj('PHASE_'+str(a),body,(.15,.23,.27));labels.append((ob,a,b))
def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def mix(a,b,t):return Vector(a).lerp(Vector(b),t)
target0=Vector((-205,0,320))
radius=2100
angle0=math.radians(-67)
def orbit(angle):
    return target0+Vector((radius*math.cos(angle),radius*math.sin(angle),670))
hero=orbit(angle0)
focus_target=Vector((-410,-21,174))
focus_cam=focus_target+Vector((0,-520,1060))
open_target=Vector((-660,-21,220))
open_cam=open_target+Vector((0,-520,1060))
# All frames have explicit editable keys; linear interpolation avoids overshoot or camera flipping.
# 0-1 hold, 1-9 360 orbit, 9-13 focus, 13-18 open, 18-21 hold, 21-24 close, 24-27 return, 27-28 hold.
for f in range(1,673):
    t=(f-1)/24
    if t<1:
        pos=hero;look=target0;scale=1700;shift=Vector((0,0,0))
    elif t<9:
        u=ease((t-1)/8)
        pos=orbit(angle0+2*math.pi*u);look=target0;scale=1700;shift=Vector((0,0,0))
    elif t<13:
        u=ease((t-9)/4)
        pos=mix(hero,focus_cam,u);look=mix(target0,focus_target,u);scale=1700+(840-1700)*u;shift=Vector((0,0,0))
    elif t<18:
        u=ease((t-13)/5)
        pos=mix(focus_cam,open_cam,u);look=mix(focus_target,open_target,u);scale=840+(1320-840)*u
        # Lift before lateral travel, so the lid clears the protruding adjuster.
        lift=130*ease((t-13)/1.4)
        slide=-540*ease((t-14.4)/3.6)
        shift=Vector((slide,0,lift))
    elif t<21:
        pos=open_cam;look=open_target;scale=1320;shift=Vector((-540,0,130))
    elif t<24:
        u=ease((t-21)/3)
        pos=mix(open_cam,focus_cam,u);look=mix(open_target,focus_target,u);scale=1320+(840-1320)*u
        slide=-540*(1-ease((t-21)/1.8))
        lift=130*(1-ease((t-22.8)/1.2))
        shift=Vector((slide,0,lift))
    elif t<27:
        u=ease((t-24)/3)
        pos=mix(focus_cam,hero,u);look=mix(focus_target,target0,u);scale=840+(1700-840)*u;shift=Vector((0,0,0))
    else:
        pos=hero;look=target0;scale=1700;shift=Vector((0,0,0))
    cam.location=pos;cam.keyframe_insert('location',frame=f)
    aim.location=look;aim.keyframe_insert('location',frame=f)
    data.ortho_scale=scale;data.keyframe_insert('ortho_scale',frame=f)
    lid.location=home+shift;lid.keyframe_insert('location',frame=f)
    # Orthographic screen coordinates; overlay stays constant in pixel size while camera zooms.
    for ob,xy,sz in [(title,(-.462,.247),.024),(subtitle,(-.462,.220),.014),(note,(-.462,-.247),.013)]:
        ob.location=(xy[0]*scale,xy[1]*scale,-50)
        ob.scale=(sz*scale,)*3
        ob.keyframe_insert('location',frame=f);ob.keyframe_insert('scale',frame=f)
    for ob,a,b in labels:
        visible=a<=f<=b
        ob.location=(.30*scale,.244*scale,-50)
        ob.scale=((.016*scale if visible else .00001),)*3
        ob.keyframe_insert('location',frame=f);ob.keyframe_insert('scale',frame=f)
# Blender 4.5 uses layered action slots. Visit channels via datablock action slots.
for owner in [cam,aim,data,lid,title,subtitle,note]+[o for o,_,_ in labels]:
    if owner.animation_data and owner.animation_data.action:
        ac=owner.animation_data.action
        for layer in ac.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='LINEAR'
sc.frame_set(1)
sc.render.image_settings.file_format='FFMPEG'
sc.render.ffmpeg.format='MPEG4';sc.render.ffmpeg.codec='H264'
sc.render.ffmpeg.constant_rate_factor='MEDIUM';sc.render.ffmpeg.ffmpeg_preset='GOOD'
sc.render.ffmpeg.audio_codec='NONE'
sc.render.filepath=str(R/'FV300_IX71_preview.mp4')
sc.render.use_file_extension=True
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.overlay.show_overlays=False
            area.spaces.active.shading.color_type='OBJECT'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'FV300_IX71_animation.blend'))
story=[{'time':'00:00–00:09','action':'整機停留與360度環繞'},
       {'time':'00:09–00:13','action':'聚焦掃描頭'},
       {'time':'00:13–00:18','action':'上蓋先抬升，再側移（展示示意）'},
       {'time':'00:18–00:21','action':'內構停留'},
       {'time':'00:21–00:24','action':'上蓋復位'},
       {'time':'00:24–00:28','action':'回到整機並停留'}]
(R/'storyboard.json').write_text(json.dumps({'fps':24,'frames':672,'duration_seconds':28,'resolution':[1920,1080],'audio':False,'shots':story},ensure_ascii=False,indent=2),encoding='utf-8')
print('SAVED ANIMATION',flush=True)
