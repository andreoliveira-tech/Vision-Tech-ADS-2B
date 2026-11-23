# Tasks

## Arquitetura e estado atual (2026-11-13)

A antiga proposta de estender `user` foi substituída pela arquitetura aprovada
com tabelas técnicas. Etapas 01–06 publicadas, Grupos 1–4 da etapa 06 concluídos;
endpoints 08–09 e integração real continuam pendentes. Veja
[progresso-mvp.md](../../../docs/progresso-mvp.md). Os registros anteriores são
históricos e não autorizam novas operações.

## 1. Modelo e dependências de autorização

- [x] 1.1 Criar `ordem_servico` com os oito campos originais, os cinco status exatos, ID nativo gerado e FKs para Técnico/Equipamento; verificar o esquema com o validador XanoScript e teste estático dos campos. Evidência remota: em 2026-11-09, a etapa `02-ordem-servico-table` foi publicada em `149143/v1` após autorização explícita; o preview mostrou exclusivamente `CREATE table ordem_servico`. A CLI informou `Pushed 1 documents`. Pull somente de definições confirmou a tabela, GUID `YMy5cTyq7_EZXyY5QraC5UNte-Q`, os oito campos (`id`, `data_entrada`, `data_saida`, `problema_relatado`, `status`, `valor_total`, `id_equipamento`, `id_tecnico`), os cinco status originais e as referências às tabelas existentes `equipamento` (GUID `utw4tCFh9WA8EJHYxfh5u36r3Ug`) e `tecnico` (GUID `nu49vX9JOpQr45J3_EhsCut0JuQ`). Isso comprova a publicação da tabela, não a execução dos endpoints nem a integração funcional.
- [x] 1.2 Alinhar as definições locais à decisão arquitetural posterior: preservar user.role=admin/member e resolver perfil/vínculo por user_application_profile e user_tecnico, sem campos funcionais em user nem alteração de signup. As tabelas técnicas foram publicadas na etapa 03 e os fluxos sequenciais da etapa 06 validados; isso não comprova integração dos endpoints de OS.
- [x] 1.3 Implementar função que valida existência de Equipamento e Técnico antes de escrita; verificar por teste estático as consultas e precondições de ambos os IDs, sem executar gravações remotas.

## 2. APIs Xano e autorização

- [x] 2.1 Implementar POST, GET lista, GET por ID e PUT completos para colaborador; validar token/perfil no backend, refs, ID preservado e ausência de DELETE por testes de contrato e validação XanoScript.
- [x] 2.2 Implementar GET das próprias OS, GET por ID restrito e PATCH somente de status para técnico; derivar técnico de `$auth.id`, filtrar cada operação por `id_tecnico` e negar OS alheia; validar fonte e sintaxe, mantendo a associação remota pendente.
- [x] 2.3 Cobrir contratos permitidos e negados, incluindo perfil sem autorização, vínculo ausente, FKs inexistentes, status fora dos cinco valores e tentativa de outro técnico; usar testes estáticos locais sem registros reais ou execução remota.

## 3. Streamlit e documentação

- [x] 3.1 Implementar cliente HTTP Bearer e configuração externa; testar URL inválida/ausente, respostas, erros 401/403/404 e ausência de token sem HTTP.
- [x] 3.2 Implementar página Streamlit para CRUD permitido a colaboradores, com IDs protegidos e campos originais; testar cadastro, lista vazia, consulta, atualização e ausência de exclusão via AppTest.
- [x] 3.3 Documentar rotas, payloads, dependências de autenticação e limites de integração em `docs/api-ordens-servico.md`; conferir exemplos contra os XanoScripts locais.

## 4. Verificação e integração futura

- [x] 4.1 Executar a suíte local após a revisão final (102 testes), validador XanoScript (13 arquivos válidos) e validação estrita do OpenSpec; revisar que Clientes/Equipamentos e dados remotos não foram alterados.
- [ ] 4.2 Integrar e validar em ambiente autorizado após publicação das tabelas, perfis e vínculo técnico; testar colaborador, técnico atribuído, técnico alheio e anônimo sem alterar registros existentes.

## 5. Correções e preparação local autorizadas (2026-11-18)

- [x] 5.1 Renovar campos de edição a cada carregamento de OS e descartar lista antiga antes de consultar novamente.
- [x] 5.2 Consumir o carregamento antes de atualizar e exigir recarga após resposta incerta, falha de confirmação ou rejeição; sem reenvio implícito.
- [x] 5.3 Cobrir correções e cenários negativos por testes locais com rede bloqueada. Dez novos testes, mais 26 de regressão direcionada aprovados; sem suíte completa ou repetição de F.
- [x] 5.4 Preparar seleção exclusiva de sete endpoints, conferir hashes, fontes e dependências reutilizadas; apresentar preview local sem push ou consultas. Pacote `deployment/xano-149143-v1-ordens/`, onze dependências reutilizadas e três testes do verificador aprovados.
- [x] 5.5 Documentar a proteção necessária em Clientes, sem modificar seus endpoints nesta etapa. Ver `docs/protecao-backend-clientes-pendente.md` e `docs/preparacao-local-ordens-servico.md`; contador preservado em 103.
