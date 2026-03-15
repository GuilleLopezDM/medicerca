from flask import Blueprint, render_template
from app.models import Medico

bp_principal = Blueprint("principal", __name__)


# TODO (Arturo) — FEATURE 1: Homepage
# GET /
# - Consultar total de médicos: Medico.query.count()
# - Consultar los 6 más recientes: order_by(Medico.creado_en.desc()).limit(6).all()
# - Template: "inicio/inicio.html"
# - Pasar: total_medicos, medicos_recientes


# TODO (Arturo) — FEATURE 2: Panel del usuario
# GET /panel
# - No requiere login (el template usa current_user directamente)
# - Template: "panel/panel.html"
