# Proposal

## Preparação de homologação E07 (2026-11-16)

Os quatro endpoints de Técnicos foram encontrados em `149143/v1` e conferidos
contra o pacote na revisão E07. As afirmações históricas abaixo sobre ausência
dessas APIs não descrevem o estado atual; não republicar recursos.
O [plano E07](../../../docs/plano-homologacao-etapa07.md) delimita a verificação
das permissões e da integração Streamlit já previstas nesta Change: contas
fictícias existentes, duas fixtures novas retidas, chamadas limitadas e nenhum
novo recurso de domínio. Sua preparação não autoriza execução remota.

## Estado atualizado das dependências (2026-11-13)

As tabelas Técnico/OS, os guards e os grupos já estão publicados. A etapa 06 tem
os Grupos 1–4 concluídos; o perfil é resolvido por `user_application_profile` e o
vínculo por `user_tecnico`, mantendo `user.role=admin/member` intacto. As referências
abaixo à inexistência dessas estruturas ou à extensão de `user` são históricas e
foram substituídas pela arquitetura aprovada. Os endpoints de negócio e a
integração Streamlit desta Change continuam pendentes, assim como concorrência e
rollback do provisionador. Ver [estado e plano](../../../docs/progresso-mvp.md).

## Decisão aprovada: uma única assistência técnica (2026-11-13)

O MVP atende uma única assistência técnica. Clientes, Equipamentos, Técnicos,
Ordens de Serviço e Serviços pertencem ao mesmo ambiente operacional, compartilhado
pelos usuários funcionalmente autorizados. Não há isolamento entre empresas neste
MVP. A tabela `tecnico` não possui `account_id` por essa decisão; os quatro endpoints
da etapa 07 permanecem inalterados e a gestão exige autenticação Xano válida e
perfil funcional `colaborador` no backend.

Essa decisão não remove nem enfraquece os controles da etapa 06: identidade pelo
token, perfis em `user_application_profile`, vínculo técnico exclusivo em
`user_tecnico` e provisionamento restrito continuam vigentes. O provisionador
continua exigindo administrador com perfil colaborador e
`pode_provisionar_perfis=true`, alvo distinto e da mesma conta. As contas técnicas
existentes, inclusive a Conta B fictícia E06, não representam empresas operacionais
separadas no MVP e não serão removidas ou alteradas por esta decisão. Técnicos
continuam restritos às OS atribuídas no painel previsto; compartilhar o cadastro
não concede acesso administrativo ao perfil técnico.

Esta atualização é documental: não modifica endpoints, tabelas, usuários ou dados,
nem comprova integração remota, concorrência ou rollback por falha de banco.

## Why

O modelo de domínio define Técnico como responsável pelas ordens de serviço, mas a entidade e suas APIs ainda não existem no workspace Xano. Implementar o cadastro de técnicos cria a base necessária para atribuições futuras e para associar a identidade autenticada ao registro de Técnico existente.

## What Changes

- Criar no Xano a entidade Técnico usando somente os campos definidos pelo professor: `id_tecnico`, `nome`, `especialidade`, `telefone` e `email`.
- Disponibilizar cadastro, listagem, consulta e atualização de técnicos por APIs Xano protegidas para colaboradores.
- Criar módulo Streamlit para colaboradores gerenciarem os campos do cadastro Técnico.
- Para o MVP, tratar `nome`, `especialidade`, `telefone` e `email` como obrigatórios; validar o formato de `email`, sem impor unicidade.
- Usar os perfis funcionais `colaborador` e `tecnico`; exigir token Xano e autorização de colaborador nas APIs. O provisionamento de contas será restrito a responsável autorizado.
- Não incluir credenciais, perfil de login ou atributos adicionais na entidade Técnico.
- Adiar exclusão de técnicos até que a entidade Ordem de Serviço e sua integridade referencial existam; não permitir exclusão que possa deixar OS órfã.

Fora do escopo: implementar login e provisionamento de usuários, alterar perfis, usuários ou endpoints de autenticação existentes, associação persistida entre conta e técnico, criação de Ordens de Serviço ou Serviços, painel do técnico e publicação remota. Os endpoints locais dependem de implementação autorizada dos perfis e provisionamento na Change de autenticação.

## Capabilities

### New Capabilities

- `gestao-tecnicos`: cadastro, listagem, consulta e atualização da entidade Técnico, mantendo os campos do modelo global e o acesso restrito a colaboradores autenticados.

### Modified Capabilities

Nenhuma. As capacidades especificadas atualmente cobrem Clientes e acesso individual do Técnico; esta Change define uma nova capacidade de gestão da entidade Técnico.

## Impact

- Backend: tabela e APIs Xano para Técnico; não há atualmente tabela Técnico nem APIs correspondentes no workspace `149143`, branch `v1`.
- Frontend: novo módulo Streamlit preparado para consumir o contrato Xano definido localmente; não há integração funcional até publicar e validar os endpoints.
- Domínio: preservar os cinco atributos existentes em `docs/domain-model.md`; não criar entidade de Usuário de negócio nem acrescentar atributos a Técnico.
- Dependências: endpoints de gestão exigem um contrato de autenticação e autorização para colaboradores definido em `acesso-tecnico-ordens-servico`. A futura Ordem de Serviço dependerá de Técnico e Equipamento; o painel definido nessa Change dependerá também das APIs e campos de OS. O vínculo da identidade do técnico ao `id_tecnico` será tratado em `acesso-tecnico-ordens-servico`, não duplicado aqui.
- Decisões do MVP, aprovadas pelo responsável e não atribuídas ao professor: perfis funcionais `colaborador` e `tecnico`; quatro campos descritivos obrigatórios; email válido e não exclusivo; identificador gerado pelo Xano; provisionamento restrito a responsável autorizado. O backend atual só declara `admin` e `member`; as APIs locais não os tratam como equivalentes e falham fechadas até a Change de autenticação.
- A tabela Equipamento existe no Xano, mas sua API ainda não está publicada. A gestão de Técnico não depende dessa API; a futura consulta do painel pode obter os dados necessários de Equipamento no backend através do relacionamento da OS.
