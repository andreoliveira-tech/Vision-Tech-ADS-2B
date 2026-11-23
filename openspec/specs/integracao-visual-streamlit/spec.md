# integracao-visual-streamlit Specification

## Purpose

Aplicar a apresentação visual aprovada às telas existentes, preservando navegação por perfil, contratos e estados de operação.

## Requirements

### Requirement: Tema aprovado nas telas reais
O frontend SHALL aplicar o tema claro aceito às telas reais e manter navegação
por perfil, labels, keys, disabled e confirmações sem novas chamadas HTTP.

#### Scenario: Técnico acessa o painel
- **WHEN** um técnico válido abre o painel
- **THEN** apenas sua navegação permanece disponível e suas OS aparecem em cartões
- **AND** atualização de status preserva o formulário e o payload existente

### Requirement: Organização local da gestão de OS
A gestão SHALL separar cadastro e listagem/consulta em abas, com indicadores e
filtros derivados exclusivamente da lista explicitamente carregada.

#### Scenario: Filtrar uma lista já carregada
- **WHEN** o colaborador modifica status, técnico ou busca local
- **THEN** nenhuma consulta de negócio ou escrita adicional é realizada pelo filtro
- **AND** a revalidação auth/me já existente em reruns do portal permanece preservada
- **AND** o alvo de edição/exclusão e suas confirmações continuam independentes

### Requirement: Estados e contratos preservados
A apresentação SHALL manter os valores internos dos cinco status e bloquear
reenvios implícitos após erro/incerteza conforme o comportamento existente.

#### Scenario: Falha de atualização de status
- **WHEN** o painel recebe resultado incerto
- **THEN** o rerun não repete a escrita nem rearma a leitura automaticamente

### Requirement: Verificação e rastreabilidade
O lote SHALL registrar regressões locais, hashes e limitações sem substituir
prova visual das telas alteradas pelo aceite da prévia anterior.

#### Scenario: Consolidação sem rede
- **WHEN** somente AppTest e análise local estão disponíveis
- **THEN** apenas os critérios comprovados são marcados concluídos
- **AND** revisão visual e aceite da integração permanecem pendentes
