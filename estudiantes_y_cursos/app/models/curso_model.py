from app.config.mysqlconnection import connectToMySQL
from flask import flash

DB_NAME = "esquema_estudiantes_cursos"

class Curso:
    """
    Representa un curso y operaciones DB.
    """

    db = DB_NAME

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data.get('nombre')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    # -------------------- CREATE --------------------
    @classmethod
    def save(cls, data):
        """
        Inserta curso
        """

        query = """
            INSERT INTO cursos (nombre)
            VALUES (%(nombre)s);
        """

        return connectToMySQL(cls.db).query_db(query, data)

    # -------------------- READ --------------------
    @classmethod
    def get_all(cls):
        """
        Obtiene todos los cursos
        """
        query = """
            SELECT * FROM cursos;
        """
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_by_id(cls, id):
        """
        Obtiene un curso por su ID
        """
        query = """
            SELECT * FROM cursos WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})
        
    @classmethod
    def get_by_nombre(cls, nombre):
        """
        Obtiene un curso por su nombre
        """
        query = """
            SELECT * FROM cursos WHERE nombre = %(nombre)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'nombre': nombre})

    # -------------------- UPDATE --------------------
    @classmethod
    def update(cls, data):
        """
        Actualiza un curso
        """
        query = """
            UPDATE cursos SET nombre = %(nombre)s WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # -------------------- DELETE --------------------
    @classmethod
    def delete(cls, id):
        """
        Elimina un curso
        """
        query = """
            DELETE FROM cursos WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': id})
        
    # -------------------- VALIDACIONES --------------------
    @staticmethod
    def validate(data):
        """
        Valida los datos de un curso
        """
        is_valid = True
        if len(data['nombre']) < 3:
            flash("Nombre debe tener al menos 3 caracteres", "nombre")
            is_valid = False
        if data['nombre'] in [curso['nombre'] for curso in Curso.get_all()]:
            flash("Nombre de curso ya existe", "nombre")
            is_valid = False
        return is_valid
