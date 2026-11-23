# Proposal

## Correção local de signup autorizada em 21/11/2026

Limitar somente metadata da auditoria de auth/signup aos mesmos seis campos
explícitos do login. Preservar o cadastro legado, sem conceder perfil ou vínculo,
e preparar um UPDATE seletivo local. Não implementar cadastro público na UI,
alterar helper, limpar logs ou publicar nesta etapa. Contador 626.

## Atualização de evidências (2026-11-13)

As etapas 01–06 estão publicadas e os Grupos 1–4 da etapa 06 foram concluídos em
`149143/v1`; as etapas 07–09 continuam sem endpoints de negócio publicados.
Os resultados e o plano de continuidade estão em
[progresso-mvp.md](../../../docs/progresso-mvp.md). Os relatos de inventários,
previews cancelados e preparação local abaixo são históricos: não representam o
estado atual nem autorização de execução.

A arquitetura vigente preserva `user.role=admin/member`, usa
`user_application_profile` e `user_tecnico`, e não altera as cinco entidades.
Os testes sequenciais não comprovam concorrência, rollback por falha DB ou
mapeamento de conflitos UNIQUE. Integração real de OS e do portal segue pendente.

## Why

O projeto ainda não possui autenticação nem separação de acesso, embora a operação exija uma área individual para o técnico acompanhar as ordens atribuídas. Esta Change especifica login de colaboradores e técnicos e o acompanhamento dessas ordens, preservando o domínio existente.

## What Changes

- Adicionar autenticação real para os perfis colaborador e técnico, com permissões distintas aplicadas no backend.
- Associar a identidade autenticada do técnico ao registro existente de Técnico; limitar os dados de OS aos registros cujo `id_tecnico` corresponda a essa associação.
- Criar uma área Streamlit para o técnico consultar ordens atribuídas, exibindo equipamento, problema relatado e status.
- Permitir atualização de status pelo técnico apenas nas OS atribuídas e conforme regras autorizadas pelo backend; colaboradores mantêm permissões operacionais mais amplas.
- Definir planejamento de integração com autenticação e APIs reais do Xano. Não simular login nem tratar controles de interface como autorização.
- Correção isolada autorizada após o Grupo 2: limitar a auditoria de `auth/login` aos seis campos legados explícitos, excluindo o campo de senha sem alterar validação de credenciais, emissão do token ou resposta. Publicação depende de aprovação específica do preview. Revisão de `auth/signup` fica pendente, fora desta correção.

Fora do escopo: criação de novas entidades de negócio, cadastro público, recuperação de senha, gestão de credenciais, redefinição do fluxo de status e publicação no Xano.

## Capabilities

### New Capabilities

- `acesso-tecnico`: autenticação com perfis distintos, vínculo da identidade do técnico ao cadastro existente e acompanhamento restrito das OS atribuídas.

### Modified Capabilities

Nenhuma. As especificações existentes cobrem apenas operações de clientes; esta Change introduz uma capacidade nova.

## Impact

- Frontend: aplicação Python/Streamlit, tela de login e área protegida do técnico.
- Backend: Xano e APIs autenticadas para sessão/identidade, autorização por perfil, consulta de OS e alteração de status.
- Dados: usar o vínculo conceitual `Ordem de Serviço.id_tecnico`; credenciais e identidade de acesso são infraestrutura de autenticação, não novas entidades do domínio.
- Evidência de planejamento: inventário somente leitura da branch `v1` (live) do workspace `149143` confirmou a tabela `user` com papéis `admin`/`member` e APIs nativas de autenticação. Não encontrou tabelas de Técnico ou Ordem de Serviço nem APIs de Técnico, Ordem de Serviço ou Equipamentos. A tabela Equipamento existe e se relaciona a Cliente, mas não tem API publicada nesse inventário.
- Dependências: [adicionar-gestao-tecnicos](../adicionar-gestao-tecnicos/proposal.md) deverá criar o cadastro Técnico antes da associação de uma identidade técnica. A implementação do painel ainda depende de uma Change que estruture Ordem de Serviço e suas APIs com vínculos a Técnico e Equipamento. A autenticação nativa existente precisa de configuração de perfis e associação; não é uma integração pronta na aplicação Streamlit.
- Nenhuma alteração ou publicação remota é autorizada por esta proposta.
