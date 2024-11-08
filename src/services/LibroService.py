from classes.Libro import Libro


class LibroService:
    def __init__(self, db):
        self.db = db

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