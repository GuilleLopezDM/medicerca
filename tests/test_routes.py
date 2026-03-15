import pytest
from app import crear_app, bd
from app.models import Usuario


@pytest.fixture
def app():
    app = crear_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        bd.create_all()
        yield app
        bd.drop_all()


@pytest.fixture
def cliente(app):
    return app.test_client()


def test_inicio(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200


def test_pagina_login(cliente):
    respuesta = cliente.get("/auth/iniciar-sesion")
    assert respuesta.status_code == 200


def test_pagina_registro(cliente):
    respuesta = cliente.get("/auth/registro")
    assert respuesta.status_code == 200


def test_lista_medicos(cliente):
    respuesta = cliente.get("/medicos/")
    assert respuesta.status_code == 200


def test_registrar_usuario(cliente):
    respuesta = cliente.post("/auth/registro", data={
        "nombre": "Dr. Test",
        "correo": "test@medicerca.com",
        "contrasena": "test1234",
        "rol": "medico"
    }, follow_redirects=True)
    assert respuesta.status_code == 200


def test_medico_no_existe(cliente):
    respuesta = cliente.get("/medicos/9999")
    assert respuesta.status_code == 404
