// Vínculo técnico de identidade, sem nullable unique e sem novo conceito de negócio.
table user_tecnico {
  auth = false

  schema {
    int id
    int user_id {
      table = "user"
    }
  
    int id_tecnico {
      table = "tecnico"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id", op: "asc"}]}
    {
      type : "btree|unique"
      field: [{name: "id_tecnico", op: "asc"}]
    }
  ]

  guid = "reGUcbHu3m8zizI4LH2r8506-js"
}