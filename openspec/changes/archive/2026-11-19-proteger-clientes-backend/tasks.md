# Tasks

## 1. Inventário e backend local
- [x] 1.1 Conferir snapshot protegido, recuperar DELETE e comparar as quatro fontes; documentar hashes e divergências.
- [x] 1.2 Proteger cinco rotas com auth e guard antes dos dados; comprovar preservação do restante por teste e parser oficial.

## 2. Frontend e verificação
- [x] 2.1 Enviar Bearer nas cinco operações e confirmações; verificar token ausente, 401/403 e ausência de retry em testes locais.
- [x] 2.2 Integrar tratamento da tela e limpeza de sessão/cache; executar regressões direcionadas de Clientes, sem rede.

## 3. Pacote e planejamento
- [x] 3.1 Preparar cinco UPDATEs por GUID, manifesto, dependências e verificador local; testar integridade e exclusividade.
- [x] 3.2 Documentar diagnóstico, roteiro remoto em lotes e orçamento; validar OpenSpec e preservar contador 230.

## 4. Etapas remotas separadas
- [x] 4.1 Sob nova autorização, reconciliar inventário e executar dry-run delete=false; exigir 0 CREATE, 5 UPDATE, 0 DELETE. Evidência: docs/preview-remoto-protecao-clientes.md; HTTP 200/200, 73 definições preservadas, contador 232; nenhuma publicação real.
- [x] 4.2 Sob autorização própria, publicar seleção e conferir definições preservadas; registrar contador e evidências. Evidência: docs/publicacao-protecao-clientes.md; HTTP 200/200, cinco endpoints conferidos e outras 68 definições preservadas, total 73; contador 234, sem testes funcionais.
- [x] 4.3 Homologar permissões e integração Clientes no escopo autorizado, preservando fixtures e sem repetir OS/Equipamentos. Evidência final: docs/homologacao-clientes-escrita-conclusao-20261119.md; lote v2 com 38 chamadas verificadas, contador 301, doze escritas indevidas negadas, CRUD da nova fixture 15 confirmado e registros anteriores preservados. Baseline final idêntico ao inicial; processo encerrado com código zero.

Change concluída: **9/9 tarefas**. Registros abaixo são históricos da preparação
e das etapas intermediárias; não representam pendências atuais de Clientes.

Leitura/permissões de 4.3 concluída: docs/homologacao-clientes-leitura-conclusao.md;
matriz 401/403/200, quatro Clientes e quatro Equipamentos preservados, contador
263. Manter a tarefa aberta até conferir escritas e integração remota da tela,
em lotes autorizados separadamente. Nenhuma escrita iniciada nessa homologação.

Preparação de escrita/tela aprovada offline: seis testes com 24 cenários,
38 chamadas simuladas e zero remotas; contador 263. Roteiro/payloads em
docs/plano-homologacao-clientes-escrita-streamlit.md. Tarefa 4.3 permanece aberta
até execução remota autorizada e conferida; proposta de limite final 301.

Correção local posterior: fixture original com IDs presumidos 1–4 não corresponde
ao baseline real (3,10,11,12). Versão v2 preparada e preflight comprovado nesse
baseline; dez testes/43 cenários locais aprovados, contador 263, sem reinício
remoto. Ver docs/diagnostico-local-clientes-escrita-20261119.md. Tarefa 4.3 aberta.
