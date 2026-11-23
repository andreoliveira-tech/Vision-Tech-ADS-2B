// Exclui cliente sem equipamentos; protecao limitada a operacoes sequenciais.
query "clientes/{id_cliente}" verb=DELETE {
  api_group = "Clientes"
  auth = "user"

  input {
    int id_cliente
  }

  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    precondition ($input.id_cliente > 0) {
      error_type = "inputerror"
      error = "Informe um identificador inteiro positivo."
    }
  
    db.get cliente {
      field_name = "id"
      field_value = $input.id_cliente
      output = ["id"]
    } as $cliente
  
    precondition ($cliente != null) {
      error_type = "notfound"
      error = "Cliente nao encontrado."
    }
  
    function.run "clientes/consultar_dependencias" {
      input = {id_cliente: $cliente.id}
    } as $dependencias
  
    precondition ($dependencias != null && $dependencias.id_cliente == $cliente.id) {
      error_type = "inputerror"
      error = "Nao foi possivel confirmar os vinculos do cliente."
    }
  
    precondition ($dependencias.bloqueia_exclusao == false && $dependencias.possui_equipamentos == false) {
      error_type = "inputerror"
      error = "Cliente possui equipamentos vinculados. Exclusao bloqueada."
    }
  
    db.del cliente {
      field_name = "id"
      field_value = $cliente.id
    }
  }

  response = {id_cliente: $cliente.id, excluido: true}

}
