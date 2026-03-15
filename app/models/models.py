# ============================================================
#  HUGO — app/models/models.py
#  Tu tarea: definir los modelos Usuario, Medico, Resena
# ============================================================

from app import bd, gestor_login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import UniqueConstraint


# --- HUGO: user_loader ---
@gestor_login.user_loader
def cargar_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))

# ============================================================
#  Modelo Usuario (tabla: usuarios)
# ============================================================
class Usuario(UserMixin, bd.Model):
    __tablename__ = "usuarios"

    id              = bd.Column(bd.Integer, primary_key=True)
    nombre          = bd.Column(bd.String(100), nullable=False)
    correo          = bd.Column(bd.String(120), unique=True, nullable=False)
    contrasena_hash = bd.Column(bd.String(256), nullable=False)
    rol             = bd.Column(bd.String(20), default='paciente')
    creado_en       = bd.Column(bd.DateTime, default=datetime.utcnow)

    # Relaciones
    perfil_medico   = bd.relationship("Medico", backref="usuario", uselist=False)
    resenas         = bd.relationship("Resena", backref="autor", lazy=True)

    def establecer_contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)

    def __repr__(self):
        return f"<Usuario {self.correo}>"

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
