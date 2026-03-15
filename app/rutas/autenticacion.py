from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import bd
from app.models import Usuario

bp_autenticacion = Blueprint("autenticacion", __name__, url_prefix="/auth")


@bp_autenticacion.get("/iniciar-sesion")
def iniciar_sesion():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacion/iniciar_sesion.html")


@bp_autenticacion.post("/iniciar-sesion")
def procesar_inicio_sesion():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    recordarme = request.form.get("recordarme") is not None

    usuario = Usuario.query.filter_by(correo=correo).first()

    if usuario and usuario.verificar_contrasena(contrasena):
        login_user(usuario, remember=recordarme)

        siguiente = request.args.get("next")
        if siguiente:
            return redirect(siguiente)

        return redirect(url_for("principal.inicio"))

    flash("Correo o contraseña incorrectos.", "danger")
    return redirect(url_for("autenticacion.iniciar_sesion"))


# TODO (Matheus) — FEATURE 3: Página de registro
# GET /auth/registro → mostrar template "autenticacion/registro.html"
# Si el usuario ya está autenticado → redirigir a principal.inicio


# TODO (Matheus) — FEATURE 4: Procesar registro
# POST /auth/registro
# - Leer campos: nombre, correo, contrasena, rol
# - Verificar que el correo no exista: Usuario.query.filter_by(correo=correo).first()
# - Si existe → flash("Ya existe una cuenta con ese correo.", "danger")
# - Si no → crear Usuario, llamar establecer_contrasena(), bd.session.add(), bd.session.commit()
# - flash("Cuenta creada exitosamente.", "success") → redirigir a autenticacion.iniciar_sesion


# TODO (Matheus) — FEATURE 5: Cerrar sesión
# GET /auth/cerrar-sesion → requiere @login_required
# - logout_user()
# - flash("Sesión cerrada.", "info")
# - redirigir a principal.inicio