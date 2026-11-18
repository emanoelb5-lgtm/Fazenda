"""Cena original e determinística. Blender >= 4.0; nenhuma extensão externa."""
import argparse
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from importar_scene_json import blender_position, ground_height, load_scene
from exportar_glb import export_glb
from renderizar import configure_render


def material(name, color, roughness=0.9):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    return mat


def move_to(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def mesh_object(name, vertices, faces, collection, mats):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    for mat in mats:
        mesh.materials.append(mat)
    return obj


def branch(name, start, end, r1, r2, collection, mat):
    start, end = Vector(start), Vector(end)
    vector = end - start
    bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=r1, radius2=r2, depth=vector.length,
                                    location=(start + end) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = vector.to_track_quat('Z', 'Y').to_euler()
    obj.data.materials.append(mat)
    move_to(obj, collection)
    return obj


def create_tree(collection, rng):
    bark = material('Casca | castanho', (0.17, 0.075, 0.032))
    leaves = [material(f'Folhagem | {i}', c) for i, c in enumerate([
        (0.10, 0.25, 0.047), (0.19, 0.36, 0.065), (0.29, 0.46, 0.09),
        (0.24, 0.39, 0.06), (0.38, 0.53, 0.13)])]
    root = bpy.data.objects.new('arvore-nativa-v1', None)
    root['asset_id'] = 'arvore-nativa-v1'
    collection.objects.link(root)
    parts = [branch('Tronco', (0, 0, 0), (0.13, 0, 5.6), 0.46, 0.19, collection, bark)]
    for i in range(5):
        angle = i * math.tau / 5 + 0.25
        end = (math.cos(angle) * 2.2, math.sin(angle) * 2.1, 6.1 + (i % 2) * 0.7)
        parts.append(branch(f'Galho-{i:02}', (0.10, 0, 3.0 + (i % 3) * 0.6), end,
                            0.21, 0.065, collection, bark))
    crowns = [(0, 0, 7.0, 2.65, 2.45, 2.2), (-2.3, 0.2, 5.9, 2.35, 2.1, 1.7),
              (1.9, 0.4, 6.2, 2.4, 2.1, 1.9), (0.5, -2.0, 6.2, 2.4, 1.9, 1.7),
              (-0.6, 1.9, 6.5, 2.3, 1.9, 1.8), (0.4, 0.3, 8.3, 1.8, 1.6, 1.5)]
    for i, (x, y, z, sx, sy, sz) in enumerate(crowns):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(x, y, z))
        obj = bpy.context.object
        obj.name = f'Copa-{i:02}'
        for v in obj.data.vertices:
            v.co *= rng.uniform(0.87, 1.12)
        obj.scale = (sx, sy, sz)
        for mat in leaves:
            obj.data.materials.append(mat)
        for polygon in obj.data.polygons:
            polygon.material_index = rng.choices(range(5), weights=[1, 3, 3, 3, 1])[0]
        move_to(obj, collection)
        parts.append(obj)
    for obj in parts:
        obj.parent = root
    # Roots stay distinct and are reusable with the tree.
    for i in range(5):
        a = i * math.tau / 5
        obj = branch(f'Raiz-{i:02}', (0, 0, 0.23), (math.cos(a) * 1.2, math.sin(a) * 1.2, 0.04),
                     0.22, 0.025, collection, bark)
        obj.parent = root
    return root


