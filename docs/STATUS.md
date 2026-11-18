# Estado do projeto

**Versão:** 0.1.0 · **Etapa:** Fase 0, prova técnica mínima.

**Resultado em 17/11/2026:** implementação e testes automáticos concluídos; publicação no Pages e aceite em Android físico pendentes.

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

## Verificação no GitHub Actions

- **Validação aprovada:** [execução 44216089848](https://github.com/emanoelb5-lgtm/Fazenda/actions/runs/44216089848), com quatro testes Node, verificação dos modelos, build e quatro testes de navegador. Também aprovada após a atualização do workflow do Blender.
- **WebGL aprovado:** Chromium em desktop (1280 × 900) e tela móvel emulada (393 × 852), com carregamento real do GLB, zoom, vista superior, retorno à vista inicial, ajuda e downloads. Nenhum erro JavaScript nos testes.
- **Render aprovado:** [execução 44216611500](https://github.com/emanoelb5-lgtm/Fazenda/actions/runs/44216611500), Blender oficial 4.3.2, download verificado por SHA-256, geração das fontes/GLBs e imagem PNG. Verificador de ativos aprovado.
- **Pacote disponível:** Artifact `fazenda-fase0-blender-glb-imagem`, ID `14387284883`, 2.108.127 bytes, retenção de 30 dias. Os arquivos de referência também estão versionados no Git.
- A tentativa inicial de instalação do Blender por apt foi substituída pelo download oficial fixado e validado no workflow acima.

## Pendências do aceite

| Critério | Estado |
| --- | --- |
| Código e arquivos no GitHub | Concluído |
| Uma imagem renderizada no Actions e disponível em Artifact | Concluído |
| Navegação WebGL em desktop e tela móvel emulada | Concluído |
| URL pública no GitHub Pages | Pendente: ativação inicial nas configurações do repositório |
| Chrome em Android físico, inclusive gestos com dois dedos | Pendente: não houve acesso a um aparelho físico |

## Publicação

O build do visualizador passou. A primeira publicação falhou na criação inicial do Pages: `Resource not accessible by integration`. A integração usada consegue escrever o projeto, mas não configurar essa ativação inicial.

Uma vez autorizado o acesso às configurações da conta, selecionar **Settings → Pages → Build and deployment → Source: GitHub Actions**. Em seguida executar **Actions → Publicar visualizador → Run workflow**. O workflow atual lê a configuração existente; não tenta criar ou ampliar permissões da conta. Registrar aqui a URL apenas depois de uma publicação aprovada.

A navegação pelo navegador remoto foi conferida no modo simplificado (SVG): vista superior, retorno à câmera inicial, zoom e ajuda. O modo WebGL completo foi validado pelos testes do Actions. Não houve teste em Android físico.

## Próximo marco

Concluir o aceite da Fase 0 antes de iniciar a fazenda de 200 × 200 m. O editor completo e personagens pertencem às fases seguintes.
