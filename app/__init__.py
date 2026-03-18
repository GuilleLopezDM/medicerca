import os
from dotenv import load_dotenv

# 🔥 Cargar variables de entorno ANTES de importar config
load_dotenv()

from flask import Flask
from app.config import Config
from app.extensions import bd, gestor_login


def crear_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config:
        app.config.update(config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    bd.init_app(app)
    gestor_login.init_app(app)
    gestor_login.login_view = "autenticacion.iniciar_sesion"

    from app.models import Usuario

    @gestor_login.user_loader
    def cargar_usuario(usuario_id):
        return bd.session.get(Usuario, int(usuario_id))

    with app.app_context():
        bd.create_all()

    from app.rutas import registrar_blueprints
    registrar_blueprints(app)

    return app


__all__ = ["crear_app", "bd", "gestor_login"]