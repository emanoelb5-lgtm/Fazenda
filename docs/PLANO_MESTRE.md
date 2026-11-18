# ESTÚDIO FAZENDA 3D
## Plano mestre de desenvolvimento com ChatGPT Work, GitHub e Blender

**Versão:** 1.0  
**Data:** 17/11/2026  
**Objetivo:** construir uma fazenda virtual 3D permanente, expansível e editável pelo celular Android; depois acrescentar personagens, máquinas e produção de animações educativas e comerciais reutilizando os mesmos ativos.

## 1. Premissas e decisões

- Operação pelo celular Android; não exigir computador próprio.
- Ferramentas centrais: **ChatGPT Work** (coordenação e desenvolvimento), **GitHub** (repositório, versões, Pages e Actions) e **Blender** (modelagem 3D, scripts, renderização).
- Ferramenta auxiliar livre: **Three.js**, usada na interface 3D no navegador, publicada no **GitHub Pages**. Não será necessário contratar outra hospedagem na primeira versão.
- Modelo de custos: não usar geração paga de imagens/vídeos por IA como dependência obrigatória. Priorizar Blender gratuito, bibliotecas livres, e GitHub Actions dentro das condições gratuitas elegíveis. ChatGPT Work utiliza a franquia do plano. Acompanhar os limites do GitHub.
- Um único repositório GitHub será a fonte versionada do projeto; nunca depender apenas dos arquivos temporários de uma sessão Work.
- A fazenda precisa existir como **mundo editável**, e não apenas como vídeo ou imagem fixa.
- Começar por uma prova de conceito pequena e verificável, só então aumentar a complexidade.

## 2. Objetivos do produto

### 2.1 Primeira entrega: fazenda e editor móvel

- Terreno de referência inicial de 200 m x 200 m, com unidades de escala reais (metros).
- Relevo suave, caminhos de terra, residência, galpão, cercas, vegetação, riacho e três talhões.
- Estilo 3D legível e agradável, adequado a Android intermediário; preferir baixa a média complexidade com materiais bem trabalhados.
- Câmera aérea/orbital, aproximação, giro e modo passeio em primeira pessoa com controle sensível ao toque.
- Seleção de objetos por toque, mover, girar, ajustar escala, duplicar, apagar, posicionar com encaixe em solo e desfazer/refazer.
- Catálogo inicial de objetos: árvores, cerca, estradas, talhões, casa, galpão, caixa-d'água, irrigação básica.
- Salvar automaticamente *localmente* no navegador (IndexedDB) e permitir **Exportar projeto (.json)** e **Importar projeto (.json)**. O salvamento local deve avisar que não equivale a um backup permanente.
- Um botão de exportação clara, gerando arquivo que possa ser enviado ao Work ou adicionado ao repositório para sincronizar a cena.
- A cena salva deverá reconstruir a mesma disposição de objetos após atualização do aplicativo.

### 2.2 Entregas posteriores

- Plantações com espécies e arranjos diversos, ferramentas e máquinas.
- Personagens rigados/animáveis, roupas e ações reutilizáveis.
- Editor de tomadas, trajetórias de câmeras e roteiro por cenas.
- Renderizações de imagens e vídeos MP4 via Blender no GitHub Actions.
- Expansão por setores, com carregamento seletivo do mapa e versionamento dos ativos.

## 3. Arquitetura técnica

### 3.1 Papéis e responsabilidades

**ChatGPT Work**
- Lê o contexto do projeto, examina o repositório, desenvolve e modifica o código, cria scripts Python para Blender e workflows.
- Valida resultados de testes e corrige erros; não afirma que algo funciona sem teste.
- Pode atuar pelo GitHub conectado, conforme permissões e disponibilidade da conexão.

**GitHub (repositório)**
- Armazena código, arquivos de cena, scripts, configurações, documentação e modelos 3D que caibam nos limites do serviço.
- Usa commits e pull requests para rastreabilidade; mantém cópias de referência e backups versionados.

**GitHub Pages**
- Hospeda gratuitamente, nas condições aplicáveis, o editor 3D em HTML/JavaScript.
- É uma hospedagem estática: não pode gravar, por si só, arquivos diretamente no repositório.
- A URL do Pages é pública. Não inserir segredos nem dados privados no site ou no código enviado a ele.

**GitHub Actions**
- Executa testes, compila o editor, publica no Pages e roda Blender em modo `--background` para gerar modelos/miniaturas/vídeos.
- Publica arquivos de saída como *Artifacts* para baixar pelo celular.
- Criar workflows manuais para tarefas pesadas, evitando re-renderizações a cada pequeno commit.

**Blender**
- É o ambiente de criação de geometrias, materiais, rigs, animações, iluminação e renderização.
- Mantém arquivos `.blend` principais e exporta modelos `.glb` para o navegador.
- Reimporta a composição da cena a partir do JSON para renderizar a mesma fazenda mostrada no editor móvel.

