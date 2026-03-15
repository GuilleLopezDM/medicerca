from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import bd
from app.models import Medico, Usuario

bp_medicos = Blueprint("medicos", __name__)


# TODO (Mathi) — FEATURE 1: Listar médicos
# GET /medicos/
# - Query base: Medico.query.join(Usuario)
# - Filtros opcionales por query params:
#     ?busqueda=  → Usuario.nombre, Medico.especialidad, Medico.hospital (ilike, OR)
#     ?especialidad= → Medico.especialidad (ilike)
#     ?ciudad= → Medico.ciudad (ilike)
#     ?universidad= → Medico.universidad_graduacion (ilike)
#     ?verificados=1 → solo Medico.verificado == True
# - Pasar al template: medicos, especialidades, ciudades, universidades, total, filtros_actuales
# - Template: "medicos/lista.html"


# TODO (Mathi) — FEATURE 2: Detalle de un médico
# GET /medicos/<int:medico_id>
# - Medico.query.get_or_404(medico_id)
# - Template: "medicos/detalle.html"


# TODO (Mathi) — FEATURE 3: Formulario de registro médico
# GET /medicos/registrar → requiere @login_required
# - Si current_user.rol != 'medico' → flash warning, redirigir a principal.inicio
# - Si ya tiene perfil_medico → redirigir al detalle
# - Template: "medicos/registrar.html"


# TODO (Mathi) — FEATURE 4: Guardar perfil médico
# POST /medicos/registrar → requiere @login_required
# - Leer campos: especialidad, numero_matricula, hospital, ciudad, telefono,
#                biografia, universidad_graduacion, anios_experiencia
# - Crear Medico con usuario_id=current_user.id
# - bd.session.add(), bd.session.commit()
# - flash("Perfil médico creado.", "success") → redirigir a detalle


# TODO (Mathi) — FEATURE 5: Formulario de edición
# GET /medicos/editar/<int:medico_id> → requiere @login_required
# - Solo el dueño (medico.usuario_id == current_user.id) o rol admin puede editar
# - Si no tiene permiso → flash danger, redirigir al detalle
# - Template: "medicos/editar.html"


# TODO (Mathi) — FEATURE 6: Guardar edición
# POST /medicos/editar/<int:medico_id> → requiere @login_required
# - Campos editables: especialidad, hospital, ciudad, telefono, biografia,
#                     universidad_graduacion, anios_experiencia
# - numero_matricula NO se edita
# - bd.session.commit()
# - flash("Perfil actualizado.", "success") → redirigir al detalle


# --- FEATURE 5: MAPA DE MÉDICOS ---
# GET /medicos/mapa → mapa interactivo con todos los médicos geolocalizados
# Solo muestra médicos que tengan latitud y longitud cargados
# @bp_medicos.route("/mapa")
# def mapa_medicos():
#     # medicos_geolocalizados = Medico.query.filter(
#     #     Medico.latitud != None,
#     #     Medico.longitud != None
#     # ).join(Usuario).all()
#     # return render_template("medicos/mapa.html", medicos=medicos_geolocalizados)
#     pass  # TODO
