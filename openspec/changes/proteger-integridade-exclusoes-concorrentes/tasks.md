# Tasks

## 1. Contrato técnico e modelo local

- [x] 1.1 Registrar evidência técnica disponível sobre duração de lock, visibilidade após espera, transação de function.run e rollback; distinguir sintaxe observada de garantia comprovada em relatório, sem HTTP nesta preparação; ausência de comprovação bloqueia liberação, não é aceita por hipótese.
- [x] 1.2 Implementar modelo local de intercalação com testes das duas ordens para Técnico–OS, Técnico–identidade e OS–Serviço, transferências PUT, commit/abort, espera com dependência nova e alvo removido; documentar que aprovação do modelo não comprova runtime e bloquear sockets externos nos testes.

## 2. Implementação local e verificações por caminho

- [x] 2.1 Proteger POST/PUT de OS com transação, lock Técnico destino e lock/releitura da OS no PUT; preservar validações, payloads e respostas; parser e testes direcionados devem detectar escrita fora da proteção, alvo removido e alteração indevida de contrato; documentar mudança.
- [x] 2.2 Proteger POST/PUT de Serviços com transação, lock OS destino e lock/releitura de Serviço no PUT; parser e testes devem cobrir transferência, pai ausente após espera e ausência de efeitos sobre status/total; documentar mudança sem repetir CRUD remoto aceito.
- [x] 2.3 Adicionar lock Técnico ao provisionador na transação atual, preservando users em ordem crescente, privilégio explícito, mesma conta, exclusividade e auditoria; parser/testes locais devem rejeitar ordem inversa, alterações parciais simuladas ou retry; documentar limite do teste de rollback simulado.
- [x] 2.4 Ajustar os dois DELETEs candidatos com transação e lock do pai antes de dependências; parser/testes devem cobrir bloqueios, ausência, falha de helper, commit/abort e preservação de resposta/guard; não alterar helpers, frontend, tabelas ou outros escritores sem nova análise de escopo.

## 3. Pacotes, fixtures e preparação operacional

- [x] 3.1 Criar seleção nova dos cinco UPDATEs e novas versões das seleções de exclusão, com hashes e dependências REUSE; verificador local deve rejeitar arquivos extras, tabelas, grupos e DELETE de definições; demonstrar 0 CREATE/5 UPDATE/0 DELETE e 4 CREATE/0 UPDATE/0 DELETE propostos, preservando pacotes históricos.
- [x] 3.2 Preparar roteiro isolado com barreiras/observação de espera, duas ordens de execução, PUT e falha de auditoria/persistência; entregar mapa de evidência por cenário, ambiente e limites; não criar ambiente remoto nem instrumentação operacional sem autorização própria.
- [ ] 3.3 Resolver proposta de fixture isolada de identidade e medir executor offline completo com contador, login/auth/me, metadados, provisionamento, preservação e limpeza; congelar orçamento por lote e hashes antes de pedir HTTP; manter o contador remoto vigente (377 após a revisão de 20/11) na preparação e rejeitar IDs protegidos ou simulados como alvos reais.

## 4. Evidência e liberação sob autorizações próprias

- [ ] 4.1 Obter evidência autorizada em ambiente isolado das garantias e intercalações previstas, registrando versão/isolamento, espera, rollback e estados finais; se ambiente/garantia faltar, interromper liberação e apresentar diagnóstico, sem teste concorrente destrutivo em Live.
- [ ] 4.2 Reconciliar inventário atual e executar somente novos previews autorizados dos lotes, verificando allowlist exata, definições não afetadas preservadas e zero DELETE de definições; registrar HTTP/contador e parar sem retry em divergência.
- [ ] 4.3 Publicar sob autorização expressa primeiro os cinco escritores protegidos, conferir por metadados e somente depois disponibilizar os quatro recursos novos autorizados; verificar ausência de janela DELETE novo/escritor antigo e preservar evidências, sem rollback remoto automático.
- [ ] 4.4 Homologar apenas cenários novos/afetados autorizados, consolidar prova de integridade/preservação e atualizar dependências das duas Changes de exclusão; entregar relatório e indicar elegibilidade para Archive sem executar arquivamento ou Git automaticamente.

Planejamento completo não equivale a implementação. Contador 375; nesta etapa
nenhum código, teste de implementação, pacote ou recurso remoto foi alterado.
As tarefas 4.x dependem de autorizações futuras; as aprovações históricas de
pacotes somente CREATE não autorizam UPDATE dos cinco endpoints existentes.

