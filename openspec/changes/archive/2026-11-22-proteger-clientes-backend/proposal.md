# Proposal — Proteção dos endpoints de Clientes

## Why

Os endpoints de Clientes precisam exigir identidade autenticada e perfil funcional autorizado no backend, sem depender apenas da navegação do Streamlit. Esta consolidação documental registra a solução já implementada e verificada, sem autorizar novas operações.

## What Changes

- Exigir autenticação e perfil `colaborador` nas cinco operações de Clientes.
- Enviar o token da sessão pelo cliente HTTP e interromper o acesso quando a autorização falhar.
- Preservar contratos, validações e bloqueio de exclusão por Equipamentos.

## Capabilities

### New Capabilities

Nenhuma capacidade adicional nesta consolidação documental.

### Modified Capabilities

- `autorizacao-clientes`: registrar retrospectivamente a proteção implementada. A especificação principal já contém os três requisitos; o delta reproduz seu conteúdo integral, sem mudança adicional de comportamento.

## Impact

Implementação existente: cinco endpoints Xano de Clientes, cliente HTTP Python e interface Streamlit. Dependências existentes: autenticação Xano e perfil funcional em `user_application_profile`. Não há alteração das cinco entidades, de relacionamentos ou de outros módulos.

Ficam fora do escopo novas funcionalidades, publicação, liberação de exclusões de Técnicos/OS e comprovação de concorrência ou rollback.

## Verification

As nove tarefas estão concluídas conforme os relatórios de leitura/permissões e escrita/integração referenciados em design.md. Estes artefatos são uma consolidação posterior das evidências existentes, não um planejamento produzido antes da implementação.
