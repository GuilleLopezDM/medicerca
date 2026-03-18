"""
seeds.py
========
Crea 10 médicos y 10 pacientes con datos paraguayos de prueba.
Ejecutar con: python seeds.py
"""

from dotenv import load_dotenv
load_dotenv(override=True)

from app import crear_app, bd
from app.models.models import Usuario, Medico, Resena

app = crear_app()

MEDICOS = [
    {
        "nombre": "Dr. Carlos Benítez",
        "correo": "carlos.benitez@medicerca.com",
        "especialidad": "Cardiología",
        "matricula": "MAT-001",
        "hospital": "Hospital Nacional de Itauguá",
        "ciudad": "Itauguá",
        "telefono": "0981-111-001",
        "biografia": "Cardiólogo con más de 15 años de experiencia en enfermedades del corazón.",
        "universidad": "Universidad Nacional de Asunción",
        "anios": 15,
        "latitud": -25.3850,
        "longitud": -57.3536,
        "direccion": "Av. República Argentina 123, Asunción",
    },
    {
        "nombre": "Dra. María Ramírez",
        "correo": "maria.ramirez@medicerca.com",
        "especialidad": "Pediatría",
        "matricula": "MAT-002",
        "hospital": "Hospital de Clínicas",
        "ciudad": "Asunción",
        "telefono": "0981-111-002",
        "biografia": "Pediatra especializada en neonatología y desarrollo infantil.",
        "universidad": "Universidad Católica Nuestra Señora de la Asunción",
        "anios": 10,
        "latitud": -25.2933,
        "longitud": -57.6500,
        "direccion": "Av. Dr. Montero 456, Asunción",
    },
    {
        "nombre": "Dr. Jorge Medina",
        "correo": "jorge.medina@medicerca.com",
        "especialidad": "Traumatología",
        "matricula": "MAT-003",
        "hospital": "Sanatorio Americano",
        "ciudad": "Asunción",
        "telefono": "0981-111-003",
        "biografia": "Traumatólogo con experiencia en cirugía ortopédica y deportiva.",
        "universidad": "Universidad Nacional de Asunción",
        "anios": 12,
        "latitud": -25.2867,
        "longitud": -57.6467,
        "direccion": "Calle Eligio Ayala 789, Asunción",
    },
    {
        "nombre": "Dra. Ana González",
        "correo": "ana.gonzalez@medicerca.com",
        "especialidad": "Dermatología",
        "matricula": "MAT-004",
        "hospital": "Centro Médico La Costa",
        "ciudad": "San Lorenzo",
        "telefono": "0981-111-004",
        "biografia": "Dermatóloga especializada en enfermedades de la piel y estética.",
        "universidad": "Universidad del Norte",
        "anios": 8,
        "latitud": -25.3397,
        "longitud": -57.5103,
        "direccion": "Av. Mariscal López 321, San Lorenzo",
    },
    {
        "nombre": "Dr. Luis Villalba",
        "correo": "luis.villalba@medicerca.com",
        "especialidad": "Neurología",
        "matricula": "MAT-005",
        "hospital": "Hospital Central del IPS",
        "ciudad": "Asunción",
        "telefono": "0981-111-005",
        "biografia": "Neurólogo con especialización en epilepsia y enfermedades degenerativas.",
        "universidad": "Universidad Nacional de Asunción",
        "anios": 20,
        "latitud": -25.2954,
        "longitud": -57.6388,
        "direccion": "Av. General Santos 654, Asunción",
    },
    {
        "nombre": "Dra. Rosa Acosta",
        "correo": "rosa.acosta@medicerca.com",
        "especialidad": "Ginecología y Obstetricia",
        "matricula": "MAT-006",
        "hospital": "Clínica Santa María",
        "ciudad": "Fernando de la Mora",
        "telefono": "0981-111-006",
        "biografia": "Ginecóloga con amplia trayectoria en atención prenatal y partos.",
        "universidad": "Universidad Católica Nuestra Señora de la Asunción",
        "anios": 14,
        "latitud": -25.3333,
        "longitud": -57.5833,
        "direccion": "Av. Primer Presidente 987, Fernando de la Mora",
    },
    {
        "nombre": "Dr. Pablo Cáceres",
        "correo": "pablo.caceres@medicerca.com",
        "especialidad": "Oftalmología",
        "matricula": "MAT-007",
        "hospital": "Centro Oftalmológico Paraguay",
        "ciudad": "Asunción",
        "telefono": "0981-111-007",
        "biografia": "Oftalmólogo especializado en cirugía refractiva y cataratas.",
        "universidad": "Universidad Nacional de Asunción",
        "anios": 11,
        "latitud": -25.2800,
        "longitud": -57.6300,
        "direccion": "Calle Palma 147, Asunción",
    },
    {
        "nombre": "Dra. Sandra Duarte",
        "correo": "sandra.duarte@medicerca.com",
        "especialidad": "Endocrinología",
        "matricula": "MAT-008",
        "hospital": "Sanatorio Migone",
        "ciudad": "Asunción",
        "telefono": "0981-111-008",
        "biografia": "Endocrinóloga experta en diabetes, tiroides y trastornos hormonales.",
        "universidad": "Universidad del Norte",
        "anios": 9,
        "latitud": -25.2920,
        "longitud": -57.6420,
        "direccion": "Av. España 258, Asunción",
    },
    {
        "nombre": "Dr. Marcos Ortiz",
        "correo": "marcos.ortiz@medicerca.com",
        "especialidad": "Psiquiatría",
        "matricula": "MAT-009",
        "hospital": "Instituto de Psiquiatría Social",
        "ciudad": "Luque",
        "telefono": "0981-111-009",
        "biografia": "Psiquiatra con enfoque en salud mental comunitaria y tratamiento de adicciones.",
        "universidad": "Universidad Nacional de Asunción",
        "anios": 13,
        "latitud": -25.2667,
        "longitud": -57.4833,
        "direccion": "Av. Mcal. Estigarribia 369, Luque",
    },
    {
        "nombre": "Dra. Elena Paredes",
        "correo": "elena.paredes@medicerca.com",
        "especialidad": "Gastroenterología",
        "matricula": "MAT-010",
        "hospital": "Hospital Bautista",
        "ciudad": "Asunción",
        "telefono": "0981-111-010",
        "biografia": "Gastroenteróloga especializada en enfermedades del sistema digestivo.",
        "universidad": "Universidad Católica Nuestra Señora de la Asunción",
        "anios": 16,
        "latitud": -25.3050,
        "longitud": -57.6550,
        "direccion": "Av. Mcal. López 741, Asunción",
    },
]

