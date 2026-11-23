# Tasks

## Grupo C funcional concluído — 20/11/2026, contador 418

32 chamadas: três logins/três auth/me, 13 negações e 13 conferências de
preservação. Anônimo/token inválido 401; técnico/sem perfil 403 nos contratos
esperados. IDs 1/2/3 e fixture 4 integralmente preservados; nenhuma escrita
negativa aceita. Cinco testes locais do coletor aprovados e snapshots protegidos
com duas leituras/hash. Ver `docs/tecnicos-permissoes-resultado-20261120.md`.
5.5 concluída; 15/21 tarefas. Auditoria integral e alcances das demais tarefas
permanecem pendentes. D/E/F não iniciados; subtotal E07 56, global 418.

## Cadastro reduzido autorizado — 20/11/2026, contador 386

Seis HTTP 200 após seis testes direcionados aprovados: login/auth/me de 3,
lista igual ao baseline, POST único da fixture 4, GET de 4 e lista final com
IDs 1/2/3 integralmente preservados. Snapshot protegido e hash conferido em duas
leituras. Ver `docs/tecnicos-cadastro-reduzido-resultado-20261120.md` e recibo.
Fixture 4 retida; não criar outra A nem repetir cadastro. B original segue
parcial no alcance de três identidades/auditoria; demais cenários ainda abertos.
Sem PUT/DELETE, publicação ou Git; subtotal E07 24 e global 386. Contagem 14/21
mantida, sem marcar tarefa composta concluída por evidência parcial.

## Conferência API autorizada — 20/11/2026, contador 380

Três chamadas após nove testes locais aprovados: login de 3, auth/me e listagem
de Técnicos, todas 200. Baseline dos IDs 1/2/3 protegido e conferido em duas
leituras SHA-256; nome/e-mail da fixture ausentes. Subtotal E07 18, sem zerar
as 15 chamadas históricas. Ver `docs/tecnicos-conferencia-api-resultado-20261120.md`
e recibo. Sem criação/PUT/DELETE de Técnico ou publicação. Auditoria não lida;
B–F e 1.1/4.1 continuam abertas nos respectivos alcances. 14/21 tarefas.

Preparação funcional B em 20/11, contador 380: proposta de 13 chamadas com
única criação de fixture A, comparação integral dos Técnicos 1/2/3 e auth/me
antes/depois. Onze testes novos em memória aprovados; nenhuma chamada real.
Ver `docs/tecnicos-b-funcional-proposta-20261120.md`. O alcance difere dos
snapshots integrais/auditoria do B original e requer aprovação explícita;
auditoria e conclusão de 5.4 continuam pendentes. Não alterar critérios nem
marcar o grupo original aprovado por esse ensaio. 14/21 tarefas preservadas.

## Preparação local da retomada em 20/11/2026

Reconciliação confirmou seis chamadas históricas de B (cinco GET 200 e login
403), sem auth/me ou criação de Técnico. Subtotal histórico E07 15/137;
contador global atual 377. Fontes de credencial diferentes foram identificadas
nos roteiros antigo e posterior, sem provar a causa da rejeição ou abrir segredos.

Política pura de seleção de descritor dedicada em
`tools/homologacao/tecnicos_fonte_credencial.py`, com dez testes sintéticos
aprovados, sem IO/DPAPI/rede e sem fallback. Ver
`docs/tecnicos-fonte-credencial-offline-20261120.md` e recibo. Não integra leitor
operacional nem altera executor antigo. 5.4–5.8, 1.1 e 4.1 permanecem abertas;
14/21 tarefas, sem declaração de autenticação atual ou homologação remota.

Ensaio de retomada B concluído localmente em 20/11: 15 novos testes aprovados,
18 chamadas sintéticas nominais, preservação de baseline e seis eventos de
auditoria simulados, sem leitura de credenciais ou HTTP. Corrigida parada imediata
na primeira coleção divergente sem alterar expectativa do teste. Ver
`docs/tecnicos-retomada-ensaio-offline-20261120.md` e recibo. Orçamento B–F revisado
proposto: 147 chamadas novas, incluindo novas sessões C/D/F; subtotal E07 162
com as 15 históricas, global condicional 524 a partir de 377. Não é autorização
nem teto congelado; projeções/auditoria/adaptador reais permanecem pendentes.
Tarefas de homologação e contagem 14/21 inalteradas, contador real 377.

