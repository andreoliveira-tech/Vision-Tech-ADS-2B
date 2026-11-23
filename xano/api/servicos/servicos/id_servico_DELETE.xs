query "servicos/{id_servico}" verb=DELETE {
  api_group = "Serviços"
  auth = "user"
  input {
    int id_servico
  }
  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao
    precondition ($input.id_servico > 0) {
      error_type = "inputerror"
      error = "id_servico deve ser um inteiro positivo."
    }
    db.get servico {
      field_name = "id"
      field_value = $input.id_servico
    } as $servico
    precondition ($servico != null) {
      error_type = "notfound"
      error = "Servico nao encontrado."
    }
    db.del servico {
      field_name = "id"
      field_value = $servico.id
    }
  }
  response = {id_servico: $servico.id, excluido: true}
}
