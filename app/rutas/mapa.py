# ============================================================
#  ARTURO + DIEGO — app/rutas/mapa.py
#  Tu tarea: rutas del mapa de médicos con Leaflet.js
# ============================================================

from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import bd
from app.models.models import Medico

bp_mapa = Blueprint("mapa", __name__)


# --- FEATURE 1: PÁGINA DEL MAPA ---
@bp_mapa.route("/")
def mapa_medicos():
    return render_template("mapa/mapa.html")


# --- FEATURE 2: API DE MÉDICOS PARA EL MAPA ---
@bp_mapa.route("/medicos.json")
def medicos_json():
    medicos = Medico.query.filter(Medico.latitud.isnot(None)).all()

    resultado = []
    for medico in medicos:
        resultado.append({
            "id":                    medico.id,
            "nombre":                medico.usuario.nombre,
            "especialidad":          medico.especialidad,
            "hospital":              medico.hospital,
            "ciudad":                medico.ciudad,
            "calificacion_promedio": medico.calificacion_promedio,
            "total_resenas":         medico.total_resenas,
            "verificado":            medico.verificado,
            "latitud":               medico.latitud,
            "longitud":              medico.longitud,
            "direccion_consultorio": medico.direccion_consultorio,
            "url_perfil":            f"/medicos/{medico.id}"
        })

    return jsonify(resultado)


# --- FEATURE 3: GUARDAR UBICACIÓN DEL MÉDICO ---
@bp_mapa.route("/seleccionar/<int:medico_id>")
@login_required
def seleccionar_ubicacion(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    return render_template("mapa/seleccionar_ubicacion.html", medico=medico)


@bp_mapa.route("/guardar-ubicacion", methods=["POST"])
@login_required
def guardar_ubicacion():
    medico = Medico.query.filter_by(usuario_id=current_user.id).first_or_404()

    medico.latitud               = request.form.get("latitud", type=float)
    medico.longitud              = request.form.get("longitud", type=float)
    medico.direccion_consultorio = request.form.get("direccion_consultorio", "")

    bd.session.commit()

    flash("Ubicación guardada correctamente.", "success")
    return redirect(url_for("medicos.detalle_medico", medico_id=medico.id))