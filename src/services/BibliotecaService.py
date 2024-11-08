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
    def registrar_autor(self, autor: Autor):
        print("--------REGISTRO DE AUTOR-------------")
        # Primero verificamos si el autor ya existe en la base de datos
        check_query = """
        SELECT COUNT(*) FROM autores
        WHERE nombre = ? AND apellido = ? AND nacionalidad = ?
        """
        check_params = (autor.nombre, autor.apellido, autor.nacionalidad)
        result = self.db.execute_query(check_query, check_params)

        # Si el autor ya existe, no lo insertamos y mostramos un mensaje
        if result[0][0] > 0:  # Si el conteo es mayor a 0, ya existe un autor con estos datos
            print("El autor ya está registrado.")
        else:
            # Si no existe, procedemos a insertarlo
            query = """
            INSERT INTO autores (nombre, apellido, nacionalidad)
            VALUES (?, ?, ?)
            """
            params = (autor.nombre, autor.apellido, autor.nacionalidad)
            
            try:
            # Ejecuta la consulta y realiza el commit
                self.db.execute_query(query, params)

                # Obtiene el id generado por SQLite y lo asigna al objeto Autor
                autor.id = self.db.cursor.lastrowid
                print(f"-----Autor registrado con exito.-----")
                
            except Exception as e:
                print(f"Error al registrar autor: {e}")


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
        params = (usuario.nombre, usuario.apellido, usuario.tipo_usuario, usuario.direccion, usuario.telefono)
        
        try:
            # Ejecuta la consulta y realiza el commit
            self.db.execute_query(query, params)
            
            # Obtiene el id generado por SQLite y lo asigna al objeto Usuario
            usuario.id = self.db.cursor.lastrowid
            print(f"-----{tipo_usuario.capitalize()} registrado con exito.-----")
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")

    
    #REGISTRO DE UN NUEVO LIBRO
    def registrar_libro(self, libro: Libro):
        print("--------REGISTRO DE LIBRO-------------")
        #Verificar que el libro que se quiere guardar no está ingresado en la base de datos (Osea que no exista un libro con el mismo cod_isbn)
        query = """
        SELECT * FROM libros L WHERE L.isbn = ?
        """
        paramsLibro = (libro.code_isbn,)
        libroEncontrado = self.db.fetch_query(query, paramsLibro, single=True)
        
        if(not libroEncontrado):
            print(f"El libro con codigo isbn {paramsLibro} NO SE ENCUENTRA REGISTRADO en la base de datos")
            
            #Buscar al autor asociado al libro (ingresado por parámetro en el main) en la base de datos
            query = """
            SELECT * FROM autores A WHERE A.id = ?
            """ 
            paramsAutor = (libro.autor.id,)
            autorEncontrado = self.db.fetch_query(query, paramsAutor, single=True)
            print(f"Se encontro el autor con id: {paramsAutor[0]}, {autorEncontrado}")
            
            if(autorEncontrado):
                print("Autor encontrado con exito - se procede al registro del libro.")

                #Insertar el libro en la base de datos
                query = """
                INSERT INTO libros (isbn, titulo, genero, ano_publicacion, id_autor, cantidad_disponible)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                params = (libro.code_isbn, libro.titulo, libro.genero, libro.anio_publicacion, libro.autor.id, libro.cant_disponible)
                try:
                # Ejecuta la consulta y realiza el commit
                    self.db.execute_query(query, params)
                    print(f"-----Libro registrado con exito.-----")
                    
                except Exception as e:
                    print(f"Error al registrar libro: {e}")
            else:
                print("No se encontro el autor.")
        else:
            print("El libro ya se encuentra registrado en la base de datos")
            print(f"Se encontro el libro con id: {paramsLibro[0]}, {libroEncontrado}")
    
    
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
