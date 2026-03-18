# ============================================================
#  MATHI — app/rutas/resenas.py
#  Tu tarea: sistema de rating y reseñas de médicos
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import bd
from app.models import Resena, Medico  # Descomentar cuando Hugo termine
from sqlalchemy import func  # se  agrego func para pensar en el promedio

bp_resenas = Blueprint("resenas", __name__, url_prefix='/resenas')


# --- HELPER: recalcular_calificacion (Lógica central) ---
def recalcular_calificacion(medico_id):
    """Calcula el promedio y total de reseñas y actualiza al médico."""
    medico = bd.session.get(Medico, medico_id)
    if not medico:
        return

    # Obtenemos todas las reseñas de este médico
    resenas = Resena.query.filter_by(medico_id=medico_id).all()

    total = len(resenas)
    if total > 0:
        promedio = sum(r.puntuacion for r in resenas) / total
    else:
        promedio = 0

    # Actualizamos los campos en el objeto Medico
    medico.total_resenas = total
    medico.calificacion_promedio = round(promedio, 1)
    bd.session.commit()


# --- FEATURE 1: AGREGAR RESEÑA ---
@bp_resenas.route("/agregar/<int:medico_id>", methods=["POST"])
@login_required
def agregar_resena(medico_id):
    # 1. Verificar si el usuario ya reseñó a este médico
    existente = Resena.query.filter_by(usuario_id=current_user.id, medico_id=medico_id).first()

    if existente:
        flash("Ya has dejado una reseña para este médico. Puedes editarla si lo deseas.", "warning")
        return redirect(url_for('medicos.detalle', medico_id=medico_id))

    # 2. Evitar que el médico se reseñe a sí mismo
    medico = Medico.query.get_or_404(medico_id)
    if medico.usuario_id == current_user.id:
        flash("No puedes calificar tu propio perfil profesional.", "danger")
        return redirect(url_for('medicos.detalle', medico_id=medico_id))

    # 3. Crear la reseña
    nueva_resena = Resena(
        usuario_id=current_user.id,
        medico_id=medico_id,
        puntuacion=request.form.get('puntuacion', type=int),
        comentario=request.form.get('comentario')
    )

    bd.session.add(nueva_resena)
    bd.session.commit()

    # 4. Actualizar estadísticas del médico
    recalcular_calificacion(medico_id)

    flash("¡Reseña publicada con éxito!", "success")
    return redirect(url_for('medicos.detalle', medico_id=medico_id))


# --- FEATURE 2: EDITAR RESEÑA PROPIA ---
@bp_resenas.route("/editar/<int:resena_id>", methods=["GET", "POST"])
@login_required
def editar_resena(resena_id):
    resena = Resena.query.get_or_404(resena_id)

    # Solo el autor puede editar
    if resena.usuario_id != current_user.id:
        flash("No tienes permiso para editar esta reseña.", "danger")
        return redirect(url_for('medicos.detalle', medico_id=resena.medico_id))

    if request.method == "POST":
        resena.puntuacion = request.form.get('puntuacion', type=int)
        resena.comentario = request.form.get('comentario')

        bd.session.commit()
        recalcular_calificacion(resena.medico_id)

        flash("Reseña actualizada.", "success")
        return redirect(url_for('medicos.detalle', medico_id=resena.medico_id))

    return render_template("resenas/editar.html", resena=resena)


# --- FEATURE 3: ELIMINAR RESEÑA PROPIA ---
@bp_resenas.route("/eliminar/<int:resena_id>", methods=["POST"])
@login_required
def eliminar_resena(resena_id):
    resena = Resena.query.get_or_404(resena_id)
    medico_id = resena.medico_id

    # Solo el autor o un admin puede eliminar
    if resena.usuario_id == current_user.id or current_user.rol == 'admin':
        bd.session.delete(resena)
        bd.session.commit()

        # Recalcular después de borrar
        recalcular_calificacion(medico_id)
        flash("Reseña eliminada correctamente.", "info")
    else:
        flash("No tienes permisos para realizar esta acción.", "danger")

    return redirect(url_for('medicos.detalle', medico_id=medico_id))
