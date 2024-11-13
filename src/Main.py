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

    # Importación de los servicios
    usuario_service = UsuarioService(db)
    autor_service = AutorService(db)
    libro_service = LibroService(db)
    prestamo_service = PrestamoService(db)
    
    # Registro de un nuevo estudiante
    nuevo_estudiante = Estudiante(nombre="Juan", apellido="Pérez", direccion="Calle Falsa 123", telefono="123456789")
    usuario_service.registrar_usuario(nuevo_estudiante)


    # Registro de un nuevo profesor
    nuevo_profesor = Profesor(nombre="Ana", apellido="Gómez", direccion="Calle Real 456", telefono="987654321")
    usuario_service.registrar_usuario(nuevo_profesor)

    # Usuario que no se registra
    nuevo_usuario = Estudiante(nombre="Martina", apellido="Pérez", direccion="Calle Falsa 123", telefono="123456789")
    
    # Registro de un nuevo autor
    nuevo_autor = Autor(nombre="Agatha", apellido="Christie", telefono="35144444", nacionalidad="Reino Unido")
    autor_service.registrar_autor(nuevo_autor)

    nuevo_autor2 =Autor(nombre="Jk", apellido="Rowling", telefono="351444455", nacionalidad="Reino Unido")
    autor_service.registrar_autor(nuevo_autor2)

    nuevo_autor3 = Autor(nombre="La autora", apellido="De los juegos del hambre", telefono="35144244", nacionalidad="Reino Unido") #Autor no guardado en la base de datos
    
    # Registro de un nuevo libro
    nuevo_libro = Libro(code_isbn="1A", titulo="Muerte en el Nilo", genero="Policial", anio_publicacion=1990, autor = nuevo_autor, cant_disponible=100)
    libro_service.registrar_libro(nuevo_libro) #Libro nuevo OK

    nuevo_libro2 = Libro(code_isbn="1B", titulo="Las Manzanas", genero="Policial", anio_publicacion=1990, autor = nuevo_autor, cant_disponible=1)
    libro_service.registrar_libro(nuevo_libro2) #Libro nuevo con mismo autor

    nuevo_libro3 = Libro(code_isbn="1C", titulo="Harry Potter", genero="Ficción", anio_publicacion=1990, autor = nuevo_autor2, cant_disponible=100)
    libro_service.registrar_libro(nuevo_libro3) #Libro nuevo con otro autor

    nuevo_libro4 = Libro(code_isbn="1A", titulo="Muerte en el Nilo", genero="Policial", anio_publicacion=1990, autor = nuevo_autor, cant_disponible=100)
    libro_service.registrar_libro(nuevo_libro4) #Libro ya registrado en la BD - ERROR

    nuevo_libro5 = Libro(code_isbn="1D", titulo="Los juegos Del Hambre", genero="Ciencia Ficción", anio_publicacion=1990, autor = nuevo_autor3, cant_disponible=100)
    libro_service.registrar_libro(nuevo_libro5) #Libro cuyo autor no está en la BD - ERROR

    nuevo_libro6 = Libro(code_isbn="1F", titulo="Los juegos Del Hambre", genero="Ciencia Ficción", anio_publicacion=2020, autor = nuevo_autor, cant_disponible=0)
    libro_service.registrar_libro(nuevo_libro6)

    # Registro de un nuevo préstamo
    nuevo_prestamo = Prestamo(usuario=nuevo_profesor, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo) #Prestamo con usuario y libro reg en la BD OK

    
    nuevo_prestamo2 = Prestamo(usuario=nuevo_profesor, libro=nuevo_libro5, fecha_prestamo=date(2000, 10, 1), fecha_devolucion=(2000, 11, 1)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo2) #Prestamo con usuario reg y libro NO reg en la BD - ERROR

    nuevo_prestamo3 = Prestamo(usuario=nuevo_usuario, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 1), fecha_devolucion=(2000, 11, 1)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo3) #Prestamo con usuario NO reg y libro reg en la BD - ERROR
    
    nuevo_prestamo4 = Prestamo(usuario=nuevo_usuario, libro=nuevo_libro5, fecha_prestamo=date(2000, 10, 1), fecha_devolucion=(2000, 11, 1)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo4) #Prestamo con usuario NO reg y libro NO reg en la BD - ERROR

    nuevo_prestamo5 = nuevo_prestamo = Prestamo(usuario=nuevo_profesor, libro=nuevo_libro2, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo5) #Prestamo de un libro con 1 sola unidad - para testear disponibilidad OK

    
    # Consulta de disponibilidad de un libro
    libro_service.consultarDispinibilidadLibro(nuevo_libro) #Libro alquilado 1 vez con disponibilidad de 100
    libro_service.consultarDispinibilidadLibro(nuevo_libro3) #Libro no alquilado
    libro_service.consultarDispinibilidadLibro(nuevo_libro2) #Libro alquilado 1 vez con disponibilidad de 1

    nuevo_prestamo6 = nuevo_prestamo = Prestamo(usuario=nuevo_profesor, libro=nuevo_libro2, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(nuevo_prestamo6) #SEGUNDO prestamo de un libro con 1 sola unidad - para testear disponibilidad OK


    #Consulta de cantidad de préstamos para profesor y estudiantes
    #Crear los préstamos
    prestamo1 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo1)

    prestamo2 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo2)

    prestamo3 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo3)

    prestamo4 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo4)

    prestamo5 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo5)

    prestamo6 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    
    print("------------------------------------------------------------------------------------")
    #Consultas
    usuario_service.tienePrestamosUsuario(nuevo_estudiante)
    usuario_service.tienePrestamosUsuario(nuevo_profesor)

    #Consulta
    libro_service.consultarDispinibilidadLibro(nuevo_libro)

    #Registro de devoluciones
    prestamo_service.registrar_devolucion_de_prestamos(nuevo_libro, nuevo_estudiante, fechaDevolucionReal=date(2024,10,10))
    prestamo_service.registrar_devolucion_de_prestamos(nuevo_libro, nuevo_estudiante, fechaDevolucionReal=date(2024,10,10))
    
    libro_service.consultarDispinibilidadLibro(nuevo_libro)

    #Registrar prestamo
    prestamo7 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo7)
    prestamo8 = Prestamo(usuario=nuevo_estudiante, libro=nuevo_libro, fecha_prestamo=date(2000, 10, 10), fecha_devolucion=date(2000, 11, 10)) 
    prestamo_service.registrar_prestamo(prestamo8)

    prestamo_service.registrar_devolucion_de_prestamos(nuevo_libro, nuevo_estudiante, fechaDevolucionReal=date(2024, 10, 10))

 
    #app = LibraryApp(db)
    #app.mainloop()

if "__main__" == __name__:
    main()