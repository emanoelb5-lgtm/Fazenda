import { copyFileSync, mkdirSync } from 'node:fs';
mkdirSync('public/data', { recursive: true });
copyFileSync('data/fazenda.scene.json', 'public/data/fazenda.scene.json');
copyFileSync('node_modules/three/LICENSE', 'public/THREE-LICENSE.txt');
