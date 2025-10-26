from flask import render_template, redirect, request, session, Blueprint, flash, url_for
from app.models.estudiante_model import Estudiante
from app.models.curso_model import Curso


bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')

# ---------- Dashboard ----------
@bp.route('/')
def dashboard():
    estudiantes = Estudiante.get_all()
    cursos = Curso.get_all()
    return render_template('dashboard.html', estudiantes=estudiantes, cursos=cursos)

# ---------- Nuevo estudiante ----------
@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_estudiante():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'edad': request.form['edad'],
            'curso_id': request.form['curso_id']
        }
        if Estudiante.validate(data):
            Estudiante.save(data)
            flash("Estudiante creado correctamente", "success")
            return redirect(url_for('cursos.dashboard'))
    cursos = Curso.get_all()
    return render_template('nuevo_estudiante.html', cursos=cursos)

# ---------- Editar estudiante ----------
@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_estudiante(id):
    if request.method == 'POST':
        data = {
            'id': id,
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'edad': request.form['edad'],
            'curso_id': request.form['curso_id']
        }

        if Estudiante.validate(data):
            Estudiante.update(data)
            flash("Estudiante actualizado correctamente", "success")
            return redirect(url_for('estudiantes.dashboard'))
    estudiante = Estudiante.get_by_id(id)
    cursos = Curso.get_all()
    return render_template('editar_estudiante.html', estudiante=estudiante, cursos=cursos)

# ---------- Eliminar estudiante ----------
@bp.route('/eliminar/<int:id>')
def eliminar_estudiante(id):
    Estudiante.delete(id)
    flash("Estudiante eliminado correctamente", "success")
    return redirect(url_for('estudiantes.dashboard'))

# ---------- Asignar estudiante a curso ----------
@bp.route('/asignar/<int:id>', methods=['GET', 'POST'])
def asignar_estudiante(id):
    if request.method == 'POST':
        data = {
            'id': id,
            'curso_id': request.form['curso_id']
        }
        if Estudiante.validate(data):
            Estudiante.asignar_curso(data)
            flash("Estudiante asignado correctamente", "success")
            return redirect(url_for('estudiantes.dashboard'))

