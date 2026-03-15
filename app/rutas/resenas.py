# ============================================================
#  MATHI — app/rutas/resenas.py
#  Tu tarea: sistema de rating y reseñas de médicos
# ============================================================

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import bd
# from app.models import Resena, Medico  # Descomentar cuando Hugo termine

bp_resenas = Blueprint("resenas", __name__)


# --- FEATURE 1: AGREGAR RESEÑA ---
# POST /resenas/agregar/<medico_id>
# Solo usuarios autenticados pueden reseñar
# Un usuario solo puede dejar UNA reseña por médico
# Campos del form: puntuacion (1-5), comentario (opcional)
# Después de guardar: recalcular calificacion_promedio y total_resenas en Medico
# Redirigir al detalle del médico
# @bp_resenas.route("/agregar/<int:medico_id>", methods=["POST"])
# @login_required
# def agregar_resena(medico_id):
#     pass  # TODO


# --- FEATURE 2: EDITAR RESEÑA PROPIA ---
# GET  /resenas/editar/<resena_id> → formulario con datos actuales
# POST /resenas/editar/<resena_id> → guardar cambios
# Solo el autor puede editar
# Recalcular calificacion_promedio del médico al guardar
# @bp_resenas.route("/editar/<int:resena_id>", methods=["GET", "POST"])
# @login_required
# def editar_resena(resena_id):
#     pass  # TODO


# --- FEATURE 3: ELIMINAR RESEÑA PROPIA ---
# POST /resenas/eliminar/<resena_id>
# Solo el autor o admin puede eliminar
# Recalcular calificacion_promedio y total_resenas del médico
# @bp_resenas.route("/eliminar/<int:resena_id>", methods=["POST"])
# @login_required
# def eliminar_resena(resena_id):
#     pass  # TODO


# --- HELPER: recalcular_calificacion ---
# Función auxiliar — NO es una ruta
# Recalcula calificacion_promedio y total_resenas de un médico
# Llamar después de agregar, editar o eliminar una reseña
# def recalcular_calificacion(medico_id):
#     pass  # TODO
