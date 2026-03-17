"""
seeds_migracion.py  (ejecutar UNA sola vez desde la raíz del proyecto)
=======================================================================
    python seeds_migracion.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import crear_app, bd          # ← crear_app y bd (no create_app ni db)
from sqlalchemy import text, inspect

app = crear_app()

with app.app_context():
    inspector = inspect(bd.engine)
    columnas  = [c["name"] for c in inspector.get_columns("usuarios")]

    if "email_verificado" in columnas:
        print("ℹ️  La columna 'email_verificado' ya existe. Nada que hacer.")
        sys.exit(0)

    with bd.engine.connect() as conn:
        conn.execute(text(
            "ALTER TABLE usuarios ADD COLUMN email_verificado BOOLEAN NOT NULL DEFAULT 0"
        ))
        conn.commit()

    print("✅ Columna 'email_verificado' agregada correctamente.")
    print("   Todos los usuarios existentes quedan con email_verificado = False.")
    print("   Si querés marcarlos como verificados ejecutá:")
    print("   UPDATE usuarios SET email_verificado = 1;")