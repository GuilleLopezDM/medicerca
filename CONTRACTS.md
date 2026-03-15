# 📋 CONTRATOS — MediCerca
# Este archivo define los contratos entre módulos del proyecto.
# TODOS los miembros del equipo deben leerlo antes de tocar código.
# Si cambiás un contrato, avisá al equipo ANTES de hacer el commit.

---

## 🗂️ ESTRUCTURA DEL PROYECTO

```
medicerca/
├── run.py                         ← Entry point. Solo ejecutá este archivo
├── requirements.txt               ← Dependencias Python
├── .env.example                   ← Variables de entorno (copiar a .env)
├── .gitignore
├── CONTRACTS.md                   ← ESTE ARCHIVO
├── seeds.py                       ← Datos de prueba (Johan)
│
├── app/
│   ├── __init__.py                ← App factory + extensiones (bd, gestor_login)
│   ├── models/
│   │   └── models.py              ← Modelos: Usuario, Medico (Hugo)
│   ├── rutas/
│   │   ├── autenticacion.py       ← Login, Registro, Cerrar sesión (Matheus)
│   │   ├── medicos.py             ← CRUD de médicos (Mathi)
│   │   └── principal.py           ← Inicio, Panel (Arturo)
│   ├── templates/
│   │   ├── base.html              ← Layout base (Diego)
│   │   ├── inicio/inicio.html
│   │   ├── autenticacion/
│   │   │   ├── iniciar_sesion.html
│   │   │   └── registro.html
│   │   ├── medicos/
│   │   │   ├── lista.html
│   │   │   ├── detalle.html
│   │   │   ├── registrar.html
│   │   │   └── editar.html
│   │   └── panel/panel.html
│   └── static/
│       ├── css/custom.css
│       ├── js/main.js
│       └── img/subidas/
│
├── migrations/                    ← Flask-Migrate (NO editar manualmente)
└── tests/
    └── test_rutas.py              ← Johan
```

---

## 👤 CONTRATO: Modelo Usuario (tabla: usuarios)

| Campo           | Tipo        | Restricciones         | Notas                          |
|-----------------|-------------|-----------------------|--------------------------------|
| id              | Integer     | PK, autoincrement     |                                |
| nombre          | String(100) | NOT NULL              |                                |
| correo          | String(120) | UNIQUE, NOT NULL      |                                |
| contrasena_hash | String(256) | NOT NULL              | Usar establecer_contrasena()   |
| rol             | String(20)  | default='paciente'    | 'paciente'/'medico'/'admin'    |
| creado_en       | DateTime    | default=now           |                                |

**Métodos:**
- `usuario.establecer_contrasena(contrasena)` → hashea y guarda
- `usuario.verificar_contrasena(contrasena)` → True/False

---

## 🩺 CONTRATO: Modelo Medico (tabla: medicos)

| Campo                  | Tipo        | Restricciones    | Notas                            |
|------------------------|-------------|------------------|----------------------------------|
| id                     | Integer     | PK, autoincrement|                                  |
| usuario_id             | Integer     | FK → usuarios.id |                                  |
| especialidad           | String(100) | NOT NULL         |                                  |
| numero_matricula       | String(50)  | UNIQUE, NOT NULL | Matrícula profesional            |
| hospital               | String(150) | nullable         |                                  |
| ciudad                 | String(100) | nullable         |                                  |
| telefono               | String(30)  | nullable         |                                  |
| biografia              | Text        | nullable         |                                  |
| universidad_graduacion | String(200) | nullable         | Dónde se graduó                  |
| foto                   | String(200) | default=...      |                                  |
| anios_experiencia      | Integer     | default=0        |                                  |
| calificacion           | Float       | default=0.0      |                                  |
| verificado             | Boolean     | default=False    | Solo admin puede cambiar         |
| creado_en              | DateTime    | default=now      |                                  |

**Relación:** `medico.usuario` → objeto Usuario relacionado

---

## 🔗 CONTRATO: Rutas (URLs)

### Blueprint autenticacion → prefijo `/auth`
| Método | URL                      | Función               | Acceso        |
|--------|--------------------------|-----------------------|---------------|
| GET    | /auth/iniciar-sesion     | Mostrar login         | Público       |
| POST   | /auth/iniciar-sesion     | Autenticar            | Público       |
| GET    | /auth/registro           | Mostrar registro      | Público       |
| POST   | /auth/registro           | Crear usuario         | Público       |
| GET    | /auth/cerrar-sesion      | Cerrar sesión         | Autenticado   |

### Blueprint medicos → prefijo `/medicos`
| Método | URL                       | Función                | Acceso              |
|--------|---------------------------|------------------------|---------------------|
| GET    | /medicos/                 | Listar médicos         | Público             |
| GET    | /medicos/<id>             | Ver médico             | Público             |
| GET    | /medicos/registrar        | Form registro médico   | Médico autenticado  |
| POST   | /medicos/registrar        | Crear perfil médico    | Médico autenticado  |
| GET    | /medicos/editar/<id>      | Form edición           | Dueño o Admin       |
| POST   | /medicos/editar/<id>      | Guardar edición        | Dueño o Admin       |

### Blueprint principal → prefijo `/`
| Método | URL      | Función       | Acceso  |
|--------|----------|---------------|---------|
| GET    | /        | Homepage      | Público |
| GET    | /panel   | Panel usuario | Público |

---

## 🎨 CONTRATO: Templates

- **SIEMPRE** extender `base.html`: `{% extends "base.html" %}`
- **SIEMPRE** definir `{% block titulo %}` y `{% block contenido %}`
- Usar clases de **Tailwind CSS** (CDN en base.html) con color `emerald`
- Flash messages ya en base.html — categorías: `success`, `danger`, `warning`, `info`

---

## 🧩 CONTRATO: División de Tareas

| Miembro   | Responsabilidad                                             |
|-----------|-------------------------------------------------------------|
| Hugo      | `app/models/models.py` + migraciones                        |
| Matheus   | `app/rutas/autenticacion.py` + templates autenticacion      |
| Mathi     | `app/rutas/medicos.py` + templates medicos                  |
| Arturo    | `app/rutas/principal.py` + templates inicio y panel         |
| Diego     | Todos los templates HTML + Tailwind CSS                     |
| Marcelo   | Búsqueda y filtros en `lista_medicos()`                     |
| Johan     | `seeds.py` + `tests/test_rutas.py` + README                 |

---

## ⚙️ CONTRATO: Setup local (para todos)

```bash
# 1. Clonar repo y entrar
git clone <repo-url>
cd medicerca

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu CLAVE_SECRETA

# 5. Cargar datos de prueba (opcional)
python seeds.py

# 6. Iniciar la app
flask run
```

---

## 🚫 REGLAS DEL EQUIPO

1. **NUNCA** commitear `.env` — está en `.gitignore`
2. **NUNCA** editar `migrations/` manualmente
3. Para agregar campos al modelo → avisar al equipo ANTES
4. Cada feature va en su propia branch: `feature/nombre-feature`
5. Pull requests a `develop`, NO a `main`
6. Un PR necesita al menos **1 review** antes de mergear

---

## 🔄 Flujo de git

```
main        ← solo producción estable
develop     ← integración del equipo (subir acá)
feature/*   ← cada miembro trabaja aquí
```

```bash
git checkout develop && git pull origin develop
git checkout -b feature/mi-feature
git add . && git commit -m "feat: descripción clara"
git push origin feature/mi-feature
# Abrir Pull Request → develop en GitHub
```
