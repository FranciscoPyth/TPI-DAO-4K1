from data.Database import DatabaseSingleton
from classes.BibliotecaService import BibliotecaService
from classes.Usuario import *

def initializer_db():
    db = DatabaseSingleton()

    # Lista de consultas separadas
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS autores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            nacionalidad VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
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
            id INT AUTO_INCREMENT PRIMARY KEY,
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
    print("Bienvenidos al TP DAO")
    initializer_db()

    biblioteca_service = BibliotecaService()

    # Registro de un nuevo estudiante
    nuevo_estudiante = Estudiante(id_usuario=1, nombre="Juan", apellido="Pérez", direccion="Calle Falsa 123", telefono="123456789")
    biblioteca_service.registrar_usuario(nuevo_estudiante)

    # Registro de un nuevo profesor
    nuevo_profesor = Profesor(id_usuario=2, nombre="Ana", apellido="Gómez", direccion="Calle Real 456", telefono="987654321")
    biblioteca_service.registrar_usuario(nuevo_profesor)


if "__main__" == __name__:
    main()