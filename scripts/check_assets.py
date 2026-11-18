"""Valida o contêiner GLB e a identidade dos objetos realmente exportados."""
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def read_glb(path):
    data = path.read_bytes()
    magic, version, length = struct.unpack_from('<4sII', data)
    assert magic == b'glTF' and version == 2 and length == len(data), path
    chunk_length, chunk_type = struct.unpack_from('<II', data, 12)
    assert chunk_type == 0x4E4F534A
    return json.loads(data[20:20 + chunk_length])


def main():
    scene = read_glb(ROOT / 'public/models/fazenda-fase0.glb')
    nodes = scene['nodes']
    for identity in ['terreno-001', 'arvore-001']:
        assert any(node.get('extras', {}).get('instance_id') == identity for node in nodes), identity
    assert not any('camera' in node for node in nodes)
    tree = read_glb(ROOT / 'public/models/arvore-nativa-v1.glb')
    assert any(node.get('extras', {}).get('asset_id') == 'arvore-nativa-v1' for node in tree['nodes'])
    assert (ROOT / 'blender/base/fazenda_base.blend').stat().st_size > 10000
    assert (ROOT / 'blender/assets/vegetacao/arvore-nativa-v1.blend').stat().st_size > 10000
    image = (ROOT / 'public/renders/fase0.png').read_bytes()
    assert image[:8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack_from('>II', image, 16) == (1280, 960)
    print(f'GLB válido: {len(nodes)} objetos; PNG 1280 × 960; fontes Blender preservadas.')


if __name__ == '__main__':
    main()
