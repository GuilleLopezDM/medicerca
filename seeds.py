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
    pass  # Tu código acá
