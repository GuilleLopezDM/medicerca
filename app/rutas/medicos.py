from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
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

    # Feature 1 — Búsqueda general
    if busqueda:
        query = query.filter(
            (Usuario.nombre.ilike(f"%{busqueda}%")) | 
            (Medico.especialidad.ilike(f"%{busqueda}%")) | 
            (Medico.hospital.ilike(f"%{busqueda}%"))
        )

    # Feature 2 — Filtro por especialidad
    if especialidad:
        query = query.filter(Medico.especialidad.ilike(f"%{especialidad}%"))

    if ciudad:
        query = query.filter(Medico.ciudad.ilike(f"%{ciudad}%"))

    if universidad:
        query = query.filter(Medico.universidad_graduacion.ilike(f"%{universidad}%"))

    if verificados == "1":
        query = query.filter(Medico.verificado == True)

    medicos = query.all()

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
    medico = bd.session.get(Medico, medico_id)
    if not medico:
        abort(404)
    return render_template("medicos/detalle.html", medico=medico)

#F3 Formulario de registro medico — FEATURE 4: Guardar perfil médico
@bp_medicos.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    if current_user.rol != 'medico':
        flash("Solo usuarios con rol 'médico' pueden crear un perfil profesional.", "warning")
        return redirect(url_for('principal.inicio'))
    
    if current_user.perfil_medico:
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

# TODO — FEATURE 5/6: Editar perfil
@bp_medicos.route("/editar/<int:medico_id>", methods=["GET", "POST"])
@login_required
def editar(medico_id):
    medico = bd.session.get(Medico, medico_id)
    if not medico:
        abort(404)

    if medico.usuario_id != current_user.id and current_user.rol != 'admin':
        flash("No tienes permiso para editar este perfil.", "danger")
        return redirect(url_for('medicos.detalle', medico_id=medico.id))

    if request.method == "POST":
        medico.especialidad = request.form.get('especialidad')
        medico.hospital = request.form.get('hospital')
        medico.ciudad = request.form.get('ciudad')
        medico.telefono = request.form.get('telefono')
        medico.biografia = request.form.get('biografia')
        medico.universidad_graduacion = request.form.get('universidad_graduacion')
        medico.anios_experiencia = request.form.get('anios_experiencia', type=int)
        medico.numero_matricula = request.form.get('numero_matricula')
        
        bd.session.commit()
        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for('medicos.detalle', medico_id=medico.id))

    return render_template("medicos/editar.html", medico=medico)

# --- FEATURE 5: MAPA DE MÉDICOS ---
@bp_medicos.route("/mapa")
def mapa_medicos():
    medicos_geolocalizados = Medico.query.filter(
        Medico.latitud.isnot(None), 
        Medico.longitud.isnot(None)
    ).join(Usuario).all()
    return render_template("medicos/mapa.html", medicos=medicos_geolocalizados)
