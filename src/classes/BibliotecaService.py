# BibliotecaService.py
from data.Database import DatabaseSingleton
from classes.Autor import Autor
from classes.Libro import Libro
from classes.Usuario import Usuario, Estudiante, Profesor

class BibliotecaService:
    def __init__(self):
        self.db = DatabaseSingleton()

    def registrar_autor(self, autor: Autor):
        query = """
        INSERT INTO autores (nombre, apellido, nacionalidad)
        VALUES (?, ?, ?)
        """
        params = (autor.nombre, autor.apellido, autor.nacionalidad)
        self.db.execute_query(query, params)
        print("Autor registrado con éxito.")

    def registrar_libro(self, libro: Libro):
        query = """
        INSERT INTO libros (isbn, titulo, genero, ano_publicacion, id_autor, cantidad_disponible)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (libro.isbn, libro.titulo, libro.genero, libro.ano_publicacion, libro.id_autor, libro.cantidad_disponible)
        self.db.execute_query(query, params)
        print("Libro registrado con éxito.")

    def registrar_usuario(self, usuario: Usuario):
        # Detectamos el tipo de usuario en base a la clase
        if isinstance(usuario, Estudiante):
            tipo_usuario = 'estudiante'
        elif isinstance(usuario, Profesor):
            tipo_usuario = 'profesor'
        else:
            raise ValueError("El tipo de usuario no es válido.")

        query = """
        INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (usuario.nombre, usuario.apellido, tipo_usuario, usuario.direccion, usuario.telefono)
        self.db.execute_query(query, params)
        print(f"{tipo_usuario.capitalize()} registrado con éxito.")
