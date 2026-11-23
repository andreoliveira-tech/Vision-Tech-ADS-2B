# Tasks

## 1. Tema e apresentação compartilhada

- [x] 1.1 Implementar tema claro e componente de apresentação local, reutilizando paleta/CSS existentes sem recursos externos; testes locais devem conferir aplicação em reruns e contraste dos pares utilizados, com documentação do padrão e sem HTTP.
- [x] 1.2 Integrar portal e entradas diretas sem duplicar marca/navegação; verificar por AppTest os perfis colaborador/técnico, ausência de perfil, logout e preservação da revalidação existente, documentando os pontos de integração.

## 2. Telas existentes e segurança dos estados

- [x] 2.1 Padronizar login e Clientes mantendo labels, keys, forms e âncoras úteis; testes negativos devem preservar configuração inválida, troca de alvo, confirmação e bloqueio de escrita incerta, sem novas chamadas; registrar mudanças visuais.
- [x] 2.2 Padronizar Equipamentos, Técnicos, OS e Serviços com cabeçalhos, formulários, tabelas, feedback e ações destrutivas; regressões afetadas devem comprovar payloads/contagens de chamadas e confirmações anteriores preservados; documentar alterações sem habilitar exclusões pendentes.
- [x] 2.3 Padronizar painel técnico mantendo navegação restrita, OS atribuídas e payload de status; testes locais devem cobrir erro e rerun sem reenvio e preservar o fluxo homologado, com registro da apresentação final.

## 3. Inicialização e configuração

- [x] 3.1 Completar seis defaults de URL no iniciar-local.cmd somente quando ausentes; testar preservação de valores próprios, configuração inválida e ausência de atribuição à flag DELETE, sem iniciar portal autenticado ou chamadas reais; atualizar frontend/README.md com precedência e execução.

## 4. Revisão visual offline e integração

- [x] 4.1 Preparar prévia identificada com dados fictícios, telas reais e bloqueio de rede/gravações; verificar a proteção com caso negativo e registrar como executar sem login real, sem alterar evidências anteriores ou contador.
- [x] 4.2 Inspecionar as sete telas no navegador em 1440 e 390 pixels, incluindo rolagem até ações inferiores, vazio/erro/desabilitado/incerto aplicáveis, foco por teclado, contraste e ausência de clipping; guardar screenshots e relatório de achados/correções, sem declarar aparência apenas por AppTest.
- [x] 4.3 Executar regressões locais direcionadas aos arquivos modificados e conferir diff/escopo por hashes, sem repetir homologação remota; consolidar testes, arquivos alterados, limitações e resultado da revisão visual em relatório de conclusão.
- [x] 4.4 Apresentar telas e evidências para aceite do responsável; registrar aceite ou pendências antes de propor sincronização/Archive, mantendo as pendências do backend separadas e sem commit/push automático.

Planejamento concluído em 20/11/2026. Nenhuma tarefa de implementação foi
executada nesta preparação. Contador 375; sem HTTP, publicação ou alteração
de código do produto. Meta do MVP: 21/11/2026, condicionada aos critérios abertos.

Evidência: docs/streamlit-apresentacao-20261120.md. 184 testes distintos
aprovados, sete telas em duas larguras revisadas offline; 10/10 tarefas após
o aceite visual explícito de 20/11/2026. Contador 375, zero HTTP ao Xano nesta etapa.

Aceite visual 4.4: ACEITO pelo usuário solicitante em 20/11/2026.
Escopo: revisão final documentada em docs/streamlit-revisao-final-20261120.md
e evidências em docs/evidencias/streamlit-revisao-final-20261120.json;
Gerente em 1440 px e Técnico em 390 px. Melhorias futuras registradas:
seletores com nome em lugar de ID e regra de Salvar status em OS concluída.
O aceite não altera a situação dos DELETEs no backend nem das homologações
funcionais pendentes, e não comprova integração da prévia ao produto.
Sem sincronização ou Archive. Recibo original preservado; aceite em
docs/evidencias/streamlit-aceite-visual-20261120.json.
Consolidação e diferenças entre a prévia isolada e o produto:
docs/streamlit-revisao-final-20261120.md.
