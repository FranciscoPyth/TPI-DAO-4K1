from data.Database import DatabaseSingleton
from services.BibliotecaService import BibliotecaService
from classes.Usuario import *
from windows.LibraryApp import LibraryApp

def initializer_db():
    db = DatabaseSingleton()

    # Lista de consultas separadas
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
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
            fecha_devolucion DATE,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (isbn_libro) REFERENCES libros(isbn) ON DELETE CASCADE
        );
        """
    ]

    # Ejecutar cada consulta individualmente
    for query in create_table_queries:
        try:
            db.execute_query(query)
            print("Tabla creada exitosamente")
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")


def main():
    initializer_db()    

    app = LibraryApp()
    app.mainloop()

if "__main__" == __name__:
    main()