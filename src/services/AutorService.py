from classes.Autor import Autor
from data.Database import DatabaseSingleton


class AutorService():

    #Instancia de BD
    def __init__(self, db):
        self.db = db

    #Buscar autor por id - lo uso para registrar los libros
    def findAutorById(self, autor: Autor):
        query = """
        SELECT * FROM autores A WHERE A.id = ?
        """ 
        paramsAutor = (autor.id,)
        return self.db.fetch_query(query, paramsAutor, single=True)
        

    #Encontrar autores segun su telefono 
    def findAutorByTelefono(self, autor: Autor):
        query = """
            SELECT * FROM autores A WHERE A.telefono = ?
            """
        params = (autor.telefono,)
        return self.db.fetch_query(query, params, single=True)


    #REGISTRO DE UN NUEVO AUTOR
    def registrar_autor(self, autor: Autor):
        print("--------REGISTRO DE AUTOR-------------")

        # Primero verificamos si el autor ya existe en la base de datos
        autorEncontrado = self.findAutorByTelefono(autor)

        if(not autorEncontrado):
            print(f"El autor {autor.nombre} con telefono: {autor.telefono} NO SE ENCUENTRA en la BD - Se procede a su registro")
        
            query = """
            INSERT INTO autores (nombre, apellido, telefono, nacionalidad)
            VALUES (?, ?, ?, ?)
            """
            params = (autor.nombre, autor.apellido, autor.telefono, autor.nacionalidad)
            
            try:
            # Ejecuta la consulta y realiza el commit
                self.db.execute_query(query, params)

                 # Obtiene el id generado por SQLite y lo asigna al objeto Autor
                autor.id = self.db.cursor.lastrowid
                print(f"-----Autor registrado con exito.-----")
                
            except Exception as e:
                print(f"Error al registrar autor: {e}")
        else:
            print(f"El autor {autor.nombre} ya se encuentra en la BD")

        
    #CONSULTA DE AUTORES
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