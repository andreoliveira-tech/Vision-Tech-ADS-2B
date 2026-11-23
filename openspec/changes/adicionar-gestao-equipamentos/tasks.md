# Tasks

## 1. Contexto e contratos

- [x] 1.1 Conferir inventário e schema da tabela 908125 e contrato publicado da função 355571 por GET de metadados, sem registros; evidência e limites no design.
- [x] 1.2 Revisar os seis atributos, operações, vínculo obrigatório e decisão atual de bloqueio com OS; verificar coerência entre proposta, design e cenários.

## 2. Preparação local do backend

- [x] 2.1 Preparar grupo e cinco endpoints XanoScript locais, sem duplicar tabela/função existentes; revisar mapeamentos e ordem de validação antes da escrita. Sete definições locais passaram pelo validador de sintaxe, sem execução remota.
- [x] 2.2 Preparar consulta de dependências e DELETE que interrompe a operação em falha; documentar a referência provisória à tabela de OS e a impossibilidade de publicação atual. Ver `docs/api-equipamentos.md`; a tarefa 4.1 continua aberta.
- [x] 2.3 Documentar contratos HTTP propostos e recursos remotos necessários, distinguindo preparação de validação no runtime em `docs/api-equipamentos.md` e no README do frontend.

## 3. Frontend e testes locais

- [x] 3.1 Implementar configuração externa e cliente HTTP de CRUD, com contratos estritos, uma tentativa por ação, timeout e redirecionamentos desativados; verificar com HTTP simulado. Coberto na suíte local aprovada.
- [x] 3.2 Implementar página Streamlit com campos nullable, carregamento para edição/exclusão, confirmação explícita, recuperação de resultados incertos e controles de DELETE desabilitados até validação explícita; verificar por AppTest. Coberto na suíte local aprovada.
- [x] 3.3 Executar suíte local com rede bloqueada, corrigir falhas e conferir regressão de Clientes; registrar resultados reais na documentação. Execução inicial: 77 testes. Após incluir o gate explícito de DELETE: 79 testes aprovados (30 de Equipamentos e 49 de Clientes), sem HTTP real.
- [x] 3.4 Validar estrutura OpenSpec e referências locais; conferir preservação das onze Changes anteriores e ausência de alterações remotas. Doze Changes válidas; comparação SHA-256 dos arquivos anteriores e conferência de links sem divergências fora dos dois arquivos locais previstos.

## 4. Publicação e verificação remota — requer autorização específica

Inventário e dry-run em 2026-11-16 confirmaram dependências e sete CREATEs
exclusivos; nenhum recurso aplicado. Ver `docs/preview-publicacao-equipamentos.md`.
4.1 segue aberta para validação contextual; 4.2 para publicação/conferência.

- [x] 4.1 Resolver e verificar a consulta real de OS contra o schema aprovado, sem criar OS antecipadamente; validar XanoScript no contexto do workspace. Após publicação autorizada das rotas de OS e criação controlada das fixtures em C, Grupo E de OS confirmou DELETE do Equipamento 3 bloqueado com 400 por OS 1 vinculada, com persistência de ambos. Ver docs/homologacao-ordens-grupo-e-conclusao.md.
- [x] 4.2 Reconferir inventário e publicar apenas grupo/endpoints/helper necessários, reutilizando 908125/355571; confirmar definições publicadas e URL real. Publicação controlada de sete recursos concluída, inventário passou de 59 para 66 sem alteração das definições anteriores; GUIDs e URL reconferidos na recoleta de A e leituras reais de B/D. Ver `docs/plano-homologacao-equipamentos.md` e relatórios relacionados. Não repetir publicação do pacote sem reconciliar identidades remotas.
- [x] 4.3 Testar CRUD, rejeição sem escrita, bloqueio com OS e ausência sem dependências com fixtures autorizadas; conferir persistência e não cascata. Caminho positivo final aprovado em lote autorizado: Equipamento novo 5 criado/excluído, GET 404 exato, Equipamentos 1–4, OS 1/2 e Clientes preservados. Contador 626; ver `docs/equipamento-exclusao-livre-resultado-20261121.md`. Demais cenários reaproveitados dos relatórios aprovados; sem atribuir prova concorrente ou liberar flags.

