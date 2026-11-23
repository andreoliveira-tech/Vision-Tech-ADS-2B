# Tasks

Dependência vigente: `proteger-integridade-exclusoes-concorrentes`, contador
375. Concluir sua coordenação dos escritores antes da liberação 4.2/4.3 abaixo;
inventário de leitura já conferido não equivale a concluir 4.1, que também exige
garantias e preview. As oito tarefas marcadas comprovam somente a versão local
sequencial histórica; a revisão concorrente terá testes/pacotes próprios.
Não sobrescrever evidências nem incluir UPDATEs na seleção aditiva original.

## 1. Backend local

- [x] 1.1 Conferir material técnico local sobre garantias da referência Serviço–OS e concorrência; registrar evidência necessária antes da liberação e interromper se a solução exigir modificar writers/schema fora da proposta, sem HTTP ou garantia presumida.
- [x] 1.2 Implementar helper exists de Serviços e DELETE de OS com guard primeiro, ID positivo, existência e booleano estrito; testes locais cobrem OS com Serviço, livre, ausente, consulta falha/incompleta e todos os status; parser oficial sem erros/avisos, sem db.del fora de OS.
- [x] 1.3 Documentar contratos e mensagens exatas; conferir por testes de fonte os sete endpoints atuais, os cinco de Serviços e helpers preservados, sem novos atributos/transições/total automático.

## 2. Integração local

- [x] 2.1 Implementar DELETE sem corpo no cliente HTTP, contrato estrito e incerteza; testes sem rede cobrem 200, bloqueio 400, 401/403, 404 conhecido/desconhecido, timeout, 5xx e confirmação inválida, sem retry nem mudança no PATCH técnico.
- [x] 2.2 Integrar ação administrativa confirmada por OS/geração e GET de ausência, invalidar alvo/lista e bloquear escritas incertas; AppTest cobre troca de alvo, reruns, 401/403, DELETE aceito mas GET falho, reconferência explícita e preservação do painel.
- [x] 2.3 Atualizar documentação e executar regressões locais direcionadas de gestão/painel, preservando payloads e estados aprovados; comprovar ausência de HTTP real e de reenvios automáticos.

## 3. Pacote e ensaio

- [x] 3.1 Preparar pacote exclusivamente helper+DELETE, hashes e dependências REUSE; testes do verificador rejeitam tabelas/grupos/guards, recursos de Serviços, UPDATE/DELETE e outros módulos; preview local condicional de 2 CREATE.
- [x] 3.2 Preparar plano/payloads de novas OS livre/com Serviço e IDs provenientes de POST, preservar OS 1/2 e demais cadastros; especificar sequência de limpeza Serviço→OS e custo, executável somente com autorização própria após sucesso.
- [ ] 3.3 Ensaiar offline bloqueio por Serviço, exclusão permitida, negações e interface; medir chamadas incluindo login/auth/me/fixtures/metadados/reruns/limpeza e congelar orçamento antes de pedir HTTP, contador global 374 preservado nesta preparação.

## 4. Operações remotas sob autorizações próprias

- [ ] 4.1 Reconciliar inventário/baseline/dependências e evidência técnica sob leitura autorizada; dry-run somente da seleção, exatamente 2 CREATE, 0 UPDATE, 0 DELETE se ausentes, definições anteriores preservadas; interromper em divergência.
- [ ] 4.2 Publicar somente após aprovação expressa e conferir novos recursos/preservação por metadados; registrar evidências/contador sem repetição automática, sem alterar endpoints existentes de OS/Serviços.
- [ ] 4.3 Homologar DELETE negado, bloqueado por Serviço, livre e ausente/ID inválido, com fixtures novas e tela; confirmar não cascata por baseline, ausência final e nenhum reenvio, sem repetir OS B–F ou CRUD completo de Serviços e sem limpeza em erro.
- [ ] 4.4 Consolidar evidências, domínio e limites técnicos; concluir apenas critérios comprovados e apresentar sincronização/Archive em etapa separada, sem commit/push e sem encerrar pendências de outras Changes por associação.

Evidência local: docs/implementacao-local-exclusoes-tecnicos-os-20261119.md; 48 testes distintos aprovados, parser oficial 8 arquivos sem erros/avisos e dois pacotes aditivos validados. Contador 374; zero HTTP. 8/13 tarefas. A 3.3 permanece aberta: ensaio simulado de 54 chamadas aprovado, porém executor/orçamento operacional depende de fixture isolada de identidade, rotas de metadados reais e conferência de garantias técnicas. Tarefas remotas 4.x não executadas.
