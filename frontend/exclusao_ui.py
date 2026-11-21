"""Confirmação compartilhada de exclusão; nunca envia requisição por rerun."""
import streamlit as st
from apresentacao import botao_destrutivo


def invalidar(estado, campo):
    estado[campo] = None
    estado["lista"] = None
    estado["geracao"] += 1


def pendente(estado, campo, consultar, ausente, erro, tratar):
    identifier = estado.get("exclusao_pendente")
    if identifier is None:
        return False
    st.warning("Exclusão não confirmada. Confira o estado antes de outra escrita.")
    if st.button("Conferir exclusão pendente"):
        try:
            consultar(identifier)
        except ausente:
            invalidar(estado, campo)
            estado.update(exclusao_pendente=None, aviso="Ausência observada na conferência. Nenhuma exclusão foi reenviada.")
        except erro as error:
            tratar(error)
            return True
        else:
            invalidar(estado, campo)
            estado.update(exclusao_pendente=None, aviso="O registro ainda existe. Carregue e confirme novamente antes de outra tentativa.")
        st.rerun()
    return True


def render(estado, campo, identifier, nome, excluir, consultar, ausente, erro, tratar):
    confirmed = st.checkbox(f"Confirmo excluir {nome} {identifier}",
        key=f"excluir_{campo}_{identifier}_{estado['geracao']}")
    if not (botao_destrutivo(f"Excluir {nome}", disabled=not confirmed) and confirmed):
        return
    invalidar(estado, campo)
    estado.update(sucesso=None, aviso=None, exclusao_pendente=identifier)
    try:
        excluir(identifier)
    except erro as error:
        if not error.incerto:
            estado["exclusao_pendente"] = None
        estado["aviso"] = "Exclusão não confirmada. Confira o estado antes de uma nova tentativa."
        tratar(error)
    else:
        try:
            consultar(identifier)
        except ausente:
            estado.update(exclusao_pendente=None, sucesso="Registro excluído e ausência confirmada.")
        except erro as error:
            estado["aviso"] = "Exclusão não confirmada. Use a conferência explícita."
            tratar(error)
        else:
            estado["aviso"] = "O registro ainda existe. Exclusão não confirmada."
    st.rerun()
