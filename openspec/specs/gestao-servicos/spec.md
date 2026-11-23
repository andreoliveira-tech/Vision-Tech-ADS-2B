# gestao-servicos Specification

## Purpose

Registrar e administrar os serviços realizados em Ordens de Serviço existentes,
com autorização no backend e operação integrada à interface administrativa.

## Requirements

### Requirement: Serviço preserva os campos originais e o vínculo com OS
O sistema MUST representar Serviço somente com `id_servico`, `descricao`, `valor`
e `id_os`. O identificador MUST ser gerado pelo backend e permanecer estável em
atualizações. Descrição MUST ser texto informado e valor MUST ser um número
decimal finito informado; tipos incompatíveis e campos obrigatórios ausentes
MUST ser rejeitados antes da gravação. O vínculo MUST apontar para OS existente.

#### Scenario: Cadastro válido
- **WHEN** colaborador informa descrição, valor e identificador de OS existente
- **THEN** o backend cria um Serviço, gera seu ID e retorna seus quatro campos

#### Scenario: Dados ou referência inválidos
- **WHEN** campos obrigatórios estão ausentes, tipos são incompatíveis ou a OS não existe
- **THEN** a operação é rejeitada sem criar ou alterar Serviço nem OS

### Requirement: CRUD de Serviços exige perfil colaborador
As operações POST/GET de coleção e GET/PUT/DELETE individual MUST exigir Bearer
válido e perfil funcional colaborador confirmado pelo backend. Papel legado
admin/member MUST NOT substituir o perfil funcional. Técnicos e usuários sem
perfil MUST NOT obter acesso administrativo ao módulo.

#### Scenario: Colaborador autorizado
- **WHEN** colaborador autenticado chama uma das cinco operações de Serviços
- **THEN** o backend executa a operação conforme seus dados e referências válidos

#### Scenario: Identidade sem autorização
- **WHEN** uma chamada é anônima, tem token inválido ou pertence a técnico/usuário sem perfil
- **THEN** o backend nega acesso antes de ler ou alterar dados de Serviço

### Requirement: Consulta e atualização mantêm contrato verificável
O sistema MUST listar Serviços, permitir identificar os pertencentes a uma OS,
consultar Serviço individual e atualizar seus três campos editáveis. Uma
atualização de `id_os` MUST validar a nova OS antes de gravar. A resposta
individual MUST conter exatamente os quatro campos do domínio. Identificador
inexistente MUST produzir ausência, sem criar um registro substituto.

#### Scenario: Consulta dos serviços de uma OS
- **WHEN** colaborador seleciona uma OS para consultar serviços associados
- **THEN** a interface apresenta somente os Serviços cujo id_os corresponde à seleção

#### Scenario: Alteração de Serviço existente
- **WHEN** colaborador envia uma atualização válida para Serviço existente
- **THEN** os valores enviados são persistidos, o ID é preservado e uma leitura confirma o estado

### Requirement: Exclusão de Serviço preserva os demais registros
DELETE MUST excluir somente o Serviço selecionado, exigir que ele exista e
retornar confirmação identificável. O sistema MUST NOT excluir sua OS, outros
Serviços, Equipamentos, Clientes ou Técnicos. CRUD de Serviço MUST NOT modificar
automaticamente `valor_total`, status ou qualquer outro campo de OS.

#### Scenario: Exclusão confirmada
- **WHEN** colaborador confirma exclusão de Serviço existente
- **THEN** somente esse Serviço é removido e sua consulta posterior confirma ausência

#### Scenario: OS com outros Serviços
- **WHEN** um Serviço associado à OS é alterado ou excluído
- **THEN** a OS e todos os demais Serviços mantêm seus valores e relacionamentos

### Requirement: Interface confirma operações sem reenvio implícito
O sistema MUST disponibilizar gestão de Serviços exclusivamente em Streamlit
para colaboradores, enviando o token da sessão nas operações e confirmações.
Trocar de Serviço MUST limpar dados do formulário anterior. Listagem falha MUST
invalidar resultados anteriores. Falha de autorização MUST interromper acesso;
401 MUST limpar a sessão e 403 MUST impedir exposição administrativa indevida.
Resultado de escrita incerto MUST impedir reenvio automático e exigir conferência
explícita. Sucesso MUST depender de resposta válida e confirmação por leitura.

#### Scenario: Troca de seleção
- **WHEN** colaborador muda o Serviço selecionado para edição ou exclusão
- **THEN** a tela descarta o estado anterior e exige carregar o novo alvo antes de escrever

#### Scenario: Timeout ou confirmação falha
- **WHEN** POST, PUT ou DELETE fica incerto ou sua leitura de confirmação falha
- **THEN** a tela informa a incerteza e não repete a escrita em reruns ou novas interações implícitas
