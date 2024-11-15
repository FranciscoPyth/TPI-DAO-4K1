from data.Database import DatabaseSingleton
#from services.BibliotecaService import BibliotecaService
from classes.Usuario import *
from classes.Autor import *
from classes.Libro import *
from classes.Prestamo import *
from windows.LibraryApp import LibraryApp
from services.UsuarioService import UsuarioService
from services.AutorService import AutorService
from services.LibroService import LibroService
from services.PrestamoService import PrestamoService
from datetime import date

def initializer_db(db):
    # Lista de consultas separadas
    drop_table_queries = [
        "DROP TABLE IF EXISTS autores",
        "DROP TABLE IF EXISTS usuarios",
        "DROP TABLE IF EXISTS libros",
        "DROP TABLE IF EXISTS prestamos"
    ]

    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            telefono VARCHAR(100) NOT NULL,
            nacionalidad VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            tipo_usuario VARCHAR(50) CHECK (tipo_usuario IN ('estudiante', 'profesor')),
            direccion VARCHAR(255),
            telefono VARCHAR(15)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS libros (
            isbn VARCHAR(13) PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            genero VARCHAR(100),
            ano_publicacion INT,
            id_autor INT,
            cantidad_disponible INT DEFAULT 0,
            FOREIGN KEY (id_autor) REFERENCES autores(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INT,
            isbn_libro VARCHAR(13),
            fecha_prestamo DATE NOT NULL,
            fecha_devolucion DATE NOT NULL,
            fecha_devolucion_real DATE,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (isbn_libro) REFERENCES libros(isbn) ON DELETE CASCADE
        );
        """
    ]

    # Eliminar tablas si ya existen
    for query in drop_table_queries:
        try:
            db.execute_query(query)
            print("Tabla eliminada exitosamente")
        except Exception as e:
            print(f"Error al eliminar la tabla: {e}")


    # Ejecutar cada consulta individualmente
    for query in create_table_queries:
        try:
            db.execute_query(query)
            print("Tabla creada exitosamente")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")


def main():
    db = DatabaseSingleton()
    initializer_db(db) 
 
    app = LibraryApp(db)
    app.mainloop()

if "__main__" == __name__:
    main()