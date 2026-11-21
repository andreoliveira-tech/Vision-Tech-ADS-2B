"""Login Streamlit baseado exclusivamente no Xano Authentication."""

import streamlit as st
from apresentacao import aplicar_tema, botao_destrutivo

import auth_api
import auth_session
from config import load_auth_api_base_url
from login_erp import layout_login


def render():
    aplicar_tema()
    with layout_login():
        st.title("Entrar no Sistema de Assistência Técnica")
        notice = st.session_state.pop("auth_notice", None)
        if notice:
            st.warning(notice)
        config_error = False
        try:
            base = load_auth_api_base_url()
        except ValueError as error:
            st.error(str(error))
            base = None
            config_error = True
        if base is None:
            if not config_error:
                st.info("Configure XANO_AUTH_API_BASE_URL com a URL do grupo Authentication publicado.")
        if auth_session.usuario_atual() and st.session_state.get("auth_token"):
            st.info("A sessão está guardada localmente; o perfil será revalidado pelo Xano antes de liberar a navegação.")
            st.button("Sair da sessão local", on_click=auth_session.encerrar_sessao)
            return
        with st.form("login_xano", clear_on_submit=True, enter_to_submit=False):
            email = st.text_input("E-mail", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")
            submit = st.form_submit_button("Entrar", disabled=base is None)
        if submit:
            try:
                result = auth_api.autenticar(base, email, password)
            except auth_api.AuthError as error:
                st.error(str(error))
            else:
                auth_session.salvar_sessao(result["token"], result["user"])
                st.rerun()
        st.caption("O acesso depende de uma conta provisionada e autorizada no Xano.")


render()
