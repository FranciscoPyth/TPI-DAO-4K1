from data.Database import DatabaseSingleton
from classes.Usuario import Usuario, Estudiante, Profesor

class UsuarioService:

    #Instancia de la BD
    def __init__(self, db):
        self.db = db

    #Buscar usuario segun su ID
    def findUsuarioById(self, usuario: Usuario):
        query= """
        SELECT U.id FROM usuarios U WHERE U.id = ?
        """
        params = (usuario.id,)
        return self.db.fetch_query(query, params, single=True)

    
    #Buscar usuario segun su Teléfono
    def findUsuarioByDni(self, usuario: Usuario):
        query = """
        SELECT * FROM usuarios U WHERE U.telefono = ?
        """
        params = (usuario.telefono,)
        return self.db.fetch_query(query, params, single=True)
    

    #Detectar el tipo de usuario
    def getTipoUsuario(self, usuario: Usuario):
        if isinstance(usuario, Estudiante):
            return 'estudiante'
        elif isinstance(usuario, Profesor):
            return 'profesor'
        else:
            raise ValueError("El tipo de usuario no es valido")
        
    
    #Verificar si el usuario tiene prestamos disponbles
    def tienePrestamosUsuario(self, usuario : Usuario):
        print("--------CONSULTA DE DISPONIBILIDAD DE PRESTAMOS-------------")
        
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

        
    #REGISTRO DE UN NUEVO USUARIO
    def registrar_usuario(self, usuario: Usuario):
        print("--------REGISTRO DE USUARIO-------------")

        #Revisamos si el usuario que se intenta agregar a la BD ya está ingresado
        usuarioEncontrado = self.findUsuarioByDni(usuario)

        if(not usuarioEncontrado):
            print(f"El usuario {usuario.nombre} con telefono: {usuario.telefono} NO SE ENCUENTRA en la base de datos - se porcede a su registro")

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
                print(f"-----{tipo_usuario.capitalize()} registrado con exito-----")
                
            except Exception as e:
                print(f"Error al registrar usuario: {e}")
        else:
            print(f"El usuario con Telefono: {usuario.telefono} ya se encuentra en la BD")