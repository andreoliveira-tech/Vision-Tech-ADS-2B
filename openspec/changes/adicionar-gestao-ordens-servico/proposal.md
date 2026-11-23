# Proposal

## Estado atualizado das dependências (2026-11-13)

As tabelas Técnico/OS, os guards e os grupos já estão publicados. A etapa 06 tem
os Grupos 1–4 concluídos; o perfil é resolvido por `user_application_profile` e o
vínculo por `user_tecnico`, mantendo `user.role=admin/member` intacto. As referências
abaixo à inexistência dessas estruturas ou à extensão de `user` são históricas e
foram substituídas pela arquitetura aprovada. Os endpoints de negócio e a
integração Streamlit desta Change continuam pendentes, assim como concorrência e
rollback do provisionador. Ver [estado e plano](../../../docs/progresso-mvp.md).

## Why

O modelo global prevê OS vinculadas a Equipamento e Técnico, mas ainda não há tabela ou APIs de Ordens de Serviço locais. Implementá-las é necessário para permitir o gerenciamento colaborativo e sustentar o acesso restrito do técnico às ordens atribuídas.

## What Changes

- Criar tabela e APIs locais XanoScript para OS, preservando exatamente `id_os`, `data_entrada`, `data_saida`, `problema_relatado`, `status`, `valor_total`, `id_equipamento` e `id_tecnico`.
- Preservar os cinco status do modelo: Aguardando avaliação, Em manutenção, Aguardando peça, Concluído e Entregue; validar pertinência do status, sem definir transições.
- Validar no backend a existência de Equipamento e Técnico antes de cadastrar/atualizar OS.
- Proteger operações gerais de cadastro, listagem, consulta e atualização para colaboradores autenticados.
- Fornecer consulta de OS do próprio técnico e atualização somente do status de OS atribuída, filtrando pelo vínculo da identidade autenticada e negando acesso a OS alheia.
- Estender localmente o esquema técnico de autenticação com os identificadores de perfil `colaborador` e `tecnico` e o vínculo opcional `user.id_tecnico`, preservando `admin`/`member` e sem alterar contas ou signup.
- Criar cliente HTTP e interface Streamlit para colaboradores gerenciarem OS.
- Criar testes locais de contratos, vínculos e autorização com transporte simulado; não declarar testes remotos.

Fora do escopo: implementar login, provisionar/alterar contas existentes, alterar signup, Serviços de uma OS, exclusão de OS, publicação no Xano e regras de transição de status.

## Capabilities

### New Capabilities

- `gestao-ordens-servico`: cadastro, consulta e atualização de OS, integridade referencial, gestão de colaboradores e acesso limitado do Técnico às ordens atribuídas.

### Modified Capabilities

Nenhuma. A Change `acesso-tecnico-ordens-servico` já especifica acesso às OS atribuídas; esta Change implementa a persistência e os endpoints dos quais aquela capacidade depende.

## Impact

- Backend: tabela `ordem_servico`, grupo/endpoints XanoScript e funções de validação/autorização; extensão local do esquema técnico `user` para papéis funcionais e associação a Técnico.
- Frontend: cliente HTTP e página Streamlit de gestão para colaborador.
- Dependências: tabela `equipamento` e API local existentes; tabela `tecnico` criada localmente em `adicionar-gestao-tecnicos`; perfis funcionais definidos no design de `acesso-tecnico-ordens-servico`.
- Limite de integração: no Xano atual, `user.role` contém somente `admin` e `member`, não existe `user.id_tecnico`, e a tabela Técnico ainda não está publicada. As definições locais acrescentam suporte aos novos perfis sem apagar os antigos e nunca concedem equivalência automática. Contas e signup permanecem intactos. Nada será publicado remotamente.
