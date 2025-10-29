from app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, timedelta
import re

EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
DB_NAME = "inicio_de_sesion_y_registro"

class Usuario:
    """
    Representa un usuario y operaciones DB.
    """

    db = DB_NAME

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password_hash = data.get('password_hash')
        self.fecha_nacimiento = data.get('fecha_nacimiento')
        self.genero = data.get('genero')
        self.acepta_terminos = data.get('acepta_terminos')
        self.fecha_registro = data.get('fecha_registro')

    # -------------------- CREATE --------------------
    @classmethod
    def save(cls, data):
        """
        Inserta usuario
        """

        query = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash, fecha_nacimiento, genero, acepta_terminos, fecha_registro)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s, %(fecha_nacimiento)s, %(genero)s, %(acepta_terminos)s, NOW());
        """

        return connectToMySQL(cls.db).query_db(query, data)
    
    # -------------------- READ --------------------
    @classmethod
    def get_by_email(cls, email):
        """
        Obtiene un usuario por su email
        """
        query = """
            SELECT * FROM usuarios WHERE email = %(email)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'email': email})
    
    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un usuario por su ID
        """
        query = """
            SELECT * FROM usuarios WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})
    
    # -------------------- VALIDATIONS --------------------
    @staticmethod
    def validate_registration(data):
        """
        Valida datos de registro
        """
        is_valid = True

        if len(data.get('nombre', '')) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error")
            is_valid = False
        
        if len(data.get('apellido', '')) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "error")
            is_valid = False
        
        if not re.match(EMAIL_REGEX, data.get('email', '')):
            flash("Email inválido.", "error")
            is_valid = False

        if len(data.get('password', '')) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            is_valid = False
        
        if data.get('password') != data.get('confirm_password'):
            flash("Las contraseñas no coinciden.", "error")
            is_valid = False
        if not data.get('acepta_terminos'):
            flash("Debes aceptar los términos y condiciones.", "error")
            is_valid = False
        if not data.get('fecha_nacimiento'):
            flash("Debes ingresar una fecha de nacimiento.", "error")
            is_valid = False
        if not isinstance(data.get('fecha_nacimiento'), datetime):
            flash("La fecha de nacimiento debe ser una fecha válida.", "error")
            is_valid = False        
        elif datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d').date() > datetime.now().date():
            flash("La fecha de nacimiento no puede ser mayor a la fecha actual.", "error")
            is_valid = False
        elif datetime.now().date() - datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d').date() < timedelta(days=365*18):
            flash("Debes tener al menos 18 años para registrarte.", "error")
            is_valid = False
        if not data.get('genero'):
            flash("Debes seleccionar un género.", "error")
            is_valid = False
        if Usuario.get_by_email(data.get('email')):
            flash("El email ya está registrado.", "error")
            is_valid = False

        return is_valid