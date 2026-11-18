export function validateScene(scene) {
  if (scene?.schema_version !== '1.0.0' || scene.units !== 'meters' || scene.coordinate_system !== 'right-handed-y-up') {
    throw new Error('Formato de cena não compatível.');
  }
  const ids = new Set();
  const assets = new Set(scene.assets.map(asset => asset.asset_id));
  for (const instance of scene.instances) {
    if (!instance.instance_id || ids.has(instance.instance_id)) throw new Error('Identificador de objeto repetido.');
    ids.add(instance.instance_id);
    if (!assets.has(instance.asset_id)) throw new Error('Ativo não cadastrado.');
    for (const key of ['position', 'rotation', 'scale']) {
      if (!Array.isArray(instance[key]) || instance[key].length !== 3 || !instance[key].every(Number.isFinite)) {
        throw new Error(`Transformação inválida: ${key}.`);
      }
    }
    if (instance.scale.some(value => value <= 0)) throw new Error('Escala deve ser positiva.');
  }
  return scene;
}

export function toBlenderPosition([x, y, z]) { return [x, -z, y]; }
export function fromBlenderPosition([x, y, z]) { return [x, z, -y]; }
