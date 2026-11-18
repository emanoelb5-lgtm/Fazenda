# Decisões técnicas

1. **Fase 0 isolada.** O planejamento exige comprovar a integração antes da fazenda completa. O terreno mínimo mede 40 × 40 m; os 200 × 200 m pertencem à Fase 1.
2. **Uma fonte para a composição.** `data/fazenda.scene.json` gera o GLB no Blender. O visualizador carrega esse mesmo GLB e confere os IDs com o JSON; não recria uma árvore paralela no JavaScript.
3. **Vite apenas como empacotador.** A interface final é estática, sem servidor, sem segredo e com caminhos relativos compatíveis com o subdiretório do GitHub Pages.
4. **Fontes e exportações pequenas no Git.** Os `.blend`, GLBs e PNG da prova são versionados e reprodutíveis. Não foi necessário introduzir LFS nem serviço de ativos.
5. **Render CPU portátil.** OpenImageDenoise não existe na instalação local do Blender; render sem denoiser evita essa dependência também no runner.
6. **Compatibilidade sem WebGL.** O navegador de revisão bloqueia GPU/WebGL. Nessa situação, SVGRenderer permite explorar a mesma geometria com materiais simplificados e sem capim. O visualizador informa a limitação; WebGL continua sendo o modo principal no Android compatível.
7. **Teste de WebGL no CI.** O workflow usa Chromium com rasterização por software para verificar o carregamento, câmeras, links e duas larguras de tela. Isso não substitui testar um Android físico.
8. **Sem recursos das fases seguintes.** Não há editor de objetos, salvamento local, personagens ou vídeos na prova. Preservar esse limite até uma solicitação de avanço.
9. **Blender fixado no CI.** A instalação pelo gerenciador de pacotes do runner permaneceu ocupada por vários minutos. O workflow passou a baixar o Blender 4.3.2 diretamente do distribuidor oficial, verificar seu SHA-256 publicado e guardar a instalação em cache. Assim a versão do render não depende da versão do pacote Ubuntu.
