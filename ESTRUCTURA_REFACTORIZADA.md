# MediCerca refactorizado sin romper el proyecto

## Qué se reorganizó
- Se centralizó la configuración en `app/config.py`.
- Se movieron las extensiones Flask a `app/extensions.py`.
- Se simplificó el factory en `app/__init__.py`.
- Se centralizó el registro de blueprints en `app/rutas/__init__.py`.
- Se agregaron templates faltantes para recuperación de contraseña.
- Se unificaron tests duplicados en una estructura más limpia con `tests/conftest.py`.
- Se eliminaron archivos generados (`.git`, `__pycache__`, `.pyc`, base SQLite local).

## Qué no se tocó
- No se cambió la lógica principal de negocio.
- No se renombraron endpoints.
- No se movieron rutas a otras carpetas para evitar imports rotos.
- Se mantuvo compatibilidad con `from app import crear_app, bd`.

## Próximos pasos recomendados
- Separar validaciones de formularios en helpers o WTForms.
- Mover lógica administrativa pesada a servicios.
- Agregar más tests para panel admin, reseñas y perfiles médicos.
