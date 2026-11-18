# Estúdio Fazenda 3D

Leia `docs/PLANO_MESTRE.md` e `docs/STATUS.md` antes de continuar.

- O repositório `emanoelb5-lgtm/Fazenda` é a fonte permanente deste projeto.
- A implementação atual é somente a Fase 0. Não iniciar fazenda completa, editor ou personagens sem uma nova solicitação.
- Preserve IDs, fontes Blender e disposição canônica em `data/fazenda.scene.json`.
- Use metros; JSON e Three.js Y-up, Blender Z-up. Conversão: `(x,y,z) -> (x,-z,y)`.
- Objetos principais devem permanecer independentes. Não substituir fontes por imagens.
- Todos os controles do visualizador precisam funcionar por toque.
- Não adicionar serviços pagos, tokens públicos ou ativos sem licença documentada.
- Antes de enviar alterações: `npm test`, `npm run check:assets`, `npm run build`. Quando mudar geração, execute Blender e valide os arquivos.
- Os testes de navegador rodam no Actions; nunca registrar como teste em aparelho físico.
- Registre resultados reais e limitações em `docs/STATUS.md`.
