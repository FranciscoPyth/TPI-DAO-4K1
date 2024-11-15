from classes.Autor import Autor

class AutorService:
    def __init__(self, db):
        self.db = db

    def _get_autor_by_field(self, field, value, single=True):
        """Método privado para buscar autores por cualquier campo"""
        query = f"SELECT id, nombre, apellido, telefono, nacionalidad FROM autores WHERE {field} = ?"
        return self.db.fetch_query(query, (value,), single=single)

    def get_all_autores(self):
        """Obtiene todos los autores de la base de datos"""
        query = """
        SELECT id, nombre, apellido, telefono, nacionalidad 
        FROM autores
        ORDER BY nombre, apellido
        """
        return self.db.fetch_query(query)

    def find_autor_by_id(self, autor_id):
        """Busca un autor por su ID"""
        return self._get_autor_by_field("id", autor_id)

    def find_autor_by_telefono(self, telefono):
        """Busca un autor por su teléfono"""
        return self._get_autor_by_field("telefono", telefono)

    def create_autor(self, autor):
        """Crea un nuevo autor en la base de datos"""
        if self.find_autor_by_telefono(autor.telefono):
            raise ValueError(f"Ya existe un autor con el teléfono {autor.telefono}")

        query = """
        INSERT INTO autores (nombre, apellido, telefono, nacionalidad)
        VALUES (?, ?, ?, ?)
        """
        params = (autor.nombre, autor.apellido, autor.telefono, autor.nacionalidad)
        self.db.execute_query(query, params)
        return self.db.cursor.lastrowid

    def update_autor(self, autor_id, autor_data):
        """Actualiza un autor existente"""
        query = """
        UPDATE autores 
        SET nombre=?, apellido=?, telefono=?, nacionalidad=?
        WHERE id=?
        """
        params = (
            autor_data['nombre'],
            autor_data['apellido'],
            autor_data['telefono'],
            autor_data['nacionalidad'],
            autor_id
        )
        self.db.execute_query(query, params)

    def delete_autor(self, autor_id):
        """Elimina un autor por su ID"""
        query = "DELETE FROM autores WHERE id=?"
        self.db.execute_query(query, (autor_id,))