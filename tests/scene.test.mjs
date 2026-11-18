import { readFileSync } from 'node:fs';
import test from 'node:test';
import assert from 'node:assert/strict';
import { validateScene, toBlenderPosition, fromBlenderPosition } from '../web/src/scene-data.js';

const scene = JSON.parse(readFileSync(new URL('../data/fazenda.scene.json', import.meta.url)));
test('a cena mínima mantém os identificadores e uma árvore', () => {
  assert.equal(validateScene(scene).instances.length, 1);
  assert.equal(scene.phase, 0);
});
test('conversão de eixos preserva coordenadas e alturas', () => {
  const point = [12, 3, -8];
  assert.deepEqual(toBlenderPosition(point), [12, 8, 3]);
  assert.deepEqual(fromBlenderPosition(toBlenderPosition(point)), point);
});
test('recusa duas instâncias com o mesmo ID', () => {
  const invalid = structuredClone(scene);
  invalid.instances.push(structuredClone(invalid.instances[0]));
  assert.throws(() => validateScene(invalid), /repetido/);
});
test('recusa transformações inválidas e ativos desconhecidos', () => {
  for (const change of [s => s.instances[0].scale[0] = 0, s => s.instances[0].position[1] = NaN, s => s.instances[0].asset_id = 'inexistente']) {
    const invalid = structuredClone(scene);
    change(invalid);
    assert.throws(() => validateScene(invalid));
  }
});
