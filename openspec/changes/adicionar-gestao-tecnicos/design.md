# Design

## Preparação de retomada em 20/11/2026

Fonte dedicada de credencial do usuário fictício 3 deve substituir a seleção
histórica em um futuro roteiro novo, sem fallback nem alteração do executor
preservado como evidência. A política de descritores públicos foi implementada
e testada somente em memória: dez testes, sem ler credenciais, DPAPI ou rede.
Ver `docs/tecnicos-fonte-credencial-offline-20261120.md`. Não foi integrado leitor
real, e a causa do login 403 antigo continua indeterminada. Contador 377.
Antes de execução remota, revisar baseline, auditoria e orçamento E07, incluindo
as 15 chamadas históricas; preparar roteiro simulado e obter autorização própria.
Intervalo vigente para propostas futuras: mínimo dez segundos, substituindo a
referência histórica de cinco segundos abaixo. Não repetir login nem liberar
DELETEs por esta preparação; requisitos de runtime e tarefas abertas preservados.

## Homologação planejada E07 (2026-11-16)

As quatro APIs já existem em `149143/v1`; não executar a migração histórica
abaixo. A [revisão E07](../../../docs/revisao-etapa07.md) identifica os GUIDs e as
evidências locais. O [roteiro de homologação](../../../docs/plano-homologacao-etapa07.md)
define grupos A–F, dados fictícios, resultados esperados, retenção de duas
fixtures e teto de 137 chamadas. As tarefas de integração continuam abertas.

O portal revalida `auth/me` em reruns; login e confirmação de PUT disparam
sequências de chamadas. O grupo de UI depende de executor de teste que serialize
o transporte real, conte chamadas e mantenha cinco segundos após cada resposta,
sem mocks ou repetição automática. Esse executor foi implementado e verificado
localmente na tarefa 5.2; seus [controles e limites](../../../docs/executor-homologacao-etapa07.md)
não substituem o roteiro de execução autorizado. Não alterar autenticação ou regras do produto para
viabilizar o teste. Preparar o plano não comprova homologação nem autoriza
login, publicação ou escrita remota. Os requisitos da spec permanecem iguais.

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

## Context

Consulte [proposal.md](proposal.md) para motivação e [spec.md](specs/gestao-tecnicos/spec.md) para os contratos observáveis.

O inventário autorizado da branch `v1` do workspace `149143` encontrou `user`, `equipamento` e `cliente`, mas não `tecnico`. A tabela de autenticação atual possui os perfis `admin` e `member`. Os perfis funcionais escolhidos para a aplicação são `colaborador` e `tecnico`; a compatibilidade de provisionamento permanece dependente de uma mudança de autenticação separada. O cadastro Técnico não duplica a identidade autenticada.

## Goals / Non-Goals

**Goals:** criar persistência e APIs para o cadastro Técnico, expor gestão por Streamlit e manter o contrato de campos do professor.

**Non-Goals:** implementar login, alterar autenticação/perfis/provisionamento ou persistir vínculo de conta; criar OS/Serviço; disponibilizar painel do técnico; excluir técnicos antes de haver integridade verificável com OS.

## Decisions

### Estrutura Xano

Criar tabela física `tecnico` com identificador nativo `id` mapeado para o identificador conceitual `id_tecnico`; preservar `nome`, `especialidade`, `telefone` e `email`. Não incluir `password`, `role`, `account_id`, status de ativo ou outro campo na entidade de domínio. Decisão de implementação do MVP, aprovada pelo responsável e não atribuída ao professor: os quatro campos descritivos são obrigatórios; `email` usa o tipo nativo Xano `email` para validar formato; email não recebe índice exclusivo. Não acrescentar validações de negócio extras.

### APIs e autorização

Seguir o padrão de APIs Xano versionáveis com operações POST/GET de lista/GET por ID/PUT. Não criar DELETE nesta Change: como a tabela de OS não existe, não há como verificar atribuições ou garantir que a exclusão não deixe referências órfãs. Retomar exclusão somente junto da implementação da integridade Técnico–OS.

