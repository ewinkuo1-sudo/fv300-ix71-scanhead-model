import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
movies=list(R.glob('*.mp4'))
assert len(movies)==1,movies
p=movies[0]
if p.name!='FV300_IX71_preview.mp4':p.rename(R/'FV300_IX71_preview.mp4')
p=R/'FV300_IX71_preview.mp4'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='Standard'
ed=s.sequence_editor_create()
strip=ed.strips.new_movie('Encoded_MP4_check',str(p),channel=1,frame_start=1)
report={'file':p.name,'frames':strip.frame_final_duration,'width':strip.elements[0].orig_width,'height':strip.elements[0].orig_height,'bytes':p.stat().st_size}
assert report['frames']==672,report
assert (report['width'],report['height'])==(1920,1080),report
for f in [1,120,312,432,480,672]:
 s.frame_set(f);s.render.filepath=str(R/'checks'/f'video_{f:04}.png');bpy.ops.render.render(write_still=True)
(R/'video_inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
