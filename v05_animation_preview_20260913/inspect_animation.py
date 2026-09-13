import bpy
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'FV300_IX71_animation.blend'))
s=bpy.context.scene
(R/'checks').mkdir(exist_ok=True)
s.render.resolution_percentage=50
s.render.image_settings.file_format='PNG'
for f in [1,120,216,312,370,432,480,550,672]:
 s.frame_set(f);s.render.filepath=str(R/'checks'/f'frame_{f:04}.png');bpy.ops.render.render(write_still=True)
