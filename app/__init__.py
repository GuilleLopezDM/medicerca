from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bd = SQLAlchemy()
gestor_login = LoginManager()


def crear_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medicerca.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    # TODO: Arturo — from app.rutas.principal import bp_principal
    #                 app.register_blueprint(bp_principal)
    # TODO: Hugo — from app.rutas.busqueda import bp_busqueda
    #               app.register_blueprint(bp_busqueda)
    # TODO: Diego — from app.rutas.perfil import bp_perfil
    #                app.register_blueprint(bp_perfil)

    return app