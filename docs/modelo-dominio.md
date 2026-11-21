# Modelo de domínio

## Escopo

O sistema organiza uma única assistência técnica. Há cinco entidades de negócio: Cliente, Equipamento, Técnico, Ordem de Serviço e Serviço. Não há separação operacional entre empresas nesta versão.

Este documento apresenta nomes de campos e relacionamentos, sem valores de registros ou identificadores operacionais.

## Entidades e campos

Os identificadores abaixo seguem os nomes expostos pelos contratos de API. As tabelas locais utilizam a chave física `id`, apresentada pelas APIs com o nome correspondente à entidade.

| Entidade | Finalidade | Campos principais |
| --- | --- | --- |
| Cliente | Proprietário dos equipamentos | `id_cliente`, `nome`, `cpf`, `telefone`, `email` |
| Equipamento | Item recebido para atendimento | `id_equipamento`, `tipo`, `marca`, `modelo`, `numero_serie`, `id_cliente` |
| Técnico | Profissional responsável pelo atendimento | `id_tecnico`, `nome`, `especialidade`, `telefone`, `email` |
| Ordem de Serviço | Registro do atendimento de um equipamento | `id_os`, `data_entrada`, `data_saida`, `problema_relatado`, `status`, `valor_total`, `id_equipamento`, `id_tecnico` |
| Serviço | Trabalho registrado em uma OS | `id_servico`, `descricao`, `valor`, `id_os` |

A data de saída pode estar ausente enquanto não for informada. Marca, modelo e número de série são campos opcionais na definição local de Equipamento. Não são acrescentados atributos de estoque, pagamento ou faturamento a esse modelo.

## Relacionamentos

| Relacionamento | Cardinalidade | Significado |
| --- | --- | --- |
| Cliente → Equipamento | 1:N | Um Cliente pode possuir vários Equipamentos; cada Equipamento pertence a um Cliente |
| Equipamento → Ordem de Serviço | 1:N | Um Equipamento pode ter várias OS; cada OS referencia um Equipamento |
| Técnico → Ordem de Serviço | 1:N | Um Técnico pode receber várias OS; cada OS referencia um Técnico |
| Ordem de Serviço → Serviço | 1:N | Uma OS pode ter vários Serviços; cada Serviço pertence a uma OS |

```text
Cliente 1 ----- N Equipamento
Equipamento 1 - N Ordem de Serviço
Técnico 1 ----- N Ordem de Serviço
Ordem de Serviço 1 ----- N Serviço
```

As referências são representadas pelos campos `id_cliente`, `id_equipamento`, `id_tecnico` e `id_os`, conforme a entidade que mantém o vínculo. A cardinalidade conceitual não implica exclusão automática de registros relacionados.

## Jornada de uma Ordem de Serviço

1. O Colaborador cadastra ou consulta o Cliente.
2. Registra ou seleciona o Equipamento relacionado ao Cliente.
3. Confere o cadastro do Técnico responsável.
4. Abre uma OS com Equipamento, Técnico, problema relatado, data de entrada, status e valor total.
5. O Técnico consulta o atendimento atribuído em Minhas Ordens e pode atualizar seu status.
6. O Colaborador registra Serviços associados à OS, com descrição e valor, e acompanha ou edita o atendimento.
7. Quando aplicável, informa a data de saída e atualiza o status correspondente à entrega.

Essa é uma jornada de utilização, não uma sequência de transições obrigatórias. O cadastro de Serviços não calcula automaticamente o valor total da OS; esse valor é informado no formulário.

## Status disponíveis

| Valor do contrato | Rótulo visual |
| --- | --- |
| Aguardando avaliação | Aguardando avaliação |
| Em manutenção | Em manutenção |
| Aguardando peça | Aguardando peça |
| Concluído | Concluída |
| Entregue | Entregue |

Os cinco valores existem nos contratos locais. A apresentação transforma somente o rótulo Concluído em Concluída. Não há comprovação de uma ordem obrigatória de transições; a documentação não impõe uma sequência adicional.

A regra específica para alteração de status de uma OS concluída permanece como melhoria futura. Não se afirma um bloqueio que não esteja implementado.

## Técnico e identidade de acesso

O cadastro de Técnico descreve o profissional e sua especialidade. A identidade de acesso corresponde à conta autenticada e ao perfil funcional. São responsabilidades distintas: cadastrar um Técnico não cria automaticamente uma conta, senha ou permissão.

- Colaborador: gestão dos cinco módulos, respeitando os bloqueios existentes.
- Técnico: consulta das OS atribuídas ao seu vínculo e atualização somente do status por seu painel.
- Usuário sem perfil válido ou Técnico sem vínculo válido: não deve obter o acesso correspondente.

As fontes locais do backend derivam o vínculo da identidade autenticada; o painel não permite escolher outra identidade técnica para ampliar acesso. Essas regras não são comprovadas integralmente apenas pelos controles de interface, e não houve nova consulta remota para preparar este documento.

## Regras e limitações

- Equipamentos vinculados a OS têm bloqueio de exclusão documentado. A opção de exclusão de Equipamentos também depende de configuração explícita.
- A exclusão de Clientes está sujeita aos relacionamentos existentes; não se deve apagar registros relacionados para contornar impedimentos.
- Exclusões de Técnicos e OS permanecem indisponíveis por segurança, mesmo que a interface contenha controles preparados.
- Equipamento e Técnico são informados por ID nos formulários de OS; seletores por nome são melhoria futura.
- O total da OS não é a soma automática dos Serviços.
- Não há isolamento entre empresas.
- Não se declara garantia de concorrência ou recuperação transacional ainda não comprovada.
- O backend privado e seus dados não integram a distribuição pública.

Consulte a [arquitetura](arquitetura.md) e o [README](../README.md) para configuração, uso e demais limitações.
