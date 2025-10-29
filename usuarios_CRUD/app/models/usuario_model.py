from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime

EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'

DB_NAME = "usuarios_crud"

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
        # created_at normalmente viene como string desde la DB, por ejemplo '2025-10-28 23:08:18'
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @property
    def fecha_creacion(self):
        """
        Devuelve la fecha de creación formateada para mostrar en plantillas.
        Intenta parsear `created_at` si es string, soportando formatos con/microsegundos.
        Si no se puede parsear, devuelve el valor crudo como string.
        """
        raw = self.created_at
        if not raw:
            return ''
        if isinstance(raw, datetime):
            dt = raw
        else:
            s = str(raw)
            dt = None
            for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
                try:
                    dt = datetime.strptime(s, fmt)
                    break
                except ValueError:
                    continue
            if dt is None:
                # Si no coincide con los formatos esperados, devolver la cadena tal cual
                return s
        # Formato Día/Mes/Año Hora:Minutos (ajusta según prefieras)
        return dt.strftime('%Y-%m-%d')

    # -------------------- CREATE --------------------
    @classmethod
    def save(cls, data):
        """
        Inserta usuario
        """
        query = """
            INSERT INTO usuarios (nombre, apellido, email, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, NOW(), NOW());
        """

        return connectToMySQL(cls.db).query_db(query, data)
    
    # -------------------- READ --------------------
    @classmethod
    def get_all(cls):
        """
        Obtiene todos los usuarios
        """
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db).query_db(query)
        usuarios = [cls(row) for row in results]
        return usuarios
    
    @classmethod
    def get_by_email(cls, email):
        """
        Obtiene un usuario por su email
        """
        query = """
            SELECT * FROM usuarios WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un usuario por su ID
        """
        query = """
            SELECT * FROM usuarios WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        if results:
            return cls(results[0])
        return None
    
    # -------------------- UPDATE --------------------
    @classmethod
    def update(cls, data):
        """
        Actualiza datos de un usuario
        """
        query = """
            UPDATE usuarios
            SET nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    # -------------------- DELETE --------------------
    @classmethod
    def delete(cls, id):
        """
        Elimina un usuario por su ID
        """
        query = """
            DELETE FROM usuarios WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})
    

    
    # -------------------- VALIDATIONS --------------------
    @staticmethod
    def validate(data):
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
        if data.get('email'):
            existing_user = Usuario.get_by_email(data['email'])
            if existing_user and (not data.get('id') or existing_user.id != data.get('id')):
                flash("El email ya está registrado.", "error")
                is_valid = False

        return is_valid
    
