// Lista somente os campos do domínio e exige autorização no backend.
query tecnicos verb=GET {
  api_group = "Técnicos"
  auth = "user"

  input {
  }

  stack {
    function.run "tecnicos/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    db.query tecnico {
      return = {type: "list"}
      output = ["id", "nome", "especialidade", "telefone", "email"]
    } as $tecnicos
  }

  response = $tecnicos|map:{
    id_tecnico: $$.id
    nome: $$.nome
    especialidade: $$.especialidade
    telefone: $$.telefone
    email: $$.email
  }
}
