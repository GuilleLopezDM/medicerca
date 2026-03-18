"""
app/rutas/admin.py
==================
Panel de administración — solo accesible para usuarios con rol='admin'.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from app.extensions import bd
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
    contrasena = request.form.get("contrasena", "").strip()

    if not nombre or not correo:
        flash("Nombre y correo son obligatorios.", "danger")
        return redirect(url_for("admin.editar_usuario", usuario_id=usuario_id))

    existente = Usuario.query.filter_by(correo=correo).first()
    if existente and existente.id != usuario.id:
        flash("Ese correo ya está en uso por otro usuario.", "danger")
        return redirect(url_for("admin.editar_usuario", usuario_id=usuario_id))

    usuario.nombre = nombre
    usuario.correo = correo

    if contrasena:
        usuario.establecer_contrasena(contrasena)

    bd.session.commit()
    flash(f"Usuario {nombre} actualizado correctamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


# ── Editar usuario completo (usuario + médico si aplica) ─────────────────
@bp_admin.get("/usuarios/<int:usuario_id>/editar-completo")
@login_required
@solo_admin
def editar_completo_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    medico = usuario.perfil_medico
    resenas = []
    if medico:
        resenas = Resena.query.filter_by(medico_id=medico.id).all()
    return render_template("admin/editar_completo.html", usuario=usuario, medico=medico, resenas=resenas)


@bp_admin.post("/usuarios/<int:usuario_id>/editar-completo")
@login_required
@solo_admin
def procesar_editar_completo_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    medico = usuario.perfil_medico

    # Actualizar usuario (sin tocar el rol)
    usuario.nombre = request.form.get('nombre', usuario.nombre)
    usuario.correo = request.form.get('correo', usuario.correo)
    contrasena = request.form.get('contrasena')
    if contrasena:
        usuario.establecer_contrasena(contrasena)

    # Actualizar médico si existe
    if medico:
        medico.especialidad           = request.form.get('especialidad', medico.especialidad)
        medico.numero_matricula       = request.form.get('numero_matricula', medico.numero_matricula)
        medico.hospital               = request.form.get('hospital', medico.hospital)
        medico.ciudad                 = request.form.get('ciudad', medico.ciudad)
        medico.telefono               = request.form.get('telefono', medico.telefono)
        medico.biografia              = request.form.get('biografia', medico.biografia)
        medico.universidad_graduacion = request.form.get('universidad_graduacion', medico.universidad_graduacion)
        medico.anios_experiencia      = request.form.get('anios_experiencia', type=int) if request.form.get('anios_experiencia') else medico.anios_experiencia
        medico.verificado             = request.form.get('verificado') == 'on'
        medico.latitud                = request.form.get('latitud', type=float) if request.form.get('latitud') else medico.latitud
        medico.longitud               = request.form.get('longitud', type=float) if request.form.get('longitud') else medico.longitud
        medico.direccion_consultorio  = request.form.get('direccion_consultorio', medico.direccion_consultorio)

    bd.session.commit()
    flash(f"Usuario {usuario.nombre} actualizado correctamente.", "success")
    return redirect(url_for("admin.listar_usuarios"))


# ── Seleccionar ubicación para médico (admin) ──
@bp_admin.get("/medicos/<int:medico_id>/ubicacion")
@login_required
@solo_admin
def seleccionar_ubicacion_admin(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    return render_template("admin/seleccionar_ubicacion.html", medico=medico)


@bp_admin.post("/medicos/<int:medico_id>/guardar-ubicacion")
@login_required
@solo_admin
def guardar_ubicacion_admin(medico_id):
    medico = Medico.query.get_or_404(medico_id)

    medico.latitud               = request.form.get("latitud", type=float)
    medico.longitud              = request.form.get("longitud", type=float)
    medico.direccion_consultorio = request.form.get("direccion_consultorio", "")

    bd.session.commit()
    flash("Ubicación guardada correctamente.", "success")
    return redirect(url_for("admin.editar_completo_usuario", usuario_id=medico.usuario_id))


# ── Eliminar reseña individual ─────────────────
@bp_admin.post("/resenas/<int:resena_id>/eliminar")
@login_required
@solo_admin
def eliminar_resena_admin(resena_id):
    resena = Resena.query.get_or_404(resena_id)
    medico_id = resena.medico_id

    bd.session.delete(resena)
    bd.session.commit()

    from app.rutas.resenas import recalcular_calificacion
    recalcular_calificacion(medico_id)

    flash("Reseña eliminada correctamente.", "info")
    return redirect(request.referrer or url_for("admin.listar_usuarios"))


# ── Eliminar usuario ───────────────────────────
@bp_admin.post("/usuarios/<int:usuario_id>/eliminar")
@login_required
@solo_admin
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == current_user.id:
        flash("No podés eliminar tu propia cuenta.", "danger")
        return redirect(url_for("admin.listar_usuarios"))

    # 1. Reseñas escritas por este usuario (como autor/paciente)
    Resena.query.filter_by(usuario_id=usuario.id).delete()

    # 2. Reseñas recibidas en su perfil médico + perfil médico
    if usuario.perfil_medico:
        Resena.query.filter_by(medico_id=usuario.perfil_medico.id).delete()
        bd.session.delete(usuario.perfil_medico)

    # 3. El usuario
    nombre = usuario.nombre
    bd.session.delete(usuario)
    bd.session.commit()

    flash(f"Usuario {nombre} y datos asociados eliminados.", "success")
    return redirect(url_for("admin.listar_usuarios"))