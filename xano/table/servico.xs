// Proposta local: ID nativo exposto como id_servico pela API.
table servico {
  auth = false
  schema {
    int id
    text descricao
    decimal valor
    int id_os { table = "ordem_servico" }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "id_os"}]}
  ]
}
