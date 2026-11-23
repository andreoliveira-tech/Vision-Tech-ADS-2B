query "servicos" verb=POST {
  api_group = "Serviços"
  auth = "user"
  input {
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
        db.get ordem_servico {
          field_name = "id"
          field_value = $input.id_os
          output = ["id"]
          lock = true
        } as $ordem_protegida

        function.run "servicos/validar_os" {
          input = {id_os: $input.id_os}
        } as $vinculo
        db.add servico {
          data = {descricao: $input.descricao, valor: $input.valor, id_os: $vinculo.id_os}
        } as $resultado
      }
    }
  }
  response = {id_servico: $resultado.id, descricao: $resultado.descricao, valor: $resultado.valor, id_os: $resultado.id_os}
}
