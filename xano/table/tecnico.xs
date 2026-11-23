// Definição local para o MVP. id físico é apresentado como id_tecnico.
// Não contém dados de autenticação e não define índice exclusivo de email.
table tecnico {
  auth = false

  schema {
    int id

    text nome filters=trim|min:1

    text especialidade filters=trim|min:1

    text telefone filters=trim|min:1

    email email filters=trim|lower
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
}
