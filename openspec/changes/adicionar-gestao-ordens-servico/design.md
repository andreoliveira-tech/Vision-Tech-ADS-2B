# Design

## Correções locais autorizadas em 2026-11-18

Cada carregamento renova a geração das chaves de edição, inclusive para o mesmo
ID. A tentativa de atualizar consome o carregamento; somente PUT com payload
confirmado e GET correspondente restaura a edição. Erro exige ação de carregar,
sem retry. Listagens antigas são descartadas antes de consultar. Avisos e sucesso
são preservados para renderização após rerun, sem repetir HTTP.

Preparar pacote separado de quatro rotas administrativas e três do painel,
reutilizando grupo, tabelas e helpers observados no baseline. O preview desta
etapa é uma comparação local, não dry-run da CLI nem prova do inventário atual.

## Estado atualizado das dependências (2026-11-13)

As tabelas Técnico/OS, os guards e os grupos já estão publicados. A etapa 06 tem
os Grupos 1–4 concluídos; o perfil é resolvido por `user_application_profile` e o
vínculo por `user_tecnico`, mantendo `user.role=admin/member` intacto. As referências
abaixo à inexistência dessas estruturas ou à extensão de `user` são históricas e
foram substituídas pela arquitetura aprovada. Os endpoints de negócio e a
integração Streamlit desta Change continuam pendentes, assim como concorrência e
rollback do provisionador. Ver [estado e plano](../../../docs/progresso-mvp.md).

## Context

Consulte `proposal.md` e `specs/gestao-ordens-servico/spec.md`. Não há código de OS local nem APIs remotas de OS. As definições locais de `equipamento` e `tecnico` existem. O Xano remoto, conforme inventário somente leitura documentado nas Changes, ainda não tem a tabela `tecnico` nem os endpoints desta Change. A autenticação remota declara apenas `admin` e `member`; a associação `user.id_tecnico` não existe.

## Goals / Non-Goals

**Goals:** implementar localmente persistência, validação de vínculos, endpoints segregados por papel, cliente HTTP e interface de colaborador.

**Non-Goals:** alterar os módulos/APIs de Clientes e Equipamentos; implementar login/signup/provisionamento; editar dados reais ou publicar Xano; criar Serviços, exclusão de OS ou fluxo de transições.

## Decisions

### Modelo físico e campos

Usar tabela física `ordem_servico` com ID nativo `id` exposto como `id_os`. Manter somente os oito atributos do domínio. `data_entrada` e `data_saida` usarão `date`; `valor_total`, `decimal`; problema, `text`; status, `enum` com os cinco valores exatos. `id_equipamento` e `id_tecnico` serão inteiros com referências às tabelas correspondentes. A escolha de `date` (sem horário), decimal e `data_saida` anulável é uma decisão de representação para o MVP: uma OS pode permanecer aberta sem data de saída. Não será validada ordem cronológica entre as datas nem faixa de valor. Essas escolhas não são requisitos adicionais do professor e devem ser revistas se o material acadêmico determinar outra representação.

`data_entrada`, problema, status, valor e ambos os vínculos serão obrigatórios na API. `data_saida` pode ser nula. O status não receberá valor padrão: o colaborador escolhe um dos valores do domínio. Não adicionar campos de auditoria ou relacionamentos com Serviço nesta Change.

### Integridade de relacionamentos

Uma função XanoScript compartilhada consulta `equipamento.id` e `tecnico.id`, validando os dois antes de `db.add`/`db.edit`. Os endpoints não confiam em IDs como prova de existência. Referências ausentes geram rejeição antes de persistir; não há escrita parcial. A tabela declarará FKs e índices não exclusivos para `id_equipamento` e `id_tecnico`.

### Papéis e associação técnica

Cada endpoint privado declara `auth = "user"`. Uma função de autorização busca o perfil pelo `$auth.id`; endpoints gerais exigem exatamente `colaborador`. A consulta técnica deriva o ID apenas do registro de identidade autenticada, nunca de input do cliente. A função de técnico exige perfil `tecnico`, `user.id_tecnico` não nulo e referência a `tecnico.id` existente. Listagem, consulta individual e atualização de status filtram pela mesma associação.

Para viabilizar essa verificação sem nova entidade de negócio, o XanoScript local estenderá a tabela técnica `user`: preservar `admin` e `member`, adicionar os valores funcionais `colaborador` e `tecnico`, e declarar `id_tecnico` opcional com referência a `tecnico`. Isso não cria contas, não muda registros, não modifica signup e não atribui equivalência entre papéis. A futura Change de autenticação/provisionamento deve implementar e testar a atribuição restrita desses perfis/vínculos antes da integração. O esquema remoto permanece incompatível até publicação autorizada.

### Contratos e Streamlit

Grupo local `assistencia-tecnica-ordens-servico`: `POST /ordens-servico`, `GET /ordens-servico`, `GET/PUT /ordens-servico/{id_os}` para colaboradores; `GET /minhas-ordens`, `GET /minhas-ordens/{id_os}` e `PATCH /minhas-ordens/{id_os}/status` para técnicos. O PATCH recebe somente `status`; não há endpoint DELETE.

O cliente envia Bearer token recebido de sessão real. A tela de colaborador usa URL externa, valida respostas e não declara sucesso sem resposta confirmada. O contrato da tela técnica permanece fora do escopo visual desta Change, mas seus endpoints ficam disponíveis para a futura área prevista em `acesso-tecnico-ordens-servico`.

## Risks / Trade-offs

- [Papéis e vínculo ausentes na autenticação remota] → adicionar somente definições locais, preservar papéis antigos e falhar fechado; não publicar até a Change de autenticação provisionar e validar colaborador/técnico.
- [Tabelas dependentes ainda não publicadas juntas] → publicar Técnico antes de OS e testar as referências no ambiente autorizado.
- [Representação temporal/monetária não definida pelo domínio] → documentar `date`, decimal e nulabilidade de `data_saida` como escolhas de implementação, sem inferir regras de cronologia ou faixa.
- [Sem validação de transições] → aceitar qualquer dos cinco estados em qualquer ordem, conforme pedido; não inferir máquina de estados.
- [Concorrência de vínculos] → verificações de existência são sequenciais e não substituem transações/garantias concorrentes; validar recursos transacionais disponíveis antes de depender deles.

## Migration Plan

1. Criar a tabela `ordem_servico` e funções locais de vínculo/autorização.
2. Criar endpoints de colaborador e técnico com os filtros/guardas descritos.
3. Criar cliente HTTP, tela de OS e testes locais sem rede.
4. Validar XanoScript e OpenSpec.
5. Em Change futura autorizada, implementar login/provisionamento e a associação `user.id_tecnico`; publicar na ordem `tecnico` → `ordem_servico` → funções/endpoints; validar casos autorizados/negados e persistência. Não executar esses passos remotos nesta Change.

Rollback local consiste em reverter os arquivos desta Change. Nenhuma migração ou rollback remoto será executado aqui.

## Evidência de publicação remota

Em 2026-11-09, as etapas autorizadas `01-tecnico-table` e `02-ordem-servico-table` foram publicadas em `149143/v1`. A etapa 02 teve preview exclusivamente `CREATE table ordem_servico`; a CLI confirmou um documento enviado. Um pull posterior somente de definições confirmou a tabela e o GUID `YMy5cTyq7_EZXyY5QraC5UNte-Q`, seus oito campos, os cinco status e as referências para `tecnico` e `equipamento`. As funções, endpoints, alterações da tabela `user`, autorização em runtime e integração Streamlit ainda não foram publicadas nem verificadas. A tarefa 4.2 permanece aberta.