As APIs de gestão usam `auth = "user"` e uma verificação no servidor de que `$auth.id` pertence a registro cujo perfil funcional seja `colaborador`. A identidade é lida do token, nunca do corpo. O inventário remoto encontrou somente `admin` e `member`, que não são equivalentes aos perfis funcionais. Por instrução explícita, esta Change não altera a tabela de autenticação, usuários, signup nem endpoints existentes. A checagem local exige o literal `colaborador` e falha fechada para `admin`/`member`; as operações reais permanecerão indisponíveis até a Change de autenticação implementar perfis e provisionamento autorizado. Contas da aplicação só podem ser provisionadas por responsável autorizado.

### Interface Streamlit

Adicionar página no módulo Streamlit existente, consumir um URL base configurado externamente para o grupo Xano de Técnicos e reutilizar padrões HTTP existentes. A interface não determina a identidade ou autorização localmente; todas as operações ficam sujeitas à decisão do backend. Não introduzir framework ou dependência de frontend adicional.

### Dependências com OS, identidade e painel

Esta Change deve criar `tecnico` antes da futura Ordem de Serviço, que precisará referenciar `tecnico.id` e `equipamento.id`. A tabela de identidade `user` deve ser associada a `tecnico.id` em `acesso-tecnico-ordens-servico` depois da criação do cadastro, sem acrescentar credenciais à entidade Técnico. O painel só pode ser implementado depois de uma Change própria criar a persistência e as APIs de OS com `id_tecnico`, `id_equipamento`, `problema_relatado` e `status`. Ainda não foi encontrada uma Change de gestão de OS; essa dependência continua por planejar.

## Risks / Trade-offs

- [Perfis funcionais ainda não provisionáveis no Xano atual] → manter guarda local que exige `colaborador` e falha fechada; implementar perfis/provisionamento em Change autorizada antes de liberar as APIs.
- [OS ainda não existe] → não implementar exclusão nesta Change; evitar referências órfãs e planejar a regra quando a relação Técnico–OS for construída.
- [Obrigatoriedade é decisão do MVP, não requisito do professor] → manter essa distinção explícita e não acrescentar unicidade ou validações além de email válido/campos obrigatórios.
- [Painel depende de recursos ainda ausentes] → não incluir OS, auth ou painel no escopo desta Change; registrar a dependência para a próxima sequência.

## Situação de implementação e dependências pendentes

O responsável do projeto resolveu a ambiguidade para o MVP: `nome`, `especialidade`, `telefone` e `email` obrigatórios; email válido; sem unicidade. Essa é uma decisão de implementação, não uma exigência original do professor. O identificador físico `id` é gerado pelo Xano e representa `id_tecnico`.

Os perfis funcionais escolhidos para o MVP são `colaborador` e `tecnico`; colaborador gerenciará Técnicos e futuramente OS, e técnico acessará somente suas OS atribuídas. O inventário remoto anterior encontrou `admin` e `member`, sem evidência de equivalência. Por instrução explícita, os recursos de autenticação, papéis e usuários existentes permanecem intocados nesta Change, inclusive signup público. As APIs locais têm guarda autenticada que exige `colaborador`, mas nenhum perfil atual pode satisfazê-la; portanto, falham fechadas até implementação autorizada da Change de autenticação. O provisionamento de contas da aplicação deve ser restrito a responsável autorizado.

O cliente HTTP recebe somente token de sessão real do fluxo de autenticação; não cria nem simula sessão. A página não libera operações quando o token não está disponível e continua dependendo da autorização Xano. Somente a tabela Técnico está publicada e verificada no Xano. As definições de APIs, funções, autenticação e painel permanecem locais e não são consideradas integradas antes de publicação autorizada e verificação remota própria.

## Migration Plan

O plano original previa não publicar nem migrar nesta Change. Por autorização posterior e específica do responsável, a tabela Técnico foi publicada como etapa 01 isolada; essa autorização não abrange as etapas seguintes. A ordem restante é: (1) publicar a tabela Ordem de Serviço; (2) aplicar a alteração aditiva em `user` somente após revisão dos efeitos; (3) publicar funções de autorização e grupos; (4) publicar autenticação/provisionamento; (5) publicar gestão de Técnicos e OS; (6) publicar o painel técnico; (7) validar os contratos e a autorização em execução real. Cada etapa requer autorização própria e verificação antes de prosseguir. A associação da identidade e o painel continuam dependentes das Changes de autenticação e OS.
