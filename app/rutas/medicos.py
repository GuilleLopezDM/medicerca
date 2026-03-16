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




# TODO (Mathi) — FEATURE 5: Formulario de edición
@bp_medicos.route("/editar/<int:medico_id>", methods=["GET", "POST"])
@login_required
def editar(medico_id):
    medico = Medico.query.get_or_404(medico_id)

    # Seguridad: Solo dueño o Admin
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
        medico.numero_matricula = request.form.get('Numero de Matricula')
        
        
        bd.session.commit()
        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for('medicos.detalle', medico_id=medico.id))

    return render_template("medicos/editar.html", medico=medico)

# TODO (Mathi) — FEATURE 6: Guardar edición



# --- FEATURE 5: MAPA DE MÉDICOS ---