Evidência: docs/implementacao-integridade-exclusoes-20261119.md. Oito tarefas
locais completas, cinco abertas. 76 testes distintos aprovados; parser oficial
16 arquivos sem erros/avisos. Runtime/fixture/executor operacional não
comprovados, portanto não liberar DELETEs. Contador 375, zero HTTP nesta etapa.

## 5. Replanejamento gratuito — sem execução na revisão inicial

Restrição registrada em 20/11 pelo responsável: Xano Free, somente fonte live,
Add Test Data Sources exige upgrade, sem contratação paga. Contador **377**.
Oito tarefas históricas continuam completas; tarefas runtime permanecem abertas.

- [x] 5.1 Consolidar matriz requisito/evidência/lacuna para concorrência, rollback, contratos e preservação, reaproveitando os 76 testes/parser e recibos existentes; identificar somente novos testes locais necessários, sem repetir homologações aprovadas.
- [x] 5.2 Preparar e ensaiar offline as lacunas autorizadas de contratos, autorização e escrita incerta, com mocks/fixtures sintéticos e sockets externos bloqueados; registrar limites sem declarar locks/rollback do Xano comprovados; preservar evidências e contador 377.
- [ ] 5.3 Fechar desenho do executor offline e orçamento proposto de 3.3, distinguindo números/IDs simulados de chamadas reais; mapear em documento de planejamento os lotes independentes de Técnicos, Clientes e acesso para aprovação própria, sem ampliar implementação desta Change.
- [ ] 5.4 Apresentar no marco de 21/11 às 18h a situação da prova runtime e o impacto na entrega de 22/11 às 18h; sem ambiente isolado gratuito comprovado, manter 4.1 e liberação subsequente bloqueadas e solicitar decisão explícita sobre pendências, sem declarar MVP completo ou arquivar.

As tarefas 5.x são propostas futuras, não executadas nesta revisão documental.
3.3 pode avançar em sua parcela offline, mas sua fixture operacional não está
resolvida. 4.1 exige runtime; 4.2–4.4 não recebem liberação com testes locais.
Os contadores 375 nos registros anteriores são históricos. Nenhuma nova chamada,
implementação, endpoint, flag ou expectativa de teste foi alterada nesta etapa.


### Execução local da preparação — 20/11/2026

5.1 concluída: matriz requisito/evidência/lacuna e roteiros C/T incorporados ao
design, com fontes e métodos de teste identificados. 9/17 tarefas concluídas.
Não foram repetidos testes históricos, alterados código, pacotes ou expectativas,
nem executadas chamadas remotas. Contador 377. 5.2/5.3 continuam abertas pelos
alcances ainda não executados; 3.3/4.x e dependências runtime preservadas.

Preparação subsequente em 20/11: payloads dos 46 casos negativos de Clientes
e dois exemplos de normalização conferidos somente por verificações locais do
artefato. Ver `docs/clientes-validacao-preparacao-offline-20261120.md` e fixture
`docs/fixtures/clientes-validacao-offline-20261120.json`. 5.2 permanece aberta:
executor e ensaio completo ainda não executados. O total nominal de 104 não
congela orçamento remoto, pois a leitura prévia de dependências para eventual
limpeza ainda precisa de definição e contagem. Contador 377; sem código de
produção, endpoint, flag, rede ou Git alterados.

Conclusão de 5.2 em 20/11: executor exclusivo em memória e 18 novos testes
aprovados, nominal de 104 chamadas simuladas e cenários negativos sem retry ou
limpeza automática. Ver `docs/clientes-validacao-ensaio-offline-20261120.md` e
recibo correspondente. Fixture/fontes e evidências anteriores preservadas.
10/17 tarefas; 3.3/4.x/5.3/5.4 continuam abertas. Contador remoto 377; nenhuma
prova runtime ou orçamento remoto aprovado decorre desse ensaio.

Reconciliação local de Técnicos em 20/11: diário e interrupção E07 íntegros;
cinco GETs 200 e um login 403, subtotal histórico E07 15. Fontes dos loaders
mostram caminhos diferentes para a credencial de 3; autenticações posteriores
bem-sucedidas registradas não provam a causa antiga nem validade atual. Ver
`docs/tecnicos-reconciliacao-local-20261120.md` e recibo. Sem leitura de segredos,
descriptografia ou HTTP; contador 377. Nenhuma tarefa remota encerrada; 5.3
permanece aberta no alcance de executor/orçamento concorrente.
