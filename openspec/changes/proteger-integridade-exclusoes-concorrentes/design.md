# Design

## Context

Ver proposal.md. Em 19/11, uma GET autorizada confirmou as 81 definições
preservadas e os quatro candidatos ausentes; contador 375. As fontes de
POST/PUT de OS validam Técnico antes da escrita, sem transação/lock explícitos.
POST/PUT de Serviços fazem o mesmo para OS. O provisionador já usa transação,
locks de user em ordem crescente e índices únicos, mas lê Técnico sem lock.
Os dois DELETEs locais consultam dependências e depois removem, sem coordenação.

Há sintaxe local existente de db.transaction e db.get com lock=true no
provisionador. Isso sustenta uma proposta compatível com o projeto, mas não
comprova semântica real de isolamento, duração dos locks ou consultas auxiliares.
Design necessário por envolver integridade e cinco escritores já publicados.

## Goals / Non-Goals

**Goals:** serializar decisões de vínculo/exclusão nas mesmas linhas pai;
manter contratos e reduzir alterações aos cinco escritores e aos DELETEs novos.

**Non-Goals:** alterar schema, SQL direto, tabelas de mutex, novas bibliotecas,
novas entidades, serialização global, mudanças de UI/painel ou ampliar controle
de concorrência para Cliente–Equipamento e Equipamento–OS. Não se declara que
esses relacionamentos anteriores receberam garantia nova por esta Change.
Não permitir testes concorrentes destrutivos em Live nem editar seus dados.

## Decisions

### Uma proteção cooperativa por registro pai

Dentro de transação de dados, bloquear Técnico antes de validar/gravar OS ou
user_tecnico; bloquear OS antes de validar/gravar Serviço. DELETE bloqueia o
mesmo pai antes da consulta de dependências e mantém a proteção até remover
ou abortar. O caminho completo deve ser coberto: proteger só DELETE ou só
writers deixa a corrida aberta. Mover consultas decisórias para depois do lock;
pré-leituras não bloqueantes só podem fornecer candidatos a reler.

Se vinculação vence e confirma, DELETE deve observar dependência e bloquear.
Se DELETE vence e confirma, escritor deve observar pai ausente e rejeitar sem
efeito parcial. Se uma tentativa aborta, o outro caminho decide pelo estado
confirmado, sem reenvio automático. As consultas do helper executado dentro
da transação precisam participar da mesma unidade e observar commits após espera.

Alternativas: pré-consulta isolada não fecha a janela; transação sem proteção
compartilhada também não basta. Foreign keys restritivas seriam outra barreira,
mas sua existência não foi comprovada e alterar schema está fora desta proposta.
Mutex global/tabela nova adicionaria escopo e contenção desnecessários.

### Ordem de locks e atualização do alvo

Ordem global proposta para os registros realmente bloqueados:
user (IDs crescentes) → Técnico → OS → Serviço. Se um caminho precisar de vários
registros da mesma tabela, ordenar IDs antes de bloquear. Não introduzir um
lock inverso em helper ou guard. Autorização administrativa permanece antes
de acesso a dados de negócio; os locks de user do provisionador são preservados.

| Caminho | Proteção e releitura propostas |
| --- | --- |
| POST OS | Técnico destino; validar referências após adquirir proteção; gravar na mesma transação |
| PUT OS | Técnico destino, depois OS alvo; reler alvo após lock e rejeitar ausência antes de editar |
| POST Serviço | OS destino; validar e inserir na mesma transação |
| PUT Serviço | OS destino, depois Serviço alvo; reler alvo e destino sob proteção antes de editar |
| Provisionamento | Manter users em ordem crescente; adicionar lock do Técnico destino antes de decisões/escritas de perfil, vínculo e auditoria |
| DELETE Técnico | Técnico alvo; consultar OS e user_tecnico após adquirir lock; só remover se ambos ausentes |
| DELETE OS | OS alvo; consultar Serviços após adquirir lock; só remover se ausentes |