**Three.js (biblioteca auxiliar)**
- Faz visualização e edição 3D via toque no navegador Android.
- Não substitui o Blender para operações avançadas de modelagem, rigging e renderização.

### 3.2 Fonte de verdade dos dados

- Cada ativo (casa, árvore, trator, galpão) recebe um `asset_id` estável e seu `.blend` original é preservado.
- Cada instância posicionada na fazenda recebe um `instance_id` próprio.
- A disposição da fazenda — coordenadas, rotação, escala, setor, referência de ativo — fica em `data/fazenda.scene.json`.
- O editor modifica o JSON da cena; o Blender importa esse JSON para montar as posições e fazer a renderização. Evitar duas versões independentes da localização dos objetos.
- Padronizar metros e sistema de coordenadas; documentar conversão entre Blender (Z para cima) e Three.js (Y para cima).
- Modelos podem ser exportados em GLB, mas preservar os `.blend`, pois nem todos os dados do Blender sobrevivem ao formato GLB.

### 3.3 Sincronização sem servidor adicional

**Versão 1:** editar no celular, salvar localmente, exportar JSON; o Work importa o arquivo para o GitHub e atualiza a cena base. Assim não é necessário introduzir autenticação insegura no navegador.

**Versão futura:** caso seja indispensável salvar direto no repositório, desenvolver autenticação e backend apropriados, sem colocar token pessoal ou credenciais permanentes no front-end público. Não implementar escrita direta em GitHub Pages usando token embutido.

## 4. Estrutura proposta do repositório

```text
estudio-fazenda-3d/
├── README.md
├── docs/
│   ├── PLANO_MESTRE.md
│   ├── PADRAO_ASSETS.md
│   └── REGISTRO_DE_DECISOES.md
├── data/
│   ├── fazenda.scene.json
│   └── schemas/
│       └── scene.schema.json
├── blender/
│   ├── base/
│   │   └── fazenda_base.blend
│   ├── assets/
│   │   ├── construcoes/
│   │   ├── vegetacao/
│   │   ├── culturas/
│   │   ├── maquinas/
│   │   └── personagens/
│   └── scripts/
│       ├── gerar_cenario.py
│       ├── exportar_glb.py
│       ├── importar_scene_json.py
│       └── renderizar.py
├── public/
│   └── models/               # GLB otimizados para visualização
├── web/
│   ├── src/
│   ├── public/
│   └── package.json
├── tests/
├── .github/workflows/
│   ├── tests.yml
│   ├── deploy-pages.yml
│   ├── export-assets.yml
│   └── render-video.yml
└── .gitignore
```

A estrutura é inicial; o Work pode refiná-la tecnicamente, desde que documente os motivos e preserve o princípio de uma fonte única de dados.

## 5. Plano de execução e critérios de aceite

### Fase 0 — Prova técnica mínima
**Tarefas:** criar repositório, instalar/declarar versões, criar um arquivo Blender com terreno e uma árvore; renderizar 1 imagem no GitHub Actions; gerar GLB; disponibilizar visualizador básico no GitHub Pages; testar acesso no Android.

**Aceite:** uma imagem renderizada para download nos Artifacts + cena 3D navegável pelo Chrome do celular + arquivos no GitHub. Sem esta prova, não avançar.

### Fase 1 — Fazenda inicial
**Tarefas:** criar malha de terreno 200 x 200 metros; relevo suave, riacho, estradas, casa, galpão, cercas, vegetação e 3 talhões; criar iluminação diurna e materiais; organizar posições no JSON; gerar `.blend` de referência e `.glb` otimizados.

**Aceite:** fazenda visível no navegador com proporções coerentes; modelos independentes; nenhuma construção principal fundida ao terreno; ativos originais preservados.

### Fase 2 — Editor móvel funcional
**Tarefas:** controles por toque, orbit/zoom, andar, selecionar, mover, girar, redimensionar, duplicar, excluir; encaixar objeto no solo; undo/redo; salvar/carregar IndexedDB; importar/exportar JSON.

**Aceite:** no Android, mover uma árvore, inserir uma cerca, salvar, fechar e reabrir a página; alterações persistem. Exportar JSON, reimportar e obter a mesma cena.

### Fase 3 — Biblioteca agrícola e aprimoramento visual
**Tarefas:** talhões configuráveis, espécies agrícolas, irrigação, estruturas de viveiro, ferramentas e máquinas; melhorar texturas, vegetação e atmosfera; perfis de qualidade gráfica para smartphones.

**Aceite:** adicionar equipamentos sem modificar a base; bom desempenho no dispositivo-alvo; biblioteca documentada com IDs de ativos e licenças.

### Fase 4 — Personagens permanentes
**Tarefas:** criar personagem principal; preparar rig, materiais, expressões e conjuntos de animações (parado, caminhar, apontar, usar ferramentas); validar importação para editor e Blender. Acrescentar personagens secundários depois.

**Aceite:** mesmo personagem identificável e reutilizável entre cenas; movimentos demonstrados por vídeo curto; arquivos fonte preservados.