Análise local da leitura segura em 20/11: projeções dos coletores históricos
ocorrem no cliente após recebimento; projeção de conteúdo no servidor não foi
comprovada pelos materiais locais. Auditoria histórica já exigiu duas páginas.
Ver `docs/tecnicos-viabilidade-leitura-segura-20261120.md`. Não preparar execução
com parâmetros presumidos nem receber registros completos como fallback.
Consulta à documentação pública oficial é o próximo passo proposto, sem acesso
ao workspace e sob autorização própria. Zero HTTP nesta análise, contador 377;
nenhuma tarefa remota ou limite operacional foi aprovado por associação.

Consulta documental pública autorizada em 20/11 concluída: GET de conteúdo
documenta paginação; busca avançada é POST com escopo de leitura, não executada.
Não foi encontrado seletor de colunas documentado nas operações examinadas.
Ver `docs/tecnicos-documentacao-leitura-segura-20261120.md`: propõe conferência
assistida somente leitura na interface para decisão do responsável, sem afirmar
projeção de rede, substituir baseline automaticamente ou encerrar a auditoria.
Nenhum acesso ao workspace; contador 377, tarefas de runtime preservadas.

Conferência assistida informada pelo responsável em 20/11: identidades, perfis
e vínculos conferem; tecnico contém três registros, incluindo
`E07 Tecnico Homologacao Atualizado`, sem nome iniciado pelo marcador exato
E07-20261116-01. Ver `docs/tecnicos-conferencia-manual-20261120.md`. Preservar os
três registros e verificar colisão pelo e-mail fictício antes de propor POST;
nome semelhante não comprova propriedade ou descartabilidade. Evidência manual,
sem API/hashes de registros ou auditoria conferida; 14/21 tarefas inalteradas.

Complemento manual: e-mail `e07-20261116-01@example.invalid` não localizado na
pesquisa realizada; IDs atuais 1/2/3 confirmados pelo responsável e protegidos.
Não identificada colisão nominal/de e-mail nos critérios pesquisados, sem
equivalência a snapshot completo. Nenhuma criação/login foi autorizada por essa
informação; baseline integral, auditoria e homologação B–F continuam pendentes.

## Grupo B interrompido (2026-11-16)

O responsável confirmou identidades/payload e intervalo de dez segundos.
Cinco GETs de metadados aprovaram o baseline; o primeiro login (usuário 3)
recebeu HTTP 403 e interrompeu o procedimento sem retry. Nenhum POST Técnico,
auth/me ou Grupo C executado. Acumulado de 15/137 chamadas; auditoria posterior
pendente. Ver [relatório B](../../../docs/homologacao-etapa07-grupo-b.md).
O executor foi ajustado para dez segundos, com 13 testes específicos aprovados;
o procedimento B teve cinco testes simulados aprovados. Tarefa 5.4 segue aberta.

## Grupo A concluído (2026-11-16)

Inventário e baseline aprovados em nove GETs de metadados, sem login ou escrita
remota. Técnicos preexistentes 1 e 2 preservados; marcador E07 ausente; perfis dos
usuários 3/5/6 compatíveis e URLs conferidas. Ver
[relatório](../../../docs/homologacao-etapa07-grupo-a.md).
Grupos B–F e tarefas 1.1/4.1 permanecem pendentes.

## Preparação de homologação real (2026-11-16)

O [roteiro E07](../../../docs/plano-homologacao-etapa07.md) organiza as tarefas
1.1 e 4.1 em grupos autorizáveis separadamente. Plano e executor foram preparados
e verificados localmente; nenhuma chamada real foi executada nesta preparação.
Ver seção 5 ao final.

