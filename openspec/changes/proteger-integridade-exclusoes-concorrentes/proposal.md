# Proposal

## Why

Uma OS, Serviço ou associação de identidade pode ser criada entre a consulta de
dependências e a exclusão do registro pai. O inventário remoto conferido em
19/11 preserva 81 definições, mas não comprova barreira de banco para essa corrida;
os novos DELETEs precisam de coordenação com os escritores antes da liberação.

## What Changes

- Coordenar DELETE de Técnico com POST/PUT de OS e provisionamento de perfil
  técnico; coordenar DELETE de OS com POST/PUT de Serviços.
- Propor transação de dados e bloqueio do registro pai em todos esses caminhos,
  com decisões de existência/dependências realizadas depois do bloqueio.
- Preservar autenticação, autorização, campos, contratos sequenciais, auditoria
  e atomicidade do provisionamento; não adicionar cascata ou retry automático.
- Preparar testes locais de intercalação, sintaxe e escopo, distinguindo modelo
  simulado de comprovação do comportamento real de locks/transações do Xano.
- Separar cinco UPDATEs de endpoints existentes dos quatro CREATEs dos pacotes
  de exclusão. Exigir preview novo e autorização própria antes de publicar.

## Capabilities

### New Capabilities

- `integridade-exclusoes-concorrentes`: coordenação dos escritores de vínculos
  e exclusões de Técnico/OS para impedir referências órfãs sob concorrência.

### Modified Capabilities

Nenhuma spec principal é reescrita: os contratos de gestao-servicos permanecem.
A nova capacidade explicita a garantia transversal adicional; complementa as
duas Changes de exclusão e não encerra os critérios de acesso/provisionamento.

## Impact

Cinco fontes existentes candidatas a UPDATE:

- xano/api/ordens/ordens_servico_POST.xs;
- xano/api/ordens/ordens_servico/id_os_PUT.xs;
- xano/api/servicos/servicos_POST.xs;
- xano/api/servicos/servicos/id_servico_PUT.xs;
- xano/api/members_accounts/admin/user_application_profile_POST.xs.

As duas fontes DELETE ainda locais serão ajustadas nas Changes de exclusão;
os dois helpers de dependências continuam recursos novos dessas Changes.
Total agregado candidato: 4 CREATE, 5 UPDATE, 0 DELETE de definições, não um
preview executado. Não recriar tabelas, grupos, guards nem modificar frontend,
painel técnico, schema, campos de domínio ou registros por esta proposta.

Dependências: runtime deve sustentar locks até commit/rollback, visibilidade
adequada das leituras após espera e participação das consultas auxiliares na
transação. Se isso não puder ser comprovado, interromper liberação e apresentar
alternativa antes de ampliar escopo. Importações/edições manuais fora das APIs
não são abrangidas por bloqueios cooperativos; exigiriam garantia de banco.

Autorizada nesta etapa somente elaboração dos artefatos. Contador 375; nenhuma
chamada remota, implementação, publicação ou Git. Meta de entrega: 21/11/2026.

## Revisão de planejamento é 20/11/2026, contador 377

O responsável confirmou visualmente no Xano: workspace 149143 no plano Free,
com somente a fonte de dados `live`; em Manage Data Sources, Add Test Data
Sources exige upgrade. Essa informação é evidência declarada pelo responsável,
sem nova consulta remota nesta revisão. Não há autorização nem interesse em
contratar serviços pagos. Não presumir disponibilidade de outro workspace,
branch com dados separados, trial ou recurso gratuito equivalente.

A estratégia passa a priorizar preparação e validação local gratuitas,
reaproveitando os 76 testes e o parser já aprovados. Simulação, mocks e análise
estática comprovam contratos/desenho, não semântica de banco do Xano. Não mudar
arquitetura, schema ou requisitos para contornar a restrição. DELETEs continuam
sem liberação enquanto faltar a prova runtime requerida; não usar a fonte live
para corrida destrutiva ou falha induzida de persistência/auditoria.

A meta vigente é 22/11/2026 às 18h, Brasília. A data de 21/11 e o contador 375
acima descrevem a proposta histórica. Esta revisão altera somente planejamento
OpenSpec, mantém 377 chamadas e não autoriza implementação, testes novos,
publicação, alterações remotas, flags, sync, Archive ou Git.
