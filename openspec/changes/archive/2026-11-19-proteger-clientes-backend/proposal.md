# Proposal

## Why

As cinco operações de Clientes não exigem autenticação no inventário protegido.
A navegação protegida do Streamlit não impede acesso direto aos dados.

## What Changes

- **BREAKING**: exigir Bearer válido e perfil funcional colaborador nas cinco rotas existentes.
- Reutilizar o guard publicado que consulta user_application_profile, sem inferir autoridade de user.role.
- Enviar token em todas as operações e confirmações do Streamlit; limpar estado em 401 e bloquear 403 sem retry.
- Preparar cinco UPDATEs pelos GUIDs existentes, preservando integralmente contratos e lógica de negócio.

## Capabilities

### New Capabilities

- `autorizacao-clientes`: autenticação e acesso administrativo aos Clientes, preservando CRUD e integridade existentes.

### Modified Capabilities

Nenhuma alteração aos requisitos de campos, persistência ou dependências existentes.

## Impact

Somente cinco endpoints Clientes, cliente HTTP, tela Clientes, limpeza de sessão,
testes e pacote seletivo. Nenhuma tabela/helper/grupo recriado. Preparação local
autorizada; publicação e homologação remotas dependem de nova autorização. Contador 230.
