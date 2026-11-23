# Tasks

## 1. Cadastro e validação compartilhada

- [x] 1.1 Disponibilizar POST `/clientes` com nome, CPF, telefone e e-mail obrigatórios e retorno dos cinco campos do cliente. Critério: contrato do endpoint 4099966 e `xano/api/clientes/clientes_POST.xs`.
- [x] 1.2 Aplicar a validação compartilhada antes de criar ou atualizar registros. Critério: chamadas anteriores a `db.add`/`db.edit` nas definições documentadas e regras presentes em `xano/function/clientes/validar_dados.xs`; o interior publicado da função não foi conferido nesta inspeção.
- [x] 1.3 Verificar cadastro válido consultável. Evidência: POST 200 e GET do descartável 13 registrados em `docs/validacao-mvp-clientes.md`.

## 2. Validação de rejeições e normalização

Execução autorizada interrompida em 20/11 após dois GETs 200, contador 507,
antes de login ou escrita. Corpo atual não foi preservado antes da comparação;
causa imediata indeterminada, sem prova de divergência remota. Tarefa 2.1
permanece aberta. Diagnóstico separado de uma leitura ainda não autorizado;
ver `docs/clientes-validacao-interrupcao-20261120.md`.

Preparação local em 20/11, contador 505: novo lote proposto de até 104 chamadas,
com conferência inicial de definições, 46 rejeições, normalização POST/PUT e
retenção da fixture sem DELETE. Oito testes locais aprovados; execução remota
pendente de autorização e tarefa 2.1 continua aberta. Ver
`docs/clientes-validacao-controlada-preparacao-20261120.md`.

- [x] 2.1 Comprovar no backend a rejeição integral de dados inválidos sem criar ou alterar registros e a normalização em POST/PUT, correspondente à tarefa original 1.3. Executado em lote autorizado: 23 POST e 23 PUT inválidos HTTP 400, normalização no POST e em dois PUTs, 51 comparações integrais de listagem. Fixture 16 retida sem DELETE, Clientes 3/10/11/12 preservados. Retomada de 103 chamadas, acumulado 611; ver `docs/clientes-validacao-conclusao-20261120.md`. Sem prova de concorrência ou rollback.

## Evidências

As marcações se baseiam na implementação e nas verificações registradas em [design.md](design.md#verification), com rastreabilidade às tarefas **2.1 e 1.3** de [mvp-assistencia-tecnica](../2026-11-22-mvp-assistencia-tecnica/tasks.md).

Datas comprovadas e limites estão no [histórico do design](design.md#histórico-e-fontes). Este checklist não registra novas execuções.
