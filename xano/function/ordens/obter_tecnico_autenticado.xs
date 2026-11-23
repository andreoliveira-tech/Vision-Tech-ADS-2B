// O vínculo deriva da identidade autenticada; não aceita id_tecnico do request.
function "ordens/obter_tecnico_autenticado" {
  description = "Retorna o Técnico associado à identidade autenticada."

  input {
    int user_id
  }

  stack {
    db.get user_application_profile {
      field_name = "user_id"
      field_value = $input.user_id
      output = ["user_id", "perfil_aplicacao"]
    } as $usuario

    precondition ($usuario != null && $usuario.perfil_aplicacao == "tecnico") {
      error_type = "accessdenied"
      error = "Identidade tecnica sem associacao valida."
    }

    db.get user_tecnico {
      field_name = "user_id"
      field_value = $usuario.user_id
      output = ["user_id", "id_tecnico"]
    } as $vinculo

    precondition ($vinculo != null) {
      error_type = "accessdenied"
      error = "Identidade tecnica sem associacao valida."
    }

    db.get tecnico {
      field_name = "id"
      field_value = $vinculo.id_tecnico
      output = ["id"]
    } as $tecnico

    precondition ($tecnico != null && $tecnico.id == $vinculo.id_tecnico) {
      error_type = "accessdenied"
      error = "Identidade tecnica sem associacao valida."
    }
  }

  response = {id_tecnico: $tecnico.id}
}
