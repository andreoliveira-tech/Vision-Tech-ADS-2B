"""Estado efêmero de autenticação na sessão Streamlit."""

import streamlit as st


AUTH_KEYS = ("auth_token", "auth_user", "auth_notice")
PAGE_STATE_KEYS = ("tecnicos", "equipamentos", "ordens", "painel_tecnico",
                   "clientes_listagem", "cliente_consulta", "cliente_edicao",
                   "cliente_exclusao", "clientes_acesso_negado", "servicos")


def encerrar_sessao():
    for key in (*AUTH_KEYS, *PAGE_STATE_KEYS):
        st.session_state.pop(key, None)


def salvar_sessao(token, user):
    st.session_state["auth_token"] = token
    st.session_state["auth_user"] = user
    st.session_state.pop("auth_notice", None)


def usuario_atual():
    user = st.session_state.get("auth_user")
    return user if isinstance(user, dict) else None


def exigir_perfil(*profiles):
    user = usuario_atual()
    if not st.session_state.get("auth_token") or not user:
        st.info("Entre com uma conta autorizada para acessar esta área.")
        st.stop()
    if user.get("role") not in profiles:
        st.error("Seu perfil não tem acesso a esta área.")
        st.stop()
    return st.session_state["auth_token"], user


def tratar_erro_api(error):
    if error.__class__.__name__ in ("SessaoExpirada", "SessaoNecessaria"):
        encerrar_sessao()
        st.session_state["auth_notice"] = "A sessão expirou. Entre novamente."
        st.rerun()
    st.error(str(error))
