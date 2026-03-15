from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

bd = SQLAlchemy()
gestor_login = LoginManager()
migrar = Migrate()


def crear_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("CLAVE_SECRETA", "clave-dev-cambiar")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("BASE_DE_DATOS", "sqlite:///medicerca.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    bd.init_app(app)
    gestor_login.init_app(app)
    migrar.init_app(app, bd)

    gestor_login.login_view = "autenticacion.iniciar_sesion"
    gestor_login.login_message = "Iniciá sesión para continuar."
    gestor_login.login_message_category = "info"

    # --- REGISTRAR BLUEPRINTS ---
    # TODO: Matheus — from app.rutas.autenticacion import bp_autenticacion
    #                  app.register_blueprint(bp_autenticacion, url_prefix="/auth")

    # TODO: Mathi   — from app.rutas.medicos import bp_medicos
    #                  app.register_blueprint(bp_medicos, url_prefix="/medicos")
    #                  from app.rutas.resenas import bp_resenas
    #                  app.register_blueprint(bp_resenas, url_prefix="/resenas")

    # TODO: Arturo  — from app.rutas.principal import bp_principal
    #                  app.register_blueprint(bp_principal)
    #                  from app.rutas.mapa import bp_mapa
    #                  app.register_blueprint(bp_mapa, url_prefix="/mapa")

    with app.app_context():
        bd.create_all()

    return app
