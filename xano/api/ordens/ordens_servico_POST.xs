// Cadastro para colaborador; Xano gera ordem_servico.id, exposto como id_os.
query "ordens-servico" verb=POST {
  api_group = "Ordens de Serviço"
  auth = "user"

  input {
    date data_entrada
    date? data_saida?
    text problema_relatado
    enum status {
      values = ["Aguardando avaliação", "Em manutenção", "Aguardando peça", "Concluído", "Entregue"]
    }
    decimal valor_total
    int id_equipamento
    int id_tecnico
  }

  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    // Proteção cooperativa: decisões e escrita na mesma transação de dados.
    db.transaction {
      stack {
        db.get tecnico {
          field_name = "id"
          field_value = $input.id_tecnico
          output = ["id"]
          lock = true
        } as $tecnico_protegido

        function.run "ordens/validar_vinculos" {
          input = {
            id_equipamento: $input.id_equipamento
            id_tecnico: $input.id_tecnico
          }
        } as $vinculos

        db.add ordem_servico {
          data = {
            data_entrada: $input.data_entrada
            data_saida: $input.data_saida
            problema_relatado: $input.problema_relatado
            status: $input.status
            valor_total: $input.valor_total
            id_equipamento: $vinculos.id_equipamento
            id_tecnico: $vinculos.id_tecnico
          }
        } as $ordem
      }
    }
  }

  response = {
    id_os: $ordem.id
    data_entrada: $ordem.data_entrada
    data_saida: $ordem.data_saida
    problema_relatado: $ordem.problema_relatado
    status: $ordem.status
    valor_total: $ordem.valor_total
    id_equipamento: $ordem.id_equipamento
    id_tecnico: $ordem.id_tecnico
  }
}
