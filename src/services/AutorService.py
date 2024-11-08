from classes.Autor import Autor


class AutorService:
    def __init__(self, db):
        self.db = db

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

        
    def consultar_autores(self):
        query = "SELECT id, nombre, apellido, nacionalidad FROM autores"
        try:
            # Ejecutamos la consulta para obtener todos los autores
            results = self.db.execute_query(query)

            # Creamos una lista de objetos Autor a partir de los resultados
            autores = [Autor(nombre=row[1], apellido=row[2], nacionalidad=row[3]).get_nombre() for row in results]

            return autores

        except Exception as e:
            print(f"Error al consultar autores: {e}")
            return []