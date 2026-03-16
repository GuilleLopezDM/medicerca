from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import bd
from app.models import Usuario

bp_autenticacion = Blueprint("autenticacion", __name__, url_prefix="/auth")


# pagina de login
@bp_autenticacion.get("/iniciar-sesion")
def iniciar_sesion():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacion/iniciar_sesion.html")


# procesar login
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


# pagina de registro
@bp_autenticacion.get("/registro")
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacion/registro.html")


# procesar registro
@bp_autenticacion.post("/registro")
def procesar_registro():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    rol = request.form.get("rol", "").strip()

    usuario_existente = Usuario.query.filter_by(correo=correo).first()

    if usuario_existente:
        flash("Ya existe una cuenta con ese correo.", "danger")
        return redirect(url_for("autenticacion.registro"))

    nuevo_usuario = Usuario(
        nombre=nombre,
        correo=correo,
        rol=rol
    )
    nuevo_usuario.establecer_contrasena(contrasena)

    bd.session.add(nuevo_usuario)
    bd.session.commit()

    flash("Cuenta creada exitosamente.", "success")
    return redirect(url_for("autenticacion.iniciar_sesion"))


# logout
@bp_autenticacion.get("/cerrar-sesion")
@login_required
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("principal.inicio"))