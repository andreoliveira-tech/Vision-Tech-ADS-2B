# Design

## Dependência técnica vigente — contador 375

O design sequencial abaixo não é suficiente para liberação. A Change
`proteger-integridade-exclusoes-concorrentes` especifica transação e lock da OS
compartilhado entre DELETE e POST/PUT de Serviços, com releitura após espera.
Ela detém os cinco UPDATEs dos escritores; esta Change detém helper e DELETE
novos. Publicar escritores protegidos antes dos DELETEs, somente após comprovação
das garantias e novas autorizações. Preservar os pacotes históricos aditivos.
A tarefa 3.3 continua aberta; modelo local não comprova runtime. Esta revisão
documental não altera o painel técnico, código ou registros.

## Context

Ver proposal.md. Inspecionados OS, Serviços, helper servicos/validar_os, guard
de OS, GET/PUT administrativos, cliente/tela e DELETE de Equipamentos/Serviços.
Serviços tem id_os obrigatório e índice; OS tem referências a Equipamento e
Técnico. Não existe DELETE de OS nas fontes ou na interface. Serviços foi
homologado, fixture 1 removida e baseline preservado, contador 374. Ausência
remota do novo DELETE não foi reconferida nesta preparação.

## Goals / Non-Goals

**Goals:** completar CRUD administrativo de OS com bloqueio por Serviços e
confirmação na tela, preservando seus oito campos e vínculos existentes.

**Non-Goals:** alterar status/transições, calcular totais, atualizar painel
técnico, permitir DELETE técnico, excluir Serviços/cadastros em cascata.

## Decisions

### Backend e contrato

Propor function ordens/consultar_dependencias e
api/ordens/ordens_servico/id_os_DELETE.xs. Guard ordens/autorizar_colaborador
primeiro; depois ID positivo, OS existente, helper e validação estrita de
id_os/possui_servicos booleano; excluir somente se ausência confirmada.
Helper usa consulta exists por servico.id_os, sem status ou lista paginada.

Mensagens propostas: 400 `id_os deve ser um inteiro positivo.` e
`Ordem de servico possui servicos vinculados. Exclusao bloqueada.`; manter
404 `Ordem de servico nao encontrada.`. Sucesso 200 {id_os, excluido:true}.
Consulta inválida/falha interrompe, nunca se converte em ausência. DELETE sem
corpo, sem autenticação derivada de parâmetros e sem alteração em outros dados.

Preferir bloqueio a cascade: Serviços registram trabalho da OS e a exclusão
automática apagaria dados de outra entidade. Não adicionar restrição por status,
pois ela não consta do escopo aprovado.

### Cliente e tela

ordens_api considera escritas POST/PUT/PATCH e interpreta sucesso como OS ou
status. Adicionar DELETE ao tratamento de escrita, validação estrita de resposta
e confirmação de ausência 404 conhecida. Evitar alterar contratos de PATCH ou
ampliar acesso do painel técnico. Reusar padrões existentes de Serviços.

Na tela administrativa, OS carregada e ID estável, confirmação própria por
geração, consumo do carregamento antes do envio e confirmação por GET. Troca
de alvo limpa confirmação; erro de listagem não recupera dados antigos. Resultado
incerto bloqueia outras escritas no alvo até conferência explícita; ausência
conhecida resolve a pendência sem DELETE novamente. Sucesso limpa lista e alvo.

### Concorrência e dependências

Consulta antes de db.del comprova somente comportamento sequencial. Criação
concorrente de Serviço pode introduzir dependência entre checagem e exclusão.
Conferir garantias efetivas das referências/runtime antes de liberar; se exigir
alteração de writers/schema/constraint, parar e apresentar escopo separado.
Não modificar POST/PUT de Serviços já homologados por conveniência. Publicação
transaction não prova transação nem serialização dos dados em execução.
Não autorizar homologação concorrente destrutiva em v1 Live por este plano.

## Risks / Trade-offs

- OS 1/2 preservadas → fixtures novas com IDs obtidos de POST, nunca inferidos
  de sequências. Reutilizar Equipamento/Técnico somente como referências de leitura.
- Serviços ausentes no baseline atual → novo Serviço fictício precisa aprovação
  própria para validar bloqueio; não repetir a homologação inteira de Serviços.
- Falha ou exclusão indevida aceita → parar imediatamente, preservar evidências,
  sem cleanup/rollback automático.
- Interface não é aparência no navegador → AppTest cobre estado/HTTP; revisão
  visual global continua no planejamento do MVP.

## Migration Plan

1. Aplicação local autorizada, testes negativos e parser; pacote só helper+DELETE,
   grupos/tabelas/guard como REUSE. Conferir preservação dos sete endpoints OS.
2. Ensaio offline com autenticações/reruns/leituras contado; congelar payloads,
   baseline, fixture de OS livre e fixture OS com Serviço, e orçamento antes de HTTP.
3. Autorizações próprias para reconciliar inventário, preview 2 CREATE/0 UPDATE/
   0 DELETE condicionado à ausência, publicar e conferir definições anteriores.
4. Homologar DELETE negado aos quatro atores, bloqueio por Serviço e preservação,
   exclusão permitida da OS livre e GET 404; somente fixtures novas aprovadas.
5. Limpeza de fixtures com vínculos exige ordem Serviço→OS, plano/orçamento e
   autorização explícitos, só após cenários aprovados; erro interrompe sem limpeza.
6. Consolidar sem repetir OS B–F ou CRUD completo de Serviços; nenhuma reversão
   remota ou commit/push automático. Garantias concorrentes precisam de decisão
   técnica própria antes da liberação.
