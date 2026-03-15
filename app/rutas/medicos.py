from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import bd
from app.models import Medico, Usuario

bp_medicos = Blueprint("medicos", __name__, url_prefix='/medicos')

#F1 listamos medicos
@bp_medicos.route("/")
def lista_medicos():
    query = Medico.query.join(Usuario)

    # Captura de filtros desde la URL
    busqueda = request.args.get('busqueda')
    especialidad = request.args.get('especialidad')
    ciudad = request.args.get('ciudad')
    universidad = request.args.get('universidad')
    verificados = request.args.get('verificados')

    # Aplicación de lógica de filtros (ILIKE para ignorar mayúsculas)
    if busqueda:
        query = query.filter(
            (Usuario.nombre.ilike(f"%{busqueda}%")) | 
            (Medico.especialidad.ilike(f"%{busqueda}%")) | 
            (Medico.hospital.ilike(f"%{busqueda}%"))
        )
    if especialidad:
        query = query.filter(Medico.especialidad.ilike(f"%{especialidad}%"))
    if ciudad:
        query = query.filter(Medico.ciudad.ilike(f"%{ciudad}%"))
    if universidad:
        query = query.filter(Medico.universidad_graduacion.ilike(f"%{universidad}%"))
    if verificados == "1":
        query = query.filter(Medico.verificado == True)

    medicos = query.all()

    # Datos para llenar los selects del buscador en el template
    # Usamos db.session.query(distintos) para no repetir opciones en los filtros
    especialidades = bd.session.query(Medico.especialidad).distinct().all()
    ciudades = bd.session.query(Medico.ciudad).distinct().all()

    return render_template(
        "medicos/lista.html", 
        medicos=medicos, 
        especialidades=[e[0] for e in especialidades if e[0]],
        ciudades=[c[0] for c in ciudades if c[0]],
        total=len(medicos),
        filtros_actuales=request.args
    )

#F2 detalle de un medico
@bp_medicos.route("/<int:medico_id>")
def detalle(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    return render_template("medicos/detalle.html", medico=medico)

#F3 Formulario de registro medico
@bp_medicos.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    # Seguridad de Rol
    if current_user.rol != 'medico':
        flash("Solo usuarios con rol 'médico' pueden crear un perfil profesional.", "warning")
        return redirect(url_for('principal.inicio'))
    
    # Evitar perfiles duplicados
    if current_user.perfil_medico: # Asumiendo relación backref en Usuario
        return redirect(url_for('medicos.detalle', medico_id=current_user.perfil_medico.id))

    if request.method == "POST":
        nuevo_medico = Medico(
            usuario_id=current_user.id,
            especialidad=request.form.get('especialidad'),
            numero_matricula=request.form.get('numero_matricula'),
            hospital=request.form.get('hospital'),
            ciudad=request.form.get('ciudad'),
            telefono=request.form.get('telefono'),
            biografia=request.form.get('biografia'),
            universidad_graduacion=request.form.get('universidad_graduacion'),
            anios_experiencia=request.form.get('anios_experiencia', type=int)
        )
        bd.session.add(nuevo_medico)
        bd.session.commit()
        flash("Perfil médico creado exitosamente.", "success")
        return redirect(url_for('medicos.detalle', medico_id=nuevo_medico.id))

    return render_template("medicos/registrar.html")


# TODO (Mathi) — FEATURE 4: Guardar perfil médico
# POST /medicos/registrar → requiere @login_required
# - Leer campos: especialidad, numero_matricula, hospital, ciudad, telefono,
#                biografia, universidad_graduacion, anios_experiencia
# - Crear Medico con usuario_id=current_user.id
# - bd.session.add(), bd.session.commit()
# - flash("Perfil médico creado.", "success") → redirigir a detalle


# TODO (Mathi) — FEATURE 5: Formulario de edición
# GET /medicos/editar/<int:medico_id> → requiere @login_required
# - Solo el dueño (medico.usuario_id == current_user.id) o rol admin puede editar
# - Si no tiene permiso → flash danger, redirigir al detalle
# - Template: "medicos/editar.html"


# TODO (Mathi) — FEATURE 6: Guardar edición
# POST /medicos/editar/<int:medico_id> → requiere @login_required
# - Campos editables: especialidad, hospital, ciudad, telefono, biografia,
#                     universidad_graduacion, anios_experiencia
# - numero_matricula NO se edita
# - bd.session.commit()
# - flash("Perfil actualizado.", "success") → redirigir al detalle


# --- FEATURE 5: MAPA DE MÉDICOS ---
# GET /medicos/mapa → mapa interactivo con todos los médicos geolocalizados
# Solo muestra médicos que tengan latitud y longitud cargados
# @bp_medicos.route("/mapa")
# def mapa_medicos():
#     # medicos_geolocalizados = Medico.query.filter(
#     #     Medico.latitud != None,
#     #     Medico.longitud != None
#     # ).join(Usuario).all()
#     # return render_template("medicos/mapa.html", medicos=medicos_geolocalizados)
#     pass  # TODO
