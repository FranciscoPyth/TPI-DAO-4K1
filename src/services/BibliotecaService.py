# BibliotecaService.py
from data.Database import DatabaseSingleton
from classes.Autor import Autor
from classes.Libro import Libro
from classes.Usuario import Usuario, Estudiante, Profesor
from classes.Prestamo import Prestamo

class BibliotecaService:
    def __init__(self):
        self.db = DatabaseSingleton()

    #REGISTRO DE UN NUEVO AUTOR
    


    #REGISTRO DE UN NUEVO USUARIO
    # Detectamos el tipo de usuario en base a la clase
    def getTipoUsuario(self, usuario: Usuario):
        if isinstance(usuario, Estudiante):
            return 'estudiante'
        elif isinstance(usuario, Profesor):
            return 'profesor'
        else:
            raise ValueError("El tipo de usuario no es valido.")

    def registrar_usuario(self, usuario: Usuario):
        print("--------REGISTRO DE USUARIO-------------")
        # Detectamos el tipo de usuario en base a la clase
        tipo_usuario = self.getTipoUsuario(usuario)
        query = """
        INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (usuario.nombre, usuario.apellido, tipo_usuario, usuario.direccion, usuario.telefono)
        
        try:
            # Ejecuta la consulta y realiza el commit
            self.db.execute_query(query, params)
            
            # Obtiene el id generado por SQLite y lo asigna al objeto Usuario
            usuario.id = self.db.cursor.lastrowid
            print(f"-----{tipo_usuario.capitalize()} registrado con exito.-----")
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")

    
    #REGISTRO DE UN NUEVO PRÉSTAMO
    def registrar_prestamo(self, prestamo: Prestamo):
        print("--------REGISTRO DE PRESTAMO-------------")

        #Verificar que el usuario asociado al préstamo exista en la BD
        query= """
        SELECT U.id FROM usuarios U WHERE U.id = ?
        """
        parametersUsuario = (prestamo.usuario.id,)
        usuarioPrestamo = self.db.fetch_query(query, parametersUsuario, single=True)


        #Verificar que el libro asociado al préstamo exista en la BD
        query= """
        SELECT L.isbn FROM libros L WHERE L.isbn = ?
        """
        parametersLibro = (prestamo.libro.code_isbn,)
        libroPrestamo = self.db.fetch_query(query, parametersLibro, single=True)

        #Verificar que el libro asociado al préstamo esté disponible, que el usuario esté reg y que el libro también lo esté
        if(usuarioPrestamo is not None and libroPrestamo is not None and self.consultarDispinibilidadLibro(prestamo.libro) and self.consultarPrestamosUsuario(prestamo.usuario)):
            
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
                print(f"-----Prestamo registrado con exito.-----")
            
            except Exception as e:
                print(f"Error al registrar prestamo: {e}")
        else:
            print(f"No se pudo registrar el prestamo del libro {str(prestamo.libro.titulo)}")
        
    #CONSULTAR LA DISPONIBILIDAD DE UN LIBRO
    def consultarDispinibilidadLibro(self, libro: Libro):
        print("--------CONSULTA DE DISPONIBILIDAD-------------")
        query = """
            SELECT COUNT(*) FROM libros L JOIN prestamos P ON L.isbn = P.isbn_libro WHERE L.isbn = ?
            """
        parameters = (libro.code_isbn,)
        cantPrestamosLibro= self.db.fetch_query(query, parameters, single=True)
        if(cantPrestamosLibro is None):
            print(f"El libro {libro.titulo} esta disponible - Posee una disponibilidad de: {str(libro.cant_disponible)} unidades")
            return True
        elif(cantPrestamosLibro[0] < libro.cant_disponible):
            print(f"El libro {libro.titulo} esta disponible - Posee una disponibilidad de: {str(libro.cant_disponible - cantPrestamosLibro[0])} unidades")
            return True
        else:
            print(f"El libro {libro.titulo} no se encuentra disponible.")
            return False
        
    #CONSULTAR CANTIDAD DE PRESTAMOS DE USUARIOS
    def consultarPrestamosUsuario(self, usuario : Usuario):
        tipo_usuario = self.getTipoUsuario(usuario)
        query = """
        SELECT COUNT(*) FROM prestamos P JOIN usuarios U ON (P.id_usuario = U.id) WHERE U.tipo_usuario = ?       
        """
        parameters = (tipo_usuario,)
        cantPrestamosUsuario = self.db.fetch_query(query, parameters, single=True)

        if(tipo_usuario == 'estudiante' and (cantPrestamosUsuario[0] >= 3 )):
            print("[ESTUDIANTE] - Se pasa de los 3 prestamos para estudiante")
            return False
        elif(tipo_usuario == 'profesor' and (cantPrestamosUsuario[0] >= 5 )):
            print("[PROFESOR] - Se pasA de los 5 prestamos para profesor")
            return False
        elif(tipo_usuario == 'estudiante'):
            print("[ESTUDIANTE] - Tiene prestamos disponibles")
            return True
        elif(tipo_usuario == 'profesor'):
            print("[PROFESOR] - Tiene prestamos disponibles")
            return True
