# TODO (Johan) — FEATURE 2: Tests con pytest
# Correr con: pytest tests/ -v
#
# Necesitás:
#   - Fixture 'app' con bd en memoria (sqlite:///:memory:) y TESTING=True
#   - Fixture 'cliente' usando app.test_client()
#
# Tests requeridos:
#   a. test_inicio              → GET /          retorna 200
#   b. test_pagina_login        → GET /auth/iniciar-sesion  retorna 200
#   c. test_pagina_registro     → GET /auth/registro        retorna 200
#   d. test_lista_medicos       → GET /medicos/             retorna 200
#   e. test_registrar_usuario   → POST /auth/registro crea usuario y redirige
#   f. test_login_usuario       → POST /auth/iniciar-sesion con credenciales correctas
#   g. test_medico_no_existe    → GET /medicos/9999         retorna 404

import pytest
from app import crear_app, bd

@pytest.fixture()
def app():
    """App configurada con base de datos en memoria para tests."""
    app = crear_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,          # deshabilita CSRF si usas Flask-WTF
        "SECRET_KEY": "clave-test-segura",
    })

    with app.app_context():
        _bd.create_all()
        yield app
        _bd.session.remove()
        _bd.drop_all()


@pytest.fixture()
def cliente(app):
    """Cliente de pruebas HTTP."""
    return app.test_client()

def registrar_usuario_de_prueba(cliente, correo="test@mail.com", password="test1234"):
    """Registra un usuario paciente y devuelve la respuesta."""
    return cliente.post("/auth/registro", data={
        "nombre": "Usuario Test",
        "correo": correo,
        "contrasena": password,
        "rol": "paciente",
    }, follow_redirects=False)

def test_inicio_retorna_200(cliente):
    """GET / debe devolver 200."""
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200


def test_pagina_login_retorna_200(cliente):
    """GET /auth/iniciar-sesion debe devolver 200."""
    respuesta = cliente.get("/auth/iniciar-sesion")
    assert respuesta.status_code == 200


def test_pagina_registro_retorna_200(cliente):
    """GET /auth/registro debe devolver 200."""
    respuesta = cliente.get("/auth/registro")
    assert respuesta.status_code == 200


def test_lista_medicos_retorna_200(cliente):
    """GET /medicos/ debe devolver 200."""
    respuesta = cliente.get("/medicos/")
    assert respuesta.status_code == 200


def test_registrar_usuario_post_redirige(cliente):
    """POST /auth/registro con datos válidos debe redirigir (3xx)."""
    respuesta = registrar_usuario_de_prueba(cliente)
    assert respuesta.status_code in (301, 302, 303, 307, 308)


def test_login_usuario_post_retorna_200(cliente):
    """POST /auth/iniciar-sesion con credenciales válidas debe retornar 200
    (siguiendo la redirección final)."""
    # Primero registramos el usuario
    registrar_usuario_de_prueba(cliente, correo="login@mail.com")

    # Luego intentamos iniciar sesión siguiendo redirecciones
    respuesta = cliente.post("/auth/iniciar-sesion", data={
        "correo": "login@mail.com",
        "contrasena": "test1234",
    }, follow_redirects=True)

    assert respuesta.status_code == 200


def test_medico_no_existe_retorna_404(cliente):
    """GET /medicos/9999 debe devolver 404 para un médico inexistente."""
    respuesta = cliente.get("/medicos/9999")
    assert respuesta.status_code == 404
# Tu código acá
