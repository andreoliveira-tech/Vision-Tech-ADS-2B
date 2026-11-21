"""Gestão Streamlit de Ordens de Serviço para colaboradores autorizados."""

from datetime import date

import streamlit as st
from apresentacao import (aplicar_tema, botao_destrutivo, status_rotulo, badge_status,
                          filtrar_ordens, indicadores_ordens)

import ordens_api as api
import auth_session
import exclusao_ui
from config import load_ordens_api_base_url


def _id(text):
    if not isinstance(text, str) or not text.strip().isdecimal() or int(text) <= 0:
        raise api.OrdemError("Informe um identificador inteiro positivo.")
    return int(text)


def _invalidar_ordem(estado):
    estado["ordem"] = None
    estado["geracao"] += 1


def _erro_exclusao(error, estado):
    if isinstance(error, api.AcessoNegado):
        base = estado["base"]
        estado.clear()
        estado.update(base=base, bloqueado=True)
        st.rerun()
    auth_session.tratar_erro_api(error)


def _form(prefix, atual=None):
    atual = atual or {}
    entrada_default = date.fromisoformat(atual["data_entrada"]) if atual.get("data_entrada") else date.today()
    saida_atual = atual.get("data_saida")
    entrada = st.date_input("Data de entrada", value=entrada_default, key=prefix + "entrada")
    tem_saida = st.checkbox("Informar data de saída", value=saida_atual is not None, key=prefix + "tem_saida")
    saida = st.date_input("Data de saída", value=date.fromisoformat(saida_atual) if saida_atual else date.today(), key=prefix + "saida") if tem_saida else None
    problema = st.text_area("Problema relatado", value=atual.get("problema_relatado", ""), key=prefix + "problema")
    status = st.selectbox("Status", api.STATUS, index=api.STATUS.index(atual["status"]) if atual.get("status") in api.STATUS else 0, key=prefix + "status", format_func=status_rotulo)
    valor = st.number_input("Valor total", value=float(atual.get("valor_total", 0)), key=prefix + "valor")
    equipamento = st.number_input("ID do equipamento", min_value=1, step=1, value=int(atual.get("id_equipamento", 1)), key=prefix + "equipamento")
    tecnico = st.number_input("ID do técnico", min_value=1, step=1, value=int(atual.get("id_tecnico", 1)), key=prefix + "tecnico")
    return {"data_entrada": entrada.isoformat(), "data_saida": saida.isoformat() if saida else None, "problema_relatado": problema, "status": status, "valor_total": valor, "id_equipamento": int(equipamento), "id_tecnico": int(tecnico)}


