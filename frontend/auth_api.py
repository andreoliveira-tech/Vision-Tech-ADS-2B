"""Cliente para os endpoints Xano Authentication locais; nenhum token é simulado."""

import requests


PERFIS = ("colaborador", "tecnico")


class AuthError(Exception):
    pass


class CredenciaisInvalidas(AuthError):
    pass


class SessaoExpirada(AuthError):
    pass


class PerfilSemAcesso(AuthError):
    pass


class BackendIndisponivel(AuthError):
    pass


def _http(base, method, route, *, token=None, payload=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    options = {"headers": headers, "timeout": (5, 20), "allow_redirects": False}
    if payload is not None:
        options["json"] = payload
    try:
        response = requests.request(method, f"{base.rstrip('/')}/{route}", **options)
    except requests.RequestException:
        raise BackendIndisponivel("Não foi possível conectar ao serviço de autenticação.") from None
    if response.status_code == 401 or response.status_code == 403:
        if route == "auth/login":
            raise CredenciaisInvalidas("E-mail ou senha inválidos.")
        if response.status_code == 401:
            raise SessaoExpirada("A sessão expirou. Entre novamente.")
        raise PerfilSemAcesso("A identidade autenticada não tem acesso à aplicação.")
    if response.status_code != 200:
        raise BackendIndisponivel("O serviço de autenticação está indisponível ou retornou resposta inesperada.")
    try:
        return response.json()
    except ValueError:
        raise BackendIndisponivel("O serviço de autenticação retornou uma resposta inválida.") from None


def _perfil(user, expected_id=None):
    if not isinstance(user, dict):
        raise BackendIndisponivel("O serviço de autenticação retornou uma identidade inválida.")
    identifier = user.get("id")
    role = user.get("perfil_aplicacao")
    if type(identifier) is not int or identifier <= 0 or (expected_id is not None and identifier != expected_id):
        raise BackendIndisponivel("A identidade retornada não corresponde ao login.")
    if role not in PERFIS:
        raise PerfilSemAcesso("Este perfil não está provisionado para a aplicação.")
    result = {"id": identifier, "role": role, "name": user.get("name", ""), "email": user.get("email", "")}
    if role == "tecnico":
        technician_id = user.get("id_tecnico")
        if type(technician_id) is not int or technician_id <= 0:
            raise PerfilSemAcesso("A conta técnica não tem vínculo válido com o cadastro de Técnico.")
        result["id_tecnico"] = technician_id
    return result


def consultar_usuario(base, token, *, expected_id=None):
    if not isinstance(token, str) or not token.strip():
        raise SessaoExpirada("A sessão expirou. Entre novamente.")
    body = _http(base, "GET", "auth/me", token=token.strip())
    return _perfil(body, expected_id)


def autenticar(base, email, password):
    if not isinstance(email, str) or not email.strip() or not isinstance(password, str) or not password:
        raise CredenciaisInvalidas("Informe e-mail e senha.")
    body = _http(base, "POST", "auth/login", payload={"email": email.strip(), "password": password})
    if not isinstance(body, dict):
        raise BackendIndisponivel("O serviço de autenticação retornou uma resposta inválida.")
    token, user_id = body.get("authToken"), body.get("user_id")
    if not isinstance(token, str) or not token.strip() or type(user_id) is not int or user_id <= 0:
        raise BackendIndisponivel("O serviço de autenticação retornou uma resposta inválida.")
    user = consultar_usuario(base, token.strip(), expected_id=user_id)
    return {"token": token.strip(), "user": user}
