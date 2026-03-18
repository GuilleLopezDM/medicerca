from .admin import bp_admin
from .autenticacion import bp_autenticacion
from .mapa import bp_mapa
from .medicos import bp_medicos
from .principal import bp_principal
from .resenas import bp_resenas


def registrar_blueprints(app):
    app.register_blueprint(bp_autenticacion)
    app.register_blueprint(bp_principal)
    app.register_blueprint(bp_medicos)
    app.register_blueprint(bp_mapa, url_prefix="/mapa")
    app.register_blueprint(bp_resenas, url_prefix="/resenas")
    app.register_blueprint(bp_admin)
