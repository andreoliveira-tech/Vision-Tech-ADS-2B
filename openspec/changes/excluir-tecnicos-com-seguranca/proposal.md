# Proposal

## Dependência de liberação — atualização 19/11, contador 375

Implementação sequencial local em 8/13 tarefas; leitura autorizada confirmou os
dois recursos ainda ausentes e as 81 definições preservadas. Esta Change depende
de `proteger-integridade-exclusoes-concorrentes` para coordenar DELETE com
POST/PUT de OS e provisionamento. Os cinco UPDATEs de escritores pertencem à
nova Change, não à seleção aditiva deste pacote. Preparação documental somente;
nenhuma autorização de publicação ou dispensa da fixture isolada de identidade.
O texto abaixo registra o escopo original, preservado.

## Why

O MVP prevê excluir Técnicos, mas as fontes atuais oferecem somente POST,
GET e PUT. OS e vínculos de identidade já existem; a exclusão só pode ser
oferecida preservando essas referências.

## What Changes

- Acrescentar DELETE /tecnicos/{id_tecnico}, autenticado e restrito a colaborador.
- Bloquear se existir OS de qualquer status ou vínculo em user_tecnico.
- Excluir somente Técnico sem dependências, sem cascade ou desprovisionamento.
- Acrescentar ação explícita na tela Streamlit, com confirmação e GET de ausência;
  resultado incerto bloqueia reenvio até conferência explícita.
- Preparar seleção aditiva, testes locais e homologação delimitada.

## Capabilities

### New Capabilities

- `exclusao-tecnicos`: exclusão administrativa de Técnico com verificação de
  dependências de OS e identidade, preservação e confirmação pela interface.

### Modified Capabilities

Nenhuma spec principal muda. `gestao-tecnicos` está em Change não arquivada;
esta capacidade complementa seu CRUD, sem substituir contratos existentes.

## Impact

Propostos helper `tecnicos/consultar_dependencias` e um endpoint DELETE no grupo
existente. Integração em frontend/tecnicos_api.py e tecnicos_ui.py; reutilizar
tecnicos/autorizar_colaborador, tabelas tecnico/ordem_servico/user_tecnico e
configuração vigente. Sem novos campos, tabelas, perfis, módulos ou bibliotecas.

Esta etapa prepara artefatos apenas. Contador 374; zero chamadas remotas.
Ausência reconferida por metadados no contador 375. A seleção aditiva desta
Change não pode modificar recursos existentes; os escritores terão seleção e
aprovação próprias na Change de integridade. Condições de concorrência precisam de
verificação técnica antes da liberação; não atribuir garantia a pré-consulta.
Não encerrar pendências de homologação da Change original de Técnicos.
