// Cadastro protegido; o Xano gera tecnico.id, apresentado como id_tecnico.
query tecnicos verb=POST {
  api_group = "Técnicos"
  auth = "user"

  input {
    text nome filters=trim|min:1
    text especialidade filters=trim|min:1
    text telefone filters=trim|min:1
    email email filters=trim|lower
  }

  stack {
    function.run "tecnicos/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    db.add tecnico {
      data = {
        nome: $input.nome
        especialidade: $input.especialidade
        telefone: $input.telefone
        email: $input.email
      }
    } as $tecnico
  }

  response = {
    id_tecnico: $tecnico.id
    nome: $tecnico.nome
    especialidade: $tecnico.especialidade
    telefone: $tecnico.telefone
    email: $tecnico.email
  }
}
