from app.config.mysqlconnection import connectToMySQL
from flask import flash

DB_NAME = "esquema_estudiantes_cursos"

class Estudiante:
    """
    Representa un estudiante y operaciones DB.
    """
    db = DB_NAME

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data.get('nombre') or data.get('first_name')
        self.apellido = data.get('apellido') or data.get('last_name')
        self.edad = data.get('edad')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.curso_id = data.get('curso_id')

    # -------------------- CREATE --------------------
    @classmethod
    def save(cls, data):
        """
        Inserta estudiante
        """

        query = """
            INSERT INTO estudiantes (nombre, apellido, edad, curso_id)
            VALUES (%(nombre)s, %(apellido)s, %(edad)s, %(curso_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # -------------------- READ --------------------
    @classmethod
    def get_all(cls):
        """
        Obtiene todos los estudiantes
        """
        query = """
            SELECT * FROM estudiantes;
        """
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un estudiante por su ID
        """
        query = """
            SELECT * FROM estudiantes WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})

    @classmethod
    def get_by_curso_id(cls, curso_id):
        """
        Obtiene todos los estudiantes por el ID del curso
        """
        query = """
            SELECT * FROM estudiantes WHERE curso_id = %(curso_id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'curso_id': curso_id})

    # -------------------- UPDATE --------------------
    @classmethod
    def update(cls, data):
        """
        Actualiza un estudiante
        """
        query = """
            UPDATE estudiantes SET nombre = %(nombre)s, apellido = %(apellido)s, edad = %(edad)s, curso_id = %(curso_id)s WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # -------------------- DELETE --------------------
    @classmethod
    def delete(cls, id):
        """
        Elimina un estudiante
        """
        query = """
            DELETE FROM estudiantes WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})

    @classmethod
    def delete_curso_id(cls, curso_id):
        """
        Elimina al estudainte de un curso
        """

        query = """
            UPDATE estudiantes SET curso_id = NULL WHERE curso_id = %(curso_id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'curso_id': curso_id})

    @classmethod
    def asignar_curso(cls, data):
        """
        Asigna un estudiante a un curso
        """
        query = """
            UPDATE estudiantes SET curso_id = %(curso_id)s WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # -------------------- VALIDACIONES --------------------

    @staticmethod
    def validate(data):
        """
        Valida los datos de un estudiante
        """
        is_valid = True
        if len(data['nombre']) < 3:
            flash("Nombre debe tener al menos 3 caracteres", "nombre")
            is_valid = False
        if len(data['apellido']) < 3:
            flash("Apellido debe tener al menos 3 caracteres", "apellido")
            is_valid = False
        if len(data['edad']) < 1:
            flash("Edad debe ser mayor a 0", "edad")
            is_valid = False
        if len(data['edad']) > 100:
            flash("Edad debe ser menor a 100", "edad")
            is_valid = False
        if data['curso_id'] is None:
            flash("Curso es requerido", "curso_id")
            is_valid = False
        return is_valid