"""Cliente HTTP para o contrato local proposto de Técnicos; sem login embutido."""

import requests


CAMPOS = ("nome", "especialidade", "telefone", "email")
CAMPOS_RESPOSTA = ("id_tecnico", *CAMPOS)
AUSENTE = "Tecnico nao encontrado."


class TecnicoError(Exception):
    def __init__(self, message, *, incerto=False):
        super().__init__(message)
        self.incerto = incerto


class TecnicoNaoEncontrado(TecnicoError):
    pass


class SessaoNecessaria(TecnicoError):
    pass


class AcessoNegado(TecnicoError):
    pass


def _id(value):
    if type(value) is not int or value <= 0:
        raise TecnicoError("Informe um identificador inteiro positivo.")
    return value


def _dados(value):
    if not isinstance(value, dict):
        raise TecnicoError("Informe os quatro campos obrigatórios do técnico.")
    if any(not isinstance(value.get(field), str) or not value[field].strip() for field in CAMPOS):
        raise TecnicoError("Nome, especialidade, telefone e email são obrigatórios.")
    return {field: value[field] for field in CAMPOS}


def _tecnico(value, expected=None):
    if not isinstance(value, dict) or set(value) != set(CAMPOS_RESPOSTA):
        raise ValueError
    identifier = _id(value.get("id_tecnico"))
    dados = _dados(value)
    if expected is not None and identifier != expected:
        raise ValueError
    return {"id_tecnico": identifier, **dados}


def _request(base, token, method, identifier=None, dados=None, ausencia_estrita=False):
    if not isinstance(token, str) or not token.strip():
        raise SessaoNecessaria("Faça login para acessar a gestão de técnicos.")
    url = f"{base.rstrip('/')}/tecnicos"
    if identifier is not None:
        url += f"/{_id(identifier)}"
    options = {
        "headers": {"Authorization": f"Bearer {token.strip()}"},
        "timeout": (5, 20),
        "allow_redirects": False,
    }
    escrita = method in ("POST", "PUT", "DELETE")
    if method in ("POST", "PUT"):
        options["json"] = _dados(dados)
    try:
        response = requests.request(method, url, **options)
    except requests.RequestException:
        raise TecnicoError(
            "Falha de comunicação. Confira o estado atual antes de tentar novamente.",
            incerto=escrita,
        ) from None
    try:
        body = response.json()
    except ValueError:
        body = None
    status = response.status_code
    if status == 401:
        raise SessaoNecessaria("Sessão expirada ou inválida. Entre novamente.")
    if status == 403:
        raise AcessoNegado("Seu perfil não tem permissão para gerenciar técnicos.")
    if status == 404 and isinstance(body, dict) and (
        body.get("code") == "ERROR_CODE_NOT_FOUND" and body.get("message") == AUSENTE
        and (not ausencia_estrita or (set(body) <= {"code", "message", "payload"}
                                     and body.get("payload") in (None, {}, "")))
    ):
        raise TecnicoNaoEncontrado("Técnico não encontrado.")
    if status != 200:
        incerto = escrita and (status == 408 or status >= 500 or status < 400)
        raise TecnicoError(
            "Não foi possível confirmar a operação. Confira o estado atual."
            if incerto else "O serviço rejeitou a operação ou não retornou o resultado esperado.",
            incerto=incerto,
        )
    try:
        if method == "DELETE":
            if (not isinstance(body, dict) or set(body) != {"id_tecnico", "excluido"}
                    or type(body.get("id_tecnico")) is not int or body["id_tecnico"] != identifier
                    or body.get("excluido") is not True):
                raise ValueError
            return body
        if method == "GET" and identifier is None:
            if not isinstance(body, list):
                raise ValueError
            return [_tecnico(item) for item in body]
        return _tecnico(body, identifier)
    except (ValueError, TecnicoError):
        raise TecnicoError(
            "Resposta fora do contrato esperado. Confira o estado atual.", incerto=escrita
        ) from None


def cadastrar_tecnico(base, token, dados):
    return _request(base, token, "POST", dados=dados)


def listar_tecnicos(base, token):
    return _request(base, token, "GET")


def consultar_tecnico(base, token, identificador, *, confirmar_ausencia=False):
    return _request(base, token, "GET", _id(identificador), ausencia_estrita=confirmar_ausencia)


def atualizar_tecnico(base, token, identificador, dados):
    return _request(base, token, "PUT", _id(identificador), dados)


def excluir_tecnico(base, token, identificador):
    return _request(base, token, "DELETE", _id(identificador))
