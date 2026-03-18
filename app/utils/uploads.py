import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def archivo_permitido(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def guardar_imagen(subida):
    if not subida or not subida.filename:
        return None

    if not archivo_permitido(subida.filename):
        return None

    nombre_seguro = secure_filename(subida.filename)
    extension = nombre_seguro.rsplit(".", 1)[1].lower()
    nombre_final = f"{uuid.uuid4().hex}.{extension}"

    ruta_carpeta = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_completa = os.path.join(ruta_carpeta, nombre_final)
    subida.save(ruta_completa)

    return nombre_final