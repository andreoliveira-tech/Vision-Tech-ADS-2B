"""Gestão administrativa de Serviços, com escritas explícitas e conferidas."""
import streamlit as st
from apresentacao import aplicar_tema, botao_destrutivo
import auth_session
import servicos_api as api
from config import load_servicos_api_base_url


def _id(text):
    if not isinstance(text, str) or not text.strip().isdecimal():
        raise api.ServicoError("Informe um identificador inteiro positivo.")
    return api.identificador(int(text))


def _fields(prefix, row=None):
    row = row or {}
    description = st.text_input("Descrição", value=row.get("descricao", ""), key=prefix + "descricao")
    price = st.number_input("Valor", value=float(row.get("valor", 0)), key=prefix + "valor", format="%.4f")
    order = st.text_input("ID da OS", value=str(row.get("id_os", "")), key=prefix + "os")
    return {"descricao": description, "valor": price}, order


def _clear_target(state):
    state.update(dados=None, geracao=state["geracao"] + 1)


def _error(error, state):
    if isinstance(error, api.AcessoNegado):
        base = state["base"]
        state.clear()
        state.update(base=base, bloqueado=True)
        st.rerun()
    auth_session.tratar_erro_api(error)


def render():
    aplicar_tema()
    token, _ = auth_session.exigir_perfil("colaborador")
    st.title("Serviços")
    st.caption("Serviços realizados nas Ordens de Serviço. O total da OS permanece independente.")
    try:
        base = load_servicos_api_base_url()
    except ValueError as error:
        st.error(str(error))
        return
    if base is None:
        st.info("Configure a URL do grupo Serviços publicado para usar este módulo.")
        return
    previous = st.session_state.get("servicos", {})
    if previous.get("base") != base:
        st.session_state.servicos = {"base": base, "lista": None, "dados": None,
            "selecao": "", "geracao": previous.get("geracao", 0) + 1,
            "sucesso": None, "aviso": None, "cadastro_pendente": None,
            "exclusao_pendente": None, "bloqueado": False}
    state = st.session_state.servicos
    if state["bloqueado"]:
        st.error("Acesso administrativo negado. Saia e entre novamente para revalidar a sessão.")
        return
    if state["sucesso"]:
        st.success(state["sucesso"])
    if state["aviso"]:
        st.warning(state["aviso"])

    st.subheader("Cadastrar serviço")
    pending = state["cadastro_pendente"]
    with st.form("cadastro_servico", enter_to_submit=False):
        payload, order = _fields("servico_novo_")
        submit = st.form_submit_button("Cadastrar serviço", disabled=pending is not None)
    if submit and pending is None:
        state.update(sucesso=None, aviso=None, lista=None)
        try:
            payload["id_os"] = _id(order)
            payload = api.dados(payload)
            created = api.cadastrar_servico(base, token, payload)
        except api.ServicoError as error:
            _error(error, state)
            if error.incerto:
                state["cadastro_pendente"] = {"dados": payload, "id": None, "consultado": False}
                state["aviso"] = "Cadastro incerto. Confira a listagem antes de autorizar outra tentativa."
                st.rerun()
        else:
            state["cadastro_pendente"] = {"dados": payload, "id": created["id_servico"], "consultado": False}
            try:
                if api.consultar_servico(base, token, created["id_servico"]) != created:
                    raise api.ServicoError("Conferência divergente.")
            except api.ServicoError as error:
                _error(error, state)
                state["aviso"] = "Cadastro não confirmado. Use a conferência explícita."
            else:
                state.update(cadastro_pendente=None, sucesso=f"Serviço cadastrado e conferido. ID: {created['id_servico']}.")
            st.rerun()

    pending = state["cadastro_pendente"]
    if pending is not None:
        st.warning("Novo cadastro bloqueado até conferir o resultado anterior.")
        if st.button("Conferir cadastro pendente"):
            try:
                if pending["id"] is None:
                    rows = api.listar_servicos(base, token)
                    state["lista"] = rows
                    matches = [r for r in rows if {k: r[k] for k in api.CAMPOS} == pending["dados"]]
                    state["aviso"] = f"Conferência: {len(matches)} registro(s) compatível(is). Isso não atribui a criação à tentativa anterior. Revise a listagem."
                    pending["consultado"] = True
                else:
                    row = api.consultar_servico(base, token, pending["id"])
                    if {k: row[k] for k in api.CAMPOS} != pending["dados"]:
                        raise api.ServicoError("Conferência divergente; cadastro continua bloqueado.")
                    state.update(cadastro_pendente=None, aviso=None, sucesso=f"Serviço {pending['id']} conferido.")
            except api.ServicoError as error:
                _error(error, state)
            st.rerun()
        if pending["id"] is None and pending["consultado"]:
            reviewed = st.checkbox("Revisei a listagem e autorizo preparar outro cadastro", key="servico_revisao_cadastro")
            if st.button("Liberar novo formulário", disabled=not reviewed) and reviewed:
                state.update(cadastro_pendente=None, aviso=None)
                st.rerun()

    st.subheader("Serviços cadastrados")
    filter_order = st.text_input("Filtrar por ID da OS (opcional)", key="servico_filtro_os")
    if st.button("Atualizar serviços"):
        state.update(lista=None, sucesso=None)
        try:
            state["lista"] = api.listar_servicos(base, token)
        except api.ServicoError as error:
            _error(error, state)
    if state["lista"] is not None:
        try:
            selected = _id(filter_order) if filter_order.strip() else None
            rows = [r for r in state["lista"] if selected is None or r["id_os"] == selected]
        except api.ServicoError as error:
            st.error(str(error))
        else:
            if rows:
                st.dataframe(rows, hide_index=True)
            else:
                st.info("Nenhum serviço encontrado para a seleção.")

    st.subheader("Consultar, editar ou excluir serviço")
    selection = st.text_input("ID do serviço", key="servico_selecao")
    if selection != state["selecao"]:
        _clear_target(state)
        state.update(selecao=selection, sucesso=None, aviso=None)
    if st.button("Carregar serviço"):
        _clear_target(state)
        state.update(sucesso=None, aviso=None)
        try:
            state["dados"] = api.consultar_servico(base, token, _id(selection))
        except api.ServicoError as error:
            _error(error, state)

    pending_delete = state["exclusao_pendente"]
    if pending_delete is not None and st.button("Conferir exclusão pendente"):
        try:
            api.consultar_servico(base, token, pending_delete)
        except api.ServicoNaoEncontrado:
            state.update(exclusao_pendente=None, lista=None, aviso="Ausência observada. A tentativa anterior permaneceu sem confirmação.")
        except api.ServicoError as error:
            _error(error, state)
        else:
            state.update(exclusao_pendente=None, aviso="Serviço ainda existe. Carregue e confirme novamente antes de outra tentativa.")
        st.rerun()

    row = state["dados"]
    if row is None:
        return
    identifier = row["id_servico"]
    st.write(row)
    with st.form("editar_servico", enter_to_submit=False):
        payload, order = _fields(f"servico_editar_{state['geracao']}_", row)
        save = st.form_submit_button("Salvar serviço")
    if save:
        _clear_target(state)
        state.update(sucesso=None, aviso=None, lista=None)
        try:
            payload["id_os"] = _id(order)
            updated = api.atualizar_servico(base, token, identifier, payload)
            if api.consultar_servico(base, token, identifier) != updated:
                raise api.ServicoError("Consulta posterior divergente.")
        except api.ServicoError as error:
            _error(error, state)
            state["aviso"] = "Atualização não confirmada. Carregue novamente para conferir antes de outra escrita."
        else:
            state["sucesso"] = "Serviço atualizado e conferido."
        st.rerun()

    confirmed = st.checkbox(f"Confirmo excluir o serviço {identifier}", key=f"servico_excluir_{state['geracao']}")
    if botao_destrutivo("Excluir serviço", disabled=not confirmed) and confirmed:
        _clear_target(state)
        state.update(sucesso=None, aviso=None, lista=None)
        try:
            api.excluir_servico(base, token, identifier)
        except api.ServicoError as error:
            _error(error, state)
            if error.incerto:
                state["exclusao_pendente"] = identifier
            state["aviso"] = "Exclusão não confirmada. Confira o estado antes de uma nova tentativa."
        else:
            try:
                api.consultar_servico(base, token, identifier)
            except api.ServicoNaoEncontrado:
                state.update(exclusao_pendente=None, sucesso="Serviço excluído e ausência confirmada.")
            except api.ServicoError as error:
                _error(error, state)
                state.update(exclusao_pendente=identifier, aviso="Exclusão não confirmada. Use a conferência explícita.")
            else:
                state.update(exclusao_pendente=identifier, aviso="O serviço ainda existe. Exclusão não confirmada.")
        st.rerun()
