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
#  Modelo Medico (tabla: medicos)
# ============================================================
class Medico(bd.Model):
    __tablename__ = "medicos"

    id                     = bd.Column(bd.Integer, primary_key=True)
    usuario_id             = bd.Column(bd.Integer, bd.ForeignKey("usuarios.id"), nullable=False)
    especialidad           = bd.Column(bd.String(100), nullable=False)
    numero_matricula       = bd.Column(bd.String(50), unique=True, nullable=False)
    hospital               = bd.Column(bd.String(150), nullable=True)
    ciudad                 = bd.Column(bd.String(100), nullable=True)
    telefono               = bd.Column(bd.String(30), nullable=True)
    biografia              = bd.Column(bd.Text, nullable=True)
    universidad_graduacion = bd.Column(bd.String(200), nullable=True)
    foto                   = bd.Column(bd.String(200), default='medico_default.png')
    anios_experiencia      = bd.Column(bd.Integer, default=0)
    calificacion_promedio  = bd.Column(bd.Float, default=0.0)
    total_resenas          = bd.Column(bd.Integer, default=0)
    verificado             = bd.Column(bd.Boolean, default=False)
    creado_en              = bd.Column(bd.DateTime, default=datetime.utcnow)

    # Ubicación
    latitud                = bd.Column(bd.Float, nullable=True)
    longitud               = bd.Column(bd.Float, nullable=True)
    direccion_consultorio  = bd.Column(bd.String(255), nullable=True)

    # Relaciones
    resenas                = bd.relationship("Resena", backref="medico", lazy=True)

    def __repr__(self):
        return f"<Medico {self.especialidad} — matrícula {self.numero_matricula}>"
# ============================================================
#  Modelo Resena (tabla: resenas)
# ============================================================
class Resena(bd.Model):
    __tablename__ = "resenas"

    id         = bd.Column(bd.Integer, primary_key=True)
    medico_id  = bd.Column(bd.Integer, bd.ForeignKey("medicos.id"), nullable=False)
    usuario_id = bd.Column(bd.Integer, bd.ForeignKey("usuarios.id"), nullable=False)
    puntuacion = bd.Column(bd.Integer, nullable=False)  # 1–5
    comentario = bd.Column(bd.Text, nullable=True)
    creado_en  = bd.Column(bd.DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('medico_id', 'usuario_id', name='uq_resena_usuario_medico'),
    )

    def __repr__(self):
        return f"<Resena puntuacion={self.puntuacion} medico_id={self.medico_id}>"