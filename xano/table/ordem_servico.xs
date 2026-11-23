// Modelo físico local da OS; os nomes conceituais são preservados.
table ordem_servico {
  auth = false

  schema {
    int id

    date data_entrada

    date? data_saida?

    text problema_relatado

    enum status {
      values = ["Aguardando avaliação", "Em manutenção", "Aguardando peça", "Concluído", "Entregue"]
    }

    decimal valor_total

    int id_equipamento {
      table = "equipamento"
    }

    int id_tecnico {
      table = "tecnico"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_equipamento"}]}
    {type: "btree", field: [{name: "id_tecnico"}]}
  ]
}