Transferências por PUT devem proteger o novo pai. Não é necessário bloquear o
pai antigo para impedir órfão nesse relacionamento: antes do commit existe a
referência anterior e depois existe a nova. A comprovação deve incluir esse
caso e a visibilidade de dependências após espera. Se runtime exigir proteção
adicional do pai antigo, interromper e revisar ordem/escopo antes de aplicar.
Bloqueio do alvo no PUT impede que uma leitura antiga seja seguida de edição
de registro já excluído. Não transformar db.edit em upsert nem usar fallback.

Helpers de validação e dependência existentes não ganham locks por padrão:
os chamadores delimitam a transação e adquirem os locks explicitamente.
Preservar mensagens, campos, enumerações, checks de identidade e guards.
Nenhum catch genérico de banco e nenhum HTTP 409 inventado antes de conhecer
o erro real; timeout/erro operacional não pode virar sucesso ou retry.

### Condições de comprovação, não perguntas adiáveis

Antes de liberar, evidenciar que lock=true bloqueia operações concorrentes
pertinentes até commit/rollback; que quem aguarda relê existência/dependências
confirmadas; que function.run não sai da transação; e que erro de persistência
ou auditoria desfaz todas as escritas. São critérios impeditivos, não garantias
derivadas de parser ou do exemplo existente. Se o runtime não os sustentar,
parar e propor alternativa; não adicionar SQL/schema silenciosamente.

Testes locais: modelo de intercalação para as duas ordens, commit/abort,
transferências, alvo apagado e ausência de retry; verificações das fontes,
parser oficial e regressões direcionadas dos cinco contratos. Modelo que
implementa locks ideais só verifica o desenho, não o banco real.

Comprovação real: roteiro autorizado em ambiente isolado compatível com Xano,
com barreiras/observação para demonstrar sobreposição e espera; requests apenas
disparados juntos não provam qual corrida ocorreu. Não criar instrumentação
ou ambiente remoto nesta etapa. Evidência técnica deve registrar versão,
isolamento, transações e estado final. Se ambiente não existir, manter pendência
explícita; não executar por conveniência em v1 Live.

## Risks / Trade-offs

- Locks cooperativos não cobrem escrita manual/importações → delimitar cobertura
  às APIs e exigir avaliação adicional se outros escritores forem habilitados.
- Snapshot anterior à espera pode ignorar novo vínculo → exigir leitura atual
  e prova das duas ordens de execução antes da liberação.
- Inversão de locks pode causar deadlock → revisão da ordem global e falha
  sem retry, inclusive nos caminhos do provisionador já existentes.
- Mudança em recurso homologado → atualizar somente cinco endpoints e executar
  regressão local afetada; evidências antigas continuam históricas e intactas.
- Fixture de identidade ausente → plano e autorização separados; não alterar
  vínculos dos usuários atuais nem concluir cenário só com simulação.

## Migration Plan

1. Após nova autorização, implementar localmente transações/locks nos cinco
   escritores e nos DELETEs candidatos; helpers/contratos sem ampliação.
2. Parser, testes locais e pacote novo com hashes. Manter pacotes/recibos
   anteriores como histórico; não sobrescrever o pacote aditivo aprovado.
3. Fechar evidência técnica e roteiro isolado/orçamento sob autorizações próprias.
   Runtime não comprovado bloqueia liberação dos DELETEs.
4. Novo inventário/preview autorizado e seletivo. Lote escritores: 0 CREATE,
   5 UPDATE, 0 DELETE; lote exclusões: 4 CREATE, 0 UPDATE, 0 DELETE, condicionado
   à ausência. Se um lote conjunto for escolhido, exigir 4 CREATE/5 UPDATE/0
   DELETE e aprovação expressa dessa seleção; não herdar aprovação antiga.
