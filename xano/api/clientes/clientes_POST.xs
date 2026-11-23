// Cadastra um cliente somente após validar e normalizar todos os dados.
query clientes verb=POST {
  api_group = "Clientes"
  auth = "user"

  input {
    text nome
    text cpf
    text telefone
    email email
  }

  stack {
    function.run "ordens/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    function.run "clientes/validar_dados" {
      input = {
        nome: $input.nome
        cpf: $input.cpf
        telefone: $input.telefone
        email: $input.email
      }
    } as $dados_validados

    db.add cliente {
      data = {
        nome: $dados_validados.nome
        cpf: $dados_validados.cpf
        telefone: $dados_validados.telefone
        email: $dados_validados.email
      }
    } as $cliente
  }

  response = {
    id_cliente: $cliente.id
    nome: $cliente.nome
    cpf: $cliente.cpf
    telefone: $cliente.telefone
    email: $cliente.email
  }
}
