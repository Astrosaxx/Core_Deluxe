from flask import render_template, redirect, request, session, Blueprint, flash, url_for
from app.models.usuario_model import Usuario


bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# ---------- Dashboard ----------
@bp.route('/')
def dashboard():
    usuarios = Usuario.get_all()
    return render_template('dashboard.html', usuarios=usuarios)

# ---------- Crear Usuario ----------
@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email']
        }
        if Usuario.validate(data):
            Usuario.save(data)
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('usuarios.dashboard'))
    return render_template('nuevo_usuario.html')

# ---------- Ver Usuario ----------
@bp.route('/<int:id>')
def ver_usuario(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.dashboard'))
    return render_template('ver_usuario.html', usuario=usuario)

# ---------- Editar Usuario ----------
@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.dashboard'))
    
    if request.method == 'POST':
        data = {
            'id': id,
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email']
        }
        if Usuario.validate(data):
            Usuario.update(data)
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.dashboard'))
    
    return render_template('editar_usuario.html', usuario=usuario)

# ---------- Eliminar Usuario ----------
@bp.route('/borrar/<int:id>', methods=['POST'])
def borrar_usuario(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado', 'error')
    else:
        Usuario.delete(id)
        flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('usuarios.dashboard'))