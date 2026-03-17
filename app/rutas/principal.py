from flask import Blueprint, render_template
from app.models import Medico

bp_principal = Blueprint("principal", __name__)


# FEATURE 1: Homepage
@bp_principal.route("/")
def inicio():
    total_medicos = Medico.query.count()
    medicos_recientes = Medico.query.order_by(Medico.creado_en.desc()).limit(6).all()
    return render_template("inicio/inicio.html",total_medicos=total_medicos,medicos_recientes=medicos_recientes)

# FEATURE 2: Panel del usuario
@bp_principal.route("/panel")
def panel():
    return render_template("panel/panel.html")
