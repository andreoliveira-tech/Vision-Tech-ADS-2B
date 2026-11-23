# Tasks

## 1. Backend local

- [x] 1.1 Preparar tabela servico com quatro campos, referência/index de OS e helper de validação de OS existente; conferir tipos, ausência de novos atributos e preservação das fontes OS.
- [x] 1.2 Preparar cinco endpoints de Serviços com auth user e guard colaborador antes do acesso aos dados; validar CRUD, IDs, ausência e contratos por parser oficial e testes locais, sem publicar.

## 2. Integração Streamlit local

- [x] 2.1 Implementar cliente HTTP com Bearer obrigatório, URL externa, timeouts, zero retry/redirect e tratamento de 401/403/404 e respostas incertas; testar ausência de token e falhas sem rede.
- [x] 2.2 Implementar cadastro/listagem/consulta/edição/exclusão e seleção por OS, exigindo confirmações por leitura, descarte de dados antigos e bloqueio de reenvio em resultado incerto; cobrir cenários negativos por AppTest.
- [x] 2.3 Integrar página de Serviços somente à navegação colaborador e à limpeza de sessão; testar técnico/sem perfil sem acesso administrativo e preservar navegação dos módulos homologados.

## 3. Preparação de publicação e homologação

- [x] 3.1 Preparar seleções estruturais/endpoints, manifestos, hashes, dependências reutilizadas e verificador; comprovar que OS, Equipamentos, Clientes, Técnicos, guard e autenticação existentes não serão atualizados ou excluídos.
- [x] 3.2 Executar ensaio offline completo com rede bloqueada; medir chamadas incluindo login, auth/me, reruns e conferências, validar fixture de ID dinâmico e produzir roteiro/payloads/orçamento remoto antes de pedir autorização.
- [x] 3.3 Documentar API, configuração, preservação e dependência futura de bloqueio de DELETE de OS por Serviços; validar OpenSpec e contador inalterado durante preparação local.

## 4. Operações remotas sob autorizações próprias

- [x] 4.1 Reconciliar inventário protegido por leitura autorizada, confirmar identidades/dependências e executar somente preview seletivo delete=false; interromper em divergência ou inclusão de outros módulos. Evidência: docs/preview-remoto-servicos-20261119.md; HTTP 200/200, 73 definições preservadas, quatro dependências confirmadas, oito recursos ausentes e preview exato 8 CREATE/0 UPDATE/0 DELETE, sem avisos. Contador 303; nenhuma publicação/login/teste funcional.
- [x] 4.2 Após aprovação expressa do preview, publicar seleção transacional e conferir definições novas e preservação das anteriores; registrar evidências e contador sem retry automático. Evidência: docs/publicacao-servicos-20261119.md; HTTP 200/200, oito recursos criados, 73 anteriores preservados, total 81, contador 305. Comparador interrompeu por três normalizações; conferência exclusivamente local dos snapshots confirmou conteúdo de negócio equivalente e Swagger false adicionado ao grupo. Sete controles locais aprovados, parada original preservada, sem retry/correção remota/teste funcional.
- [x] 4.3 Homologar cinco rotas, negações e dados inválidos com fixtures novas aprovadas; confirmar persistência e preservação da OS/outros Serviços, sem alterar OS ou registros anteriores. Evidência: docs/servicos-homologacao-conclusao-20261119.md; 20 negações no lote anterior; continuação 347→374 completa os cenários pendentes, três rejeições 400, PUT positivo, DELETE e GET 404; baseline final idêntico, fixture 1 removida.
- [x] 4.4 Executar roteiro Streamlit aprovado, incluindo seleção correta e confirmações; conferir baseline final, ausência de reenvio e quantidade exata de chamadas, sem repetir Equipamentos/OS. Portal AppTest com HTTP real controlado nos dois lotes; cadastro/consulta iniciais e edição/exclusão na continuação autorizada de exatamente 27 chamadas; sem retry ou repetição de grupos aprovados. Revisão visual no navegador é incremento separado.
- [x] 4.5 Consolidar evidências e revisão de aderência ao domínio; concluir somente tarefas comprovadas e apresentar a Change para arquivamento separado, sem commit/push automático. Relatório final e índice sanitizado de conclusão registram limites, hashes, baseline, chamada histórica interrompida e contador 374; quatro campos e vínculo mantidos, sem total automático ou escrita em OS/outros módulos. Elegível para revisão de specs/Archive separado, não executado.

Evidencia local: docs/preparacao-local-servicos.md; 44 testes aprovados, 16
arquivos no parser sem erros/avisos, oito recursos propostos com hashes e
ensaio offline de 54 chamadas. Zero chamadas remotas; contador 301. Tarefas
4.x aguardam autorizacoes proprias, sem arquivamento ou publicacao.

Atualização remota: 4.1 concluída conforme recibo acima; 9/13 tarefas concluídas.
4.2–4.5 permanecem abertas. Publicação proposta do mesmo payload transacional
validado no preview conjunto depende de autorização expressa posterior.

Atualização posterior: publicação autorizada concluída e 4.2 conferida por
metadados; 10/13 tarefas, contador 305. Tarefas 4.3–4.5 continuam abertas.

Preparação local complementar: executor e entradas de baseline/funcional,
dez testes novos aprovados, rede bloqueada, cotas 3 GET e 54 chamadas separadas.
Ver docs/preparacao-executor-servicos-20261119.md. Zero chamadas remotas nesta
preparação, contador 305; nenhuma tarefa 4.3–4.5 concluída por simulação.

Atualização de homologação: baseline real aprovado em três GETs (contador 308).
Execução funcional autorizada interrompida na chamada 39, contador **347**:
expectativa local incorreta para id_os 0 (backend exige ID positivo antes de
buscar OS). Cadastro/listagem/consulta e 20 negações comprovados; fixture
Serviço ID 1 não removida, edição/exclusão/conferência final pendentes. Sem
retry, correção remota ou chamadas após parada. Ver
docs/servicos-funcional-parcial-20261119.md. Tarefas 4.3–4.5 permanecem abertas;
continuação depende de plano corrigido e autorização própria.

Preparação local da continuação aprovada: contratos de erro separados numa nova
versão, preservando a execução original. Nove testes locais aprovados; roteiro
medido de 27 chamadas (347→374), fixture existente Serviço ID 1, uma nova
autenticação, sem repetir cadastro ou 20 negações. Ver
docs/servicos-continuacao-preparacao-20261119.md. Zero chamadas remotas nesta
preparação; contador 347, tarefas 4.3–4.5 abertas, execução não autorizada ainda.

Conclusão posterior autorizada: continuação executada com sucesso em 27 chamadas,
contador **374**, fixture Serviço 1 removida, baseline final igual ao inicial,
fontes e evidências anteriores preservadas. Ver
docs/servicos-homologacao-conclusao-20261119.md. **13/13** tarefas; históricos de
parada e preparação acima preservados. Sem publicação, Archive, commit/push ou
início de novo grupo nesta continuação.
