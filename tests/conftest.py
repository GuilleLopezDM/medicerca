import pytest

from app import crear_app, bd


@pytest.fixture()
def app():
    app = crear_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "clave-test-segura",
        "EMAIL_ENABLED": False,
    })
    with app.app_context():
        bd.create_all()
        yield app
        bd.session.remove()
        bd.drop_all()


@pytest.fixture()
def cliente(app):
    return app.test_client()
