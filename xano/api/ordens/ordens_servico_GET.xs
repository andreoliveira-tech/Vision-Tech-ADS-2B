query "ordens-servico" verb=GET {
  api_group = "Ordens de Serviço"
  auth = "user"

  input {
  }

  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    db.query ordem_servico {
      return = {type: "list"}
      output = ["id", "data_entrada", "data_saida", "problema_relatado", "status", "valor_total", "id_equipamento", "id_tecnico"]
    } as $ordens
  }

  response = $ordens|map:{
    id_os: $$.id
    data_entrada: $$.data_entrada
    data_saida: $$.data_saida
    problema_relatado: $$.problema_relatado
    status: $$.status
    valor_total: $$.valor_total
    id_equipamento: $$.id_equipamento
    id_tecnico: $$.id_tecnico
  }
}