## Revisão e inventário de 2026-11-16

129 testes locais aprovados, parser oficial sem erros/avisos em 11 arquivos,
OpenSpec estrito válido e 21 hashes conferidos. Corrigido formulário que
preservava valores do técnico anterior ao carregar outro cadastro.
Inventário remoto encontrou os quatro endpoints já existentes em `149143/v1`,
correspondentes ao pacote. Isso substitui as afirmações abaixo de que ainda
não foram publicados; data/autoria da publicação não foram determinadas.
Não republicar. Tarefas 1.1 e 4.1 continuam abertas para homologação real.
Ver [revisão da etapa 07](../../../docs/revisao-etapa07.md).

## Dependência atual (2026-11-13)

Perfis e provisionamento sequencial já estão publicados e validados nos Grupos
1–4 da etapa 06. Os quatro endpoints de Técnicos ainda são locais; 1.1 permanece
aberta na parte de comprovar a autorização nas APIs de negócio, e 4.1 permanece
aberta para integração real. Ver [plano da etapa 07](../../../docs/progresso-mvp.md#5-próxima-etapa-proposta-07--gestão-de-técnicos).

## Decisão aprovada: uma única assistência técnica (2026-11-13)

O MVP atende uma única assistência técnica. Clientes, Equipamentos, Técnicos,
Ordens de Serviço e Serviços pertencem ao mesmo ambiente operacional, compartilhado
pelos usuários funcionalmente autorizados. Não há isolamento entre empresas neste
MVP. A tabela `tecnico` não possui `account_id` por essa decisão; os quatro endpoints
da etapa 07 permanecem inalterados e a gestão exige autenticação Xano válida e
perfil funcional `colaborador` no backend.

Essa decisão não remove nem enfraquece os controles da etapa 06: identidade pelo
token, perfis em `user_application_profile`, vínculo técnico exclusivo em
`user_tecnico` e provisionamento restrito continuam vigentes. O provisionador
continua exigindo administrador com perfil colaborador e
`pode_provisionar_perfis=true`, alvo distinto e da mesma conta. As contas técnicas
existentes, inclusive a Conta B fictícia E06, não representam empresas operacionais
separadas no MVP e não serão removidas ou alteradas por esta decisão. Técnicos
continuam restritos às OS atribuídas no painel previsto; compartilhar o cadastro
não concede acesso administrativo ao perfil técnico.

Esta atualização é documental: não modifica endpoints, tabelas, usuários ou dados,
nem comprova integração remota, concorrência ou rollback por falha de banco.

## 1. Contratos e dependências

- [ ] 1.1 Concluir a verificação de autorização de colaborador alinhada a acesso-tecnico-ordens-servico. A dependência estrutural foi atendida: tabelas técnicas, guard e etapa 06 publicados; falta verificar, nos endpoints de gestão ainda não publicados, colaborador permitido e técnico/anônimo/sem perfil negados. O papel legado não equivale ao perfil funcional.
- [x] 1.2 Registrar a decisão aprovada pelo responsável para o MVP: `nome`, `especialidade`, `telefone` e `email` obrigatórios, email válido, sem unicidade; verificar mapeamento para os cinco campos do domínio. Esta é decisão de implementação, não exigência original do professor.
- [x] 1.3 Confirmar que a ausência de DELETE nesta Change e a dependência de integridade Técnico–OS estão documentadas; verificar referências às dependências de identidade e painel. Evidência: `proposal.md` e `design.md` excluem DELETE até ser possível verificar a integridade Técnico–OS e registram as dependências da associação de identidade e do painel.

**Dependência de autenticação:** perfis já são representados nas tabelas técnicas, preservando user.role=admin/member. A comprovação de autorização nas APIs de Técnicos ainda depende da etapa 07; os cenários do provisionador não substituem esse teste.

## 2. Backend Xano

- [x] 2.1 Criar tabela `tecnico` com os cinco campos do modelo e ID físico mapeado para `id_tecnico`; verificar XanoScript e correspondência integral ao modelo, sem atributos adicionais. Evidência local: `xano/table/tecnico.xs`; validador XanoScript aprovou os sete arquivos novos, sem erros/avisos. Evidência remota: em 2026-11-09, a etapa `01-tecnico-table` foi publicada em `149143/v1` após autorização explícita; o preview mostrou somente `CREATE table tecnico`, e um pull somente de definições confirmou a tabela, o GUID `nu49vX9JOpQr45J3_EhsCut0JuQ` e os campos `id`, `nome`, `especialidade`, `telefone` e `email`. Isso não comprova publicação das APIs nem integração funcional.
- [x] 2.2 Criar APIs locais autenticadas para POST, GET de lista, GET por identificador e PUT; verificar contratos de entrada/saída, guarda de colaborador e preservação do ID. Evidência: quatro endpoints usam `auth = "user"`, derivam identidade de `$auth.id` e chamam a guarda; a guarda só aceita `colaborador`. A impossibilidade de provisionar esse perfil no Xano atual e o teste runtime permanecem pendentes em 1.1 e 4.1.
- [x] 2.3 Adicionar testes/validações locais dos contratos de API para cadastro, lista vazia, consulta existente/inexistente, atualização e guarda de autorização; verificar que DELETE não foi criado. Evidência: `frontend/tests/test_tecnicos.py` cobre HTTP simulado, respostas 401/403 e inspeção das definições. Isso não comprova autorização em runtime Xano.
- [x] 2.4 Documentar rotas, campos, autenticação e dependências do backend; verificar exemplos contra as definições XanoScript e não declarar publicação sem evidência. Evidência: `docs/api-tecnicos.md` distingue definições locais, dependência de auth e ausência de publicação.

## 3. Frontend Streamlit

- [x] 3.1 Implementar configuração externa e cliente HTTP de Técnicos autenticado; verificar URL ausente/inválida, envio de token e validação estrita das respostas com transporte simulado. Evidência: `frontend/config.py`, `frontend/tecnicos_api.py` e testes locais de configuração, Bearer e contrato.
- [x] 3.2 Implementar página Streamlit para cadastrar, listar, consultar e atualizar Técnicos; verificar que apresenta somente os campos do domínio, preserva o ID e respeita falhas de autorização. Evidência: `frontend/pages/2_Tecnicos.py`, `frontend/tecnicos_ui.py` e testes AppTest com HTTP simulado.
- [x] 3.3 Adicionar testes da interface e documentar configuração/uso; verificar fluxos permitidos, sessão expirada, acesso negado, campos e ausência de ação de exclusão. Evidência: `frontend/tests/test_tecnicos.py`, `frontend/README.md` e `docs/api-tecnicos.md`.

## 4. Integração e encerramento

- [ ] 4.1 Verificar backend e Streamlit integrados em ambiente autorizado; testar acesso de colaborador e rejeição de técnico/usuário anônimo sem consultar ou alterar registros não autorizados.
- [x] 4.2 Revisar diff, contratos e documentação contra `docs/domain-model.md`; verificar que nenhuma entidade ou atributo além dos cinco definidos foi adicionado. Evidência: teste estático compara exatamente `id`, `nome`, `especialidade`, `telefone` e `email` na tabela; os contratos e respostas expõem somente esses campos. Não houve alteração nas cinco entidades existentes.
- [x] 4.3 Registrar evidências de execução real, manter tarefas sem comprovação abertas e arquivar somente após critérios remotos aprovados; verificar que publicação não ocorreu sem autorização específica. Evidência: a publicação da tabela Técnico foi explicitamente autorizada e verificada por pull remoto em 2026-11-09; as tarefas 1.1 e 4.1 permanecem abertas por dependerem de autenticação e integração real. Esta Change não foi arquivada e não se considera concluída.

## 5. Homologação E07 — execução pendente

Atualização de 21/11, contador 633: perfis/vínculos relevantes de 3/5/6
conferidos em duas leituras autorizadas, HTTP 200/200, sem login ou alterações.
Ver docs/tecnicos-f-perfis-resultado-20261121.md. Definições já conferidas;
5.8 continua aberta somente no alcance ainda não comprovado, especialmente
auditoria. Não repetir CRUD/definições/perfis para encerrar essa lacuna.

Chamada 508: sete definições de Técnicos comparadas e preservadas por meio da
resposta de definições autorizada para Clientes. Nenhuma consulta adicional.
5.8 permanece aberta para tabelas internas e auditoria. Ver
`docs/clientes-definicoes-diagnostico-resultado-20261120.md`.

Atualização posterior: contador 474. `body_id_override` aprovado com consulta
individual e comparação integral da listagem. Resta `put_missing_id`: guarda
local impediu o envio do PUT /5, sem tentativa HTTP. 5.6 permanece aberta.
Ver `docs/tecnicos-d-integridade-interrupcao-20261120.md`.

Atualização de 20/11: retomada de entradas/edição concluída com 45 chamadas,
acumulado 467. Fixture 4 editada e confirmada; IDs 1/2/3 preservados.
5.6 permanece aberta para `body_id_override` e `put_missing_id`, não executados
nesta seleção. Grupos E/F não iniciados. Evidência:
`docs/tecnicos-entradas-edicao-resultado-20261120.md`.

- [x] 5.1 Preparar roteiro revisável de cenários, identidades, payloads, fixtures, orçamento, evidências e interrupção; sem executar chamadas reais. Evidência: `docs/plano-homologacao-etapa07.md`.
- [x] 5.2 Preparar e verificar localmente executor de homologação com transporte real serializado, intervalo mínimo, limites de destino/método/chamadas, proteção de segredos e interrupção sem retry; necessário antes do grupo E, sem alterar código do produto. Evidência: `frontend/executor_homologacao.py`, 13 testes sem rede em `frontend/tests/test_executor_homologacao.py` e `docs/executor-homologacao-etapa07.md`; portal testado com três perfis e HTTP simulado. Nenhuma chamada real executada.
- [x] 5.3 Executar grupo A autorizado: reconferir destino, URLs, definições, identidades e baseline; até dez chamadas somente leitura. Evidência: `docs/homologacao-etapa07-grupo-a.md`, nove GETs HTTP 200 e intervalo mínimo de cinco segundos; baseline DPAPI conferido e relatório sanitizado. Nenhum login ou escrita remota.
- [ ] 5.4 Executar grupo B autorizado: autenticar as três identidades fictícias e criar/conferir fixture A; até oito chamadas, sem provisionamento.
- [x] 5.5 Executar grupo C autorizado: testar quatro rotas para anônimo/técnico/sem perfil e token inválido com conferência de preservação; até 26 chamadas. Executado em 20/11 com seis chamadas adicionais explícitas de autenticação: 32 no total, globais 387–418; ver relatório e recibo.
- [x] 5.6 Executar grupo D autorizado: rejeições de entrada, preservação de ID, atualização válida e inexistente. Concluído no alcance do roteiro por lotes expressamente autorizados, com orçamentos revisados documentados; acumulado final 480. PUT inexistente rejeitado sem criação, registros 1/2/3/4 preservados. Ver `docs/tecnicos-d-conclusao-20261120.md`; não se declara cumprimento do teto histórico de 45 chamadas para o conjunto das recuperações.
- [x] 5.7 Executar grupo E autorizado pelo portal real: três perfis, fixture B, troca de cadastro, confirmação de edição e navegação negada. Concluído com 25 chamadas reais, acumulado 505; fixture B=5, registros 1/2/3/4 preservados. Ver `docs/tecnicos-grupo-e-resultado-20261120.md`. Controle DELETE existente não acionado/homologado, conforme ressalva da preparação autorizada; Grupo F pendente.
- [ ] 5.8 Executar grupo F autorizado: comparar baseline, duas fixtures retidas, perfis/vínculos, definições e auditoria; até oito chamadas. Registrar lacunas e só concluir 1.1/4.1 com suas evidências comprovadas.
