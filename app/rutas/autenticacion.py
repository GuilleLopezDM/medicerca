from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import bd
from app.models.models import Usuario
from app.utils.uploads import guardar_imagen

from app.utils.tokens import (
    generar_token_reset,
    verificar_token_reset,
)
from app.services.email_service import get_email_service

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


@bp_autenticacion.get("/registro")
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    return render_template("autenticacion/registro.html")


@bp_autenticacion.post("/registro")
def procesar_registro():
    if current_user.is_authenticated:
        return redirect(url_for("principal.inicio"))

    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    rol = request.form.get("rol", "").strip()
    imagen = request.files.get("imagen_perfil")

    usuario_existente = Usuario.query.filter_by(correo=correo).first()

    if usuario_existente:
        flash("Ya existe una cuenta con ese correo.", "danger")
        return redirect(url_for("autenticacion.registro"))

    nombre_imagen = guardar_imagen(imagen)

    nuevo_usuario = Usuario(
        nombre=nombre,
        correo=correo,
        rol=rol,
        email_verificado=True,
        imagen_perfil=nombre_imagen,
    )
    nuevo_usuario.establecer_contrasena(contrasena)

    bd.session.add(nuevo_usuario)
    bd.session.commit()

    # Correo de bienvenida según rol
    svc = get_email_service()
    if rol == "medico":
        svc.enviar_bienvenida_medico(email=correo, nombre=nombre)
    else:
        svc.enviar_bienvenida(email=correo, nombre=nombre)

    login_user(nuevo_usuario)
    flash("¡Cuenta creada exitosamente! Bienvenido/a a MediCerca.", "success")
    return redirect(url_for("principal.inicio"))


@bp_autenticacion.get("/cerrar-sesion")
@login_required
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("principal.inicio"))


@bp_autenticacion.route("/recuperar", methods=["GET", "POST"])
def recuperar_contrasena():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario:
            token = generar_token_reset(correo)
            get_email_service().enviar_reset_contrasena(
                email=correo,
                nombre=usuario.nombre,
                token=token,
            )

        flash(
            "Si ese correo está registrado, te enviamos las instrucciones.",
            "success",
        )
        return redirect(url_for("autenticacion.iniciar_sesion"))

    return render_template("autenticacion/recuperar_contrasena.html")


@bp_autenticacion.route("/nueva-contrasena/<token>", methods=["GET", "POST"])
def nueva_contrasena(token):
    correo, error = verificar_token_reset(token)

    if error == "expirado":
        flash("El enlace expiró. Solicitá uno nuevo.", "warning")
        return redirect(url_for("autenticacion.recuperar_contrasena"))

    if error or not correo:
        flash("El enlace no es válido.", "danger")
        return redirect(url_for("autenticacion.recuperar_contrasena"))

    if request.method == "POST":
        nueva = request.form.get("contrasena", "")
        repetir = request.form.get("confirmar", "")

        if len(nueva) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "danger")
            return render_template("autenticacion/nueva_contrasena.html", token=token)

        if nueva != repetir:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("autenticacion/nueva_contrasena.html", token=token)

        usuario = Usuario.query.filter_by(correo=correo).first()
        usuario.establecer_contrasena(nueva)
        bd.session.commit()

        flash("✅ Contraseña actualizada. Ya podés iniciar sesión.", "success")
        return redirect(url_for("autenticacion.iniciar_sesion"))

    return render_template("autenticacion/nueva_contrasena.html", token=token)