from flask import render_template, redirect, request, session, Blueprint, flash, url_for
from functools import wraps
from app.models.usuario_model import Usuario
from app import bcrypt


bp = Blueprint('login', __name__, url_prefix='/')

# ---------- Decorador de sesión ----------
def login_requerido(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página.", 'error')
            return redirect(url_for('login.iniciar_sesion'))
        return fn(*args, **kwargs)
    return _wrap

# ---------- Página de inicio de sesión ----------
@bp.route('/', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario_data = Usuario.get_by_email(email)
        if not usuario_data:
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for('login.iniciar_sesion'))

        usuario = Usuario(usuario_data[0])

        if not bcrypt.check_password_hash(usuario.password_hash, password):
            flash("Email o contraseña incorrectos", "error")
            return redirect(url_for('login.iniciar_sesion'))

        session['usuario_id'] = usuario.id
        session['usuario_nombre'] = usuario.nombre
        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for('login.dashboard'))

    return render_template('login.html')

# ---------- Cerrar sesión ----------
@bp.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('login.iniciar_sesion'))

# ---------- Página de registro ----------
@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener contraseñas tal como vienen del formulario
        raw_password = request.form.get('password', '')
        raw_password_confirm = request.form.get('password_confirm', '')

        # Datos para validación (incluimos confirm_password para coincidir con la validación del modelo)
        data_validation = {
            'nombre': request.form.get('nombre', ''),
            'apellido': request.form.get('apellido', ''),
            'email': request.form.get('email', ''),
            'password': raw_password,
            'confirm_password': raw_password_confirm,
            'fecha_nacimiento': request.form.get('fecha_nacimiento', ''),
            'genero': request.form.get('genero', ''),
            'acepta_terminos': 'acepta_terminos' in request.form
        }

        # Validar antes de persistir
        if Usuario.validate_registration(data_validation):
            save_data = {
                'nombre': data_validation['nombre'],
                'apellido': data_validation['apellido'],
                'email': data_validation['email'],
                'password_hash': bcrypt.generate_password_hash(raw_password).decode('utf-8'),
                'fecha_nacimiento': data_validation['fecha_nacimiento'],
                'genero': data_validation['genero'],
                # Guardar como entero (1 o 0) para compatibilidad con MySQL tinyint
                'acepta_terminos': 1 if data_validation['acepta_terminos'] else 0
            }

            nuevo_id = Usuario.save(save_data)
            # Asegurarnos de iniciar sesión automáticamente después del registro
            session['usuario_id'] = nuevo_id
            session['usuario_nombre'] = save_data['nombre']
            flash("Registro exitoso.", "success")
            return redirect(url_for('login.dashboard'))
        else:
            # Si la validación falla, redirigir de nuevo al formulario de registro
            return redirect(url_for('login.registro'))
        
# ---------- Dashboard ----------
@bp.route('/dashboard')
@login_requerido
def dashboard():
    usuario_data = Usuario.get_by_id(session['usuario_id'])
    if not usuario_data:
        flash("Usuario no encontrado.", 'error')
        return redirect(url_for('login.iniciar_sesion'))

    usuario = Usuario(usuario_data[0])
    return render_template('dashboard.html', usuario=usuario)