from classes.Prestamo import Prestamo
from services.UsuarioService import *
from services.AutorService import *
from services.LibroService import *


class PrestamoService:

    #Instancia de la BD
    def __init__(self, db):
        self.db = db

    #Buscar Prestamo en la BD por ID
    def findPrestamoById(self, prestamo: Prestamo):
        query= """
        SELECT P.id FROM prestamos P WHERE P.id = ?
        """
        params = (prestamo.id,)
        return self.db.fetch_query(query, params, single=True)
    

    #REGISTRO DE UN PRESTAMO
    def registrar_prestamo(self, prestamo: Prestamo):
        print("--------REGISTRO DE PRESTAMO-------------")

        #Instancias de servicios
        usuario_service = UsuarioService(self.db)
        libro_service = LibroService(self.db)

        #Verificar que el usuario asociado al préstamo exista en la BD
        usuarioPrestamo = usuario_service.find_usuario_by_id(prestamo.usuario)


        #Verificar que el libro asociado al préstamo exista en la BD
        libroPrestamo = libro_service.findLibroByIsdn(prestamo.libro)


        #Verificar si el libro tiene ejemplares disponibles
        estaDisponible = libro_service.consultarDispinibilidadLibro(prestamo.libro)

        #verificar si el usuario tiene prestamos disponibles
        tienePrestamos = usuario_service.tiene_prestamos_disponibles(prestamo.usuario)

        #Verificar que el libro asociado al préstamo esté disponible, que el usuario esté reg y que el libro también lo esté
        if(usuarioPrestamo is not None and libroPrestamo is not None and estaDisponible and tienePrestamos):
            query = """
            INSERT INTO prestamos (id_usuario, isbn_libro, fecha_prestamo, fecha_devolucion)
            VALUES (?, ?, ?, ?)
            """
            params = (prestamo.usuario.id, prestamo.libro.code_isbn, prestamo.fecha_prestamo, prestamo.fecha_devolucion)
            
            try:
            # Ejecuta la consulta y realiza el commit
                self.db.execute_query(query, params)
                
                # Obtiene el id generado por SQLite y lo asigna al objeto Usuario
                prestamo.id = self.db.cursor.lastrowid
                print(f"-----Prestamo registrado con exito-----")
            
            except Exception as e:
                print(f"Error al registrar prestamo: {e}")
        else:
            print(f"No se pudo registrar el prestamo del libro {str(prestamo.libro.titulo)}")


#-----------------------------------------------DEVOLUCION-----------------------------------------------------------------------------------------------
    #REGISTRAR DEVOLUCION DE UN PRESTAMO
    def registrar_devolucion_de_prestamos(self, libro: Libro, usuario: Usuario, fechaDevolucionReal):

        #Buscar los prestamos por libro y usuario
        prestamos = self.findPrestamoByLibroYUsuario(usuario.id, libro.code_isbn)
        if(len(prestamos) != 0):
            print("Se encontro el prestamo")
            
            #recorrer todos los prestamos que corresponen al libro y usuario (capaz un usuario alquila varias copias del mismo libro)
            for prestamo_data in prestamos:
                # Crear una instancia de Prestamo a partir de la tupla
                prestamo = Prestamo(
                    usuario=usuario,
                    libro=libro,
                    fecha_prestamo=prestamo_data[3],      # Ajusta el índice de acuerdo a la posición de fecha_prestamo en la tupla
                    fecha_devolucion=prestamo_data[4],    # Ajusta el índice de acuerdo a la posición de fecha_devolucion en la tupla
                    )
                prestamo.id = prestamo_data[0]  # Asigna el id desde la tupla
                self.registrar_devolucion(prestamo, fechaDevolucionReal) #registrar la devolucion
        else: print(f"No se puedieron encontrar prestamos del libro {libro.titulo} asociados al usuario {usuario.nombre}")

    
    #Buscar prestamo por libro y usuario
    def findPrestamoByLibroYUsuario(self, idUsuario, isbnLibro):
        query= """
        SELECT * FROM prestamos P WHERE P.id_usuario = ? AND P.isbn_libro = ? AND P.fecha_devolucion_real IS NULL
        """
        params = (idUsuario, isbnLibro)
        return self.db.fetch_query(query, params, single=False)


    #Registrar la devolución (setear la fecha de devolución)
    def registrar_devolucion(self, prestamo: Prestamo, fechaDevolucionReal):
        prestamo.setFechaDevolucionReal(fechaDevolucionReal)

        query = """
        UPDATE prestamos SET fecha_devolucion_real = ? WHERE id = ?
        """
        params = (fechaDevolucionReal, prestamo.id)

        try:
         
         self.db.execute_query(query, params)

        except Exception as e:
            print(f"Error al registrar la devolución: {e}")

                
        print(f"{prestamo.usuario.nombre} devolvio el libro {prestamo.libro.titulo} cuyo prestamo tiene el id: {prestamo.id}")

                    
    def get_all_prestamos(self):
        """Obtiene todos los préstamos registrados en la base de datos."""
        query = """
            SELECT p.id, u.nombre AS usuario, l.titulo AS libro, p.fecha_prestamo, p.fecha_devolucion
            FROM prestamos p
            JOIN usuarios u ON p.id_usuario = u.id
            JOIN libros l ON p.isbn_libro = l.isbn;
        """
        return self.db.fetch_query(query)