### Fase 5 — Sistema de animações
**Tarefas:** cenas baseadas em JSON, câmeras, trajetórias, timeline simples, importação de áudio de narração, renderização de quadros e montagem de MP4; workflows manuais no GitHub Actions.

**Aceite:** vídeo de teste de 5–10 segundos, gerado com os ativos existentes; MP4 nos Artifacts; nenhuma alteração destrutiva na fazenda mestre.

### Fase 6 — Expansão e manutenção
**Tarefas:** setores anexáveis, salvamento por setores, carregamento sob demanda, catálogo ampliado, versões de ativos, otimização e backups.

**Aceite:** novo setor com ao menos uma construção e um talhão, sem quebrar vídeos antigos nem mudar o posicionamento do setor original.

## 6. Regras permanentes de desenvolvimento

1. Não avançar de fase sem entregar e validar critérios de aceite.
2. Não reconstruir fazenda, personagens ou equipamentos que já existam; reutilizar IDs e ativos.
3. Qualquer mudança destrutiva deve ser feita em branch e verificada antes da integração.
4. Trabalhar com arquivos versionados e documentação; evitar depender da memória de uma conversa.
5. Todos os recursos de edição precisam ser utilizáveis com toque, sem mouse nem teclado.
6. Testar cenário simples antes de renderizações custosas. Nas cenas complexas, testar primeiro 1 quadro e depois 3–5 segundos em resolução reduzida.
7. Evitar ativos externos sem licença clara; documentar origem, licença e atribuição quando necessária.
8. Não introduzir ferramentas pagas sem autorização do proprietário do projeto.
9. Não inserir tokens de autenticação no site estático ou no código público.
10. Apresentar relatório breve por fase: o que foi criado, o que foi testado, links, problemas conhecidos e próximo marco.

## 7. Desempenho e limites

- Começar com objetos de baixa/média densidade, texturas otimizadas e renderização por CPU quando necessário.
- A área de 200 x 200 metros é um ponto de partida, não uma limitação definitiva.
- Preferir renderização de vídeos em jobs manuais do Actions e armazenar resultados em Artifacts com prazo de retenção conhecido.
- Observar limites de tempo, armazenamento, tamanho de arquivos e minutos de GitHub Actions, que dependem do plano e da visibilidade do repositório.
- Arquivos grandes de Blender/GLB exigem gestão de tamanho (eventualmente Git LFS ou outro armazenamento, se necessário e aprovado).
- Renderizar vídeos sofisticados pode demorar e superar limites gratuitos; isto será medido nos testes.

## 8. O que deverá existir depois da primeira fase de implementação

- Repositório GitHub com código e histórico.
- URL pública do editor móvel na página GitHub Pages (sem informações sensíveis).
- Arquivos `.blend` e `.glb` originais e exportados da primeira fazenda.
- `fazenda.scene.json` reproduzível em Three.js e Blender.
- Ferramenta no celular para navegar pela cena e, na segunda fase, editá-la.
- Workflow de teste e renderização no GitHub Actions.
- Instruções de uso para Android e registro do que foi efetivamente validado.

## 9. Como integrar este planejamento ao projeto ChatGPT

1. Criar um Projeto no ChatGPT, por exemplo **Estúdio Fazenda 3D**.
2. Mover a conversa de planejamento para o projeto, pelo menu da conversa **Mover para projeto**.
3. Anexar este arquivo `Plano_Estudio_Fazenda_3D_Work_GitHub_Blender.md` ao projeto, caso deseje manter o plano como referência separada da conversa.
4. Conectar o GitHub ao ChatGPT conforme as permissões solicitadas.
5. Iniciar uma nova conversa **Work** dentro desse mesmo projeto, para herdar o contexto do projeto quando o recurso estiver disponível.
6. Enviar o comando de abertura abaixo e executar apenas a Fase 0 antes de autorizar a Fase 1.

## 10. Comando inicial ao ChatGPT Work

> Este projeto contém o plano mestre do Estúdio Fazenda 3D. Leia todo o plano e utilize o repositório GitHub correspondente como fonte permanente. Precisamos criar uma fazenda 3D editável e explorável pelo celular, com Blender para os modelos/renderizações e GitHub Pages/Actions para a interface e automação.
>
> **Execute somente a Fase 0 (prova técnica mínima).** Confirme o repositório, estruture os arquivos, crie um terreno com uma árvore no Blender por script, configure o GitHub Actions para renderizar uma imagem e exportar um GLB, publique uma página de visualização 3D acessível no Android e documente os resultados. Não avance para a fazenda completa ou para personagens. Se houver falha, investigue, corrija, teste novamente e relate claramente o que conseguiu validar. Não utilize serviços pagos e não publique credenciais.

---

**Orientação estratégica:** o editor Android é o instrumento para posicionar e administrar a fazenda; o Blender preserva e renderiza os ativos mestres; o GitHub garante continuidade. Personagens e filmes serão acrescentados apenas depois de o ambiente funcionar bem.
