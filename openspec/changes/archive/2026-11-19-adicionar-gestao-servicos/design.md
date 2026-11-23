# Design

## Context

Ver proposal.md. Fontes inspecionadas: modelo global, tabela `ordem_servico`,
guard `ordens/autorizar_colaborador`, clientes HTTP/UI de OS/Equipamentos,
portal e configuração. Não há `servico`/tela/API nas fontes locais; o inventário
de specs principais também não contém essa capacidade. A ausência remota não
foi conferida nesta etapa. Existem 73 definições no último inventário protegido;
contador global 301 após homologação de Clientes.

## Goals / Non-Goals

**Goals:** implementar o CRUD originalmente previsto, autorizando colaboradores
pela arquitetura atual, e completar o vínculo OS 1:N Serviço com interface simples.

**Non-Goals:** alterar OS, calcular totais, criar catálogo, permitir gestão pelo
técnico, instituir limites de preço/precisão ou regras de transição, excluir OS
ou redesenhar todas as telas. Descrição é texto obrigatório na entrada, sem nova
regra de unicidade/comprimento mínimo; valor é decimal obrigatório, sem impor
limite mínimo, desconto ou arredondamento não aprovados. Esses limites não
constam do domínio e não serão acrescentados silenciosamente.

## Decisions

### Persistência e referências

Tabela física proposta `servico`: `id` inteiro nativo, `descricao` texto,
`valor` decimal, `id_os` inteiro obrigatório referenciando `ordem_servico.id`;
índice não exclusivo em `id_os`. API expõe `id` como `id_servico`, sem atributo
novo. Reutilizar tabela OS existente. Helper próprio de validação consulta sua
existência antes de POST/PUT; falha de consulta interrompe antes da gravação.
Não reutilizar `ordens/validar_vinculos`: ele valida Técnico/Equipamento, não OS.

Sem endpoint DELETE de OS nesta Change; a futura exclusão de OS precisará
verificar Serviços vinculados antes de ser habilitada, por Change própria.
Não atribuir proteção contra exclusão concorrente da OS a uma consulta prévia.

### API e segurança

Grupo proposto `Serviços`, cinco endpoints `/servicos` POST/GET e
`/servicos/{id_servico}` GET/PUT/DELETE. Todos usam `auth="user"` e o guard
publicado `ordens/autorizar_colaborador` com `$auth.id` como primeira decisão,
antes de ler/validar dados de negócio. Sem duplicar tabelas de usuário/perfil
ou helpers de autorização; nenhuma autoridade derivada de user.role.

POST/PUT recebem exatamente descricao, valor, id_os, devolvem os quatro campos;
GET coleção devolve lista, GET individual os quatro campos. DELETE devolve
`id_servico` e `excluido:true`, sem corpo de entrada. Usar 200 para sucesso,
400 para entrada/referência inválida, 404 para Serviço inexistente, 401/403
conforme autenticação/guard existente. Conferir envelopes reais somente em
homologação autorizada, sem presumir que a serialização textual seja idêntica.

A seleção por OS será feita na tela sobre a lista autorizada, evitando endpoint
ou contrato de filtro adicional. Escopo acadêmico simples: registrar como
limitação se paginação remota ou volume exigirem revisão, sem truncar resultados
silenciosamente. PUT pode corrigir id_os, sempre validando o novo destino.

### Streamlit e HTTP

Adicionar cliente `servicos_api.py`, UI `servicos_ui.py` e página administrativa,
URL externa `XANO_SERVICOS_API_BASE_URL`, mantendo o validador HTTPS vigente.
Reutilizar formatos de exceção/integração de auth_session, ampliar apenas suas
chaves de limpeza. Nenhuma chamada na importação; timeout explícito, redirects
e retries desabilitados; token ausente bloqueado antes de HTTP.

Listagem por ação explícita; seleção por OS e ID, rascunhos descartados na troca.
Cadastro/edição/exclusão exigem submissão explícita; excluir exige carregar alvo
e confirmar desmarcado por padrão. GET após POST/PUT confirma quatro campos;
após DELETE, GET 404 com contrato conhecido confirma ausência. Resultado incerto
consome a tentativa e bloqueia novas escritas até conferência explícita; para
POST incerto sem ID conhecido, não tentar resolver reenviando cadastro. Não
presumir idempotência de POST, PUT ou DELETE.

Manter componentes nativos Streamlit e a organização atual; padronização global
de cores/layout será outro incremento, preservando estados e confirmações.

## Risks / Trade-offs

- Inventário remoto histórico → antes de publicar, reconciliar identidade/definições;
  reutilizar recurso compatível existente, interromper em divergência.
- Mudança de vínculo ou futura exclusão de OS → validar referência e registrar
  limite sequencial; não habilitar DELETE de OS sem proteção de Serviços.
- Decimal entre Xano/JSON/Streamlit → testar número finito e preservação do valor,
  sem inventar limites/escala ou modificar total da OS.
- Reruns e auth/me consomem chamadas → ensaio offline do portal mede todas as
  chamadas antes de aprovar orçamento remoto; nenhum lote automático.
- Pacote com dependência nova → tabela/grupo/helper primeiro, endpoints depois;
  dependências publicadas existentes ficam fora da seleção.

## Migration Plan

1. Implementação local após aprovação da proposta, parser, testes negativos e
   ensaio offline. Preservar baseline/evidências e contador 301.
2. Preparar pacote estrutural e pacote de endpoints, manifestos/hashes e
   dependências. Quantidades exatas dependem da reconciliação remota posterior;
   não afirmar CREATE remoto só pela ausência de arquivos locais.
3. Sob autorização, inventário somente leitura e preview remoto `delete=false`,
   transacional, seleção mínima. Publicação exige autorização separada, conferência
   de definições novas e preservação das anteriores. Nunca alterar OS/guards
   existentes por inclusão acidental em pacote.
4. Homologação por grupos autorizados, fixture Serviço nova ligada a OS fictícia
   explicitamente aprovada; negar acesso a anônimo/token inválido/técnico/sem
   perfil, validar entrada, CRUD e preservação de OS/outros Serviços.
5. Confirmações funcionais e de interface encerram tarefas. Falha interrompe sem
   retry ou rollback de dados automático. Arquivar só após revisão/evidências;
   implementação local isolada não autoriza publicar nem encerrar a Change.
