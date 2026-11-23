# Design

## Context

Ver proposal.md. Inventário protegido existente contém cinco rotas públicas,
incluindo DELETE ausente das fontes locais. Recuperar a definição exata do
snapshot e comparar as quatro demais antes de aplicar a proteção.

## Goals / Non-Goals

Proteger todas as operações de Clientes na arquitetura de assistência única.
Não alterar entidades, normalização, respostas, dependências, tenancy ou módulos homologados.

## Decisions

Adicionar auth=user e executar ordens/autorizar_colaborador com $auth.id no
início do stack, antes de qualquer leitura/validação/escrita de negócio.
Reutilizar o guard publicado evita criar outro mecanismo de perfil. Não modificar
sua descrição ou lógica nesta seleção. Manter GUIDs e comparar o restante do
XanoScript com o original, ignorando apenas normalização lexical sem significado.

O cliente HTTP receberá token por argumento obrigatório em tempo de execução,
inclusive nos GETs de confirmação; 401/403 terão exceções próprias compatíveis
com os erros existentes. A tela interromperá processamento em falha de autorização;
401 encerra sessão e caches, 403 remove dados de Clientes e não reenvia operações.

## Risks / Trade-offs

- Inventário é histórico → reconciliação remota e dry-run exigidos em etapa posterior autorizada.
- Frontend antigo deixa de funcionar após proteção → publicar backend e disponibilizar frontend atualizado na mesma janela controlada.
- DELETE deve preservar proteção de vínculos → recuperar fonte e testar equivalência; nenhuma exclusão remota nesta preparação.
- Erros incertos não autorizam rollback/retry → manter recuperação explícita existente.

## Migration Plan

Preparação/testes locais; depois inventário e preview delete=false com exatamente
cinco UPDATEs; publicação transacional somente após aprovação expressa; conferência
de definições e homologação seletiva em lotes autorizados. Nenhum rollback automático
para endpoints públicos. Falha causa parada e diagnóstico.
