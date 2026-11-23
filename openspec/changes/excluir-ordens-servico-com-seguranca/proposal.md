# Proposal

## Dependência de liberação — atualização 19/11, contador 375

Implementação sequencial local em 8/13 tarefas; leitura autorizada confirmou os
dois recursos ainda ausentes e as 81 definições preservadas. Esta Change depende
de `proteger-integridade-exclusoes-concorrentes` para coordenar DELETE com
POST/PUT de Serviços. Os cinco UPDATEs de escritores pertencem à nova Change;
esta seleção continua somente helper+DELETE novos, sem UPDATE implícito.
O texto abaixo registra a proposta original; esta atualização é documental,
sem liberação ou autorização de publicação.

## Why

A exclusão de OS faz parte do escopo original, mas ainda não existe nas fontes
do backend nem na tela. Serviços já publicados/homologados dependem da OS;
excluir sem conferir esse vínculo deixaria registros órfãos.

## What Changes

- Acrescentar DELETE /ordens-servico/{id_os}, com Bearer e perfil colaborador.
- Bloquear OS com qualquer Serviço; permitir somente OS sem Serviços.
- Preservar Equipamento, Técnico, Cliente, outras OS e todos os Serviços;
  sem cascade, mudança de status, total ou dependências.
- Acrescentar ação confirmada na tela Streamlit e GET posterior de ausência,
  bloqueando reenvio em resultado incerto.
- Preparar pacote aditivo, testes e roteiro próprio sem repetir OS B–F.

## Capabilities

### New Capabilities

- `exclusao-ordens-servico`: exclusão administrativa de OS sem Serviços,
  autorização no servidor, preservação e confirmação Streamlit.

### Modified Capabilities

Nenhuma spec principal muda. `gestao-ordens-servico` está em Change aberta;
`gestao-servicos` já foi sincronizada e arquivada. Manter seus contratos e
incorporar somente exclusão; a garantia concorrente está na nova Change citada.

## Impact

Helper proposto `ordens/consultar_dependencias` e um DELETE no grupo existente;
frontend/ordens_api.py e ordens_ui.py, testes e pacote seletivo. Reutilizar
ordens/autorizar_colaborador, ordem_servico, servico e configuração vigente.
Não modificar painel técnico, seus GET/PATCH, helpers ou tabelas existentes.

Somente planejamento local, contador 374, sem HTTP. Serviços depende de OS;
esta proposta não autoriza removê-los para liberar exclusão. Não adicionar
restrição por status ou entidade nova. Concorrência entre criação de Serviço
e DELETE de OS é questão técnica impeditiva da liberação até conferência,
sem prometer atomicidade por pré-consulta ou pelo push transacional.
