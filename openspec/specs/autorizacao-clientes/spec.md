# autorizacao-clientes Specification

## Purpose

Restringir a administração de Clientes a colaboradores autenticados, preservando os contratos existentes e impedindo acesso direto por identidades sem autorização.

## Requirements

### Requirement: Autenticação e perfil obrigatórios

As cinco operações POST/GET coleção e GET/PUT/DELETE individual MUST exigir token Bearer válido e perfil funcional colaborador antes do acesso a dados. Papel legado, parâmetros enviados e associação técnica MUST NOT conceder acesso administrativo.

#### Scenario: Colaborador autenticado
- **WHEN** o token identifica usuário com perfil funcional colaborador
- **THEN** a operação segue as validações e contratos originais

#### Scenario: Acesso sem autorização
- **WHEN** o token está ausente/inválido ou a identidade é técnica/sem perfil funcional
- **THEN** nenhuma leitura administrativa ou escrita de Cliente é permitida

### Requirement: Preservação do contrato de negócio

A proteção MUST preservar rotas, GUIDs, campos, respostas, validações e bloqueio de exclusão por Equipamentos, sem criar recursos de outros módulos.

#### Scenario: Cliente com Equipamentos
- **WHEN** colaborador solicita exclusão de Cliente vinculado
- **THEN** o bloqueio original continua aplicável sem cascata

### Requirement: Sessão no frontend

O frontend MUST enviar o token da sessão nas cinco operações e confirmações, rejeitar token ausente antes de HTTP, encerrar sessão/cache em 401 e interromper acesso em 403. Falhas MUST NOT causar reenvio automático ou exibir dados anteriores como resultado autorizado.

#### Scenario: Falha de autorização em confirmação
- **WHEN** GET após PUT/DELETE retorna 401 ou 403
- **THEN** sucesso não é anunciado, acesso é interrompido e a escrita não é repetida
