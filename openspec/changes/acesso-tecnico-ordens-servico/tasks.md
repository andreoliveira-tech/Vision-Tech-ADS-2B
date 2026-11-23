# Tasks

## 10. Composição de Equipamento no painel — correção local

- [x] 10.1 Corrigir somente GET /minhas-ordens para compor dados pelo Equipamento da OS autorizada, mantendo autenticação, filtro e contrato; não alterar pacote publicado.
- [x] 10.2 Cobrir tipo null, marca/modelo opcionais, exibição correta e ausência de repetição/escrita após falha; validar sintaxe local e preservar contador 148. Cinco testes novos e dez regressões direcionadas aprovados; parser oficial sem erros/avisos em fonte e pacote. Runtime pendente.
- [x] 10.3 Preparar UPDATE seletivo por GUID e documentar limites da verificação local, sem publicação nem retomada de D. Pacote separado xano-149143-v1-ordens-painel-fix; sete arquivos originais preservados. Ver docs/correcao-local-equipamento-painel.md.

## 9. Recuperação do painel autorizada (2026-11-18)

- [x] 9.1 Diferenciar consulta inicial, lista vazia e falha; exigir atualização explícita após erro e invalidar dados após PATCH incerto, sem GET/PATCH implícito em rerun.
- [x] 9.2 Cobrir falhas de consulta/status, recuperação explícita e sessão expirada com testes locais sem rede; manter homologação remota aberta. Conjuntos direcionados de OS/painel e verificador: 39 testes aprovados. Ver `docs/preparacao-local-ordens-servico.md`; nenhuma chamada remota, contador 103.

## Estado de homologação (2026-11-13)

Grupos 1–4 da etapa 06 concluídos; ver a seção 8 e o
[relatório consolidado](../../../docs/progresso-mvp.md). O checklist preserva
registros históricos. Publicação de autenticação não conclui APIs/painel de OS,
expiração, vínculo inválido, concorrência ou rollback. Nenhuma tarefa de isolamento
é encerrada por testes sequenciais; esta atualização é apenas documental.

## 1. Descoberta e decisÃµes arquiteturais

- [x] 1.1 Inspecionar cÃ³digo e inventÃ¡rio autorizado do Xano para autenticaÃ§Ã£o, TÃ©cnico, Equipamento e OS; evidÃªncias: branch `v1` confirmada live e pull somente leitura de 44 definiÃ§Ãµes do workspace `149143` para pasta temporÃ¡ria, sem registros/env/rascunhos; localmente, Streamlit usa `requests` sem autenticaÃ§Ã£o. Ver `design.md` seÃ§Ã£o â€œEvidÃªncias do inventÃ¡rio remotoâ€.
- [x] 1.2 Definir e documentar mecanismo real de autenticaÃ§Ã£o, sessÃ£o/token, provisionamento e perfis suportados; verificar se o contrato Ã© suportado pelo Xano disponÃ­vel. Evidencia: contrato remoto de `auth/login` (authToken/user_id) compativel com o cliente, `auth/me` remoto inspecionado e incompatibilidade de perfil/vinculo registrada no design; nenhuma autenticacao real foi declarada.
- [x] 1.3 Definir associacao univoca por `user_tecnico`, com FKs obrigatorias e indices UNIQUE em `user_id` e `id_tecnico`; arquitetura aprovada e definicoes locais criadas. Runtime ainda pendente.
- [x] 1.4 Registrar a matriz de navegacao local e a incompatibilidade: APIs de Clientes/Equipamentos nao validam os perfis funcionais no backend (docs/acesso-tecnico-autenticacao.md).
- [x] 1.5 Registrar contratos: OS fornece id_equipamento e os campos marca/modelo dependem do GET de Equipamentos, que nao exige auth e ainda nao foi publicado (docs/acesso-tecnico-autenticacao.md).

## 2. Backend e autorizaÃ§Ã£o

- [x] 2.1 Implementar autenticação real e validação de sessão no backend; Grupo 2: logins válidos 200, credenciais inválidas 403 e token inválido 401; campos de identidade preservados em auth/me. Grupos 3–4 confirmam sessões reais para os fluxos autorizados. Expiração natural e integração Streamlit permanecem no escopo aberto da 4.1.
- [ ] 2.2 Resolver perfil e associaÃ§Ã£o de TÃ©cnico pela identidade autenticada; verificar negaÃ§Ã£o para identidade tÃ©cnica sem vÃ­nculo vÃ¡lido.
- [x] 2.3 Implementar consulta de OS filtrada pelo `id_tecnico` associado com campos necessÃ¡rios; verificar resposta incluindo equipamento, problema e status apenas das OS atribuÃ­das.
- [x] 2.4 Implementar atualizaÃ§Ã£o de status com validaÃ§Ã£o de perfil, atribuiÃ§Ã£o e estados permitidos; verificar estado invÃ¡lido ou tÃ©cnico alheio rejeitados sem escrita.
- [x] 2.5 Proteger listagem, consulta individual e alteraÃ§Ã£o; verificar tentativas por ID direto de outra OS rejeitadas no backend.

