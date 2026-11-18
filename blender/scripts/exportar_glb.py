from pathlib import Path
import bpy


def export_glb(path, objects):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=str(path), export_format='GLB',
                              use_selection=True, export_yup=True, export_extras=True,
                              export_cameras=False, export_lights=False,
                              export_animations=False)
    bpy.ops.object.select_all(action='DESELECT')
