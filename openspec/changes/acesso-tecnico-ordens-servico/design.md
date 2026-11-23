# Design: Acesso do técnico e ordens atribuídas

## Auditoria de signup — decisão local de 21/11/2026

Substituir o objeto de usuário irrestrito somente no metadata de auth/signup
por id, created_at, name, email, account_id e role. A lista mantém consistência
com a auditoria de login e permite identificar o cadastro sem senha ou dados de
recuperação. Campos futuros não entram implicitamente. Não alterar helper,
criação, validações, validade do token, resposta, GUID ou perfil funcional.
Pacote novo xano-149143-v1-signup-audit-fix; seleção restrita a 01-signup-audit,
baseline fora da seleção. Preview local é expectativa, não resultado remoto.
Publicação e criação de usuário para homologação dependem de autorização própria.
Evidência: docs/signup-auditoria-correcao-local-20261121.md. Contador 626.

## Correção local após a primeira listagem do Grupo D

O retorno de GET /minhas-ordens incluiu OS 1, mas tipo/marca vieram null apesar
de existirem no baseline do Equipamento 3. Remover join/eval dessa consulta:
após autorização e filtro por técnico, percorrer apenas as OS autorizadas,
ler o Equipamento pelo id_equipamento da OS e compor explicitamente os onze
campos existentes. Referência ausente interrompe com erro, sem lista parcial
ou valores inventados. Marca/modelo nulos continuam válidos. Nenhuma alteração
de domínio, perfil, vínculo ou rota de escrita.

A opção usa uma leitura adicional por OS, adequada ao volume acadêmico atual;
não comprova snapshot transacional nem desempenho em grandes listas. Parser
local e testes simulados não provam a correção em runtime. Preservar o pacote
de sete criações já aprovado e preparar eventual UPDATE isolado por GUID em
outro diretório. Contador permanece 148; publicação e retomada não autorizadas
por esta correção local.

## Recuperação do painel autorizada em 2026-11-18

Marcar a consulta inicial como tentada antes do HTTP. Após erro, preservar aviso
e exigir atualização explícita. Lista nula não significa lista vazia confirmada.
Refresh invalida dados e renova chaves de status; PATCH incerto ou rejeitado
invalida o cache, sem repetição ou consulta automática. Sessão expirada continua
usando o encerramento comum. Não alterar endpoints ou perfis neste ajuste.

## Atualização de evidências (2026-11-13)

As etapas 01–06 estão publicadas e os Grupos 1–4 da etapa 06 foram concluídos em
`149143/v1`; as etapas 07–09 continuam sem endpoints de negócio publicados.
Os resultados e o plano de continuidade estão em
[progresso-mvp.md](../../../docs/progresso-mvp.md). Os relatos de inventários,
previews cancelados e preparação local abaixo são históricos: não representam o
estado atual nem autorização de execução.

A arquitetura vigente preserva `user.role=admin/member`, usa
`user_application_profile` e `user_tecnico`, e não altera as cinco entidades.
Os testes sequenciais não comprovam concorrência, rollback por falha DB ou
mapeamento de conflitos UNIQUE. Integração real de OS e do portal segue pendente.

## Correção isolada da auditoria de login (2026-11-12)

O Grupo 2 aprovado encontrou o campo de senha protegido em dois logs normais
de login. `auth/login` seleciona esse campo para `security.check_password` e
depois encaminha o objeto inteiro ao helper de auditoria. A correção autorizada
substitui somente o valor de `metadata` por um objeto explícito com `id`,
`created_at`, `name`, `email`, `account_id` e `role`. Preserva GUID, consulta,
validações, emissão/validade do token e resposta. Não modificar o helper
compartilhado, `auth/me` ou o provisionador da etapa 06.

Pacote isolado: `deployment/xano-149143-v1-login-audit-fix/01-login-audit`.
Seu preview deve mostrar exclusivamente UPDATE `auth/login POST`, GUID
`g6E8E2wr8FPWccUg-4Qqxu2csFg`, e aguardar confirmação do usuário. Não inclui
limpeza de logs antigos, execução de login ou avanço para o Grupo 3.

Pendência separada: `auth/signup` também envia `$user` inteiro ao log. Revisar
após autorização própria, sem alterar agora o contrato do signup ou seus logs.

## Estado consolidado da etapa 06 (2026-11-12)

Esta seção substitui descrições históricas abaixo sobre leituras fora da
transação, log posterior ao commit e sintaxe desconhecida. As etapas 03–05
foram publicadas e verificadas; 06–09 continuam sem publicação.