## 3. Interface Streamlit

- [x] 3.1 Implementar cliente Streamlit para auth/login + auth/me e sessao temporaria; testes mock verificam somente o contrato local, sem comprovar autenticacao real.
- [x] 3.2 Implementar navegacao por perfil retornado pelo Xano e painel tecnico; testes mock cobrem composicao dos campos retornados pelas APIs, sem comprovar autorizacao integrada.
- [x] 3.3 Implementar PATCH de status na interface; teste mock confirma payload somente com status e atualizacao local apenas apos resposta confirmada.
- [x] 3.4 Implementar mensagens para lista vazia, backend indisponivel, sessao expirada e acesso negado; testes mock verificam comportamento local, sem evidenciar respostas reais.

## 4. VerificaÃ§Ã£o e encerramento

- [ ] 4.1 Executar cenÃ¡rios de login, vÃ­nculo, perfis e expiraÃ§Ã£o em ambiente autorizado; verificar evidÃªncias de respostas reais do mecanismo escolhido.
- [ ] 4.2 Executar consultas atribuÃ­das e tentativas de acesso a OS alheia; verificar autorizaÃ§Ã£o no backend para listagem e acesso direto.
- [ ] 4.3 Executar cenÃ¡rios de exibiÃ§Ã£o e alteraÃ§Ã£o de status vÃ¡lida/invÃ¡lida/nÃ£o autorizada; verificar resposta e persistÃªncia confirmada.
- [ ] 4.4 Registrar evidÃªncias, revisar aderÃªncia Ã s cinco entidades e marcar somente tarefas verificadas; verificar revisÃ£o documental e ausÃªncia de publicaÃ§Ã£o sem autorizaÃ§Ã£o.

## 5. Provisionamento local seguro (sem integraÃ§Ã£o remota)

- [x] 5.1 Preservar integralmente `user.role=admin/member`; separar perfil funcional e sinalizador em `user_application_profile` e vinculo em `user_tecnico`; signup sem perfil funcional.
- [x] 5.2 Implementar localmente provisionamento protegido por admin da mesma conta, perfil colaborador autorizado e alvo distinto; validar tecnico e vinculo exclusivo por pre-check e constraints UNIQUE.
- [x] 5.3 Atualizar localmente `auth/me` e guards para resolver perfil/vinculo pelas tabelas tecnicas; validar contratos com testes locais, sem declarar integracao remota.
- [ ] 5.4 Concluir validação de transações, bootstrap e fluxos no ambiente autorizado. Parcial comprovada: concessão do operador e fluxos sequenciais foram publicados/testados em v1 sob autorização específica nos Grupos 1–4. Isolamento e rollback por falha DB continuam não comprovados; não presumir ambiente isolado nem autorização para novo teste.
- [x] 5.5 Regenerar o pacote seletivo e manifesto conforme a arquitetura aprovada; evidência: `deployment/xano-149143-v1-controlled-package` contém 21 definições das etapas 03-09, 21 hashes SHA-256 conferidos, e nenhuma `table/user.xs`. O pacote temporário anterior permanece obsoleto e não deve ser usado.

- [ ] 5.6 Em homologacao, confirmar rollback de `db.transaction` e identificar código/constraint reais das violações UNIQUE de `user_application_profile.user_id`, `user_tecnico.user_id` e `user_tecnico.id_tecnico` antes de mapear HTTP conflito; outros erros devem propagar.

- [ ] 5.7 Validar comportamento atômico e isolamento das tabelas técnicas em ambiente isolado autorizado. Parser e fluxos sequenciais publicados sob autorização em v1 já possuem evidências; não encerram concorrência ou rollback. Manter pendente enquanto não houver evidência específica.

## 6. Correções exclusivamente locais da etapa 06 (2026-11-12)

- [x] 6.1 Mover leituras e decisões do provisionador para a transação; bloquear operador/alvo por ID crescente usando `db.get` com `lock = true` confirmado no parser oficial; exigir `=== true`.
- [x] 6.2 Gravar auditoria como operação DB dentro da transação; manter erros DB sem captura genérica nem tradução UNIQUE presumida; documentar as três constraints a identificar.
- [x] 6.3 Executar testes locais, parser oficial e validação OpenSpec; evidência: 125 testes aprovados, quatro cópias fonte/pacote da etapa 06 sem erros/avisos no parser oficial 12.28.0, Change válida em modo estrito, 21 hashes conferidos. Nenhuma validação de runtime ou publicação realizada.

## 7. Correção isolada da auditoria de login