5. Publicar escritores protegidos antes de disponibilizar os DELETEs. Não
   admitir janela com DELETE novo e escritor antigo; conferir cada lote antes
   de avançar. Não confundir transaction da publicação com transação de dados.
6. Homologar somente cenários novos/afetados com fixtures autorizadas e baseline;
   não repetir OS B–F, Equipamentos F ou CRUD completo já aceito de Serviços.
7. Falha interrompe sem limpeza automática. Reversão de escritores enquanto
   DELETEs estão disponíveis reabre a corrida: propor desativação/reversão
   coordenada e obter autorização, sem executar rollback remoto automático.

Artefatos somente nesta etapa; nenhuma execução, pacote novo, coleta ou Git.

## Revisão: validação gratuita com somente a fonte live

### Restrição confirmada pelo responsável em 20/11

Plano Free, somente fonte `live`; inclusão de fonte de testes exige upgrade na
interface observada. Contador atual 377. Não houve verificação remota adicional
nesta revisão. Branch de código não comprova isolamento dos dados; não criar ou
publicar candidatos em Live sob a suposição de que fixtures novas bastam para
isolar transações, falhas ou efeitos em escritores compartilhados.

### Estratégia em duas camadas e critérios de evidência

| Atividade | Pode continuar localmente, após autorização própria | O que permanece dependente do Xano |
| --- | --- | --- |
| Concorrência Técnico–OS, Técnico–identidade e OS–Serviço | Revisar modelo e cobertura já existentes; planejar lacunas nas duas ordens, PUT, commit/abort e ausência após espera; não repetir 76 testes sem alteração ou lacuna identificada | Aquisição/duração real de lock, bloqueio observável, leitura após espera e participação de function.run na transação |
| Atomicidade e auditoria | Injetar falhas apenas em mocks/modelo e verificar ausência de retry/compensação; confrontar fonte e contrato | Rollback real de todas as escritas após falha de persistência/auditoria; simulação não comprova banco |
| Contratos e preservação | Conferir guards, payloads, respostas, ordem de locks, allowlists e hashes com fontes/baselines locais preservados | Estado remoto atual, compilação/execução real dos candidatos e ausência de regressões no backend após eventual publicação |
| Ensaios de exclusões | Preparar executor offline e fixtures sintéticas identificadas como simuladas, contador, casos negativos, confirmação e incerteza | Exclusão real permitida/bloqueada, preservação e concorrência; não executar nem liberar DELETEs agora |
| Demais pendências do MVP | Reconciliar evidências locais de Técnicos, mapear cenários ausentes de Clientes/acesso e seus payloads/orçamentos; ensaiar interface com mocks sem repetir homologações aceitas | Resultado real de login/perfis, validações, normalização e persistência de casos ainda não homologados |

Reutilizar testes, fontes e recibos existentes, sem sobrescrever evidências ou
marcar cenários novos como aprovados por associação. Primeiro produzir uma matriz
requisito → evidência existente → lacuna → teste proposto → limite. Só executar
novos testes locais quando a lacuna justificar; sockets externos bloqueados.
Fixtures locais devem permanecer sintéticas, sem cópia de dados/credenciais reais.

Orçamento de qualquer ensaio offline parte de 377 apenas como referência; mocks
não incrementam o contador remoto. Contabilizar explicitamente eventual login,
auth/me, metadados, preservação e limpeza em proposta futura; nenhum valor
simulado ou ID protegido deve virar alvo remoto automaticamente.

### Tratamento das pendências runtime sem contratação

Não existe nesta revisão um ambiente gratuito isolado comprovado. Se algum
ambiente alternativo gratuito vier a ser oferecido pelo responsável, avaliar
primeiro sua disponibilidade, isolamento e compatibilidade; sem presumir clone,
trial, plano ou acesso. Descoberta/criação/instrumentação exigem autorização
separada, e a prova só vale para o runtime e configuração efetivamente observados.