O provisionador executa todas as leituras na transação e bloqueia as linhas
de `user` do operador e alvo por ID crescente, sem editar seu conteúdo.
`db.get` aceita `lock = true` no parser oficial 12.28.0; Get Record documenta
seu uso transacional. As duas branches adotam a mesma ordem global, inclusive
sem perfil/vínculo inicial. Só depois dos locks lê os perfis/vínculos e valida
autoridade, conta e referências, antes das gravações. O sinalizador exige
`=== true`. As branches mutuamente exclusivas usam `elseif`.

A auditoria passa a `db.add event_log` explícito na transação, depois de perfil
e vínculo. Isso evita depender da propagação de transações através de funções
e de erro de log posterior ao commit. Rollback em falha DB deve ser validado
no Xano; não presumir rollback universal de erros não DB.

Não implementar catch, SQLSTATE ou HTTP conflito presumidos. Identificar em
homologação os erros/constraints dos três índices UNIQUE das tabelas técnicas;
outros erros devem propagar. Locks entre usuários distintos não substituem a
unicidade de `id_tecnico`. Escritores administrativos externos precisam
respeitar o protocolo; locks em `user` não serializam escritas diretas em
outras tabelas por mecanismos independentes.

`auth/me` preserva sua definição local e resposta aditiva, sem expor autoridade.
Chama o helper de log e não é teste sem escrita. Suas leituras de perfil/vínculo
não são snapshot conjunto e podem negar transitoriamente durante mudanças
concorrentes. Compatibilidade real e bootstrap permanecem pendentes.

Referências e matriz de validação:
[revisao-etapa06.md](../../../docs/revisao-etapa06.md). Testes de contratos/mock
e parser local não comprovam runtime, isolamento ou rollback. Tarefas 5.4,
5.6 e 5.7 permanecem abertas. Não executar preview nem testes remotos nesta revisão.

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

## Context

O modelo global contém cinco entidades: Cliente, Técnico, Equipamento, Ordem de Serviço e Serviço. Uma OS possui `id_tecnico`, `id_equipamento`, `problema_relatado` e `status`; Técnico possui `id_tecnico`. Esse relacionamento já permite selecionar as ordens de um técnico sem novo relacionamento de negócio.

As especificações disponíveis antes desta Change concentram-se em clientes. O inventário remoto somente leitura confirmou que autenticação nativa existe, mas os recursos de Técnico e Ordem de Serviço necessários ao painel ainda não existem na branch consultada. A aplicação Streamlit também não possui integração de autenticação.

### Evidências do inventário remoto

Consulta realizada após autorização do responsável, no workspace `149143`, branch `v1` (marcada como live). `xano branch list` confirmou a branch; `xano workspace pull` baixou 44 definições para `diretorio-local-do-projeto`. O pull não incluiu registros, variáveis de ambiente ou rascunhos. A inspeção foi limitada às definições baixadas; nenhum dado pessoal foi consultado.

- Tabelas presentes no inventário: `user`, `account`, `event_log`, `agent_conversation`, `agent_message`, `cliente` e `equipamento`.
- `user` é tabela de autenticação e contém `id`, `name`, `email`, `password`, `account_id` e enum `role` com `admin` e `member`, além de campos de recuperação de senha. `account_id` referencia `account`. Não existe associação `id_tecnico`.
- A API `Authentication` contém `POST auth/login` (email/senha, emissão de token com validade declarada de 86400 segundos), `GET auth/me` protegido e `POST auth/signup` não protegido que cria papel `member`. Há também endpoints de redefinição de senha.
- A API `Members & Accounts` contém rotas autenticadas de conta/perfil e alteração de papel; o exemplo RBAC existente usa hierarquia `admin`/`member` e não representa permissões colaborador/técnico.
- `equipamento` contém `id`, `tipo`, `marca`, `modelo`, `numero_serie` e `id_cliente`, que referencia `cliente`. Não há grupo/API de Equipamentos no inventário publicado.
- Não existem tabelas `tecnico`, `ordem_servico` ou `servico`, nem APIs de Técnico ou Ordem de Serviço. Portanto, não há vínculos físicos a verificar entre Técnico, OS e Equipamento.
- O projeto Streamlit declara `streamlit` e `requests`, sem biblioteca ou cliente de autenticação; os módulos existentes não implementam login nem Bearer token.

## Goals / Non-Goals

**Goals:** login real para colaborador e técnico; autorização efetiva no backend; identidade técnica vinculada ao cadastro de Técnico existente; colaborador com acesso às operações gerais existentes; painel com equipamento, problema relatado e status; atualização de status restrita a OS atribuídas.

**Non-Goals:** alterar o domínio de cinco entidades; adicionar tabela de negócio de usuários; implementar cadastro público, recuperação/gestão de senha ou novos estados de OS; publicar ou sincronizar recursos no Xano nesta etapa documental.

## Decisions

### Autenticação e identidades

