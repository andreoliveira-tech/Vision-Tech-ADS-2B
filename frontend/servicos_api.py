"""CRUD de Serviços: token obrigatório, uma tentativa e contratos estritos."""
import math
import requests

CAMPOS = ("descricao", "valor", "id_os")
AUSENTE = "Servico nao encontrado."


class ServicoError(Exception):
    def __init__(self, message, *, incerto=False):
        super().__init__(message)
        self.incerto = incerto


class SessaoNecessaria(ServicoError):
    pass


class AcessoNegado(ServicoError):
    pass


class ServicoNaoEncontrado(ServicoError):
    pass


def identificador(value):
    if type(value) is not int or value <= 0:
        raise ServicoError("Informe um identificador inteiro positivo.")
    return value


def dados(value):
    if not isinstance(value, dict) or set(value) != set(CAMPOS):
        raise ServicoError("Informe descrição, valor e ID da OS.")
    if not isinstance(value["descricao"], str):
        raise ServicoError("Informe descrição como texto.")
    price = value["valor"]
    try:
        finite = type(price) in (int, float) and math.isfinite(price)
    except OverflowError:
        finite = False
    if not finite:
        raise ServicoError("Informe valor numérico finito.")
    identificador(value["id_os"])
    return {k: value[k] for k in CAMPOS}


def _servico(value, expected=None):
    if not isinstance(value, dict) or set(value) != {"id_servico", *CAMPOS}:
        raise ValueError
    try:
        identifier = identificador(value["id_servico"])
        result = dados({k: value[k] for k in CAMPOS})
    except ServicoError:
        raise ValueError from None
    if expected is not None and identifier != expected:
        raise ValueError
    return {"id_servico": identifier, **result}


def _request(base, token, method, identifier=None, payload=None):
    if not isinstance(token, str) or not token.strip():
        raise SessaoNecessaria("Entre para acessar Serviços.")
    url = base.rstrip("/") + "/servicos"
    if identifier is not None:
        url += "/" + str(identificador(identifier))
    options = {"headers": {"Authorization": "Bearer " + token.strip()},
               "timeout": (5, 20), "allow_redirects": False}
    if payload is not None:
        options["json"] = dados(payload)
    write = method != "GET"
    try:
        response = requests.request(method, url, **options)
    except requests.RequestException:
        raise ServicoError("Falha de comunicação. Confira o estado antes de tentar novamente.", incerto=write) from None
    if response.status_code == 401:
        raise SessaoNecessaria("Sessão expirada ou inválida.")
    if response.status_code == 403:
        raise AcessoNegado("Seu perfil não pode administrar Serviços.")
    try:
        body = response.json()
    except ValueError:
        body = None
    if response.status_code == 404 and isinstance(body, dict) and (
        body.get("code") == "ERROR_CODE_NOT_FOUND" and body.get("message") == AUSENTE
        and set(body) <= {"code", "message", "payload"} and body.get("payload") in (None, {}, "")
    ):
        raise ServicoNaoEncontrado("Serviço não encontrado.")
    if response.status_code != 200:
        uncertain = write and (response.status_code < 400 or response.status_code in (404, 408) or response.status_code >= 500)
        raise ServicoError("Operação sem confirmação. Confira o estado atual." if uncertain else "Operação rejeitada pelo serviço.", incerto=uncertain)
    try:
        if method == "DELETE":
            if body != {"id_servico": identifier, "excluido": True} or type(body["id_servico"]) is not int or body["excluido"] is not True:
                raise ValueError
            return body
        if method == "GET" and identifier is None:
            if not isinstance(body, list):
                raise ValueError
            rows = [_servico(item) for item in body]
            if len({r["id_servico"] for r in rows}) != len(rows):
                raise ValueError
            return rows
        result = _servico(body, identifier)
        if payload is not None and {k: result[k] for k in CAMPOS} != payload:
            raise ValueError
        return result
    except (ValueError, TypeError, KeyError):
        raise ServicoError("Resposta fora do contrato. Confira o estado atual.", incerto=write) from None


def cadastrar_servico(base, token, payload):
    return _request(base, token, "POST", payload=dados(payload))


def listar_servicos(base, token):
    return _request(base, token, "GET")


def consultar_servico(base, token, identifier):
    return _request(base, token, "GET", identificador(identifier))


def atualizar_servico(base, token, identifier, payload):
    return _request(base, token, "PUT", identificador(identifier), dados(payload))


def excluir_servico(base, token, identifier):
    return _request(base, token, "DELETE", identificador(identifier))
