query "tecnicos/{id_tecnico}" verb=DELETE {
  api_group = "Técnicos"
  auth = "user"
  input { int id_tecnico }
  stack {
    function.run "tecnicos/autorizar_colaborador" {
      input = {user_id: $auth.id}
    } as $autorizacao

    // Proteção cooperativa: decisões e escrita na mesma transação de dados.
    db.transaction {
      stack {
        precondition ($input.id_tecnico > 0) {
          error_type = "inputerror"
          error = "id_tecnico deve ser um inteiro positivo."
        }
        db.get tecnico {
          field_name = "id"
          field_value = $input.id_tecnico
          lock = true
        } as $tecnico
        precondition ($tecnico != null) {
          error_type = "notfound"
          error = "Tecnico nao encontrado."
        }
        function.run "tecnicos/consultar_dependencias" {
          input = {id_tecnico: $tecnico.id}
        } as $dependencias
        precondition ($dependencias != null && $dependencias.id_tecnico == $tecnico.id && ($dependencias.possui_os == true || $dependencias.possui_os == false) && ($dependencias.possui_usuario == true || $dependencias.possui_usuario == false)) {
          error_type = "inputerror"
          error = "Nao foi possivel confirmar as dependencias do tecnico."
        }
        precondition ($dependencias.possui_os == false) {
          error_type = "inputerror"
          error = "Tecnico possui ordens de servico vinculadas. Exclusao bloqueada."
        }
        precondition ($dependencias.possui_usuario == false) {
          error_type = "inputerror"
          error = "Tecnico possui vinculo de usuario. Exclusao bloqueada."
        }
        db.del tecnico {
          field_name = "id"
          field_value = $tecnico.id
        }
      }
    }
  }
  response = {id_tecnico: $tecnico.id, excluido: true}
}
