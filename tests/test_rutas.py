import pytest
from app import crear_app, bd
from app.models import Usuario, Medico, Resena

@pytest.fixture()
def app():
    app = crear_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "clave-test-segura",
    })
    with app.app_context():
        bd.create_all()
        yield app
        bd.session.remove()
        bd.drop_all()

@pytest.fixture()
def cliente(app):
    return app.test_client()

def registrar_usuario_de_prueba(cliente, correo="test@mail.com", password="test1234"):
    return cliente.post("/auth/registro", data={
        "nombre": "Usuario Test",
        "correo": correo,
        "contrasena": password,
        "rol": "paciente",
    }, follow_redirects=False)

def test_inicio_retorna_200(cliente):
    assert cliente.get("/").status_code == 200

def test_pagina_login_retorna_200(cliente):
    assert cliente.get("/auth/iniciar-sesion").status_code == 200

def test_pagina_registro_retorna_200(cliente):
    assert cliente.get("/auth/registro").status_code == 200

def test_lista_medicos_retorna_200(cliente):
    assert cliente.get("/medicos/").status_code == 200

def test_registrar_usuario_post_redirige(cliente):
    resp = registrar_usuario_de_prueba(cliente)
    assert resp.status_code in (301, 302, 303, 307, 308)

def test_login_usuario_post_retorna_200(cliente):
    registrar_usuario_de_prueba(cliente, correo="login@mail.com")
    resp = cliente.post("/auth/iniciar-sesion", data={
        "correo": "login@mail.com",
        "contrasena": "test1234",
    }, follow_redirects=True)
    assert resp.status_code == 200

def test_medico_no_existe_retorna_404(cliente):
    assert cliente.get("/medicos/9999").status_code == 404
