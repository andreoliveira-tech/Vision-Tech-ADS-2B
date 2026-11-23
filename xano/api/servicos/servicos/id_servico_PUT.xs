query "servicos/{id_servico}" verb=PUT {
  api_group = "Serviços"
  auth = "user"
  input {
    int id_servico
    text descricao
    decimal valor
    int id_os
  }
  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    // Proteção cooperativa: decisões e escrita na mesma transação de dados.
    db.transaction {
      stack {
        precondition ($input.id_servico > 0) {
          error_type = "inputerror"
          error = "id_servico deve ser um inteiro positivo."
        }
        db.get ordem_servico {
          field_name = "id"
          field_value = $input.id_os
          output = ["id"]
          lock = true
        } as $ordem_protegida

        db.get servico {
          field_name = "id"
          field_value = $input.id_servico
          lock = true
        } as $servico
        precondition ($servico != null) {
          error_type = "notfound"
          error = "Servico nao encontrado."
        }
        function.run "servicos/validar_os" {
          input = {id_os: $input.id_os}
        } as $vinculo
        db.edit servico {
          field_name = "id"
          field_value = $servico.id
          data = {descricao: $input.descricao, valor: $input.valor, id_os: $vinculo.id_os}
        } as $resultado
      }
    }
  }
  response = {id_servico: $resultado.id, descricao: $resultado.descricao, valor: $resultado.valor, id_os: $resultado.id_os}
}
