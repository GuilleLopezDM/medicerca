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
# Tu código acá