Reutilizar como ponto de partida a autenticação nativa observada na branch: `user` e `auth/login`, com token validado por endpoints protegidos. A presença dessas definições não comprova que o Streamlit já esteja integrado nem que os papéis necessários existam. Não usar `st.session_state` como prova de identidade, credenciais hardcoded, usuário de demonstração nem resposta simulada como autenticação real.

O perfil `admin`/`member` existente não equivale automaticamente aos perfis `colaborador`/`técnico`. Adotar papéis de aplicação explícitos e verificações por perfil no backend; não usar somente a hierarquia genérica existente, pois as permissões do técnico são um escopo restrito, não apenas um nível inferior de acesso geral. Manter eventual papel `admin` para administração de contas claramente separado das permissões de colaborador.

**Decisão de implementação do MVP aprovada pelo responsável, não uma exigência original do professor:** os identificadores exatos dos perfis funcionais serão `colaborador` e `tecnico`. O perfil `colaborador` gerencia os cadastros de Técnicos e, quando implementadas, as operações gerais de OS. O perfil `tecnico` consulta e atualiza somente as OS atribuídas ao cadastro associado. Não mapear `admin` ou `member` para esses perfis. O provisionamento funcional será uma operação interna protegida, separada do signup público e do papel administrativo de conta `admin/member`.

A identidade de acesso é infraestrutura técnica, distinta das entidades de negócio. Depois que [adicionar-gestao-tecnicos](../adicionar-gestao-tecnicos/design.md) criar o cadastro Técnico, a opção preferencial é associar a identidade de `user` ao `id_tecnico` existente por vínculo persistente no backend, validado e único. Não associar por email nem confiar em `id_tecnico` vindo do frontend. Não criar tabela de negócio de usuário. Qualquer estrutura técnica adicional além do próprio vínculo no usuário requer justificativa e decisão antes da implementação.

O provisionamento deve ser administrativo e fora do signup público. O endpoint atual `auth/signup` permite criação sem autenticação e atribui `member`; a definição local mantém esse comportamento, sem aceitar campos de perfil funcional ou `id_tecnico`. A operação protegida de provisionamento funcional é separada e só pode ser usada por admin autorizado para usuários da mesma conta.

### Permissões

O backend é a autoridade para perfil, associação e escopo de dados em cada endpoint. O perfil colaborador pode realizar operações gerais de gerenciamento já existentes no sistema; o perfil técnico fica restrito a consulta e mudança de status das próprias ordens. Não confiar em `id_tecnico` enviado pelo cliente: derivar a associação da identidade autenticada. Aplicar a mesma regra em consulta individual, listagem e alteração para evitar acesso por ID direto.

### Consulta e atualização das ordens

A consulta depende de uma futura tabela/API de OS com `id_tecnico`, `id_equipamento`, `problema_relatado` e `status`, e da leitura autorizada dos campos necessários de Equipamento. Nenhuma dessas APIs de negócio existe no inventário atual. Criar uma Change de Ordem de Serviço antes de implementar a área do painel. Expor apenas campos necessários: identificação da OS, equipamento, problema relatado e status; outros dados pessoais de Cliente não são necessários ao requisito e não devem ser incluídos por padrão.

A atualização de status deve validar no backend os cinco estados já documentados: Aguardando avaliação, Em manutenção, Aguardando peça, Concluído e Entregue. A Change não decide uma máquina de transições, pois não há regra aprovada de transição além da lista de estados. Qualquer restrição adicional de transição exige requisito definido antes da implementação. Após gravar, retornar o estado persistido para confirmação da interface.

### Frontend

Implementar a experiência exclusivamente em Streamlit/Python, reutilizando a integração HTTP existente quando apropriado. A UI oculta ações fora do perfil para clareza, mas toda operação continua protegida por autorização no Xano. Tokens não devem ser versionados nem exibidos em logs; configuração segue mecanismo externo já adotado pelo projeto, a ser confirmado durante implementação.

## Risks / Trade-offs

### Implementação local e incompatibilidades verificadas

A implementação Streamlit usa `POST /auth/login` (`authToken`, `user_id`) e
`GET /auth/me` (identidade, perfil e associação técnica). O XanoScript local de
`auth/me` foi estendido para selecionar e devolver `id_tecnico` já previsto na
definição local de `user`. O inventário remoto citado acima não tinha esse campo
nem os perfis funcionais; portanto, o contrato local ainda não está disponível
na branch publicada. O token expira após 86400 segundos no endpoint de login
existente e não há endpoint de logout/revogação no inventário: o logout local
descarta o token da sessão Streamlit, sem afirmar revogação do token emitido.

