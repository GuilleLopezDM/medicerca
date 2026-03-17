from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import bd
from app.models.models import Medico

bp_mapa = Blueprint("mapa", __name__)


@bp_mapa.route("/")
def mapa_medicos():
    return render_template("mapa/mapa.html")


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


@bp_mapa.route("/seleccionar/<int:medico_id>")
@login_required
def seleccionar_ubicacion(medico_id):
    medico = bd.session.get(Medico, medico_id)
    if not medico:
        abort(404)
    return render_template("mapa/seleccionar_ubicacion.html", medico=medico)


@bp_mapa.route("/guardar-ubicacion", methods=["POST"])
@login_required
def guardar_ubicacion():
    medico = Medico.query.filter_by(usuario_id=current_user.id).first()
    if not medico:
        abort(404)

    medico.latitud               = request.form.get("latitud", type=float)
    medico.longitud              = request.form.get("longitud", type=float)
    medico.direccion_consultorio = request.form.get("direccion_consultorio", "")

    bd.session.commit()

    flash("Ubicación guardada correctamente.", "success")
    return redirect(url_for("medicos.detalle", medico_id=medico.id))
