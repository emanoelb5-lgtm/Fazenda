import math
from pathlib import Path
import bpy
from mathutils import Vector


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def configure_render(scene, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 32
    # Algumas distribuições livres não incluem OpenImageDenoise.
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 960
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(output)
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    world = bpy.data.worlds.new('Céu claro')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.75, 0.82, 0.72, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.5
    scene.world = world
    bpy.ops.object.light_add(type='AREA', location=(-18, -10, 32))
    light = bpy.context.object
    light.name = 'Luz do dia'
    light.data.energy = 11500
    light.data.shape = 'DISK'
    light.data.size = 12
    point_at(light, (0, 0, 0))
    bpy.ops.object.camera_add(location=(48, -57, 43))
    camera = bpy.context.object
    camera.name = 'Câmera | prova técnica'
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 68
    point_at(camera, (0, 0, 1))
    scene.camera = camera
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, -1.45))
    backdrop = bpy.context.object
    backdrop.name = 'Fundo de estúdio | apenas render'
    mat = bpy.data.materials.new('Fundo areia')
    mat.diffuse_color = (0.68, 0.72, 0.61, 1)
    backdrop.data.materials.append(mat)
