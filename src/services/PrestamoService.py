from classes.Prestamo import Prestamo
from services.UsuarioService import *
from services.AutorService import *
from services.LibroService import *


class PrestamoService:

    #Instancia de la BD
    def __init__(self, db):
        self.db = db

    #buscar Prestamo en la BD por ID
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
        usuarioPrestamo = usuario_service.findUsuarioById(prestamo.usuario)


        #Verificar que el libro asociado al préstamo exista en la BD
        libroPrestamo = libro_service .findLibroByIsdn(prestamo.libro)


        #Verificar si el libro tiene ejemplares disponibles
        estaDisponible = libro_service .consultarDispinibilidadLibro(prestamo.libro)

        #verificar si el usuario tiene prestamos disponibles
        tienePrestamos = usuario_service.tienePrestamosUsuario(prestamo.usuario)

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



    #DEVOLUCION DE UN PRESTAMO
    def registrar_devolucion(self, prestamo: Prestamo, fechaDevolucionReal):

        #Verificar que el prestamo existe en la bd
        prestamoEncontrado = self.findPrestamoById(prestamo)

        #Verificar que el prestamo aun no fue devuelto
        if(prestamo.fecha_devolucion_real == None and prestamoEncontrado is not None):

            prestamo.setFechaDevolucionReal(fechaDevolucionReal)
            query = """
            UPDATE prestamos
            SET fecha_devolucion_real = ?
            WHERE id = ?
            """
            params = (fechaDevolucionReal, prestamo.id)
            self.db.execute_query(query, params)
                    
            print(f"Se devolvio el libro {prestamo.libro.titulo} cuyo prestamo tiene el id: {prestamo.id}")
        else: print("No se puedo realizar la devolucion del prestamo")