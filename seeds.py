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

with app.app_context():

    print("Creando usuarios de prueba...")

    # Pacientes
    crear_usuario_si_no_existe(
        "Ana Gómez",
        "ana@medicerca.com",
        "paciente"
    )

    crear_usuario_si_no_existe(
        "Carlos López",
        "carlos@medicerca.com",
        "paciente"
    )

    # Médicos
    medico1 = crear_usuario_si_no_existe(
        "Dr. Juan Martínez",
        "juan.martinez@medicerca.com",
        "medico"
    )

    medico2 = crear_usuario_si_no_existe(
        "Dra. María Fernández",
        "maria.fernandez@medicerca.com",
        "medico"
    )

    medico3 = crear_usuario_si_no_existe(
        "Dr. Luis Ramírez",
        "luis.ramirez@medicerca.com",
        "medico"
    )

    medico4 = crear_usuario_si_no_existe(
        "Dra. Sofía Benítez",
        "sofia.benitez@medicerca.com",
        "medico"
    )

    medico5 = crear_usuario_si_no_existe(
        "Dr. Pedro González",
        "pedro.gonzalez@medicerca.com",
        "medico"
    )

    print("Creando perfiles médicos...")

    crear_medico_si_no_existe(
        medico1,
        "Cardiología",
        "MAT-1001",
        "Hospital de Clínicas",
        "Asunción",
        "0981123456",
        "Especialista en enfermedades cardiovasculares con amplia experiencia clínica.",
        "UNA",
        15,
        True
    )

    crear_medico_si_no_existe(
        medico2,
        "Pediatría",
        "MAT-1002",
        "Hospital Regional de Encarnación",
        "Encarnación",
        "0982123456",
        "Pediatra enfocada en el cuidado integral de niños y adolescentes.",
        "UCA",
        10,
        True
    )

    crear_medico_si_no_existe(
        medico3,
        "Dermatología",
        "MAT-1003",
        "Hospital Regional",
        "Ciudad del Este",
        "0983123456",
        "Dermatólogo especializado en enfermedades de la piel y tratamientos estéticos.",
        "UNINORTE",
        8,
        False
    )

    crear_medico_si_no_existe(
        medico4,
        "Neurología",
        "MAT-1004",
        "Hospital General",
        "San Lorenzo",
        "0984123456",
        "Neuróloga dedicada al diagnóstico y tratamiento de trastornos neurológicos.",
        "UA",
        12,
        True
    )

    crear_medico_si_no_existe(
        medico5,
        "Traumatología",
        "MAT-1005",
        "Hospital Distrital",
        "Luque",
        "0985123456",
        "Traumatólogo especializado en lesiones deportivas y cirugía ortopédica.",
        "UAA",
        9,
        False
    )

    print("Seeds completados correctamente.") # Tu código acá