Na ausência dessa condição, manter 4.1 e a liberação subsequente bloqueadas.
Uma eventual homologação sequencial futura em Live, com autorização e fixtures
novas, pode comprovar apenas contratos específicos; não substitui a prova de
concorrência/rollback, não autoriza induzir falhas, nem habilita DELETEs.

Não propor restauração automática de dados como segurança de teste destrutivo.
Não contratar upgrade, alterar backend, criar novas entidades ou substituir
Xano por banco local. O modelo local continua instrumento de verificação.

### Sequência até a meta de 22/11 às 18h

1. Após autorização, consolidar matriz de lacunas, inventário de evidências e
   plano offline; continuar apenas trabalho independente do runtime.
2. Ensaiar localmente lacunas prioritárias de contratos, estados incertos,
   autorização e preservação; entregar hashes e orçamento por lote proposto.
3. No marco de 21/11 às 18h, apresentar o que foi comprovado e o bloqueio runtime
   remanescente. Prazo não autoriza diminuir critérios ou liberar flags.
4. Se não houver prova suficiente até a entrega, apresentar explicitamente ao
   responsável a decisão sobre entrega demonstrável com restrições. Só ele pode
   aceitar entrega parcial; isso não equivale a MVP completo nem conclui estas
   Changes. Sync/Archive permanecem etapas separadas.

Esta revisão não executa os passos acima. Tarefas e provas históricas continuam
preservadas; código local candidato já existente não recebe status de publicado.

## Matriz consolidada e roteiro offline — 20/11, contador 377

Tarefa 5.1 concluída por análise das fontes de testes, recibos e relatórios locais.
Nenhuma suíte foi executada novamente. Os 76 testes/parser são resultados
históricos, não resultados produzidos nesta preparação. A revisão visual posterior
possui 190 testes registrados e aceite próprio; não somar totais sobrepostos.

### Evidência existente, lacunas e decisão por requisito