PACIENTES = [
    {"nombre": "Juan Ríos",        "correo": "juan.rios@gmail.com"},
    {"nombre": "Claudia Sánchez",  "correo": "claudia.sanchez@gmail.com"},
    {"nombre": "Roberto Vera",     "correo": "roberto.vera@gmail.com"},
    {"nombre": "Patricia López",   "correo": "patricia.lopez@gmail.com"},
    {"nombre": "Miguel Ferreira",  "correo": "miguel.ferreira@gmail.com"},
    {"nombre": "Natalia Romero",   "correo": "natalia.romero@gmail.com"},
    {"nombre": "Diego Giménez",    "correo": "diego.gimenez@gmail.com"},
    {"nombre": "Valeria Núñez",    "correo": "valeria.nunez@gmail.com"},
    {"nombre": "Fernando Aquino",  "correo": "fernando.aquino@gmail.com"},
    {"nombre": "Gabriela Monges",  "correo": "gabriela.monges@gmail.com"},
]

COMENTARIOS = [
    "Excelente médico, muy atento y profesional.",
    "Me atendió muy bien, lo recomiendo totalmente.",
    "Muy buen profesional, explica todo con claridad.",
    "Muy dedicado y paciente con sus pacientes.",
    "Gran profesional, me sentí muy cómodo en la consulta.",
]

def ejecutar_seeds():
    with app.app_context():

        print("🌱 Iniciando seeds...")

        # ── Pacientes ──────────────────────────────────
        pacientes_creados = []
        for datos in PACIENTES:
            if Usuario.query.filter_by(correo=datos["correo"]).first():
                print(f"  ⏭ Paciente ya existe: {datos['correo']}")
                pacientes_creados.append(Usuario.query.filter_by(correo=datos["correo"]).first())
                continue

            u = Usuario(
                nombre=datos["nombre"],
                correo=datos["correo"],
                rol="paciente",
                email_verificado=True,
            )
            u.establecer_contrasena("paciente1234")
            bd.session.add(u)
            bd.session.flush()
            pacientes_creados.append(u)
            print(f"  ✅ Paciente creado: {datos['nombre']}")

        # ── Médicos ────────────────────────────────────
        import random
        for i, datos in enumerate(MEDICOS):
            if Usuario.query.filter_by(correo=datos["correo"]).first():
                print(f"  ⏭ Médico ya existe: {datos['correo']}")
                continue

            u = Usuario(
                nombre=datos["nombre"],
                correo=datos["correo"],
                rol="medico",
                email_verificado=True,
            )
            u.establecer_contrasena("medico1234")
            bd.session.add(u)
            bd.session.flush()

            m = Medico(
                usuario_id=u.id,
                especialidad=datos["especialidad"],
                numero_matricula=datos["matricula"],
                hospital=datos["hospital"],
                ciudad=datos["ciudad"],
                telefono=datos["telefono"],
                biografia=datos["biografia"],
                universidad_graduacion=datos["universidad"],
                anios_experiencia=datos["anios"],
                verificado=True,
                latitud=datos["latitud"],
                longitud=datos["longitud"],
                direccion_consultorio=datos["direccion"],
            )
            bd.session.add(m)
            bd.session.flush()

            # Agregar 3 reseñas por médico
            for j, paciente in enumerate(pacientes_creados[:3]):
                resena = Resena(
                    medico_id=m.id,
                    usuario_id=paciente.id,
                    puntuacion=random.randint(4, 5),
                    comentario=COMENTARIOS[j % len(COMENTARIOS)],
                )
                bd.session.add(resena)

            # Actualizar promedio y total
            m.total_resenas = 3
            m.calificacion_promedio = round(random.uniform(4.0, 5.0), 1)

            print(f"  ✅ Médico creado: {datos['nombre']} ({datos['especialidad']})")

        bd.session.commit()
        print("\n🎉 Seeds completados exitosamente.")
        print("   Contraseña médicos:   medico1234")
        print("   Contraseña pacientes: paciente1234")


if __name__ == "__main__":
    ejecutar_seeds()