import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'FV300_IX71_round1.blend'))
sc=bpy.context.scene
d=bpy.data.cameras.new('CAM10_Catalog_approx')
o=bpy.data.objects.new('CAM10_Catalog_approx',d)
bpy.data.collections['99_Cameras'].objects.link(o)
o.location=(520,-1900,740)
o.rotation_euler=(Vector((-205,15,330))-o.location).to_track_quat('-Z','Y').to_euler()
d.type='ORTHO';d.ortho_scale=1190;d.clip_end=10000
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'FV300_IX71_round1.blend'))
bpy.ops.wm.open_mainfile(filepath=str(R/'FV300_IX71_round1.blend'))
sc=bpy.context.scene;sc.camera=bpy.data.objects['CAM10_Catalog_approx']
sc.render.resolution_x=1600;sc.render.resolution_y=1100
sc.render.filepath=str(R/'11_catalog_approx.png')
bpy.ops.render.render(write_still=True)

