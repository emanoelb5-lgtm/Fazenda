# Estado do projeto

**Versão:** 0.1.0 · **Etapa:** Fase 0, prova técnica mínima.

## Implementado

- Terreno original de 40 × 40 m com relevo suave, perfil do solo e cobertura vegetal.
- Uma árvore estilizada original, com fonte `.blend` independente e GLB reutilizável.
- Cena mestre `.blend`, GLB da composição, PNG 1280 × 960 e JSON com IDs estáveis.
- Visualizador responsivo: orbitar, aproximar, mover, vista superior, recuperar câmera, tela cheia e ajuda.
- Downloads de GLB, PNG e JSON na página.
- Workflows de validação, render e publicação no GitHub Pages.
- Planejamento original preservado em `docs/PLANO_MESTRE.md`.

## Verificação local

- Blender 4.3.2: geração e render CPU concluídos. GLB sem Draco e render sem denoiser.
- Verificador de ativos: validação do GLB, IDs dos objetos, fontes `.blend` e cabeçalho/dimensões do PNG.
- Testes Node: conversão de coordenadas, identidade, referência de ativos e transformação inválida.
- Build estático com caminhos relativos compatíveis com `/Fazenda/`.
- Revisão visual pelo navegador remoto usa o modo simplificado: WebGL indisponível nesse navegador.

## Aceite ainda a registrar

- Resultado dos workflows na execução inicial do GitHub Actions.
- Publicação e endereço do GitHub Pages.
- Abertura e navegação em um Android físico, incluindo gestos com dois dedos. Não foi afirmado teste em aparelho real.

## Próximo marco

Concluir o aceite da Fase 0 antes de iniciar a fazenda de 200 × 200 m. O editor completo e personagens pertencem às fases seguintes.
