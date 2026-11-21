"""Ponto de entrada com navegação Streamlit filtrada pelo perfil retornado pelo Xano."""

import streamlit as st
from apresentacao import aplicar_tema, marca

import auth_api
import auth_session
from config import load_auth_api_base_url


PAGINAS = {
    "colaborador": (
        ("Clientes", "clientes_page.py"),
        ("Equipamentos", "pages/1_Equipamentos.py"),
        ("Técnicos", "pages/2_Tecnicos.py"),
        ("Ordens de Serviço", "pages/3_Ordens_de_Servico.py"),
        ("Serviços", "pages/5_Servicos.py"),
    ),
    "tecnico": (("Minhas Ordens", "pages/4_Painel_Tecnico.py"),),
}


def paginas_do_perfil(role):
    """Retorna somente a navegação permitida ao perfil confirmado pelo backend."""
    return PAGINAS.get(role, ())


def _controles_sessao(user):
    st.sidebar.caption(f"{user.get('name') or user.get('email')} · {user['role'].capitalize()}")
    st.sidebar.button("Sair", key="logout", on_click=auth_session.encerrar_sessao)


def render():
    st.set_page_config(page_title="Assistência Técnica", layout="wide", initial_sidebar_state="auto")
    aplicar_tema()
    marca()
    try:
        auth_base = load_auth_api_base_url()
    except ValueError:
        # A página de login exibe o erro e mantém o formulário visível, mas
        # bloqueia o envio enquanto a URL não for válida.
        auth_base = None

    user = auth_session.usuario_atual()
    token = st.session_state.get("auth_token")
    if user and token and auth_base:
        try:
            current = auth_api.consultar_usuario(auth_base, token, expected_id=user.get("id"))
        except auth_api.SessaoExpirada as error:
            auth_session.encerrar_sessao()
            st.session_state["auth_notice"] = str(error)
            user = None
        except auth_api.PerfilSemAcesso as error:
            auth_session.encerrar_sessao()
            st.session_state["auth_notice"] = str(error)
            user = None
        except auth_api.BackendIndisponivel as error:
            st.session_state["auth_notice"] = str(error)
            user = None
        else:
            auth_session.salvar_sessao(token, current)
            user = current
    elif user or token:
        auth_session.encerrar_sessao()
        user = None

    login_page = st.Page("login_page.py", title="Entrar", icon="🔐", default=not user)
    if user and user["role"] == "colaborador":
        _controles_sessao(user)
        icons = {"Clientes": "👥", "Equipamentos": "🖥️", "Técnicos": "🧰", "Ordens de Serviço": "📋", "Serviços": "🔧"}
        pages = {"Administrativo": [st.Page(path, title=title, icon=icons[title]) for title, path in paginas_do_perfil(user["role"])]}
    elif user and user["role"] == "tecnico":
        _controles_sessao(user)
        pages = {"Técnico": [st.Page(path, title=title, icon="🛠️", default=True) for title, path in paginas_do_perfil(user["role"])]}
    else:
        pages = {"Acesso": [login_page]}

    st.navigation(pages, position="sidebar").run()


render()
