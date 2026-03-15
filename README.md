# 🩺 MediCerca — Directorio Médico Interactivo

> Hackathon 2025 · Python + Flask + SQLite + Tailwind CSS + Leaflet.js

**MediCerca** es una plataforma web para encontrar médicos profesionales en Paraguay. Permite buscar por especialidad y ciudad, ver el consultorio en un mapa interactivo y leer reseñas de otros pacientes.

---

## ✨ Features

| Feature | Descripción |
|---|---|
| 🔍 **Directorio de médicos** | Búsqueda y filtros por especialidad, ciudad y universidad |
| 🗺️ **Mapa interactivo** | Leaflet.js con marcadores de consultorios y preview al clickear |
| 📍 **Ubicación del consultorio** | El médico ubica su consultorio clickeando en el mapa |
| ⭐ **Rating y reseñas** | Sistema de 1-5 estrellas con recálculo automático de promedio |
| 🔐 **Autenticación** | Registro y login con roles (paciente / médico) |
| 🎓 **Perfil completo** | Matrícula, universidad, hospital, experiencia, biografía |

---

## 🛠️ Stack tecnológico

```
Backend:    Python 3.11 + Flask 3.0
Base datos: SQLite (Flask-SQLAlchemy)
Auth:       Flask-Login + Werkzeug
Frontend:   Jinja2 + Tailwind CSS (CDN)
Mapa:       Leaflet.js + OpenStreetMap (sin API key)
Testing:    pytest
```

---

## 🚀 Instalación y uso

```bash
# 1. Clonar el repositorio
git clone https://github.com/GuilleLopezDM/medicerca.git
cd medicerca

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env       # Windows
cp .env.example .env         # Mac/Linux

# 5. Cargar datos de prueba
python seeds.py

# 6. Correr la aplicación
flask run
```

Abrir → **http://127.0.0.1:5000**

---

## 👤 Usuarios de prueba

| Correo | Contraseña | Rol |
|---|---|---|
| `carlos@medicerca.com` | `test1234` | Médico — Cardiología |
| `laura@medicerca.com` | `test1234` | Médico — Pediatría |
| `roberto@medicerca.com` | `test1234` | Médico — Dermatología |
| `ana@medicerca.com` | `test1234` | Médico — Neurología |
| `miguel@medicerca.com` | `test1234` | Médico — Traumatología |
| `paciente1@test.com` | `test1234` | Paciente |

---

## 📁 Estructura del proyecto

```
medicerca/
├── run.py                        # Entry point
├── seeds.py                      # Datos de prueba
├── requirements.txt
├── .env.example
│
├── app/
│   ├── __init__.py               # App factory
│   ├── models/
│   │   └── models.py             # Usuario, Medico, Resena
│   ├── rutas/
│   │   ├── autenticacion.py      # Login, Registro, Logout
│   │   ├── medicos.py            # CRUD de médicos + filtros
│   │   ├── principal.py          # Homepage, Panel
│   │   ├── mapa.py               # Mapa Leaflet + API JSON
│   │   └── resenas.py            # Sistema de reseñas y rating
│   ├── templates/                # HTML con Jinja2 + Tailwind CSS
│   └── static/                   # CSS y JS personalizados
│
└── tests/
    └── test_rutas.py             # 8 tests con pytest
```

---

## 🧪 Tests

```bash
pip install pytest
pytest tests/ -v
```

```
tests/test_rutas.py::test_inicio              PASSED
tests/test_rutas.py::test_pagina_login        PASSED
tests/test_rutas.py::test_pagina_registro     PASSED
tests/test_rutas.py::test_lista_medicos       PASSED
tests/test_rutas.py::test_mapa                PASSED
tests/test_rutas.py::test_api_mapa_json       PASSED
tests/test_rutas.py::test_registrar_usuario   PASSED
tests/test_rutas.py::test_medico_no_existe    PASSED
```

---

## 🔗 Flujo de Git

Este proyecto siguió un flujo de ramas estructurado con una rama por feature:

```
main        ← producción estable
develop     ← integración del equipo
feature/*   ← una rama por feature, un Pull Request por merge
```

Ejemplos de branches del proyecto:
```
feature/hugo-modelo-usuario        feature/arturo-homepage
feature/hugo-modelo-medico         feature/arturo-mapa-leaflet
feature/hugo-modelo-resena         feature/arturo-api-mapa
feature/matheus-login              feature/arturo-guardar-ubicacion
feature/matheus-registro           feature/diego-base-layout
feature/mathi-lista-medicos        feature/diego-templates-medicos
feature/mathi-detalle-medico       feature/diego-template-mapa
feature/mathi-agregar-resena       feature/marcelo-filtros-basicos
feature/mathi-editar-medico        feature/marcelo-filtros-avanzados
                                   feature/johan-seeds
                                   feature/johan-tests
```

---

## 👥 Equipo

| Participante | Rol | Responsabilidad |
|---|---|---|
| **Hugo** | Backend | Modelos de base de datos (Usuario, Medico, Resena) |
| **Matheus** | Backend | Sistema de autenticación |
| **Mathi** | Backend | CRUD de médicos + sistema de reseñas |
| **Arturo** | Backend | Homepage + mapa interactivo + API JSON |
| **Diego** | Frontend | Todos los templates HTML + Tailwind CSS |
| **Marcelo** | Backend | Búsqueda y filtros avanzados |
| **Johan** | QA | Tests, seeds y integración final |

---

## 📋 Gestión del proyecto

La organización del equipo, distribución de tareas, branches y seguimiento del progreso se documentó en Notion:

> 🔗 **[Ver workspace en Notion](https://www.notion.so/32465a04b13d8122992cd26161a557ae)**

El workspace incluye:
- Página individual por integrante con checklist de features y prompts
- Tracker Kanban con estado de cada feature en tiempo real
- Documentación de la arquitectura y contratos entre módulos
- Registro de errores y soluciones durante el desarrollo

---

## 📄 Licencia

Proyecto desarrollado para Hackathon 2025. Uso educativo.