A resposta local de `GET /minhas-ordens` tem `id_equipamento`, mas não marca nem
modelo. O painel compõe esses campos por `GET /equipamentos/{id}` para cada ID
retornado pela lista autenticada. O grupo local de Equipamentos não requer token
e o inventário remoto não o encontrou publicado; uma futura integração precisa
proteger essa consulta para técnico atribuído ou devolver os dados necessários
da OS protegida. As APIs locais de Clientes e Equipamentos também não aplicam os
perfis funcionais; a navegação Streamlit as filtra apenas na interface. Essas
incompatibilidades ficam abertas e impedem considerar a autorização integrada.

- Autenticação nativa está comprovada; o inventário remoto não possui perfil funcional, vínculo com Técnico nem operação de provisionamento. A política local foi definida, mas depende de publicação e validação remota.
- Tabelas e APIs de Técnico e OS estão ausentes. O cadastro Técnico depende de [adicionar-gestao-tecnicos](../adicionar-gestao-tecnicos/proposal.md); o painel depende adicionalmente de uma Change para Ordem de Serviço e suas APIs.
- A associação da conta técnica deve ser provisionada corretamente. Associação ausente/inválida bloqueia acesso por padrão.
- Permissão apenas no Streamlit seria insuficiente; endpoint sem validação no backend não atende esta especificação.
- Sem regra de transição aprovada, esta Change valida pertencimento e estado permitido, sem presumir sequência de status.
- A cobertura do perfil colaborador depende das operações realmente existentes; mapear essas operações durante a descoberta e deixar funcionalidades futuras fora desta Change.

## Migration Plan

### Atualização local para preparação da integração

A implementação local atual da listagem do técnico resolve a identidade por
`$auth.id`, confirma o vínculo técnico antes da consulta e filtra as OS por
`id_tecnico`. A consulta usa junção à esquerda com `equipamento` e retorna tipo,
marca e modelo junto da OS. A interface Streamlit consome esses campos da
resposta autenticada e não chama o grupo público de Equipamentos. Isso elimina
a dependência local daquele endpoint para o painel, mas a autorização e a
sintaxe ainda precisam ser verificadas no Xano publicado.

O signup existente deve continuar atribuindo somente `member`; ele não deve
receber campos para papel funcional ou `id_tecnico`. Isso impede elevação direta
por parâmetros no signup, mas mantém criação pública de contas member. O
endpoint remoto de alteração de papel aceita texto livre e sua guarda genérica
de administrador por conta não comprova que somente um responsável do sistema
possa conceder perfis funcionais. A política de provisionamento e a guarda
desse endpoint precisam ser decididas antes de permitir novos perfis. Usuários
`admin`/`member` existentes permanecem com seus valores; nenhum mapeamento
automático será feito.

Na auditoria de preparação, a CLI `1.3.3` inicializou após definir `SHELL`
temporariamente no processo. A primeira consulta de branches falhou com
`fetch failed`; após leitura remota ampliada, `branch list` confirmou somente a
branch `v1`, marcada como live, e `workspace pull` baixou 44 definições para
pasta temporária, sem registros, variáveis de ambiente ou rascunhos. Não há
branch de teste listada. As permissões para criar branch ou publicar não são
expostas por essas operações de leitura e continuam desconhecidas; não presumir
que uma branch de teste possa ser criada. Não publicar alterações de autorização
diretamente na live sem confirmação de permissões, ambiente e aprovação.

Sequência recomendada: (1) baixar backup somente de definições e confirmar
branch/permissões; (2) revisar diferenças e preservar GUIDs e contratos; (3) em
branch isolada autorizada, aplicar alterações aditivas e validar schema,
funções e endpoints; (4) provisionar uma conta interna autorizada e testar
login, perfil, vínculo e OS própria/alheia; (5) validar clientes existentes,
signup e APIs de conta; (6) só então solicitar aprovação separada para
promover em live. Antes de cada passo, guardar inventário e versão anterior.
Rollback deve restaurar definições da versão revisada sem apagar tabelas nem
registros novos; qualquer rollback de dados/schema exige análise do uso após a
publicação. Se backup, branch isolada ou restauração não puderem ser verificados,
interromper antes da escrita em live.

Nenhuma migração ou publicação remota foi executada. A implementação local segue a dependência entre Técnico, Equipamento e Ordem de Serviço, e o rollout descrito acima continua condicionado à confirmação de ambiente isolado, provisionamento e aprovação específica.

### Decisão de provisionamento local (MVP)

Para não quebrar os contratos de conta existentes, `user.role` permanece com os valores `admin` e `member`. O perfil funcional é separado no campo privado `user.perfil_aplicacao` (`colaborador` ou `tecnico`); nenhum mapeamento automático entre os dois campos é permitido. `user.id_tecnico` permanece privado e opcional, com índice único para permitir múltiplas contas sem vínculo. O comportamento de múltiplos valores nulos no índice deve ser confirmado no Xano antes da publicação.

