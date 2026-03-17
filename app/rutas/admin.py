"""
app/rutas/admin.py
==================
Panel de administración — solo accesible para usuarios con rol='admin'.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from app import bd
from app.models.models import Usuario, Medico, Resena
from app.services.email_service import get_email_service

bp_admin = Blueprint("admin", __name__, url_prefix="/admin")


# ── Decorador: solo admins ─────────────────────
def solo_admin(f):
    @wraps(f)
    def decorado(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorado


# ── Dashboard ──────────────────────────────────
@bp_admin.get("/")
@login_required
@solo_admin
def dashboard():
    stats = {
        "total_usuarios":  Usuario.query.count(),
        "total_medicos":   Medico.query.count(),
        "total_resenas":   Resena.query.count(),
        "medicos_verificados": Medico.query.filter_by(verificado=True).count(),
        "por_rol": {
            "paciente": Usuario.query.filter_by(rol="paciente").count(),
            "medico":   Usuario.query.filter_by(rol="medico").count(),
            "admin":    Usuario.query.filter_by(rol="admin").count(),
        },
        "ultimos_usuarios": Usuario.query.order_by(Usuario.creado_en.desc()).limit(5).all(),
    }
    return render_template("admin/dashboard.html", stats=stats)


# ── Listado de usuarios ────────────────────────
@bp_admin.get("/usuarios")
@login_required
@solo_admin
def listar_usuarios():
    busqueda = request.args.get("q", "").strip()
    rol_filtro = request.args.get("rol", "")

    query = Usuario.query

    if busqueda:
        query = query.filter(
            (Usuario.nombre.ilike(f"%{busqueda}%")) |
            (Usuario.correo.ilike(f"%{busqueda}%"))
        )
    if rol_filtro:
        query = query.filter_by(rol=rol_filtro)

    usuarios = query.order_by(Usuario.creado_en.desc()).all()
    return render_template("admin/usuarios.html", usuarios=usuarios,
                           busqueda=busqueda, rol_filtro=rol_filtro)


# ── Crear usuario ──────────────────────────────
@bp_admin.get("/usuarios/crear")
@login_required
@solo_admin
def crear_usuario():
    return render_template("admin/crear_usuario.html")


@bp_admin.post("/usuarios/crear")
@login_required
@solo_admin
def procesar_crear_usuario():
    nombre     = request.form.get("nombre", "").strip()
    correo     = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")
    rol        = request.form.get("rol", "paciente")

    if not nombre or not correo or not contrasena:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("admin.crear_usuario"))

    if Usuario.query.filter_by(correo=correo).first():
        flash("Ya existe una cuenta con ese correo.", "danger")
        return redirect(url_for("admin.crear_usuario"))

    usuario = Usuario(
        nombre=nombre,
        correo=correo,
        rol=rol,
        email_verificado=True,
    )
    usuario.establecer_contrasena(contrasena)
    bd.session.add(usuario)
    bd.session.commit()

    flash(f"Usuario {nombre} creado exitosamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


# ── Editar usuario ─────────────────────────────
@bp_admin.get("/usuarios/<int:usuario_id>/editar")
@login_required
@solo_admin
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template("admin/editar_usuario.html", usuario=usuario)


@bp_admin.post("/usuarios/<int:usuario_id>/editar")
@login_required
@solo_admin
def procesar_editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    nombre     = request.form.get("nombre", "").strip()
    correo     = request.form.get("correo", "").strip()
    rol        = request.form.get("rol", usuario.rol)
    contrasena = request.form.get("contrasena", "").strip()

    if not nombre or not correo:
        flash("Nombre y correo son obligatorios.", "danger")
        return redirect(url_for("admin.editar_usuario", usuario_id=usuario_id))

    # Verificar que el correo no lo use otro usuario
    existente = Usuario.query.filter_by(correo=correo).first()
    if existente and existente.id != usuario.id:
        flash("Ese correo ya está en uso por otro usuario.", "danger")
        return redirect(url_for("admin.editar_usuario", usuario_id=usuario_id))

    usuario.nombre = nombre
    usuario.correo = correo
    usuario.rol    = rol

    if contrasena:
        usuario.establecer_contrasena(contrasena)

    bd.session.commit()
    flash(f"Usuario {nombre} actualizado correctamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


# ── Eliminar usuario ───────────────────────────
@bp_admin.post("/usuarios/<int:usuario_id>/eliminar")
@login_required
@solo_admin
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash("No podés eliminar tu propia cuenta.", "danger")
        return redirect(url_for("admin.listar_usuarios"))

    nombre = usuario.nombre
    bd.session.delete(usuario)
    bd.session.commit()

    flash(f"Usuario {nombre} eliminado.", "success")
    return redirect(url_for("admin.listar_usuarios"))


# ── Cambiar rol rápido ─────────────────────────
@bp_admin.post("/usuarios/<int:usuario_id>/rol")
@login_required
@solo_admin
def cambiar_rol(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash("No podés cambiar tu propio rol.", "danger")
        return redirect(url_for("admin.listar_usuarios"))

    nuevo_rol = request.form.get("rol", "paciente")
    if nuevo_rol not in ("paciente", "medico", "admin"):
        flash("Rol inválido.", "danger")
        return redirect(url_for("admin.listar_usuarios"))

    usuario.rol = nuevo_rol
    bd.session.commit()
    flash(f"Rol de {usuario.nombre} cambiado a '{nuevo_rol}'.", "success")
    return redirect(url_for("admin.listar_usuarios"))
