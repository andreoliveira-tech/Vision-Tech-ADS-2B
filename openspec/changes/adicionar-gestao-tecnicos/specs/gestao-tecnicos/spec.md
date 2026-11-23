# Spec Delta

## Purpose

Define o cadastro e a consulta de técnicos da assistência técnica usando somente os campos do modelo global aprovado. Esta capacidade fornece a base de domínio para futuras atribuições de ordens de serviço.

## ADDED Requirements

### Requirement: Cadastro Técnico preserva os campos do modelo
O sistema MUST representar cada Técnico com os campos `id_tecnico`, `nome`, `especialidade`, `telefone` e `email` definidos em `docs/domain-model.md`. O identificador MUST ser gerado e preservado pelo backend. O sistema MUST NOT acrescentar credenciais, perfil de acesso ou outros atributos à entidade Técnico.

Como decisão de implementação do MVP aprovada pelo responsável do projeto, e não como exigência original do professor, `nome`, `especialidade`, `telefone` e `email` MUST ser obrigatórios e `email` MUST ter formato válido. O sistema MUST NOT impor unicidade de email sem requisito ou justificativa adicional. O identificador físico nativo `id` do Xano representa `id_tecnico`.

#### Scenario: Cadastrar técnico
- **WHEN** um colaborador autenticado envia os campos de cadastro permitidos
- **THEN** o backend cria um Técnico com identificador gerado e os dados correspondentes aos campos do modelo

#### Scenario: Identificador não pode ser definido pelo cliente
- **WHEN** o cliente tenta escolher ou alterar `id_tecnico` durante cadastro ou atualização
- **THEN** o backend preserva o identificador gerado para o registro e não aceita substituição pelo valor enviado

### Requirement: Consulta e atualização de técnicos
O sistema MUST permitir a colaboradores autorizados listar Técnicos, consultar um registro individual e atualizar seus dados. Consultas e atualizações MUST apresentar e preservar os campos do modelo sem incluir credenciais ou dados de autenticação.

#### Scenario: Listar técnicos
- **WHEN** um colaborador autorizado solicita a lista de técnicos
- **THEN** o backend retorna os registros de Técnico com os campos definidos pelo modelo, incluindo lista vazia quando não houver registros

#### Scenario: Consultar técnico existente
- **WHEN** um colaborador autorizado consulta um `id_tecnico` existente
- **THEN** o backend retorna os dados do técnico correspondente

#### Scenario: Consultar técnico inexistente
- **WHEN** um colaborador autorizado consulta um identificador sem registro correspondente
- **THEN** o backend informa que o Técnico não foi encontrado sem retornar outro registro

#### Scenario: Atualizar técnico existente
- **WHEN** um colaborador autorizado atualiza os dados de um Técnico existente
- **THEN** o backend atualiza os campos permitidos e mantém o mesmo `id_tecnico`

### Requirement: Gestão restrita a colaboradores autenticados
As APIs de cadastro, consulta e atualização de Técnicos MUST exigir autenticação válida e autorização de colaborador no backend. A interface MUST NOT ser a única barreira de acesso, e chamadas sem sessão ou com perfil técnico MUST ser rejeitadas.

Os perfis funcionais do MVP são `colaborador` e `tecnico`, por decisão de implementação. Essa decisão não altera nem mapeia automaticamente os papéis existentes `admin` e `member`. O provisionamento será restrito a responsável autorizado, sem signup público para contas da aplicação. Esta Change MUST preservar usuários, papéis e endpoints de autenticação existentes.

#### Scenario: Solicitação sem autenticação
- **WHEN** uma chamada sem identidade autenticada solicita uma operação de gestão de Técnicos
- **THEN** o backend rejeita a chamada sem retornar ou alterar dados de técnicos

#### Scenario: Técnico tenta usar gestão de cadastro
- **WHEN** um usuário autenticado com perfil técnico solicita uma operação de gestão de Técnicos
- **THEN** o backend rejeita a operação por falta de permissão de colaborador

### Requirement: Cadastro compartilhado de uma única assistência técnica
O MVP MUST operar para uma única assistência técnica, com os cadastros de Clientes,
Equipamentos, Técnicos, Ordens de Serviço e Serviços no mesmo ambiente operacional,
acessíveis conforme a autorização funcional. A tabela `tecnico` MUST permanecer
sem `account_id`; os quatro endpoints de gestão MUST compartilhar esse cadastro
entre colaboradores autenticados, sem filtro por empresa. Esta decisão MUST NOT
remover ou enfraquecer a autenticação, os perfis funcionais, o vínculo técnico
exclusivo ou as restrições de identidade e mesma conta do provisionador da etapa 06.
O compartilhamento MUST NOT conceder gestão de Técnicos ao perfil técnico nem
ampliar o acesso do painel além das OS atribuídas.

#### Scenario: Colaborador acessa o cadastro operacional compartilhado
- **WHEN** um colaborador autenticado solicita listagem ou consulta de Técnicos
- **THEN** o backend aplica a autorização funcional e utiliza o cadastro comum da assistência, sem filtro por `account_id`

#### Scenario: Compartilhamento preserva os controles de identidade
- **WHEN** a gestão utiliza o cadastro compartilhado da única assistência
- **THEN** o backend continua exigindo colaborador autenticado e o provisionamento mantém seus controles da etapa 06, incluindo alvo distinto e mesma conta

### Requirement: Interface de gestão em Streamlit
A aplicação MUST oferecer a colaboradores autorizados uma interface Streamlit para cadastrar, listar, consultar e atualizar Técnicos. A interface MUST apresentar somente os campos do modelo e MUST informar falhas de autenticação, autorização ou ausência do registro sem declarar operação não confirmada como sucesso.

#### Scenario: Colaborador utiliza a interface
- **WHEN** um colaborador autenticado abre a gestão de Técnicos
- **THEN** a interface permite as operações especificadas usando os contratos do backend e exibe o identificador gerado após confirmação

#### Scenario: Técnico ou sessão anônima abre gestão
- **WHEN** um técnico ou usuário anônimo tenta abrir ou operar a gestão de Técnicos
- **THEN** a interface não libera as operações e respeita a rejeição de autorização do backend
