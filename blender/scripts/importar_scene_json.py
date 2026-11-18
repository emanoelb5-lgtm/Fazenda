"""Contrato comum da cena; JSON (x,y,z) -> Blender (x,-z,y)."""
import json
import math


def blender_position(position):
    x, y, z = position
    return (x, -z, y)


def ground_height(x, z, terrain):
    amplitude = terrain['height_amplitude']
    return amplitude * (0.44 + 0.32 * math.sin(x * 0.13) * math.cos(z * 0.11)
                        + 0.22 * math.cos((x + z) * 0.18))


def load_scene(path):
    data = json.loads(path.read_text())
    if data['schema_version'] != '1.0.0' or data['units'] != 'meters':
        raise ValueError('Cena ou unidade incompatível')
    if data['coordinate_system'] != 'right-handed-y-up':
        raise ValueError('Eixos incompatíveis')
    if len(data['instances']) != 1 or data['instances'][0]['asset_id'] != 'arvore-nativa-v1':
        raise ValueError('Gerador da Fase 0 aceita exatamente uma árvore de referência')
    instance = data['instances'][0]
    if instance['rotation'][0] != 0 or instance['rotation'][2] != 0:
        raise ValueError('Fase 0 suporta rotação apenas no eixo vertical')
    if any(v <= 0 for v in instance['scale']):
        raise ValueError('Escalas devem ser positivas')
    return data
