"""Tela Streamlit de gestão de Técnicos dependente da sessão real do aplicativo."""

import streamlit as st
from apresentacao import aplicar_tema, botao_destrutivo

import tecnicos_api as api
import auth_session
import exclusao_ui
from config import load_tecnicos_api_base_url


def _identificador(texto):
    try:
        if not texto.strip().isdecimal():
            raise ValueError
        value = int(texto)
        if value <= 0:
            raise ValueError
        return value
    except (ValueError, TypeError):
        raise api.TecnicoError("Informe um identificador inteiro positivo.") from None


def _campos(prefixo, dados=None):
    dados = dados or {}
    return {
        "nome": st.text_input("Nome", value=dados.get("nome", ""), key=prefixo + "nome"),
        "especialidade": st.text_input(
            "Especialidade", value=dados.get("especialidade", ""), key=prefixo + "especialidade"
        ),
        "telefone": st.text_input(
            "Telefone", value=dados.get("telefone", ""), key=prefixo + "telefone"
        ),
        "email": st.text_input("Email", value=dados.get("email", ""), key=prefixo + "email"),
    }


def _novo_estado(base, anterior=None):
    return {
        "base": base,
        "lista": None,
        "selecao": "",
        "dados": None,
        "geracao": (anterior or {}).get("geracao", 0) + 1,
        "sucesso": None,
        "aviso": None,
    }


def _erro_exclusao(error, estado):
    if isinstance(error, api.AcessoNegado):
        base = estado["base"]
        estado.clear()
        estado.update(base=base, bloqueado=True)
        st.rerun()
    auth_session.tratar_erro_api(error)


def render():
    aplicar_tema()
    auth_session.exigir_perfil("colaborador")
    st.title("Técnicos")
    st.caption("Cadastro e gerenciamento de técnicos por colaboradores autorizados.")
    try:
        base = load_tecnicos_api_base_url()
    except ValueError as error:
        st.error(str(error))
        return
    if base is None:
        st.info("Configure XANO_TECNICOS_API_BASE_URL com a URL do grupo publicado.")
        return

    # A sessão somente é consumida; esta página não autentica nem cria tokens.
    token = st.session_state.get("auth_token")
    if not isinstance(token, str) or not token.strip():
        st.info("Entre por um mecanismo de autenticação real para acessar a gestão de técnicos.")
        return

    if "tecnicos" not in st.session_state or st.session_state.tecnicos["base"] != base:
        st.session_state.tecnicos = _novo_estado(base, st.session_state.get("tecnicos"))
    estado = st.session_state.tecnicos
    if estado.get("bloqueado"):
        st.error("Acesso administrativo negado. Saia e entre novamente para revalidar a sessão.")
        return
    if exclusao_ui.pendente(estado, "dados",
            lambda identifier: api.consultar_tecnico(base, token, identifier, confirmar_ausencia=True),
            api.TecnicoNaoEncontrado, api.TecnicoError, lambda error: _erro_exclusao(error, estado)):
        return

    st.subheader("Cadastrar técnico")
    with st.form("cadastro_tecnico", enter_to_submit=False):
        dados_novos = _campos("novo_")
        cadastrar = st.form_submit_button("Cadastrar técnico")
    if cadastrar:
        estado.update(sucesso=None, aviso=None)
        try:
            criado = api.cadastrar_tecnico(base, token, dados_novos)
        except api.TecnicoError as error:
            auth_session.tratar_erro_api(error)
        else:
            estado["lista"] = None
            estado["sucesso"] = f"Técnico cadastrado. Identificador: {criado['id_tecnico']}."

    st.subheader("Técnicos cadastrados")
    if st.button("Atualizar lista de técnicos"):
        estado["lista"] = None
        try:
            estado["lista"] = api.listar_tecnicos(base, token)
        except api.TecnicoError as error:
            auth_session.tratar_erro_api(error)
    if estado["lista"] is not None:
        if estado["lista"]:
            st.dataframe(estado["lista"], hide_index=True)
        else:
            st.info("Nenhum técnico cadastrado.")

    st.subheader("Consultar ou editar técnico")
    selecao = st.text_input("ID do técnico", key="tecnico_selecao")
    if selecao != estado["selecao"]:
        estado.update(selecao=selecao, dados=None, sucesso=None, aviso=None)
        estado["geracao"] += 1
    if st.button("Carregar técnico"):
        estado.update(
            dados=None, sucesso=None, aviso=None, geracao=estado["geracao"] + 1
        )
        try:
            estado["dados"] = api.consultar_tecnico(base, token, _identificador(selecao))
        except api.TecnicoError as error:
            auth_session.tratar_erro_api(error)

    if estado["sucesso"]:
        st.success(estado["sucesso"])
    if estado["aviso"]:
        st.warning(estado["aviso"])
    atual = estado["dados"]
    if atual is None:
        return

    identificador = atual["id_tecnico"]
    st.write({"id_tecnico": identificador})
    with st.form(f"editar_tecnico_{estado['geracao']}", enter_to_submit=False):
        alterado = _campos(f"editar_{estado['geracao']}_", atual)
        salvar = st.form_submit_button("Salvar alterações")
    if salvar:
        estado.update(sucesso=None, aviso=None)
        try:
            retorno = api.atualizar_tecnico(base, token, identificador, alterado)
            conferido = api.consultar_tecnico(base, token, identificador)
            if conferido != retorno:
                raise api.TecnicoError("Consulta posterior divergente.")
        except api.TecnicoError as error:
            if error.__class__.__name__ in ("SessaoExpirada", "SessaoNecessaria"):
                auth_session.tratar_erro_api(error)
            estado.update(dados=None, aviso=str(error), geracao=estado["geracao"] + 1)
        else:
            estado.update(
                lista=None,
                dados=conferido,
                sucesso="Técnico atualizado e conferido.",
                geracao=estado["geracao"] + 1,
            )
        st.rerun()

    if st.button("Cancelar edição de técnico"):
        estado.update(dados=None, sucesso=None, aviso=None, geracao=estado["geracao"] + 1)
        st.rerun()

    exclusao_ui.render(estado, "dados", identificador, "técnico",
        lambda identifier: api.excluir_tecnico(base, token, identifier),
        lambda identifier: api.consultar_tecnico(base, token, identifier, confirmar_ausencia=True),
        api.TecnicoNaoEncontrado, api.TecnicoError, lambda error: _erro_exclusao(error, estado))
