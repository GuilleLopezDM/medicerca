import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bd = SQLAlchemy()
gestor_login = LoginManager()


def crear_app(config=None):
    load_dotenv()
    app = Flask(__name__)

    # Config por defecto + .env
    app.config.update({
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret-key"),
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///medicerca.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "UPLOAD_FOLDER": os.path.join("app", "static", "uploads"),
        "MAX_CONTENT_LENGTH": 4 * 1024 * 1024,  # 4 MB
    })

    # Overrides (tests, staging, etc.)
    if config:
        app.config.update(config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    bd.init_app(app)
    gestor_login.init_app(app)
    gestor_login.login_view = "autenticacion.iniciar_sesion"

    from app.models.models import Usuario

    @gestor_login.user_loader
    def cargar_usuario(usuario_id):
        return bd.session.get(Usuario, int(usuario_id))

    with app.app_context():
        from app.models.models import Usuario, Medico, Resena
        bd.create_all()

    from app.rutas.autenticacion import bp_autenticacion
    app.register_blueprint(bp_autenticacion)

    from app.rutas.principal import bp_principal
    app.register_blueprint(bp_principal)

    from app.rutas.medicos import bp_medicos
    app.register_blueprint(bp_medicos)

    from app.rutas.mapa import bp_mapa
    app.register_blueprint(bp_mapa, url_prefix="/mapa")

    from app.rutas.resenas import bp_resenas
    app.register_blueprint(bp_resenas, url_prefix="/resenas")

    from app.rutas.admin import bp_admin
    app.register_blueprint(bp_admin)

    return app