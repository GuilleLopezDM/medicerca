# ============================================================
#  HUGO — app/models/models.py
#  Tu tarea: definir los modelos Usuario, Medico, Resena
# ============================================================

from app import bd, gestor_login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# --- HUGO: user_loader ---
# @gestor_login.user_loader
# def cargar_usuario(usuario_id):
#     pass  # TODO


# ============================================================
#  CONTRATO: Modelo Usuario (tabla: usuarios)
# ============================================================
# class Usuario(UserMixin, bd.Model):
#     __tablename__ = "usuarios"
#     id            — Integer, PK
#     nombre        — String(100), not null
#     correo        — String(120), unique, not null
#     contrasena_hash — String(256), not null
#     rol           — String(20), default='paciente'
#     creado_en     — DateTime, default=now
#
#     # Relaciones
#     perfil_medico — relationship → Medico (uselist=False)
#     resenas       — relationship → Resena (backref='autor')
#
#     def establecer_contrasena(self, contrasena): ...
#     def verificar_contrasena(self, contrasena): ...
#
# class Usuario(UserMixin, bd.Model):
#     pass  # TODO


# ============================================================
#  CONTRATO: Modelo Medico (tabla: medicos)
# ============================================================
# class Medico(bd.Model):
#     __tablename__ = "medicos"
#     id                     — Integer, PK
#     usuario_id             — Integer, FK → usuarios.id
#     especialidad           — String(100), not null
#     numero_matricula       — String(50), unique, not null
#     hospital               — String(150), nullable
#     ciudad                 — String(100), nullable
#     telefono               — String(30), nullable
#     biografia              — Text, nullable
#     universidad_graduacion — String(200), nullable
#     foto                   — String(200), default='medico_default.png'
#     anios_experiencia      — Integer, default=0
#     calificacion_promedio  — Float, default=0.0  ← se recalcula al agregar reseñas
#     total_resenas          — Integer, default=0   ← contador de reseñas
#     verificado             — Boolean, default=False
#     creado_en              — DateTime, default=now
#
#     # Ubicación para el mapa
#     latitud                — Float, nullable       ← coordenada lat del doctor
#     longitud               — Float, nullable       ← coordenada lng del doctor
#     direccion_consultorio  — String(255), nullable ← dirección legible
#
#     # Relaciones
#     resenas — relationship → Resena (backref='medico')
#
# class Medico(bd.Model):
#     pass  # TODO


# ============================================================
#  CONTRATO: Modelo Resena (tabla: resenas)
# ============================================================
# Una reseña pertenece a un Usuario (autor) y a un Medico
#
# class Resena(bd.Model):
#     __tablename__ = "resenas"
#     id          — Integer, PK
#     medico_id   — Integer, FK → medicos.id, not null
#     usuario_id  — Integer, FK → usuarios.id, not null
#     puntuacion  — Integer, not null  ← valor entre 1 y 5
#     comentario  — Text, nullable
#     creado_en   — DateTime, default=now
#
#     # Restricción: un usuario solo puede reseñar una vez al mismo médico
#     __table_args__ = (UniqueConstraint('medico_id', 'usuario_id'),)
#
# class Resena(bd.Model):
#     pass  # TODO
