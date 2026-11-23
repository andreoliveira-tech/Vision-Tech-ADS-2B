# Exclusão de Ordens de Serviço

## Purpose

Permitir excluir OS sem Serviços, por colaborador autenticado, preservando
os registros vinculados e exigindo confirmação verificável na interface.

Os cenários sequenciais abaixo são complementados pela capacidade
`integridade-exclusoes-concorrentes` da Change
`proteger-integridade-exclusoes-concorrentes`. Sua comprovação é dependência
de liberação; estes cenários não demonstram proteção concorrente isoladamente.

## ADDED Requirements

### Requirement: Exclusão de OS exige perfil colaborador
DELETE /ordens-servico/{id_os} MUST exigir Bearer válido e perfil funcional
colaborador no backend antes de consultar OS ou dependências. Técnico MUST NOT
excluir nem a própria OS. Papéis legados MUST NOT conferir acesso administrativo.

#### Scenario: Acesso administrativo negado
- **WHEN** anônimo, token inválido, técnico ou usuário sem perfil solicita DELETE
- **THEN** a API retorna 401 ou 403 conforme autenticação e não altera registros

### Requirement: Serviço vinculado bloqueia exclusão sequencial
O sistema MUST rejeitar ID não positivo com 400 e OS ausente com 404 conhecido.
Para OS existente MUST verificar Serviços cujo id_os corresponda ao alvo;
qualquer Serviço MUST bloquear DELETE com 400. Falha ou consulta incompleta
MUST interromper sem excluir. O status MUST NOT dispensar essa verificação.

#### Scenario: OS possui Serviço
- **WHEN** existe pelo menos um Serviço vinculado à OS de qualquer status
- **THEN** a API bloqueia exclusão e preserva integralmente OS e Serviços

#### Scenario: Consulta de dependência falha
- **WHEN** não é possível confirmar ausência de Serviços
- **THEN** a API não exclui a OS nem declara sucesso

### Requirement: Exclusão preserva registros relacionados
Sem Serviços confirmados no fluxo sequencial, DELETE MUST excluir somente a
OS alvo e retornar 200 com exatamente id_os e excluido:true. MUST NOT excluir
Equipamento, Técnico, Cliente, outras OS ou alterar seus campos. MUST NOT apagar
Serviços automaticamente para viabilizar exclusão nem modificar total/status.

#### Scenario: OS livre excluída
- **WHEN** colaborador confirma DELETE de OS existente sem Serviços
- **THEN** somente essa OS é removida, GET posterior retorna 404 conhecido e registros relacionados permanecem iguais

### Requirement: Interface confirma exclusão sem repetição implícita
A tela administrativa Streamlit MUST exigir OS carregada e confirmação
explícita desmarcada por padrão. Mudar seleção MUST limpar confirmação. Sucesso
MUST exigir DELETE válido e GET 404 com contrato conhecido; falha, timeout ou
confirmação divergente MUST bloquear nova escrita até conferência explícita.
MUST NOT reenviar DELETE em reruns, reautenticar ou restaurar dados automaticamente.
401 MUST limpar sessão; 403 MUST bloquear acesso e descartar dados administrativos.

#### Scenario: Exclusão confirmada
- **WHEN** DELETE e GET de ausência passam para o ID confirmado pelo colaborador
- **THEN** a tela apresenta sucesso e limpa lista, alvo e confirmação

#### Scenario: Exclusão não confirmada
- **WHEN** DELETE fica incerto ou GET não confirma ausência
- **THEN** a tela informa incerteza, mantém apenas o necessário à conferência e não repete escrita
