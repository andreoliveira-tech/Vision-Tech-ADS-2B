# Integridade das exclusões concorrentes

## Purpose

Impedir referências órfãs entre Técnico, OS, Serviços e associação de identidade
quando operações autorizadas de vinculação e exclusão se sobrepõem.

## ADDED Requirements

### Requirement: Exclusão de Técnico coordena escritores de vínculos
O sistema MUST coordenar exclusão de Técnico com cadastro/alteração de OS e
provisionamento de associação técnica. Uma operação MUST NOT confirmar vínculo
para Técnico excluído, nem excluir Técnico cuja dependência já foi confirmada.
O bloqueio por OS ou identidade MUST preservar os contratos sequenciais vigentes.

#### Scenario: Vinculação confirmada antes da exclusão de Técnico
- **WHEN** cadastro/alteração de OS ou associação de identidade confirma vínculo antes da decisão concorrente de excluir o mesmo Técnico
- **THEN** a exclusão é bloqueada com 400 e Técnico e dependência são preservados

#### Scenario: Exclusão de Técnico confirmada antes da vinculação
- **WHEN** exclusão do Técnico confirma antes da decisão concorrente de cadastrar ou alterar vínculo para esse Técnico
- **THEN** a vinculação é rejeitada sem gravar referência órfã nem alterações parciais de perfil ou auditoria

### Requirement: Exclusão de OS coordena escritores de Serviços
O sistema MUST coordenar exclusão de OS com cadastro e alteração do vínculo de
Serviço. Nenhum Serviço confirmado MUST apontar para OS excluída. A coordenação
MUST preservar status, valor total e demais relacionamentos de domínio.

#### Scenario: Serviço confirmado antes da exclusão de OS
- **WHEN** cadastro ou transferência de Serviço para uma OS confirma antes da decisão concorrente de excluir essa OS
- **THEN** a exclusão é bloqueada com 400 e a OS e o Serviço são preservados

#### Scenario: Exclusão de OS confirmada antes da vinculação de Serviço
- **WHEN** exclusão da OS confirma antes da decisão concorrente de cadastrar ou transferir Serviço para ela
- **THEN** a vinculação é rejeitada sem criar Serviço órfão ou alterar parcialmente o Serviço existente

### Requirement: Falhas concorrentes não deixam alterações parciais
Falha de bloqueio, validação, persistência ou auditoria MUST abortar a operação
dependente sem confirmar sucesso ou persistir efeitos parciais. O sistema MUST
NOT repetir automaticamente escritas, restaurar registros por compensação ou
converter erro de consulta em ausência de dependência. A espera por outra
operação MUST NOT permitir decidir usando um estado anterior já invalidado.

#### Scenario: Falha após aquisição da proteção
- **WHEN** uma operação falha após iniciar alterações coordenadas
- **THEN** nenhuma alteração parcial dessa operação é confirmada e não ocorre reenvio automático

#### Scenario: Dependência surge enquanto exclusão aguarda
- **WHEN** a exclusão aguarda uma vinculação que confirma sua dependência
- **THEN** a exclusão considera o estado confirmado e bloqueia em vez de usar ausência observada antes da espera

### Requirement: Proteção mantém contratos e autorização existentes
Bearer, perfil colaborador e restrições adicionais do provisionador MUST ser
preservados. A coordenação MUST NOT conceder acesso a técnico ou usuário sem
perfil, alterar campos/payloads/respostas de sucesso, excluir em cascata ou
modificar registros alheios ao alvo. PUT de alvo removido MUST NOT recriá-lo.

#### Scenario: Solicitante sem permissão
- **WHEN** solicitante sem a autorização vigente tenta uma operação protegida
- **THEN** recebe a negação de acesso existente sem ler dados administrativos nem gravar registros

#### Scenario: Atualização disputa com remoção do próprio alvo
- **WHEN** uma atualização espera e seu registro alvo é removido antes de prosseguir
- **THEN** a atualização retorna ausência conforme contrato e não recria o registro

### Requirement: Liberação exige comprovação da coordenação real
O sistema MUST ter comprovação das duas ordens de concorrência para vínculos
Técnico–OS, Técnico–identidade e OS–Serviço, incluindo transferência por PUT,
rollback e visibilidade após espera. Mocks, parser e transação de publicação
MUST NOT ser apresentados como prova de garantia de dados do runtime. Sem
comprovação suficiente, os DELETEs novos MUST permanecer sem liberação.

#### Scenario: Somente ensaio simulado disponível
- **WHEN** os testes locais passam mas faltam evidências da coordenação no runtime
- **THEN** o relatório registra o limite e mantém a liberação pendente

#### Scenario: Evidência autorizada obtida em ambiente isolado
- **WHEN** ensaio isolado autorizado comprova coordenação, rollback e preservação nas ordens previstas
- **THEN** as evidências e limitações são registradas antes da decisão expressa de liberação

#### Scenario: Plano Free com somente fonte live e sem contratação
- **WHEN** o único ambiente disponível tem somente a fonte live e o responsável não autoriza contratação de fonte isolada
- **THEN** o planejamento prioriza evidências e ensaios locais gratuitos, registra separadamente as garantias ainda dependentes do runtime e mantém os DELETEs sem liberação
- **AND** testes simulados ou sequenciais não são aceitos como prova de concorrência/rollback e nenhuma corrida destrutiva ou falha de persistência/auditoria é induzida em Live