| Prioridade / requisito | Evidência local reutilizada | Lacuna efetiva | Ensaio local necessário / decisão | Limite runtime |
| --- | --- | --- | --- | --- |
| P0: duas ordens de disputa nos três vínculos | `frontend/tests/test_integridade_concorrente.py`: `test_vinculacao_primeiro_forca_espera_e_bloqueia_delete`, `test_delete_primeiro_rejeita_vinculacao_sem_efeitos`; modelo percorre os três tipos de vínculo | Não há prova observada de espera/commit no Xano | Nenhum novo teste equivalente identificado; preservar modelo e prova negativa sem lock | Duração real de lock, isolamento e visibilidade após espera continuam impeditivos |
| P0: abort, falha de auditoria/helper e PUT | Mesmo arquivo: testes `test_abort_writer_libera_delete_e_nao_vaza_perfil_auditoria`, `test_abort_delete_permite_writer_e_libera_locks`, `test_transferencias_put_em_ambas_ordens`, `test_put_alvo_removido_nao_recria`, `test_falha_de_auditoria_ou_helper_aborta_sem_retry` | Atomicidade real e transação de function.run não demonstradas | Não repetir simulação para tentar preencher lacuna do servidor | Rollback e participação real do helper exigem runtime apropriado |
| P0: guards, ordem de locks e contratos candidatos | Quatro FontesTests no mesmo arquivo; seis testes de `test_etapa06.py`; BASELINE e pacote local | Estado remoto do candidato não homologado; fonte não comprova banco | Verificação estática já existente; repetir somente após alteração das fontes | Não publicar escritores/DELETEs sob esta preparação |
| P1: escrita incerta, rerun e troca de alvo | Dez testes de `test_exclusoes_tecnicos_os.py`; `test_tecnicos.py` e `test_autorizacao_clientes.py` | Fluxos simulados não encerram as homologações reais pendentes | Não criar teste duplicado de timeout/negação; executar subset somente se futuro executor/interface for alterado | HTTP real, autorização e persistência pendentes nos respectivos lotes |
| P1: validação e normalização de Clientes | `docs/plano-validacao-backend-clientes.md`; 18 testes de `test_fluxos_clientes.py`; oito de autorização; ensaio auth/escrita já existente em `test_homologacao_clientes_escrita.py` | Plano de 23 mutações por POST/PUT ainda sem executor específico congelado e sem prova backend; ensaio de auth não equivale à validação de entradas | Preparar casos determinísticos, orçamento e transporte falso conforme roteiro C abaixo; testar seu próprio controle de preservação/parada, sem simular aprovação do XanoScript | Rejeição sem persistência, normalização e preservação dos zeros à esquerda precisam de respostas reais futuras |
| P1: retomada da gestão de Técnicos | `docs/homologacao-etapa07-grupo-b.md`: cinco GET 200 e login 403; A aprovado; `test_tecnicos.py` contém 15 casos locais | Causa do 403 não determinada; auth/me, fixture e B–F não concluídos | Reconciliar somente campos sanitizados de evidências existentes, sem abrir credenciais; propor leitura mínima se ainda inconclusivo; roteiro T abaixo | Auditoria posterior e estado/identidade atuais exigem leitura remota autorizada; não repetir login por tentativa |
| P1: acesso técnico e provisionamento | `acesso-tecnico-ordens-servico/tasks.md`, Grupos 1–4 e cenários OS já aceitos; `test_etapa06.py` | Vínculo inválido, expiração, erros UNIQUE reais, rollback e revisão de signup têm alcances ainda abertos | Mapear cada requisito sem reexecutar perfis/status já aceitos; separar revisão de signup de qualquer correção | Expiração e erros de banco reais não são provados por mocks; não fabricar falha em Live |
| P2: integridade de seleção e UI | Três testes de `test_pacote_integridade.py`, recibo da implementação; integração visual aceita | Não existe preview remoto atual dos candidatos nem liberação | Hashes/allowlist podem ser reconferidos localmente quando o lote for preparado; sem necessidade de rever o visual aceito | Preview/preservação remotos e aceite de liberação são etapas distintas |

Referência do conjunto de 76: `docs/implementacao-integridade-exclusoes-20261119.md`
e `docs/evidencias/integridade-exclusoes-implementacao-local-20261119.json`.
Não converter contagens de métodos em garantias adicionais ou somar subtests
como novas homologações. Não foi identificada lacuna local nova na modelagem de
concorrência que justificasse reexecutar os mesmos testes nesta etapa.

### Roteiro C — preparação do ensaio específico de validação de Clientes

Somente planejamento. Execução e eventual ferramenta de teste ficam pendentes.

1. Usar exclusivamente endpoint fictício `.invalid`, credenciais sintéticas e
   transporte em memória. Bloquear DNS/socket externos antes de importar ou
   executar qualquer transporte; não ler configuração, credenciais ou DPAPI reais.
2. Gerar os 23 casos do plano original para POST e PUT, cada um alterando apenas
   o campo previsto. Cada caso deve ter método, payload sintético, expectativa,
   verificação de persistência e política de interrupção explícitos. Não decidir
   mensagem/código exato desconhecido por hipótese; conferir fontes locais antes
   de congelar a expectativa e deixar divergências documentadas.
3. Representar baseline sintético protegido e fixture recém-criada com ID derivado
   de resposta simulada, não fixado para futura execução remota. Não transportar
   IDs simulados para Live. PUT/DELETE sobre baseline ou rota fora da allowlist
   devem falhar antes do transporte.
4. Fluxo nominal proposto: login + auth/me (2), baseline (1), POST fixture + GET
   (2), 23 POST negativos + 23 conferências (46), 23 PUT negativos + 23 conferências
   (46), duas normalizações + GETs (4), DELETE fixture + GET ausência (2), listagem
   final (1): **104 requisições simuladas**, correspondentes a 50 tentativas de
   escrita, 52 GETs e duas chamadas de autenticação.
