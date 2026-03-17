from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bd = SQLAlchemy()
gestor_login = LoginManager()


def crear_app(config=None):
    app = Flask(__name__)

    # Config por defecto
    app.config.update({
        "SECRET_KEY": "dev-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///medicerca.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # Overrides (tests, staging, etc.)
    if config:
        app.config.update(config)

    bd.init_app(app)
    gestor_login.init_app(app)
    gestor_login.login_view = "autenticacion.iniciar_sesion"

    from app.models.models import Usuario

    @gestor_login.user_loader
    def cargar_usuario(usuario_id):
        return Usuario.query.get(int(usuario_id))

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
    # from app.rutas.resenas import bp_resenas
    # app.register_blueprint(bp_resenas, url_prefix="/resenas")

    return app
