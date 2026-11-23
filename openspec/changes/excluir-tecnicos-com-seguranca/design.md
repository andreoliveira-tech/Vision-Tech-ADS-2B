# Design

## Dependência técnica vigente — contador 375

O design sequencial abaixo não é suficiente para liberação. A Change
`proteger-integridade-exclusoes-concorrentes` especifica transação e lock do
Técnico compartilhado entre DELETE, POST/PUT de OS e provisionamento, com
ordem global user→Técnico→OS→Serviço e releitura após espera. Ela detém os cinco
UPDATEs dos escritores; esta Change detém helper e DELETE novos. Publicar
escritores protegidos antes dos DELETEs, somente após comprovação das garantias
e novas autorizações. Pacotes históricos não serão sobrescritos.
Fixture isolada de identidade e tarefa 3.3 continuam impeditivas; não contar
modelo local como prova de runtime. Nenhuma implementação mudou nesta revisão.

## Context

Ver proposal.md. Inspecionados tecnico, ordem_servico, user_tecnico, user,
guards, quatro APIs de Técnicos, cliente/tela e implementação DELETE de
Equipamentos. OS referencia tecnico.id; user_tecnico também, com índice unique.
user não tem id_tecnico. A proposta histórica de usar user.id_tecnico foi
substituída pela arquitetura vigente; não introduzir ou remover esse atributo.
As fontes atuais não têm helper de dependências ou DELETE de Técnico.
Nenhuma nova leitura remota; 81 definições no último inventário protegido,
contador 374 após Serviços. Dependências e ausência remota serão reconferidas.

## Goals / Non-Goals

**Goals:** completar exclusão do CRUD com proteção de OS e identidade, usando
somente tabelas/guard/grupo existentes e integração na tela atual.

**Non-Goals:** desprovisionar usuários, remover vínculos/perfis, transferir OS,
excluir em cascata, alterar schema ou encerrar homologação original de Técnicos.

## Decisions

### Backend mínimo e contratos

Dois recursos novos propostos: function tecnicos/consultar_dependencias e
api/tecnicos/tecnicos/id_tecnico_DELETE.xs. Reutilizar o guard específico de
Técnicos para preservar a arquitetura desse módulo. Autorização primeiro,
ID positivo, existência, helper, validação estrita de identidade e booleanos,
bloqueios, db.del tecnico apenas. Helper retorna id_tecnico, possui_os e
possui_usuario; consultas exists sem filtrar status. Resultado indefinido não
equivale a falso. Preferir consultas de existência a listas possivelmente paginadas.

Proposta de mensagens 400: `id_tecnico deve ser um inteiro positivo.`,
`Tecnico possui ordens de servico vinculadas. Exclusao bloqueada.`,
`Tecnico possui vinculo de usuario. Exclusao bloqueada.`. Se ambas dependências
existirem, testar primeiro OS; não interpretar mensagem de um bloqueio como
prova do outro. Ausência: manter `Tecnico nao encontrado.`; sucesso
{id_tecnico, excluido:true}. Falha de consulta aborta, nunca db.del em fallback.
Envelopes reais serão conferidos em homologação própria.

### Integração e incerteza

tecnicos_api._request considera escrita somente POST/PUT e espera cadastro no
sucesso. Alterar apenas o necessário para DELETE sem corpo, resposta de exclusão
estrita e incerto em timeout/408/5xx/contrato inválido. Usar confirmação 404
conhecida, nunca qualquer 404/HTML. Reutilizar padrões de servicos_api/UI sem
substituir o módulo nem modificar seus POST/PUT já existentes.

Na tela, ação após carregar alvo, confirmação com chave por ID/geração, consumo
do carregamento antes do DELETE, confirmação GET, invalidação de lista/edição.
Incerto bloqueia também PUT no alvo até recarregar/conferir; não manter botão
de exclusão reutilizável. Ausência conhecida numa conferência explícita permite
resolver a pendência sem reenviar DELETE. Não criar login automático.

### Limite sequencial e liberação

A pré-consulta segue a integridade sequencial já usada no projeto. Não é prova
de integridade concorrente. Entre checagem e db.del pode surgir OS ou vínculo.
Antes da liberação, verificar nas ferramentas/documentação técnicas disponíveis
as garantias efetivas das referências/transações; se insuficientes, interromper
e apresentar o ajuste necessário com impactos, sem alterar escritores/schema
existentes silenciosamente. Push com transaction protege publicação, não os
registros em runtime. Não executar teste destrutivo concorrente em v1 Live.

## Risks / Trade-offs

- Histórico de Técnicos incompleto → não confundir novo DELETE com fechamento
  das tarefas antigas; reaproveitar somente evidências conclusivas.
- Vínculo de identidade bloqueado precisa fixture isolada → não remover vínculo
  de usuário existente para testar; preparar cenário e autorização próprios.
- Retorno incerto → preservar pendência e parar sem retry/rollback de dados.
- Concorrência não comprovada → decisão de liberação explícita após diagnóstico
  técnico; não declarar garantia de banco a partir de parser ou mocks.

## Migration Plan

1. Após aprovação, implementar/testar localmente; parser, pacote seletivo com
   hashes e dependências REUSE, sem tabelas/grupos/guards no payload.
2. Medir ensaio offline e congelar fixtures/roteiro/orçamento, incluindo login,
   auth/me, baseline, provisionamento de fixture se autorizado e preservação.
3. Autorizações próprias para inventário/preview e publicação. Exigir exatamente
   2 CREATE, 0 UPDATE, 0 DELETE se ambos recursos ainda estiverem ausentes.
4. Homologar nova fixture livre, outra com OS e fixture com vínculo de identidade,
   negações do DELETE, ausência/ID inválido e interface. Proteger Técnicos 1–3,
   OS 1/2 e demais cadastros; não usar seus IDs como alvos de DELETE.
5. Se faltar fixture isolada de identidade, o cenário fica impeditivo da conclusão;
   provisionamento não é autorizado por esta Change. Não publicar/limpar em erro.
6. Rollback de código local pode ser revisado antes do Git. Reversão remota precisa
   plano e autorização próprios; não restaurar registros automaticamente.
