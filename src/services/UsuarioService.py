from data.Database import DatabaseSingleton
from classes.Usuario import Usuario, Estudiante, Profesor

class UsuarioService:
    def __init__(self, db):
        self.db = db

    def get_all_usuarios(self):
        """Obtiene todos los usuarios de la base de datos ordenados por nombre"""
        query = """
        SELECT id, nombre, apellido, tipo_usuario, direccion, telefono 
        FROM usuarios
        ORDER BY nombre, apellido
        """
        return self.db.fetch_query(query)

    def find_usuario_by_id(self, usuario_id):
        """Busca un usuario por su ID"""
        query = """
        SELECT id, nombre, apellido, tipo_usuario, direccion, telefono 
        FROM usuarios 
        WHERE id = ?
        """
        return self.db.fetch_query(query, (usuario_id,), single=True)

    def find_usuario_by_telefono(self, telefono):
        """Busca un usuario por su teléfono"""
        query = """
        SELECT id, nombre, apellido, tipo_usuario, direccion, telefono 
        FROM usuarios 
        WHERE telefono = ?
        """
        return self.db.fetch_query(query, (telefono,), single=True)

    def get_tipo_usuario(self, usuario: Usuario):
        """Detecta el tipo de usuario"""
        if isinstance(usuario, Estudiante):
            return 'estudiante'
        elif isinstance(usuario, Profesor):
            return 'profesor'
        else:
            raise ValueError("El tipo de usuario no es válido")

    def tiene_prestamos_disponibles(self, usuario: Usuario):
        """Verifica si el usuario tiene préstamos disponibles"""
        tipo_usuario = self.get_tipo_usuario(usuario)
        
        query = """
        SELECT COUNT(*) 
        FROM prestamos P 
        JOIN usuarios U ON (P.id_usuario = U.id) 
        WHERE U.tipo_usuario = ? AND P.fecha_devolucion_real IS NULL       
        """
        parameters = (tipo_usuario,)
        cant_prestamos = self.db.fetch_query(query, parameters, single=True)[0]

        limite_prestamos = 5 if tipo_usuario == 'profesor' else 3
        return cant_prestamos < limite_prestamos

    def registrar_usuario(self, usuario: Usuario):
        """Registra un nuevo usuario en la base de datos"""
        # Verificar si ya existe un usuario con ese teléfono
        if self.find_usuario_by_telefono(usuario.telefono):
            raise ValueError(f"Ya existe un usuario con el teléfono {usuario.telefono}")

        tipo_usuario = self.get_tipo_usuario(usuario)

        query = """
        INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            usuario.nombre,
            usuario.apellido,
            tipo_usuario,
            usuario.direccion,
            usuario.telefono
        )
        
        try:
            self.db.execute_query(query, params)
            usuario.id = self.db.cursor.lastrowid
            return usuario.id
        except Exception as e:
            raise Exception(f"Error al registrar usuario: {str(e)}")

    def actualizar_usuario(self, usuario_id: int, datos_usuario: dict):
        """Actualiza los datos de un usuario existente"""
        # Verificar si el usuario existe
        if not self.find_usuario_by_id(usuario_id):
            raise ValueError(f"No existe un usuario con el ID {usuario_id}")

        # Verificar si el nuevo teléfono ya existe en otro usuario
        usuario_existente = self.find_usuario_by_telefono(datos_usuario['telefono'])
        if usuario_existente and usuario_existente[0] != usuario_id:
            raise ValueError(f"Ya existe otro usuario con el teléfono {datos_usuario['telefono']}")

        query = """
        UPDATE usuarios 
        SET nombre=?, apellido=?, tipo_usuario=?, direccion=?, telefono=?
        WHERE id=?
        """
        params = (
            datos_usuario['nombre'],
            datos_usuario['apellido'],
            datos_usuario['tipo_usuario'],
            datos_usuario['direccion'],
            datos_usuario['telefono'],
            usuario_id
        )
        
        try:
            self.db.execute_query(query, params)
        except Exception as e:
            raise Exception(f"Error al actualizar usuario: {str(e)}")

    def eliminar_usuario(self, usuario_id: int):
        """Elimina un usuario por su ID"""
        # Verificar si el usuario existe
        if not self.find_usuario_by_id(usuario_id):
            raise ValueError(f"No existe un usuario con el ID {usuario_id}")

        # Verificar si el usuario tiene préstamos activos
        query_prestamos = """
        SELECT COUNT(*) 
        FROM prestamos 
        WHERE id_usuario = ? AND fecha_devolucion_real IS NULL
        """
        prestamos_activos = self.db.fetch_query(query_prestamos, (usuario_id,), single=True)[0]
        
        if prestamos_activos > 0:
            raise ValueError("No se puede eliminar el usuario porque tiene préstamos activos")

        query = "DELETE FROM usuarios WHERE id=?"
        try:
            self.db.execute_query(query, (usuario_id,))
        except Exception as e:
            raise Exception(f"Error al eliminar usuario: {str(e)}")

    def crear_usuario_desde_datos(self, datos: dict):
        """Crea una instancia de Usuario (Estudiante o Profesor) a partir de un diccionario de datos"""
        clase_usuario = Estudiante if datos['tipo_usuario'] == 'estudiante' else Profesor
        return clase_usuario(
            nombre=datos['nombre'],
            apellido=datos['apellido'],
            direccion=datos['direccion'],
            telefono=datos['telefono']
        )