query "servicos" verb=GET {
  api_group = "Serviços"
  auth = "user"
  input {
  }
  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao
    db.query servico {
      return = {type: "list"}
      output = ["id", "descricao", "valor", "id_os"]
    } as $servicos
  }
  response = $servicos|map:{id_servico: $$.id, descricao: $$.descricao, valor: $$.valor, id_os: $$.id_os}
}