A definição local adiciona `POST /admin/user_application_profile` no grupo existente `Members & Accounts`. Requer token, papel legado `admin` e mesma `account_id` do alvo. Perfil `tecnico` exige `id_tecnico` existente e sem outro usuário associado; perfil `colaborador` rejeita `id_tecnico` e limpa vínculo anterior. O endpoint legado `admin/user_role` e o signup não são alterados: o primeiro continua gerenciando somente `role`, e o segundo continua criando `member` sem aceitar nem escrever `perfil_aplicacao`/`id_tecnico`. O Streamlit usa exclusivamente `auth/me.perfil_aplicacao` para decidir acesso funcional; `auth/me.role` é apenas metadado legado.

Estas são decisões de implementação local do MVP, não exigências originais do professor. Para distinguir administradores de conta de provisionadores, `user.pode_provisionar_perfis` é um sinalizador privado, sem input em endpoints públicos ou de usuário. O endpoint exige `role=admin`, esse sinalizador estritamente verdadeiro, mesma conta e usuário alvo diferente do ator. O sinalizador deve ser concedido somente por operador autorizado no console/administração do Xano após confirmar a pessoa responsável; nenhum endpoint da aplicação o define ou altera. `POST /account` continua podendo criar conta e definir `role=admin`, mas não concede o sinalizador. `admin/user_role` mantém sua função legada e também não o concede. A tabela `tecnico` não existia no inventário remoto anterior, então referência e função dependem da implantação prévia da Change de Técnicos.

O pacote de implantação controlada está descrito em `docs/xano-implantacao-controlada.md` e foi preparado em pasta temporária externa ao repositório, por etapas seletivas e sem definições de Clientes/contas legadas. O snapshot de referência contém apenas definições, não registros. A branch observada `v1` é live e foi a única listada; publicação fica bloqueada até haver ambiente isolado aprovado ou decisão/autorização explícita para o destino live.

## Auditoria de prontidao e revisao das etapas 03-09 (2026-11-09)

Esta secao atualiza as evidencias acima com o inventario mais recente do workspace 149143/v1. As tabelas `tecnico` e `ordem_servico` foram publicadas e verificadas: GUIDs `nu49vX9JOpQr45J3_EhsCut0JuQ` e `YMy5cTyq7_EZXyY5QraC5UNte-Q`. Equipamento continua sendo dependencia remota existente. O snapshot somente de definicoes encontrou 46 arquivos; ele nao comprova dados, publicacao de APIs ou comportamento em runtime.

O contrato remoto `POST auth/login` retorna `authToken` e `user_id`, compativel com a forma que o cliente Streamlit consome. A URL de grupo informada pelo responsavel e `https://SEU-WORKSPACE.n7.xano.io/ENDPOINT`. `GET auth/me` remoto ainda retorna somente campos legados (`id`, `created_at`, `name`, `email`, `account_id`, `role`); faltam `perfil_aplicacao` e `id_tecnico`. O signup permanece publico e cria `member`. Por isso, nao e seguro declarar login funcional: o frontend deve falhar fechado para `admin`, `member` ou perfil ausente, e nenhum teste real de credenciais foi enviado a producao.

A etapa 03 foi comparada com `table/user.xs` remoto pelo mesmo GUID `g8tpjso2orFaPgdxKGzuuR66M1k`. O diff estrutural pretendido e aditivo: somente `perfil_aplicacao?`, `pode_provisionar_perfis?`, `id_tecnico?` e indice unico para `id_tecnico`; os campos, enum legado `admin/member` e indices preexistentes sao preservados. Campos novos nao tem default e sao opcionais. O comentario legado foi alinhado ao texto remoto para eliminar uma diferenca textual. O manifesto do pacote temporario foi recalculado e confere com SHA-256 `A4A4762BB67B8D704C565A886EF1AAEE573BA0665B5BCBE289CF9FF54D5628AD` para esse arquivo. A tentativa local de iniciar a CLI nao produziu preview porque Node 24 ainda falha em `uv_os_get_passwd returned ENOMEM`; portanto, o resultado da revisao de operacoes Xano para esta versao corrigida nao foi confirmado. Tambem nao foram lidos registros, logo possiveis conflitos existentes e a semantica de multiplos `NULL` no indice unico permanecem riscos sem evidencia. A etapa 03 nao esta liberada para publicacao.

O pacote controlado organiza as etapas restantes assim; as chamadas sao por diretorio, nunca numa publicacao unica:

