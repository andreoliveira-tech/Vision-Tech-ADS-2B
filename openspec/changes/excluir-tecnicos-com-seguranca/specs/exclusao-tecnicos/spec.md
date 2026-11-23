# Exclusão de Técnicos

## Purpose

Permitir excluir Técnicos sem dependências, preservando as Ordens de Serviço,
os vínculos de identidade e os demais registros da assistência técnica.

Os cenários sequenciais abaixo são complementados pela capacidade
`integridade-exclusoes-concorrentes` da Change
`proteger-integridade-exclusoes-concorrentes`. Sua comprovação é dependência
de liberação; estes cenários não demonstram proteção concorrente isoladamente.

## ADDED Requirements

### Requirement: Exclusão exige identidade e perfil colaborador
DELETE /tecnicos/{id_tecnico} MUST exigir Bearer válido e perfil funcional
colaborador no servidor antes de consultar dados ou dependências. Papéis
legados admin/member MUST NOT substituir user_application_profile.

#### Scenario: Acesso sem autorização
- **WHEN** anônimo, token inválido, técnico ou usuário sem perfil solicita exclusão
- **THEN** a API nega com 401 ou 403 conforme autenticação, sem excluir ou alterar registros

### Requirement: Dependências impedem exclusão sequencial
O sistema MUST rejeitar ID não positivo com 400 e Técnico ausente com 404.
Para Técnico existente, MUST verificar todas as OS vinculadas e user_tecnico;
qualquer dependência MUST bloquear exclusão com 400, independentemente do status
da OS. Consulta falha ou resultado incompleto MUST interromper sem excluir.

#### Scenario: Técnico atribuído a OS
- **WHEN** existe OS de qualquer status com o id_tecnico solicitado
- **THEN** a exclusão é bloqueada e Técnico, OS e seus relacionamentos são preservados

#### Scenario: Técnico vinculado à identidade
- **WHEN** existe user_tecnico para o Técnico, mesmo sem OS
- **THEN** a exclusão é bloqueada sem remover vínculo, usuário ou perfil

#### Scenario: Dependência não confirmada
- **WHEN** uma consulta falha ou não permite confirmar as duas dependências
- **THEN** não ocorre exclusão nem confirmação de sucesso

### Requirement: Exclusão remove somente o alvo sem dependências
Sem dependências confirmadas no fluxo sequencial, DELETE MUST excluir somente
o Técnico alvo e retornar 200 com exatamente id_tecnico e excluido:true.
MUST NOT remover OS, user_tecnico, user, perfis ou outros cadastros.

#### Scenario: Técnico livre excluído
- **WHEN** colaborador exclui Técnico existente sem OS nem vínculo de identidade
- **THEN** somente esse Técnico é removido, e GET individual posterior retorna 404 conhecido

### Requirement: Interface exige confirmação e não reenvia resultado incerto
A tela Streamlit MUST exigir alvo carregado e confirmação explícita desmarcada
por padrão. Troca de alvo MUST invalidar confirmação. Sucesso MUST depender
do contrato DELETE e GET 404 conhecido. Timeout, falha de confirmação ou corpo
divergente MUST bloquear novas escritas no alvo até conferência explícita,
sem DELETE automático, retry ou restauração. 401/403 MUST limpar ou bloquear
acesso conforme a sessão vigente, sem manter dados administrativos expostos.

#### Scenario: Confirmação e ausência
- **WHEN** colaborador confirma excluir o Técnico carregado e recebe DELETE válido e GET 404 conhecido
- **THEN** a tela informa sucesso e invalida alvo, lista e confirmação

#### Scenario: Resultado incerto ou troca de seleção
- **WHEN** a escrita fica incerta ou o usuário muda o ID selecionado
- **THEN** a tela não reenvia DELETE e exige carregamento/conferência antes de nova ação
