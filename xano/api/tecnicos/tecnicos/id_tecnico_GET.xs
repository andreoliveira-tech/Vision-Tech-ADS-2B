query "tecnicos/{id_tecnico}" verb=GET {
  api_group = "Técnicos"
  auth = "user"

  input {
    int id_tecnico
  }

  stack {
    function.run "tecnicos/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    db.get tecnico {
      field_name = "id"
      field_value = $input.id_tecnico
      output = ["id", "nome", "especialidade", "telefone", "email"]
    } as $tecnico

    precondition ($tecnico != null) {
      error_type = "notfound"
      error = "Tecnico nao encontrado."
    }
  }

  response = {
    id_tecnico: $tecnico.id
    nome: $tecnico.nome
    especialidade: $tecnico.especialidade
    telefone: $tecnico.telefone
    email: $tecnico.email
  }
}
