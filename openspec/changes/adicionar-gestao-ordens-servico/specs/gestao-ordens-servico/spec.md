# Spec Delta

## Purpose

Permite gerenciar Ordens de Serviço ligadas a Equipamentos e Técnicos existentes e aplicar autorização de colaborador e técnico no backend.

## ADDED Requirements

### Requirement: Recuperação explícita da gestão de OS
A interface MUST renovar campos a cada carregamento, invalidar resultados antigos ao consultar e consumir o carregamento em cada tentativa de atualização. MUST NOT reenviar escrita por rerun; após falha ou confirmação divergente, MUST exigir novo carregamento antes de outra atualização.

#### Scenario: Troca ou recarga de OS
- **WHEN** outra OS ou o mesmo ID é carregado novamente
- **THEN** os campos de edição refletem a resposta atual, sem preservar valores anteriores

#### Scenario: Atualização incerta ou confirmação incompatível
- **WHEN** a atualização falha ou sua resposta/consulta posterior diverge dos dados enviados
- **THEN** a interface não declara sucesso, invalida o carregamento e exige recarga explícita sem retry

#### Scenario: Falha de listagem
- **WHEN** uma nova consulta de listagem falha
- **THEN** a lista anterior não é exibida como resultado atual e a falha não dispara repetição por rerun

### Requirement: Ordem de Serviço preserva os campos e estados originais
O sistema MUST representar uma OS somente com `id_os`, `data_entrada`, `data_saida`, `problema_relatado`, `status`, `valor_total`, `id_equipamento` e `id_tecnico`. O identificador MUST ser gerado pelo backend. O status MUST ser exatamente um dos cinco valores do domínio: `Aguardando avaliação`, `Em manutenção`, `Aguardando peça`, `Concluído` ou `Entregue`. O sistema MUST NOT adicionar estados ou regras de transição.

#### Scenario: Criar OS
- **WHEN** um colaborador autorizado envia os dados de uma OS e referências válidas a Equipamento e Técnico
- **THEN** o backend cria a OS com ID gerado e os campos permitidos

#### Scenario: Rejeitar status fora do domínio
- **WHEN** uma solicitação envia um status não listado no domínio
- **THEN** o backend rejeita a solicitação sem criar ou alterar a OS

#### Scenario: Não aceitar ID definido pelo cliente
- **WHEN** o cliente tenta definir `id_os` no cadastro ou alterar o ID pela atualização
- **THEN** o backend ignora ou rejeita o valor enviado e preserva o identificador gerado

### Requirement: Vínculos de OS referenciam registros existentes
Cada OS MUST referenciar um Equipamento e um Técnico existentes. O backend MUST validar ambos os registros antes de cadastrar ou alterar uma OS. Uma referência inexistente MUST ser rejeitada sem persistência parcial.

#### Scenario: Equipamento ou Técnico inexistente
- **WHEN** uma operação de cadastro ou atualização contém um `id_equipamento` ou `id_tecnico` sem registro correspondente
- **THEN** o backend rejeita a operação e não cria nem altera a OS

#### Scenario: Referências válidas
- **WHEN** ambos os IDs apontam para registros existentes
- **THEN** a OS conserva os relacionamentos com os registros correspondentes

### Requirement: Colaborador gerencia Ordens de Serviço
As operações de cadastro, listagem geral, consulta individual e atualização completa MUST exigir autenticação válida e perfil funcional `colaborador` verificado no backend. Os perfis existentes `admin` e `member` MUST NOT ser considerados equivalentes automaticamente. Usuários anônimos, técnicos e outros perfis MUST ser rejeitados.

#### Scenario: Colaborador autorizado gerencia OS
- **WHEN** um colaborador autenticado executa uma operação geral de OS
- **THEN** o backend permite a operação após validar suas referências e campos

#### Scenario: Perfil sem autorização tenta gerenciar OS
- **WHEN** uma sessão anônima ou autenticada como `tecnico`, `admin` ou `member` chama uma operação geral
- **THEN** o backend rejeita a chamada sem retornar dados gerais nem alterar registros

### Requirement: Técnico consulta somente suas OS
O sistema MUST resolver `id_tecnico` a partir da identidade autenticada associada e MUST retornar somente OS cujo `id_tecnico` seja igual ao vínculo resolvido. Consulta por ID MUST aplicar a mesma restrição. O cliente MUST NOT escolher ou substituir esse vínculo.

#### Scenario: Técnico consulta OS atribuídas
- **WHEN** o técnico autenticado lista suas OS
- **THEN** o backend retorna somente OS atribuídas ao `id_tecnico` ligado à sua identidade

#### Scenario: Técnico tenta consultar OS de outra pessoa
- **WHEN** o técnico solicita por ID uma OS atribuída a outro técnico
- **THEN** o backend rejeita ou omite a OS sem revelar seus dados

#### Scenario: Técnico sem vínculo válido
- **WHEN** a identidade não tem perfil `tecnico`, vínculo `id_tecnico` ou registro Técnico válido
- **THEN** o backend nega a consulta sem retornar OS

### Requirement: Técnico altera exclusivamente o status da própria OS
O sistema MUST oferecer uma operação autenticada que permita ao técnico alterar somente `status` de OS atribuída ao seu `id_tecnico`. O backend MUST validar o status contra os cinco valores do domínio e MUST rejeitar OS de outro técnico ou alterações a qualquer outro campo. Nenhuma regra de transição entre estados deve ser aplicada.

#### Scenario: Técnico atualiza status de OS atribuída
- **WHEN** o técnico autenticado envia um dos cinco estados para OS atribuída
- **THEN** o backend persiste e retorna o status confirmado, sem alterar outros campos

#### Scenario: Técnico envia status inválido ou campo adicional
- **WHEN** a operação contém status fora do domínio ou campos além de `status`
- **THEN** o backend rejeita a operação e preserva a OS

#### Scenario: Técnico altera OS de outro técnico
- **WHEN** o técnico tenta alterar status de OS não atribuída a ele
- **THEN** o backend rejeita a operação sem alterar a OS

### Requirement: Interface Streamlit de gestão para colaboradores
A aplicação MUST oferecer em Streamlit cadastro, listagem, consulta e atualização completa de OS para colaboradores autorizados. Deve apresentar os oito campos do domínio, preservar o ID e informar resultados apenas após confirmação da API. Falhas de autenticação, autorização, vínculo ou registro ausente MUST ser apresentadas sem declarar sucesso.

#### Scenario: Colaborador usa a tela de gestão
- **WHEN** um colaborador autorizado cadastra, consulta ou atualiza uma OS pela tela
- **THEN** a interface chama os endpoints correspondentes e apresenta a resposta confirmada

#### Scenario: Usuário sem token ou permissão acessa a tela
- **WHEN** a sessão está ausente, expirada ou sem permissão
- **THEN** a interface não apresenta sucesso e informa a necessidade de autenticação ou autorização
