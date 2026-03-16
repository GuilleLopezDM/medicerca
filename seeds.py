# TODO (Johan) — FEATURE 1: Script de datos de prueba
# Correr con: python seeds.py (desde la carpeta medicerca con el venv activo)
#
# Debe crear:
#   - 2 usuarios con rol='paciente'
#   - 5 usuarios con rol='medico', cada uno con su perfil Medico completo
#
# Especialidades: Cardiología, Pediatría, Dermatología, Neurología, Traumatología
# Ciudades: Asunción, Encarnación, Ciudad del Este, San Lorenzo, Luque
# Universidades:
#   'Universidad Nacional de Asunción (UNA)'
#   'Universidad Católica (UCA)'
#   'Universidad del Norte (UNINORTE)'
#   'Universidad Americana (UA)'
#   'Universidad Autónoma de Asunción (UAA)'
# Algunos verificado=True, otros False
# Password de todos: 'test1234'
# Idempotente: verificar si ya existen antes de insertar

from app import crear_app, bd
from app.models import Usuario, Medico

app = crear_app()

with app.app_context():
    def crear_usuario_si_no_existe(nombre, correo, rol):
    usuario = Usuario.query.filter_by(correo=correo).first()

    if usuario:
        return usuario

    usuario = Usuario(
        nombre=nombre,
        correo=correo,
        rol=rol
    )

    usuario.establecer_contrasena("test1234")

    bd.session.add(usuario)
    bd.session.commit()

    return usuario


def crear_medico_si_no_existe(usuario, especialidad, matricula, hospital,
                              ciudad, telefono, biografia, universidad,
                              experiencia, verificado):

    medico = Medico.query.filter_by(usuario_id=usuario.id).first()

    if medico:
        return medico

    medico = Medico(
        usuario_id=usuario.id,
        especialidad=especialidad,
        numero_matricula=matricula,
        hospital=hospital,
        ciudad=ciudad,
        telefono=telefono,
        biografia=biografia,
        universidad_graduacion=universidad,
        anios_experiencia=experiencia,
        verificado=verificado
    )

    bd.session.add(medico)
    bd.session.commit()

    return medico

    pass  # Tu código acá
