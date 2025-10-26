from flask import render_template, redirect, request, session, Blueprint, flash, url_for
from app.models.estudiante_model import Estudiante
from app.models.curso_model import Curso


bp = Blueprint('cursos', __name__, url_prefix='/')


# ---------- Dashboard ----------
@bp.route('/')
def dashboard():
    cursos = Curso.get_all()
    return render_template('dashboard.html', cursos=cursos)


# ---------- Nuevo curso ----------
@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_curso():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre']
        }
        if Curso.validate(data):
            Curso.save(data)
            flash("Curso creado correctamente", "success")
            return redirect(url_for('cursos.dashboard'))

# ---------- Ver curso ----------
@bp.route('/ver/<int:id>')
def ver_curso(id):
    curso = Curso.get_by_id(id)
    estudiantes = Estudiante.get_by_curso_id(id)
    return render_template('ver_curso.html', curso=curso, estudiantes=estudiantes)