Preparação de 20/11, contador 611: somente o cenário positivo sem OS está
preparado para execução, até 15 chamadas (611–626), sete testes locais aprovados.
Baselines protegidos e onze definições conferidos localmente. Fixture nova
vinculada ao Cliente 16, criação/exclusão ainda pendentes de autorização; não
repetir bloqueio com OS ou D/E/F. Ver
`docs/equipamento-exclusao-livre-preparacao-20261120.md`.

Atualização após Grupo E de OS: bloqueio com OS e não cascata comprovados por
HTTP 400 e leituras de persistência das duas OS e quatro Equipamentos. Contador
global 203. A ressalva temporal do Grupo F de Equipamentos foi aceita pelo
responsável; não repetir seus testes. 4.3 permanece aberta somente para o alcance
ainda sem evidência, incluindo exclusão bem-sucedida sem dependências; não
reinterpretar os relatos históricos abaixo como nova pendência de auditoria.

Evidências parciais de 2026-11-18: B e C aprovaram leitura permitida/negada;
D aprovou cadastro e edição da fixture 3, cinco rejeições e preservação dos
dois Equipamentos preexistentes. E aprovou as nove negações de escrita e
preservação de persistência. F executou 24 chamadas, confirmou integração
Streamlit por AppTest, cadastro da fixture 4, edição de 3 e preservação de 1/2
e OS; interrompido no critério de auditoria (delta 11 contra +1, sem atribuição
comprovada de eventos). Acumulado 101, sem repetição. Auditoria, DELETE/bloqueio
por OS e fechamento continuam pendentes; 4.3 permanece aberta. Conferência
adicional de auditoria: dois GETs HTTP 200, acumulado 103, onze eventos com
identidade/ações esperadas; correlação estrita de horários não comprovada.
Ver `docs/conferencia-auditoria-equipamentos-grupo-f.md` e os
relatórios D/E/F e `docs/plano-homologacao-equipamentos-grupo-f.md`.
- [ ] 4.4 Revisar os contratos publicados e as evidências integradas para encerramento; nenhuma tarefa remota pode ser encerrada com mocks. Somente após esse critério, executar o procedimento Archive do OpenSpec.

## 5. Adequação aprovada para integração autenticada (2026-11-16)

Habilitação local autorizada em 21/11/2026: launcher define a flag de exclusão
de Equipamentos somente quando ausente, após evidência de backend em 626.
Valor externo false prevalece. Testes direcionados e resultado registrados em
docs/equipamentos-ui-habilitacao-20261121.md. Contador 631; sem HTTP ou exclusão
real nesta etapa. Não encerra 4.4, não arquiva e não libera DELETEs de OS/Técnicos.

- [x] 5.1 Revisar proposta, design e spec para perfis funcionais, dependência atual de OS e limites de publicação.
- [x] 5.2 Proteger os cinco endpoints com auth Xano e guard colaborador antes do acesso a dados de negócio; validar sintaxe. Parser oficial: seis arquivos válidos, sem avisos; não comprova execução remota.
- [x] 5.3 Encaminhar Bearer da sessão em todo o CRUD e confirmações; tratar 401/403 sem perder recuperação de incerteza. Verificação local: 32 testes específicos aprovados.
- [x] 5.4 Verificar regressão local de CRUD/exclusão e contratos de autenticação; preparar seleção revisável para publicação. Suíte completa: 144 testes aprovados, 32 específicos; OpenSpec estrito válido, sete definições aprovadas pelo parser, pacote de sete arquivos com hashes conferidos em `deployment/xano-149143-v1-equipamentos/`. Inventário/preview/publicação remotos permanecem pendentes nas tarefas 4.1–4.4.