1. **03 `table/user.xs` (UPDATE no GUID existente)**: tres campos opcionais/privados e indice unico de `id_tecnico`; nenhuma alteracao em `role`, signup, `POST /account`, `admin/user_role`, Cliente ou Equipamento.
2. **04 quatro funcoes novas**: `tecnicos/autorizar_colaborador`, `ordens/autorizar_colaborador`, `ordens/obter_tecnico_autenticado` e `ordens/validar_vinculos`.
3. **05 dois grupos novos**: `Tecnicos` (`assistencia-tecnica-tecnicos`) e `Ordens de Servico` (`assistencia-tecnica-ordens-servico`).
4. **06 UPDATE de `GET auth/me` pelo GUID existente e CREATE de `POST admin/user_application_profile`**. A resposta de `auth/me` e aditiva; o provisionador requer `role=admin`, `pode_provisionar_perfis=true`, mesma conta e alvo diferente do operador. Signup e `admin/user_role` ficam fora.
5. **07 quatro endpoints de Tecnicos**: POST e GET lista em `tecnicos`, GET e PUT em `tecnicos/{id_tecnico}`.
6. **08 quatro endpoints de OS para colaborador**: POST e GET lista em `ordens-servico`, GET e PUT em `ordens-servico/{id_os}`. Validar Equipamento e Tecnico no backend.
7. **09 tres endpoints do tecnico**: GET `minhas-ordens`, GET `minhas-ordens/{id_os}` e PATCH `minhas-ordens/{id_os}/status`. Identidade deriva de `$auth.id`, OS filtra por `id_tecnico`; apenas o PATCH permite escrita e seu corpo local tem somente `status`. A lista junta Equipamento para tipo/marca/modelo sem chamar API publica.

Dependencias: 03 antes de 04 e 06; 04/05 antes dos endpoints 07-09; tabelas Tecnico/OS e Equipamento antes das funcoes/endpoints de validacao e do painel. Nos endpoints novos do pacote, a identidade vem do token Xano e a autorizacao funcional e validada no backend. Navegacao Streamlit nao substitui essas guardas. Clientes e Equipamentos existentes nao serao alterados neste conjunto; como suas APIs atuais nao verificam os novos perfis funcionais, isso permanece um risco separado para o acesso administrativo geral e nao deve ser encoberto por controles de UI.

A ordem e um plano, nao evidencia de implantacao. Stage 03 nao tem preview confirmado; stages 04-09 nao foram publicados nem executados em runtime. Antes de prosseguir na branch `v1` live, ainda sao necessarios: resolver o erro ENOMEM da CLI sem alterar credenciais, revisar o preview de cada diretorio, confirmar semantica do indice nullable e ausencia de dados conflitantes sem expor registros, aprovar mecanismo operacional para conceder o sinalizador a um operador, e autorizar cada escrita. Sem conta de teste aprovada, verificacoes de login/persistencia/permissao devem permanecer pendentes.

### Atualizacao da etapa 03 em 2026-11-11

A Xano CLI `1.3.3` voltou a iniciar com a variavel temporaria `SHELL=C:\Windows\System32\cmd.exe`. O pull somente de definicoes trouxe 46 documentos; `user` conserva o GUID conhecido. A revisao interativa exibiu `UPDATE table user` e tres `ADD_FIELD`; nao exibiu `UPDATE_FIELD`. A revisao foi cancelada com `N` e a CLI retornou `Push cancelled`.

O manifesto confere com o hash atual do unico arquivo na pasta da etapa. A mudanca inclui o indice unico de `id_tecnico`, mas a preview nao o detalhou separadamente. PostgreSQL padrao permite multiplos `NULL` em um unique index, porem a documentacao Xano consultada nao especifica diretamente a conversao desse indice e existe relato comunitario ambiguo. Mantenha a etapa bloqueada para autorizacao ate confirmar o detalhe do indice no Xano. Alternativa documentada: tabela de associacao tecnica com dois identificadores nao nulos e unicos, caso o comportamento nullable nao seja confirmado.

#### Decisao de concorrencia e revisao atualizada

Os tres campos adicionados a `user` permanecem opcionais e sem defaults. O indice unico de `id_tecnico` tambem permanece no pacote: sem ele, a consulta previa de `user.id_tecnico` no provisionador nao evita duas requisicoes concorrentes associando o mesmo tecnico a usuarios diferentes. A documentacao Xano consultada descreve transacoes ACID, mas nao especifica isolamento serializavel ou bloqueio que torne atomica a verificacao de ausencia e a gravacao; portanto, nao se considera uma transacao generica substituta comprovada para o indice.

A documentacao PostgreSQL afirma que um indice `UNIQUE` comum permite multiplos `NULL` por padrao, e a Xano declara usar PostgreSQL padrao. Isso e evidencia favoravel, nao prova do mapeamento do indice XanoScript na instancia especifica. A revisao interativa atual em workspace `149143`, branch `v1`, mostrou exclusivamente `UPDATE table user` e tres `ADD_FIELD`; nao mostrou `UPDATE_FIELD` nem detalhou o indice. A resposta foi `N`; resultado CLI: `Push cancelled`. Nenhuma escrita remota ou alteracao de registros ocorreu.