def create_terrain(data, collection, rng):
    terrain = data['terrain']
    n = terrain['resolution']
    width, depth = terrain['size']
    mats = [material(f'Capim | {i}', color) for i, color in enumerate([
        (0.28, 0.37, 0.12), (0.31, 0.40, 0.14), (0.33, 0.42, 0.15), (0.30, 0.39, 0.13)])]
    verts = []
    for j in range(n + 1):
        for i in range(n + 1):
            x, y = (i / n - 0.5) * width, (j / n - 0.5) * depth
            verts.append((x, y, ground_height(x, -y, terrain)))
    faces = []
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.extend([(a, a + 1, a + n + 2), (a, a + n + 2, a + n + 1)])
    top = mesh_object(terrain['instance_id'], verts, faces, collection, mats)
    top['instance_id'] = terrain['instance_id']
    top['asset_id'] = terrain['asset_id']
    for face in top.data.polygons:
        face.material_index = rng.randrange(len(mats))
    soil_mats = [material('Solo superficial', (0.28, 0.16, 0.07)),
                 material('Subsolo', (0.39, 0.23, 0.11)), material('Solo profundo', (0.29, 0.17, 0.09))]
    perimeter = list(range(n + 1)) + [j * (n + 1) + n for j in range(1, n + 1)]
    perimeter += [n * (n + 1) + i for i in range(n - 1, -1, -1)]
    perimeter += [j * (n + 1) for j in range(n - 1, 0, -1)]
    side_verts, side_faces = [], []
    for index in perimeter:
        x, y, z = verts[index]
        side_verts.extend([(x, y, z), (x, y, -0.28), (x, y, -0.85), (x, y, -terrain['base_depth'])])
    for k in range(len(perimeter)):
        for layer in range(3):
            a, b = k * 4 + layer, ((k + 1) % len(perimeter)) * 4 + layer
            side_faces.append((a, a + 1, b + 1, b))
    side_faces.append(tuple(k * 4 + 3 for k in reversed(range(len(perimeter)))))
    sides = mesh_object('Perfil do solo', side_verts, side_faces, collection, soil_mats)
    for i, face in enumerate(sides.data.polygons):
        face.material_index = min(i % 3, 2)
    # One combined tuft mesh, rather than hundreds of draw calls.
    grass_verts, grass_faces = [], []
    for _ in range(650):
        x, y = rng.uniform(-19, 19), rng.uniform(-19, 19)
        if x*x + y*y < 2.2:
            continue
        z = ground_height(x, -y, terrain)
        for angle in [rng.random() * math.tau, rng.random() * math.tau]:
            width, height = rng.uniform(0.06, 0.12), rng.uniform(0.16, 0.4)
            dx, dy = math.cos(angle) * width, math.sin(angle) * width
            a = len(grass_verts)
            grass_verts.extend([(x - dx, y - dy, z), (x + dx, y + dy, z), (x + dx*0.8, y + dy*0.8, z + height)])
            grass_faces.append((a, a + 1, a + 2))
    grass = mesh_object('Cobertura vegetal', grass_verts, grass_faces, collection, mats)
    for face in grass.data.polygons:
        face.material_index = rng.randrange(len(mats))
    return top


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scene', type=Path, default=ROOT / 'data/fazenda.scene.json')
    parser.add_argument('--no-render', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    data = load_scene(args.scene)
    rng = random.Random(data['seed'])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = 'Fazenda | Fase 0'
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1
    tree_collection = bpy.data.collections.new('Ativo | arvore-nativa-v1')
    terrain_collection = bpy.data.collections.new('Terreno | prova-v1')
    scene.collection.children.link(tree_collection)
    scene.collection.children.link(terrain_collection)
    tree = create_tree(tree_collection, rng)
    source_path = ROOT / 'blender/assets/vegetacao/arvore-nativa-v1.blend'
    source_path.parent.mkdir(parents=True, exist_ok=True)
    asset_scene = bpy.data.scenes.new('Árvore original | metros')
    asset_scene.collection.children.link(tree_collection)
    bpy.data.libraries.write(str(source_path), {asset_scene}, fake_user=True, compress=True)
    bpy.data.scenes.remove(asset_scene)
    export_glb(ROOT / 'public/models/arvore-nativa-v1.glb', list(tree_collection.all_objects))
    instance = data['instances'][0]
    tree.name = instance['instance_id']
    tree['instance_id'] = instance['instance_id']
    position = list(instance['position'])
    if instance['snap_to_ground']:
        position[1] += ground_height(position[0], position[2], data['terrain'])
    tree.location = blender_position(position)
    tree.rotation_euler.z = instance['rotation'][1]
    sx, sy, sz = instance['scale']
    tree.scale = (sx, sz, sy)
    create_terrain(data, terrain_collection, rng)
    export_glb(ROOT / 'public/models/fazenda-fase0.glb',
               list(tree_collection.all_objects) + list(terrain_collection.all_objects))
    configure_render(scene, ROOT / 'public/renders/fase0.png')
    base_path = ROOT / 'blender/base/fazenda_base.blend'
    base_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(base_path), compress=True)
    if not args.no_render:
        bpy.ops.render.render(write_still=True)
    manifest = {
        'phase': 0, 'scene_id': data['scene_id'], 'blender_version': bpy.app.version_string,
        'seed': data['seed'], 'units': 'meters', 'tree_instances': len(data['instances']),
        'mesh_objects': len([o for o in scene.objects if o.type == 'MESH' and not o.hide_render]),
        'polygons': sum(len(o.data.polygons) for o in scene.objects if o.type == 'MESH'),
        'render_generated': not args.no_render,
    }
    path = ROOT / 'public/data/build-info.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    print('FAZENDA_BUILD=' + json.dumps(manifest))


if __name__ == '__main__':
    main()