5. Negativos do executor: POST inválido indevidamente aceito, PUT altera registro
   protegido, confirmação GET falha, timeout após escrita, resposta paginada não
   prevista, identidade/perfil divergente, ID da fixture pertencente ao baseline,
   401/403/429 e redirecionamento. Cada caso deve parar no ponto da divergência,
   sem retry, limpeza, restauração automática ou escrita seguinte. Não exigir
   104 passos quando o próprio cenário exige parada antecipada.
6. O servidor falso verifica o executor e seus guardrails; não implementar uma
   réplica de CPF/email para alegar validação do backend. Campos normalizados
   esperados vêm de exemplos definidos, sem supor que o servidor real os produzirá.
7. Relatório deve separar chamadas simuladas do contador real **377**. Se um lote
   remoto idêntico fosse futuramente aprovado a partir desse contador, o teto
   condicional seria **481**; não é orçamento autorizado. Paginação, expiração,
   ausência de evidência de dependências para limpeza ou chamadas extras exigem
   revisão antes da execução, sem expansão silenciosa do teto.

### Roteiro T — reconciliação e preparação de Técnicos

Não repetir login nem assumir senha incorreta. Preservar o registro do 403 e
as seis chamadas do B interrompido. O histórico E07 permanece 15/137, saldo
nominal 122. C 26 + D 45 + E 40 + F 8 = 119 deixa apenas três chamadas, insuficientes
para a retomada completa de B e reconciliações. Reapresentar orçamento antes de
qualquer execução; não somar tetos antigos como se já aprovados novamente.

Revisar localmente somente existência/hash e campos sanitizados disponíveis de
journal/stopped; não abrir tokens ou senhas. Evidências posteriores de login de
outros fluxos não comprovam a causa do 403 nem o estado atual de Técnicos. Se
faltarem dados, apresentar uma proposta mínima de leitura, sem executá-la.

O ensaio subsequente deve usar três identidades inteiramente sintéticas e simular
login negado, identidade inesperada, listagem falha e PUT incerto sem reenvio.
Esses comportamentos já têm cobertura local; novos testes só se justificam para
um executor novo/alterado, não para repetir a UI aprovada. B–F continuam pendentes
no runtime e a retomada não inclui DELETE de Técnico.

### Preservação, executor de concorrência e ordem de trabalho

A proposta de concorrência continua sem orçamento operacional congelável:
barreiras, ambiente e fixture de identidade não estão resolvidos. Não atribuir
104 chamadas de Clientes ou 54 do ensaio sequencial de exclusões a esse executor.
Modelo de intercalação, executor HTTP simulado e prova real são três evidências
distintas. 3.3 e 5.3 não são encerradas nesta preparação.

Próxima sequência local: (1) congelar casos e expectativas do roteiro C;
(2) após escopo autorizado, preparar executor/testes offline apenas de suas
lacunas; (3) reconciliar T sem credenciais e apresentar eventual leitura mínima;
(4) preparar revisão própria de signup e das pendências de acesso. Não executar
outro grupo remoto, não liberar DELETEs e não arquivar Changes por esta matriz.

Na preparação inicial, 5.2 estava aberta. Atualização de 20/11: ensaio específico
exclusivamente em memória implementado, 18 testes aprovados e 104 chamadas
simuladas nominais, com negativos sem retry/limpeza automática. Fontes e fixture
preservadas, contador remoto 377. Ver
`docs/clientes-validacao-ensaio-offline-20261120.md` e recibo correspondente.
O HTTP 422 é convenção do servidor falso, não comprovação de resposta Xano.
5.3 aberta: orçamento operacional concorrente depende de condições indisponíveis.
5.4 aberta: decisão no marco de 21/11 ainda não ocorreu. Preparação local pode
avançar sem prometer encerramento integral do MVP em 22/11 enquanto esse bloqueio
runtime persistir.
