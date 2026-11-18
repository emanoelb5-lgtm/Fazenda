# Fazenda · Estúdio 3D

Base permanente para uma fazenda 3D explorável pelo celular, criada com **Blender, Three.js e GitHub**.

**Versão 0.1.0 · Fase 0:** terreno de referência de 40 × 40 metros e uma árvore original. Esta prova antecede a fazenda de 200 × 200 m, a edição de objetos e os personagens.

## Usar

No visualizador, arraste para girar. Use dois dedos para mover e aproximar. Também há botões de zoom, vista superior, enquadramento inicial e tela cheia.

Os arquivos GLB, PNG e JSON podem ser baixados pela própria página. Se o navegador bloquear WebGL, a página usa uma visualização vetorial simplificada, sem sombras nem detalhes de capim.

## Executar localmente

Node.js 22 ou superior e npm:

```bash
npm ci
node scripts/prepare-web.mjs
npm run dev
```

Para gerar novamente os modelos e uma imagem (Blender 4.0 ou superior):

```bash
blender --background --threads 4 --python blender/scripts/gerar_cenario.py
npm run check:assets
npm test
npm run build
```

As versões JavaScript são fixadas no `package-lock.json`. O Blender usado em cada geração fica em `public/data/build-info.json`. Render CPU, 32 amostras, sem exigir GPU, denoiser, extensão ou conta adicional.

## Automação

- **Validar projeto:** valida dados, modelos, build e visualizador WebGL em desktop e tela móvel emulada.
- **Blender · prova técnica:** gera `.blend`, `.glb` e uma imagem PNG no Actions. Executa quando os scripts/cena mudam ou por **Run workflow**. Os arquivos ficam no Artifact `fazenda-fase0-blender-glb-imagem` por 30 dias.
- **Publicar visualizador:** compila e publica no GitHub Pages. A configuração inicial do Pages precisa permitir a publicação por GitHub Actions; ver `docs/STATUS.md` para o estado efetivamente verificado.

Os arquivos de referência ficam versionados; expirar um Artifact não apaga as fontes do repositório. Renderizações maiores e vídeos ainda não foram implementados.

## Estrutura

| Caminho | Função |
| --- | --- |
| `data/fazenda.scene.json` | Disposição e unidades oficiais da cena |
| `blender/scripts/` | Geração, conversão de coordenadas, exportação e render |
| `blender/base/fazenda_base.blend` | Cena mestre editável no Blender |
| `blender/assets/vegetacao/` | Fonte independente da árvore |
| `public/models/` | GLBs derivados para o navegador |
| `public/renders/` | Imagem realmente renderizada no Blender |
| `web/` | Visualizador por toque |
| `docs/PLANO_MESTRE.md` | Planejamento original e fases |
| `docs/STATUS.md` | Entregas, testes e pendências verificadas |

`public/data/fazenda.scene.json` é uma cópia gerada durante o build; altere sempre o arquivo em `data/`.

Fontes e titularidade dos ativos: `docs/PADRAO_ASSETS.md`. Não há autenticação, gravação no GitHub pelo navegador ou cobrança integrada.
