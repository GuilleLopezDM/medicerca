# ============================================================
#  ARTURO + DIEGO — app/rutas/mapa.py
#  Tu tarea: rutas del mapa de médicos con Leaflet.js
# ============================================================

from flask import Blueprint, render_template, jsonify
# from app.models import Medico  # Descomentar cuando Hugo termine

bp_mapa = Blueprint("mapa", __name__)


# --- FEATURE 1: PÁGINA DEL MAPA ---
# GET /mapa/ → página con el mapa de Leaflet.js
# Muestra todos los médicos con latitud y longitud cargados
# Al hacer click en un marcador → muestra preview del médico
# @bp_mapa.route("/")
# def mapa_medicos():
#     pass  # TODO


# --- FEATURE 2: API DE MÉDICOS PARA EL MAPA ---
# GET /mapa/medicos.json → retorna JSON con todos los médicos que tienen coordenadas
# Este endpoint lo consume Leaflet.js desde el frontend (JavaScript)
# Formato de respuesta:
# [
#   {
#     "id": 1,
#     "nombre": "Dr. Juan Pérez",
#     "especialidad": "Cardiología",
#     "hospital": "Hospital Central",
#     "ciudad": "Asunción",
#     "calificacion_promedio": 4.5,
#     "total_resenas": 12,
#     "verificado": true,
#     "latitud": -25.2867,
#     "longitud": -57.6470,
#     "direccion_consultorio": "Av. España 123, Asunción",
#     "url_perfil": "/medicos/1"
#   },
#   ...
# ]
# @bp_mapa.route("/medicos.json")
# def medicos_json():
#     pass  # TODO


# --- FEATURE 3: GUARDAR UBICACIÓN DEL MÉDICO ---
# POST /mapa/guardar-ubicacion → el médico selecciona su ubicación en el mapa
# Recibe: latitud, longitud, direccion_consultorio
# Solo accesible para el médico dueño del perfil o admin
# @bp_mapa.route("/guardar-ubicacion", methods=["POST"])
# @login_required
# def guardar_ubicacion():
#     pass  # TODO