O arquivo stage 03 e o manifesto temporario foram inspecionados; hash SHA-256 conferido: `A4A4762BB67B8D704C565A886EF1AAEE573BA0665B5BCBE289CF9FF54D5628AD`. Nao foi necessario alterar pacote/manifesto. A etapa pode ser revisada, mas permanece bloqueada para publicacao ate uma verificacao controlada de `NULL` e unicidade no Xano. Essa verificacao requer tabela descartavel e dados sinteticos em ambiente isolado; nao foi executada no workspace live. Se o comportamento for incompatível ou nao puder ser comprovado, avaliar uma tabela tecnica de associacao com ambas as chaves obrigatorias e unicas, atualizando antes o desenho de `auth/me` e do provisionamento.

### Revisao consolidada do pacote (2026-11-11)

Pull somente de definicoes em `149143/v1` retornou 46 documentos. O pull nao incluiu registros, variaveis nem drafts. O GUID remoto de `user` continua `g8tpjso2orFaPgdxKGzuuR66M1k`. A diferenca da etapa 03 e aditiva: tres campos opcionais sem defaults (`perfil_aplicacao`, `pode_provisionar_perfis`, `id_tecnico`) e o indice unico de `id_tecnico`; nenhum campo, indice, tag ou configuracao legado foi removido/alterado. O preview mostrou somente `UPDATE table user` e tres `ADD_FIELD`; foi cancelado com `N`.

## Retificacao arquitetural aprovada (2026-11-11)

Esta secao substitui as propostas anteriores de adicionar campos funcionais a `user` e o plano da etapa 03 descrito acima. O responsavel aprovou a preservacao integral de `user`, de seus campos/indices atuais, da autenticacao nativa e dos contratos legados. A tabela `user.xs` local foi restaurada sem `perfil_aplicacao`, `pode_provisionar_perfis`, `id_tecnico` ou indice novo. Signup, `POST /account` e `admin/user_role` nao recebem nem alteram os dados funcionais.

Os metadados de autorizacao ficam em duas tabelas tecnicas, que nao ampliam as cinco entidades de negocio:

1. `user_application_profile`: uma linha opcional por usuario, `user_id` FK obrigatoria e UNIQUE, `perfil_aplicacao` (`colaborador`/`tecnico`) e `pode_provisionar_perfis` privado com valor inicial falso. Signup nao cria a linha; usuario sem perfil permanece sem acesso funcional.
2. `user_tecnico`: somente para identidade tecnica; `user_id` e `id_tecnico` sao FKs obrigatorias e UNIQUE. A restricao no banco protege a exclusividade mesmo com requisicoes concorrentes; nenhum indice nullable e usado.

`auth/me` conserva a resposta legada e acrescenta `perfil_aplicacao` e `id_tecnico` resolvidos pelas tabelas tecnicas. Perfil ausente devolve `perfil_aplicacao: null`, que o Streamlit nega; perfil tecnico sem vinculo/cadastro valido recebe negacao no backend. Os guards colaborador/tecnico tambem resolvem identidade atraves dessas tabelas.

O provisionador exige token valido, `user.role=admin`, perfil funcional `colaborador`, `pode_provisionar_perfis=true`, alvo diferente e mesma conta. Tecnico exige cadastro existente e rejeita duplicidade observada. As gravacoes e remocoes de vinculo estao sob `db.transaction`; a sintaxe exata e o rollback requerem validacao do XanoScript/runtime antes de publicacao. As constraints UNIQUE sao a garantia contra corrida; a conversao da violacao concorrente em HTTP conflito permanece pendente ate o codigo/constraint real ser confirmado em homologacao. Nenhum endpoint de aplicacao pode conceder o sinalizador.

O pacote temporario anterior ainda contem a antiga etapa 03 (`UPDATE table user`). Ele nao foi alterado e nao pode ser usado; deve ser regenerado em pasta de trabalho autorizada com as duas novas tabelas e manifesto novo. Nenhuma publicacao ou escrita remota foi realizada nesta atualizacao.

Foram revisados e cancelados os previews de 04-09: quatro funcoes; dois grupos; `UPDATE auth/me` mais `CREATE admin/user_application_profile`; quatro endpoints de Tecnico; quatro endpoints de OS; tres endpoints do painel. Os previews 07-09 sinalizaram helpers da etapa 04 ausentes, pois ainda nao foram publicados. A ordem dependente permanece obrigatoria, e cada preview dependente deve ser repetido depois da etapa anterior para confirmar que os avisos desaparecem.

