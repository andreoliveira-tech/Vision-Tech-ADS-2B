# Tasks

Dependência vigente: `proteger-integridade-exclusoes-concorrentes`, contador
375. Concluir sua coordenação dos escritores antes da liberação 4.2/4.3 abaixo;
inventário de leitura já conferido não equivale a concluir 4.1, que também exige
garantias e preview. As oito tarefas marcadas comprovam somente a versão local
sequencial histórica; a revisão concorrente terá testes/pacotes próprios.
Não sobrescrever evidências nem incluir UPDATEs na seleção aditiva original.

## 1. Backend local

- [x] 1.1 Documentar a verificação técnica das garantias de referência/concorrência disponíveis no material local e os requisitos para liberação; identificar precisamente se falta evidência remota, sem chamar Xano ou presumir constraint. Se exigir outro schema/writer, apresentar escopo antes de alterar.
- [x] 1.2 Implementar helper de existência OS/user_tecnico e DELETE com guard primeiro, ID/existência, validação estrita e bloqueios; verificar por testes de fonte e parser oficial sem erros/avisos, inclusive falha de consulta, zero, ausente e ambas dependências, sem escrever fora de tecnico.
- [x] 1.3 Documentar contrato e mensagens; testes locais devem distinguir bloqueio por OS, vínculo isolado, ID inválido e ausência, com autenticação/perfil anterior ao acesso de negócio; conferir preservação dos quatro endpoints atuais.

## 2. Cliente e interface locais

- [x] 2.1 Acrescentar DELETE sem corpo, Bearer, contrato estrito e tratamento de escrita incerta no cliente; testes sem rede cobrem 200, 400, 401, 403, 404 conhecido/desconhecido, timeout, 5xx e corpo inválido, com zero retry.
- [x] 2.2 Adicionar confirmação por ID/geração, consumo do alvo e GET de ausência, bloqueando escritas em resultado incerto; AppTest cobre troca de seleção, rerun, DELETE aceito mas GET falho, resolução por conferência explícita e limpeza de sessão/perfil, sem refazer CRUD existente.
- [x] 2.3 Atualizar documentação de execução/configuração sem URL nova obrigatória; conferir integração do menu existente e regressões locais direcionadas dos quatro fluxos atuais, sem chamadas reais.

## 3. Preparação seletiva e homologação

- [x] 3.1 Preparar pacote somente helper+DELETE, manifestos/hashes e dependências REUSE; verificador local rejeita tabelas/grupos/guard e qualquer UPDATE/DELETE ou outro módulo; preview local condicional 2 CREATE.
- [x] 3.2 Preparar fixtures isoladas livre/com OS/com identidade e plano de provisionamento separado quando necessário; preservar Técnicos 1–3, OS 1/2 e usuários atuais; verificar pelo roteiro que nenhum ID protegido vira alvo de DELETE e que ausência de fixture de identidade impede concluir o cenário.
- [ ] 3.3 Ensaiar offline fluxo completo e negativos, contar login/auth/me/metadados/reruns/fixtures/preservação/limpeza aprovada e congelar orçamento, payloads e executor antes de solicitar HTTP; comprovar contador global 374 inalterado na preparação.

## 4. Etapas remotas sob autorizações próprias

- [ ] 4.1 Reconciliar inventário/baseline e garantias técnicas por leituras autorizadas; executar somente dry-run aprovado e exigir exatamente 2 CREATE, 0 UPDATE, 0 DELETE se ausentes; evidenciar preservação das definições anteriores e parar em divergência.
- [ ] 4.2 Após autorização expressa, publicar transacionalmente apenas os dois recursos aprovados e conferir metadados anteriores/novos, sem retry; registrar contador/evidências e não confundir transaction de publicação com garantia de dados.
- [ ] 4.3 Homologar fixture livre, bloqueios isolados OS/identidade, acesso negado, ID/ausência e tela conforme orçamento autorizado; comparar baseline/relacionamentos e registrar ausência de reenvio, sem limpeza em falha ou conclusão baseada em mocks.
- [ ] 4.4 Consolidar revisão do domínio, garantias comprovadas/limites e evidências com hashes; concluir apenas critérios efetivos e apresentar Archive separado, mantendo pendências da gestão original de Técnicos e demais Changes, sem commit/push.

Evidência local: docs/implementacao-local-exclusoes-tecnicos-os-20261119.md; 48 testes distintos aprovados, parser oficial 8 arquivos sem erros/avisos e dois pacotes aditivos validados. Contador 374; zero HTTP. 8/13 tarefas. A 3.3 permanece aberta: ensaio simulado de 54 chamadas aprovado, porém executor/orçamento operacional depende de fixture isolada de identidade, rotas de metadados reais e conferência de garantias técnicas. Tarefas remotas 4.x não executadas.
