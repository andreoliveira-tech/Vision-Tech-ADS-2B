// Atualização completa; id_tecnico vem somente da rota e não é alterado.
query "tecnicos/{id_tecnico}" verb=PUT {
  api_group = "Técnicos"
  auth = "user"

  input {
    int id_tecnico
    text nome filters=trim|min:1
    text especialidade filters=trim|min:1
    text telefone filters=trim|min:1
    email email filters=trim|lower
  }

  stack {
    function.run "tecnicos/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    db.get tecnico {
      field_name = "id"
      field_value = $input.id_tecnico
    } as $existente

    precondition ($existente != null) {
      error_type = "notfound"
      error = "Tecnico nao encontrado."
    }

    db.edit tecnico {
      field_name = "id"
      field_value = $existente.id
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
