# Proposal

## Why

O escopo original inclui Serviços vinculados às Ordens de Serviço, mas não há
fontes locais de tabela, APIs ou tela desse módulo. Sem esse fluxo o atendimento
não registra os serviços realizados e o MVP permanece incompleto.

## What Changes

- Representar Serviço somente com `id_servico`, `descricao`, `valor`, `id_os`;
  ID gerado pelo Xano e vínculo obrigatório com OS existente.
- Oferecer cinco endpoints de CRUD, protegidos por Bearer e perfil funcional
  colaborador com o guard vigente de `user_application_profile`.
- Integrar cliente HTTP e tela Streamlit à navegação administrativa, incluindo
  listagem dos serviços associados a uma OS e confirmações de escrita.
- Preparar seleção de publicação por dependências, testes offline e homologação
  remota delimitada, mantendo as funcionalidades já aprovadas.

## Capabilities

### New Capabilities

- `gestao-servicos`: CRUD autenticado de Serviços, vínculo com OS e interface
  administrativa Streamlit, sem cálculo automático do valor total da OS.

### Modified Capabilities

Nenhuma capacidade principal existente muda de requisito nesta Change.

## Impact

Planejar tabela `servico`, grupo Serviços, helpers próprios necessários e cinco
endpoints; `frontend/servicos_api.py`, `servicos_ui.py`, página de entrada,
configuração externa, navegação e limpeza de estado de sessão. Reutilizar OS,
usuários, perfis e guard existentes; não republicá-los.

Não há nova coleta remota: existência/ausência desses recursos no Xano ainda
precisa ser reconciliada antes de propor CREATE/UPDATE. Não introduzir descontos,
catálogo, novas entidades, permissões técnicas, soma automática, exclusão de OS,
reestilização global ou alterações em outros contratos. Meta global 23/11/2026;
contador permanece 301 durante o planejamento. A presente etapa cria apenas
artefatos; implementação e operações remotas são etapas distintas.