- [x] 7.1 Substituir somente metadata de auth/login pelos seis campos explícitos aprovados, preservando GUID e fluxo de autenticação; não editar helper, auth/me, provisionador ou signup.
- [x] 7.2 Executar testes locais/parser, conferir pacote de um endpoint e abrir preview interativo sem confirmar publicação; evidência: 128 testes aprovados, parser oficial sem erros/avisos em fonte e pacote, OpenSpec estrito válido e preview limitado a UPDATE auth/login POST, parado em Proceed with push? (y/N).
- [x] 7.3 Após aprovação específica, publicar somente auth/login e verificar definição e auditoria; evidência: CLI confirmou um documento, pull de 55 definições com outras 54 intactas, único login E06 do operador retornou 200 e criou log 6 sem password. Registros anteriores preservados; sem limpeza retroativa ou início do Grupo 3.
- [x] 7.4 Revisar auth/signup por autorização separada: revisão local em 21/11 confirmou encaminhamento de `$user` completo. Ver docs/seguranca-fechamento-revisao-local-20261121.md; não comprova conteúdo dos logs remotos.

## 11. Correção seletiva local da auditoria de signup — 21/11/2026

- [x] 11.1 Substituir somente metadata de signup pelos seis campos explícitos já usados no login, preservando criação, token, resposta, GUID e demais recursos.
- [x] 11.2 Preparar seleção de um UPDATE com baseline/hashes e testes locais negativos de campos sensíveis/futuros e preservação do contrato; parser em fonte/pacote. Ver docs/signup-auditoria-correcao-local-20261121.md.
- [x] 11.3 Sob autorização própria, reconciliar definição remota e executar preview com delete=false; resultado em 21/11: HTTP 200/200, somente 0 CREATE/1 UPDATE/0 DELETE de POST auth/signup. Sem publicação; contador 628. Ver docs/signup-auditoria-preview-20261121.md.
- [x] 11.4 Após aprovação própria, publicar seletivamente e conferir definições/preservação: 21/11, um UPDATE de signup, 81 definições finais e outras 80 preservadas. HTTP 200 nas três chamadas; contador 631. Ver docs/signup-auditoria-publicacao-20261121.md. Sem criação de usuário ou limpeza de logs.
- [x] 11.5 Homologar em runtime o evento de novo signup sob lote autorizado: fixture 7 criada sem perfil/vínculo em 635; conferência assistida do responsável confirmou evento 313/signup com exatamente as seis chaves permitidas, sem chaves sensíveis. Valores/demais eventos não conferidos; não declara auditoria integral. Ver docs/signup-auditoria-conferencia-assistida-20261121.md. Logs históricos preservados sem limpeza; contador instrumentado 644, tráfego manual não medido.

## 8. Homologação sequencial da etapa 06 — Grupos 1–4

Comprovação adicional em 21/11, contador 644: fixture 7 recebeu sob autorização
específica somente perfil tecnico com provisionamento false e sem vínculo;
auth/me e minhas-ordens negaram 403, com perfis existentes/vínculos preservados.
Ver docs/acesso-final-vinculo-resultado-20261121.md. O cenário de vínculo ausente
está comprovado; 4.1 permanece aberta pela expiração real e demais alcances
não atendidos. Não declarar vínculo apontando a cadastro inexistente testado.

- [x] 8.1 Conferir preparação fictícia E06 do Grupo 1: conta 2, usuários 2/3, perfil do operador 1 e técnico 1; recibo verified=true, definições e auditoria preservadas, credenciais fora do Git.
- [x] 8.2 Registrar Grupo 2: sete chamadas públicas, credenciais inválidas 403, token inválido 401, login/auth/me válidos 200 e campos legados preservados; documentar achado de auditoria e correção posterior de login.
- [x] 8.3 Registrar Grupo 3 e a retomada autorizada: colaborador → técnico → colaborador no alvo 3; vínculo temporário 1 criado/removido; perfil 2 preservado; primeira rodada interrompida por 429, sem retry; leitura do estado e retomada documentadas, sem apagar o histórico.
- [x] 8.4 Conferir sete fixtures adicionais do Grupo 4: conta 3; usuários 4/5/6; perfis 3/4 com provisionamento false; vínculo 2 entre usuário 6 e técnico 1; registros preexistentes preservados. A interrupção por verificação local de password e a retomada sem duplicação estão registradas.
- [x] 8.5 Executar os seis cenários negativos autorizados do Grupo 4: HTTP 403/403/403/403/400/400; uma autenticação e uma tentativa por cenário; registros, papéis, perfis, permissões, vínculos e definições inalterados; somente logs de login 18–23, nenhum provisionamento bem-sucedido.
- [x] 8.6 Consolidar evidências dos Grupos 1–4 e planejamento de continuidade na documentação local; manter 4.1–4.4, 5.4, 5.6 e 5.7 abertas nos respectivos alcances ainda não comprovados. Não arquivar a Change nem declarar concorrência/rollback homologados.

Evidência de conclusão de 2.3–2.5: docs/homologacao-ordens-grupo-d-conclusao.md e reconferência da listagem corrigida. Contador acumulado 172; demais tarefas de homologação e isolamento permanecem abertas.
