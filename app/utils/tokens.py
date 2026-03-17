"""
app/utils/tokens.py
====================
Tokens firmados con itsdangerous (ya incluido en Flask).
No necesitás guardar nada extra en la base de datos.
"""

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app

_SALT_VERIFICACION = "verificar-email-medicerca-2025"
_SALT_RESET        = "reset-password-medicerca-2025"
_TTL               = 3600   # 1 hora en segundos


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


# ── Verificación de email ──────────────────────
def generar_token_verificacion(correo: str) -> str:
    return _serializer().dumps(correo, salt=_SALT_VERIFICACION)


def verificar_token_verificacion(token: str) -> tuple[str | None, str | None]:
    """
    Returns:
        (correo, None)        → válido
        (None, "expirado")    → venció
        (None, "invalido")    → manipulado / malformado
    """
    try:
        correo = _serializer().loads(token, salt=_SALT_VERIFICACION, max_age=_TTL)
        return correo, None
    except SignatureExpired:
        return None, "expirado"
    except BadSignature:
        return None, "invalido"


# ── Recuperación de contraseña ─────────────────
def generar_token_reset(correo: str) -> str:
    return _serializer().dumps(correo, salt=_SALT_RESET)


def verificar_token_reset(token: str) -> tuple[str | None, str | None]:
    """
    Returns:
        (correo, None)        → válido
        (None, "expirado")    → venció
        (None, "invalido")    → manipulado / malformado
    """
    try:
        correo = _serializer().loads(token, salt=_SALT_RESET, max_age=_TTL)
        return correo, None
    except SignatureExpired:
        return None, "expirado"
    except BadSignature:
        return None, "invalido"
