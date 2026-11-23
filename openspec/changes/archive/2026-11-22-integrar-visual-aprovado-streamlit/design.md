# Design

## Context

Contexto em docs/project-overview.md, docs/domain-model.md e openspec/config.yaml.
Reutilizar Streamlit, clientes HTTP e navegação por perfil existentes. A prévia
aceita e o lote em docs/preparacao-lotes-finais-20261120.md definem o escopo.

## Decisions

Paleta: página #F4F7FB, superfícies brancas, borda #E2E8F0, texto #1F2937,
secundário #475569/#5F6F85 e azul #2563EB; sidebar branca com ativo #EFF6FF.
Toolbar minimal apenas se suportada na versão instalada. Larguras 1240/780 px.

Componentes de apresentação sem HTTP, HTML sempre escapado para dados de domínio.
Status Concluída é apresentação de Concluído; valores/payloads originais intactos.
Badges com texto e contraste >=4,5:1. Dados administrativos de OS não incluem
nomes de equipamento/técnico no contrato: exibir IDs verdadeiros sem inventar
nomes ou buscar outras APIs. Painel usa nomes de equipamento já fornecidos.

Reorganizar blocos inteiros em abas sem mover widgets para dentro/fora de forms.
Filtros e indicadores usam somente última lista obtida explicitamente e não
alteram alvo de consulta/edição/exclusão. Sem lista carregada, não exibir totais
fictícios. Erro/incerteza não preserva lista desatualizada nem rearma escrita.
Filtros não acrescentam consultas de negócio. Reruns do portal ainda executam
o auth/me previsto pelo fluxo atual; incluir isso no orçamento remoto futuro,
sem remover a revalidação para simular ausência absoluta de HTTP.

Painel preserva carregamento, tentada/geracao, retorno incerto, keys e payloads;
cartões brancos, problema destacado, equipamento/data lado a lado e divisória
antes do form. Atualizar e salvar com alvos >=44 px; largura total no celular.
Destaque azul quando alterado somente por CSS limitado ao cartão e valores
confirmados do seletor com menu fechado; não introduzir callback ou rerun.

Tema nas demais telas, sem reorganizar seus fluxos. Acesso continua decidido
pelo backend e auth_session; não alterar permissões para reproduzir simulação.

## Verification and Limits

Congelar hashes e contratos antes/depois. Regressões existentes sem alterar
expectativas de negócio; novos testes pertinentes para filtros, escape e status.
AppTest e dados fictícios, transporte externo proibido; nenhuma sessão real.
Inspeção visual das telas reais em 1440/390 px fica distinguida do aceite prévio
da simulação. Sem rede nesta etapa, evidência visual não obtida por AppTest
deve permanecer explicitamente pendente, sem reaproveitar screenshots da prévia
como se fossem as telas reais alteradas.

Seletores com nomes e regra de status de OS concluída são melhorias futuras,
fora deste lote. Sem novas entidades, testes de DELETE ou alterações remotas.
