# Padrão de ativos

## Coordenadas e identidade

- Um metro equivale a uma unidade.
- JSON/Three.js: X lateral, Y vertical, Z profundidade. Blender: X lateral, Y profundidade invertida, Z vertical.
- Converter posição JSON para Blender: `(x, y, z) → (x, -z, y)`. O exportador glTF reverte essa mudança ao exportar Y-up.
- Rotação vertical JSON em radianos corresponde à rotação Z do Blender. A Fase 0 aceita apenas essa rotação; o gerador recusa inclinações em outros eixos.
- Escala JSON `(sx, sy, sz)` precisa ser convertida para Blender `(sx, sz, sy)` quando não uniforme.
- `asset_id` identifica o modelo reutilizável; `instance_id` identifica sua colocação na cena.
- Ao posicionar com `snap_to_ground`, a altura do terreno é somada à altura relativa do JSON.

## Ativos originais

| ID | Fonte | Exportação | Origem e direitos |
| --- | --- | --- | --- |
| `arvore-nativa-v1` | `blender/assets/vegetacao/arvore-nativa-v1.blend` | `public/models/arvore-nativa-v1.glb` | Geometria e materiais originais produzidos por script para Emanuel Bonfim / B5 Soluções; sem ativo de terceiros |
| `terreno-prova-v1` | `blender/base/fazenda_base.blend` + script | Cena `public/models/fazenda-fase0.glb` | Malha, perfil do solo e capim originais produzidos por script para o projeto |

A árvore é uma representação estilizada genérica. Não identifica uma espécie botânica. A cena completa mantém a árvore separada do terreno e preserva tronco, galhos, raízes e copas como objetos.

Não foi concedida uma licença pública automática para os modelos originais. Preserve a titularidade do projeto ao reutilizá-los.

## Dependências

- Three.js, versão declarada em `package.json`: MIT, aviso incluído em `public/THREE-LICENSE.txt` e no site.
- Vite e Playwright: dependências de desenvolvimento com suas respectivas licenças nos pacotes instalados.
- Fontes opcionais DM Sans e Manrope via Google Fonts (SIL Open Font License); sem disponibilidade, usar Arial local. Nenhuma imagem ou modelo externo é necessário para a cena.

## Reproduzir

O gerador usa semente 42, modelo JSON e fontes Python versionados. Câmera/luzes/fundo do render não são exportados para o GLB. A imagem é PNG, 1280 × 960, renderizada em CPU com 32 amostras. O GLB não exige Draco.
