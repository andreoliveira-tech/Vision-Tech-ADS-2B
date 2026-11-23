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
- [x] 4.3 Homologar permissões e integração Clientes no escopo autorizado, preservando fixtures e sem repetir OS/Equipamentos.


## Reconciliação documental em 22/11/2026

A tarefa 4.3 já estava concluída conforme docs/homologacao-clientes-leitura-conclusao.md e docs/homologacao-clientes-escrita-conclusao-20261119.md. Este último registra expressamente 9/9 tarefas. O checklist foi reconciliado exclusivamente com essas evidências, sem repetir testes ou chamadas remotas. Na reconciliação inicial, o arquivamento permaneceu pendente pela ausência de proposta, design e delta de especificação. Esses três documentos foram posteriormente consolidados a partir das fontes existentes, sob autorização do responsável, sem alterar comportamento ou ampliar as evidências.