def render():
    aplicar_tema()
    auth_session.exigir_perfil("colaborador")
    st.title("Ordens de Serviço")
    st.caption("Cadastro e acompanhamento de ordens por colaboradores autorizados.")
    try:
        base = load_ordens_api_base_url()
    except ValueError as error:
        st.error(str(error))
        return
    if base is None:
        st.info("Configure XANO_ORDENS_API_BASE_URL com a URL do grupo publicado.")
        return
    token = st.session_state.get("auth_token")
    if not isinstance(token, str) or not token.strip():
        st.info("Entre por um mecanismo de autenticação real para acessar as ordens.")
        return

    anterior = st.session_state.get("ordens", {})
    if anterior.get("base") != base:
        st.session_state["ordens"] = {
            "base": base, "lista": None, "ordem": None,
            "geracao": anterior.get("geracao", 0) + 1,
            "aviso": None, "sucesso": None,
        }
    estado = st.session_state["ordens"]
    if estado.get("bloqueado"):
        st.error("Acesso administrativo negado. Saia e entre novamente para revalidar a sessão.")
        return
    for chave, valor in (("geracao", 0), ("aviso", None), ("sucesso", None)):
        estado.setdefault(chave, valor)
    if exclusao_ui.pendente(estado, "ordem",
            lambda identifier: api.consultar_ordem(base, token, identifier, confirmar_ausencia=True),
            api.OrdemNaoEncontrada, api.OrdemError, lambda error: _erro_exclusao(error, estado)):
        return
    lista_aba, cadastro_aba = st.tabs(["Ordens cadastradas", "Cadastrar OS"])
    with cadastro_aba:
        st.subheader("Cadastrar Ordem de Serviço")
        with st.form("cadastro_ordem", enter_to_submit=False):
            dados = _form("nova_")
            enviar = st.form_submit_button("Cadastrar OS", type="primary")
        if enviar:
            estado.update(aviso=None, sucesso=None)
            try:
                criada = api.cadastrar_ordem(base, token, dados)
            except api.OrdemError as error:
                auth_session.tratar_erro_api(error)
            else:
                estado["lista"] = None
                st.success(f"Ordem de Serviço cadastrada. Identificador: {criada['id_os']}.")

    with lista_aba:
        with st.container(key="os_table_header"):
            titulo_lista, acao_lista = st.columns([1, 1], gap="small")
            titulo_lista.subheader("Ordens cadastradas")
            with acao_lista:
                atualizar_lista = st.button("Atualizar lista de OS")
        if atualizar_lista:
            estado.update(lista=None, sucesso=None)
            try:
                estado["lista"] = api.listar_ordens(base, token)
            except api.OrdemError as error:
                auth_session.tratar_erro_api(error)
        if estado["lista"] is not None:
            if estado["lista"]:
                indicadores_ordens(estado["lista"])
                f_status, f_tecnico, f_busca = st.columns(3)
                status_filtro = f_status.selectbox("Filtrar por status", ["Todos", *api.STATUS], key="os_filtro_status", format_func=status_rotulo)
                tecnicos = sorted({o["id_tecnico"] for o in estado["lista"]})
                tecnico_filtro = f_tecnico.selectbox("Filtrar por técnico", ["Todos", *tecnicos], key="os_filtro_tecnico", format_func=lambda v: v if v == "Todos" else f"Técnico #{v}")
                busca = f_busca.text_input("Buscar OS", key="os_filtro_busca")
                filtradas = filtrar_ordens(estado["lista"], status_filtro, tecnico_filtro, busca)
                if filtradas:
                    import pandas as pd
                    from apresentacao import STATUS_CORES
                    tabela = pd.DataFrame(filtradas).style.map(lambda valor: "color:"+STATUS_CORES[valor][0]+";background-color:"+STATUS_CORES[valor][1], subset=["status"]).format({"status": status_rotulo})
                    st.dataframe(tabela, hide_index=True)
                else:
                    st.info("Nenhuma OS corresponde aos filtros.")
            else:
                st.info("Nenhuma Ordem de Serviço cadastrada.")

        st.subheader("Consultar ou editar OS")
        # Fora de form: a troca do ID invalida imediatamente a confirmação anterior.
        texto_id = st.text_input("ID da OS", key="ordem_consulta_id")
        carregar = st.button("Carregar OS")
        if carregar:
            _invalidar_ordem(estado)
            estado.update(aviso=None, sucesso=None)
            try:
                estado["ordem"] = api.consultar_ordem(base, token, _id(texto_id))
            except api.OrdemError as error:
                auth_session.tratar_erro_api(error)
        if estado["aviso"]:
            st.warning(estado["aviso"])
        if estado["sucesso"]:
            st.success(estado["sucesso"])
        atual = estado["ordem"]
        if atual is not None and texto_id.strip() != str(atual["id_os"]):
            _invalidar_ordem(estado)
            atual = None
        if atual is not None:
            st.write({"id_os": atual["id_os"]})
            st.markdown(badge_status(atual["status"]), unsafe_allow_html=True)
            with st.form("editar_ordem", enter_to_submit=False):
                alterados = _form(f"editar_{estado['geracao']}_", atual)
                salvar = st.form_submit_button("Salvar alterações")
            if salvar:
                identificador = atual["id_os"]
                # Consome o alvo e os controles antes de qualquer tentativa de escrita.
                _invalidar_ordem(estado)
                estado.update(lista=None, aviso=None, sucesso=None)
                try:
                    retorno = api.atualizar_ordem(base, token, identificador, alterados)
                    if retorno != {"id_os": identificador, **alterados}:
                        raise api.OrdemError("A resposta divergiu dos dados enviados.", incerto=True)
                    conferido = api.consultar_ordem(base, token, identificador)
                    if retorno != conferido:
                        raise api.OrdemError("A consulta posterior divergiu da atualização.")
                except api.OrdemError as error:
                    estado["aviso"] = "Atualização não confirmada. Carregue a OS novamente antes de outra escrita. " + str(error)
                    auth_session.tratar_erro_api(error)
                else:
                    estado.update(ordem=conferido, sucesso="Ordem de Serviço atualizada e conferida por nova consulta.")
                st.rerun()
            exclusao_ui.render(estado, "ordem", atual["id_os"], "OS",
                lambda identifier: api.excluir_ordem(base, token, identifier),
                lambda identifier: api.consultar_ordem(base, token, identifier, confirmar_ausencia=True),
                api.OrdemNaoEncontrada, api.OrdemError, lambda error: _erro_exclusao(error, estado))