O endpoint de provisionamento faz pre-check e rejeita vinculo duplicado observado antes da atualizacao. O indice unico garante no banco que uma corrida nao persista duas associacoes iguais. Contudo, nao existe no arquivo local tratamento explicito que converta a violacao concorrente do indice em resposta de conflito propria; a requisicao perdedora pode receber erro generico do banco. Portanto, a integridade dos dados e garantida pelo indice, mas o contrato amigavel de conflito ainda precisa ser verificado/corrigido antes da integracao Streamlit de provisionamento.

### Pacote regenerado para a arquitetura aprovada (2026-11-11)

Foi criado `deployment/xano-149143-v1-controlled-package` com 21 definições nas etapas 03-09. O pacote contém as tabelas técnicas `user_application_profile` e `user_tecnico`, funções, grupos, atualização de `auth/me`, provisionador e endpoints de Técnicos, OS e painel. Não inclui `table/user.xs`, tabela Cliente/Equipamento, recursos legados, nem as etapas 01-02 já publicadas. O manifesto contém 21 entradas SHA-256, todas conferidas contra os arquivos empacotados. A tarefa 5.5 está concluída apenas para o pacote local; publicação e integração permanecem pendentes.

A fonte local do provisionador usa `db.transaction { stack { ... } }`. A documentação oficial do Xano descreve Database Transaction como grupo atômico de operações, mas a CLI local 1.3.3 não oferece comando `validate` para compilar/verificar XanoScript. A ajuda local da CLI confirma que importações são envolvidas em transação por padrão (com opção explícita para desativar), o que se refere à importação do bundle e não prova a sintaxe nem a atomicidade da transação de runtime na função. Portanto, parser/runtime, rollback e mapeamento da violação UNIQUE permanecem não comprovados. Como o workspace atual tem somente `v1` live e a página de planos põe CLI sandbox e branching no plano Essential, não há validação isolada confirmada no plano atual. Nenhuma publicação ou escrita remota foi executada.

### Publicação verificada da etapa 03 (2026-11-11)

Após autorização explícita, o preview mostrou exclusivamente `CREATE table user_application_profile` e `CREATE table user_tecnico`; a CLI informou `Pushed 2 documents to workspace 149143`. Pull somente de definições retornou 48 documentos e confirmou as duas tabelas, seus GUIDs (`0ErthpeUwMp6CNa_uRjGfNRbgzo` e `reGUcbHu3m8zizI4LH2r8506-js`), FKs obrigatórias (`user_id` para `user`, `id_tecnico` para `tecnico`) e índices UNIQUE em `user_application_profile.user_id`, `user_tecnico.user_id` e `user_tecnico.id_tecnico`. O SHA-256 do `table/user.xs` no snapshot anterior e no posterior é idêntico; nenhum arquivo de `user` integrou a etapa e nenhum registro foi consultado ou alterado. As etapas 04-09 não foram executadas.

O pull remoto normalizou `pode_provisionar_perfis` como booleano opcional privado, sem declarar `=false` como default na definição exportada. O provisionador grava explicitamente `false` ao criar uma linha e a autorização exige comparação estrita com `true`, portanto valor ausente/null nega; essa diferença foi refletida na definição local e no pacote/manifesto. A tarefa de runtime para transações e tratamento de violação concorrente UNIQUE continua pendente.

### Encerramento da revisão da etapa 04 (2026-11-11)

Pull somente de definições confirmou novamente a branch única `v1` live e 48 documentos; as tabelas `user_application_profile`, `user_tecnico`, `tecnico`, `equipamento` e `ordem_servico` estão presentes. A pasta `04-authorization-functions` contém exatamente quatro arquivos e os quatro hashes conferem com `MANIFEST.csv`. O preview no workspace `149143` mostrou apenas `CREATE function` para `ordens/autorizar_colaborador`, `ordens/obter_tecnico_autenticado`, `ordens/validar_vinculos` e `tecnicos/autorizar_colaborador`; não mostrou atualizações nem exclusões. A resposta `N` produziu `Push cancelled`. Nenhuma função da etapa 04 foi publicada. Os endpoints futuros devem passar `$auth.id` como `user_id` aos guards, e aplicar autorização de colaborador antes de chamar `validar_vinculos`. Retomar pela revisão da etapa 04; não avançar para 05 sem autorização específica. Nenhuma tarefa de implementação ou integração foi concluída por este preview.

Os hashes do manifesto conferem para etapa 03 e etapas 04-09. As entradas 01-02 diferem porque os arquivos do pacote receberam os GUIDs atribuidos apos a publicacao; nao reenviar essas etapas. O pull pos-publicacao da etapa 03 deve conferir schema apenas, sem consultar usuarios nem modificar registros: GUID e campos/indices legados preservados; tres campos novos opcionais/privados sem defaults; indice unico presente. Isso nao comprova comportamento de runtime de `NULL`/duplicidade. Nenhuma etapa 03-09 foi publicada nesta revisao e nenhuma tarefa de integracao foi marcada concluida.

