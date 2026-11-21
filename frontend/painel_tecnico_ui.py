"""Painel de OS atribuídas; a API protegida fornece também os dados do equipamento."""

import streamlit as st
from html import escape
from apresentacao import aplicar_tema, badge_status, status_rotulo, destaque_status

import auth_session
import ordens_api
from config import load_ordens_api_base_url


def _carregar(base_os, token):
    return ordens_api.listar_minhas_ordens(base_os, token)


def render():
    aplicar_tema()
    token, _ = auth_session.exigir_perfil("tecnico")
    with st.container(key="tech_header"):
        titulo, acao = st.columns([3, 1], gap="small")
        with titulo:
            st.title("Minhas Ordens de Serviço")
            st.caption("Ordens vinculadas ao seu cadastro de Técnico.")
        with acao:
            atualizar = st.button("Atualizar minhas ordens", key="refresh_minhas_ordens")
    try:
        base_os = load_ordens_api_base_url()
    except ValueError as error:
        st.error(str(error))
        return
    if base_os is None:
        st.error("Configure a URL do grupo Ordens de Serviço publicado.")
        return

    anterior = st.session_state.get("painel_tecnico", {})
    if anterior.get("base_os") != base_os:
        st.session_state["painel_tecnico"] = {
            "base_os": base_os, "ordens": None, "tentada": False,
            "geracao": anterior.get("geracao", 0) + 1, "erro": None, "sucesso": None,
        }
    state = st.session_state["painel_tecnico"]
    for chave, valor in (("tentada", state["ordens"] is not None), ("geracao", 0), ("erro", None), ("sucesso", None)):
        state.setdefault(chave, valor)

    if atualizar:
        state.update(ordens=None, tentada=False, erro=None, sucesso=None, geracao=state["geracao"] + 1)

    if state["ordens"] is None and not state["tentada"]:
        # Uma falha não pode rearmar a consulta em um rerun qualquer.
        state["tentada"] = True
        try:
            state["ordens"] = _carregar(base_os, token)
        except ordens_api.OrdemError as error:
            state["erro"] = str(error)
            auth_session.tratar_erro_api(error)
            return

    if state["erro"]:
        st.error(state["erro"] + " Use Atualizar minhas ordens para consultar novamente.")
        return
    if state["sucesso"]:
        st.success(state["sucesso"])

    ordens = state["ordens"]
    if ordens is None:
        return
    if not ordens:
        st.info("Você não tem Ordens de Serviço atribuídas.")
        return

    with st.container(key="technician_preview"):
        _cartoes(ordens, state, base_os, token)


def _cartoes(ordens, state, base_os, token):
    for order in ordens:
        marca = order["equipamento_marca"] or "Não informado"
        modelo = order["equipamento_modelo"] or "Não informado"
        title = f"OS {order['id_os']} · {marca} {modelo}"
        chave = f"tech_card_{order['id_os']}"
        destaque_status(chave, order["status"], ordens_api.STATUS)
        with st.container(border=True, key=chave):
            st.subheader(title)
            st.markdown(badge_status(order["status"]), unsafe_allow_html=True)
            equipamento = f"{order['equipamento_tipo']} — {marca} {modelo}"
            st.markdown('<div class="tech-card-data"><div class="tech-problem">'
                        '<span class="tech-pair-label">Problema relatado</span>'
                        '<div class="tech-pair-value">'+escape(order['problema_relatado'])+'</div></div>'
                        '<div class="tech-pairs"><div><span class="tech-pair-label">Equipamento</span>'
                        '<div class="tech-pair-value">'+escape(equipamento)+'</div></div>'
                        '<div><span class="tech-pair-label">Data de entrada</span>'
                        '<div class="tech-pair-value">'+escape(order['data_entrada'])+'</div></div></div></div>',
                        unsafe_allow_html=True)
            st.divider()
            with st.form(f"status_os_{order['id_os']}", enter_to_submit=False):
                selected = st.selectbox(
                    "Atualizar status",
                    ordens_api.STATUS,
                    index=ordens_api.STATUS.index(order["status"]),
                    key=f"status_selecionado_{order['id_os']}_{state['geracao']}",
                    format_func=status_rotulo,
                )
                submit = st.form_submit_button("Salvar status")
            if submit:
                state["sucesso"] = None
                try:
                    confirmed = ordens_api.atualizar_status_minha_ordem(base_os, token, order["id_os"], selected)
                except ordens_api.OrdemError as error:
                    state.update(ordens=None, tentada=True, erro="Atualização não confirmada. " + str(error),
                                 geracao=state["geracao"] + 1)
                    auth_session.tratar_erro_api(error)
                else:
                    order["status"] = confirmed["status"]
                    state.update(sucesso=f"Status da OS {confirmed['id_os']} confirmado: {confirmed['status']}.",
                                 geracao=state["geracao"] + 1)
                st.rerun()
