"""Cliente HTTP local para OS. Requer token de autenticação real; sem fallback simulado."""

import requests


STATUS = ("Aguardando avaliação", "Em manutenção", "Aguardando peça", "Concluído", "Entregue")
CAMPOS = ("data_entrada", "data_saida", "problema_relatado", "status", "valor_total", "id_equipamento", "id_tecnico")
CAMPOS_RESPOSTA = ("id_os", *CAMPOS)
CAMPOS_EQUIPAMENTO = ("equipamento_tipo", "equipamento_marca", "equipamento_modelo")
AUSENTE = "Ordem de servico nao encontrada."


class OrdemError(Exception):
    def __init__(self, message, *, incerto=False):
        super().__init__(message)
        self.incerto = incerto


class SessaoNecessaria(OrdemError):
    pass


class AcessoNegado(OrdemError):
    pass


class OrdemNaoEncontrada(OrdemError):
    pass


def _id(value):
    if type(value) is not int or value <= 0:
        raise OrdemError("Informe um identificador inteiro positivo.")
    return value


def _dados(value):
    if not isinstance(value, dict) or set(value) != set(CAMPOS):
        raise OrdemError("Informe todos os campos originais da Ordem de Serviço.")
    if not isinstance(value["data_entrada"], str) or not value["data_entrada"]:
        raise OrdemError("Informe a data de entrada.")
    if value["data_saida"] is not None and not isinstance(value["data_saida"], str):
        raise OrdemError("A data de saída deve ser uma data ou ficar sem valor.")
    if not isinstance(value["problema_relatado"], str):
        raise OrdemError("Informe o problema relatado como texto.")
    if value["status"] not in STATUS:
        raise OrdemError("Selecione um dos cinco status previstos.")
    if isinstance(value["valor_total"], bool) or not isinstance(value["valor_total"], (int, float)):
        raise OrdemError("Informe o valor total como número.")
    _id(value["id_equipamento"])
    _id(value["id_tecnico"])
    return {field: value[field] for field in CAMPOS}


def _ordem(value, expected=None):
    if not isinstance(value, dict) or set(value) != set(CAMPOS_RESPOSTA):
        raise ValueError
    identifier = _id(value.get("id_os"))
    dados = _dados({field: value[field] for field in CAMPOS})
    if expected is not None and identifier != expected:
        raise ValueError
    return {"id_os": identifier, **dados}


def _ordem_tecnico(value):
    if not isinstance(value, dict) or set(value) != set(CAMPOS_RESPOSTA + CAMPOS_EQUIPAMENTO):
        raise ValueError
    order = _ordem({field: value[field] for field in CAMPOS_RESPOSTA})
    if not isinstance(value["equipamento_tipo"], str):
        raise ValueError
    for field in ("equipamento_marca", "equipamento_modelo"):
        if value[field] is not None and not isinstance(value[field], str):
            raise ValueError
    return {**order, **{field: value[field] for field in CAMPOS_EQUIPAMENTO}}


def _request(base, token, method, path="ordens-servico", identifier=None, data=None, ausencia_estrita=False):
    if not isinstance(token, str) or not token.strip():
        raise SessaoNecessaria("Entre por um mecanismo de autenticação real para continuar.")
    url = f"{base.rstrip('/')}/{path}"
    if identifier is not None:
        safe_id = _id(identifier)
        url += f"/{safe_id}"
        if method == "PATCH":
            url += "/status"
    options = {"headers": {"Authorization": f"Bearer {token.strip()}"}, "timeout": (5, 20), "allow_redirects": False}
    escrita = method in ("POST", "PUT", "PATCH", "DELETE")
    if method in ("POST", "PUT"):
        options["json"] = _dados(data)
    elif method == "PATCH":
        if not isinstance(data, dict) or set(data) != {"status"} or data["status"] not in STATUS:
            raise OrdemError("A atualização do técnico aceita somente um dos cinco status previstos.")
        options["json"] = {"status": data["status"]}
    try:
        response = requests.request(method, url, **options)
    except requests.RequestException:
        raise OrdemError("Falha de comunicação. Confira o estado atual antes de tentar novamente.", incerto=escrita) from None
    try:
        body = response.json()
    except ValueError:
        body = None
    if response.status_code == 401:
        raise SessaoNecessaria("Sessão expirada ou inválida. Entre novamente.")
    if response.status_code == 403:
        raise AcessoNegado("O perfil autenticado não pode executar esta operação.")
    if (response.status_code == 404 and isinstance(body, dict) and body.get("code") == "ERROR_CODE_NOT_FOUND"
            and body.get("message") == AUSENTE and (not ausencia_estrita or
                (set(body) <= {"code", "message", "payload"} and body.get("payload") in (None, {}, "")))):
        raise OrdemNaoEncontrada("Ordem de Serviço não encontrada.")
    if response.status_code != 200:
        incerto = escrita and (response.status_code == 408 or response.status_code >= 500 or response.status_code < 400)
        raise OrdemError("Não foi possível confirmar a operação. Confira o estado atual." if incerto else "O serviço rejeitou a operação ou não retornou o resultado esperado.", incerto=incerto)
    try:
        if method == "DELETE":
            if (not isinstance(body, dict) or set(body) != {"id_os", "excluido"}
                    or type(body.get("id_os")) is not int or body["id_os"] != identifier
                    or body.get("excluido") is not True):
                raise ValueError
            return body
        if method == "GET" and identifier is None:
            if not isinstance(body, list):
                raise ValueError
            if path == "minhas-ordens":
                return [_ordem_tecnico(item) for item in body]
            return [_ordem(item) for item in body]
        if method == "PATCH":
            if not isinstance(body, dict) or set(body) != {"id_os", "status"} or _id(body["id_os"]) != identifier or body["status"] != data["status"]:
                raise ValueError
            return {"id_os": identifier, "status": data["status"]}
        return _ordem(body, identifier)
    except (ValueError, OrdemError):
        raise OrdemError("Resposta fora do contrato esperado. Confira o estado atual.", incerto=escrita) from None


def cadastrar_ordem(base, token, data):
    return _request(base, token, "POST", data=data)


def listar_ordens(base, token):
    return _request(base, token, "GET")


def consultar_ordem(base, token, identifier, *, confirmar_ausencia=False):
    return _request(base, token, "GET", identifier=identifier, ausencia_estrita=confirmar_ausencia)


def atualizar_ordem(base, token, identifier, data):
    return _request(base, token, "PUT", identifier=identifier, data=data)


def excluir_ordem(base, token, identifier):
    return _request(base, token, "DELETE", identifier=_id(identifier))


def listar_minhas_ordens(base, token):
    return _request(base, token, "GET", path="minhas-ordens")


def consultar_minha_ordem(base, token, identifier):
    return _request(base, token, "GET", path="minhas-ordens", identifier=identifier)


def atualizar_status_minha_ordem(base, token, identifier, status):
    return _request(base, token, "PATCH", path="minhas-ordens", identifier=identifier, data={"status": status})
