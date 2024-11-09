from classes.Libro import Libro
from services.AutorService import *

class LibroService:

    #Instancia de la BD
    def __init__(self, db):
        self.db = db

    #Buscar libro por codigo isbn:
    def findLibroByIsdn(self, libro: Libro):
        query = """
        SELECT * FROM libros L WHERE L.isbn = ?
        """
        paramsLibro = (libro.code_isbn,)
        return self.db.fetch_query(query, paramsLibro, single=True)
    
    #Consultar la disponibilidad de un libro
    def consultarDispinibilidadLibro(self, libro: Libro):
        print("--------CONSULTA DE DISPONIBILIDAD-------------")
        
        query = """
            SELECT COUNT(*) FROM libros L JOIN prestamos P ON L.isbn = P.isbn_libro WHERE L.isbn = ?
            """
        params = (libro.code_isbn,)
        cantPrestamosLibro= self.db.fetch_query(query, params, single=True)
        
        if(cantPrestamosLibro is None):
            print(f"El libro {libro.titulo} esta disponible - Posee una disponibilidad de: {str(libro.cant_disponible)} unidades")
            return True
        elif(cantPrestamosLibro[0] < libro.cant_disponible):
            print(f"El libro {libro.titulo} esta disponible - Posee una disponibilidad de: {str(libro.cant_disponible - cantPrestamosLibro[0])} unidades")
            return True
        else:
            print(f"El libro {libro.titulo} no se encuentra disponible")
            return False

        
    #REGISTRO DE UN NUEVO LIBRO
    def registrar_libro(self, libro: Libro):
        print("--------REGISTRO DE LIBRO-------------")

        #Instancias de servicios
        autor_service = AutorService(self.db)

        #Verificar que el libro no está ingresado en la BD
        libroEncontrado = self.findLibroByIsdn(libro)


        if(not libroEncontrado):
            print(f"El libro {libro.titulo} con codigo isbn {libro.code_isbn} NO SE ENCUENTRA REGISTRADO en la base de datos")
            
            #Buscar al autor asociado al libro en la BD
            autorEncontrado = autor_service.findAutorById(libro.autor)
            
            if(autorEncontrado):
                print("Autor encontrado con exito")

                if(libro.anio_publicacion <= 2024 and libro.cant_disponible > 0):
                    print(f"El anio de publicacion del libro es: {libro.anio_publicacion} y se registra con: {libro.cant_disponible} ejemplares - Se procede al registro del libro")
                    #Insertar el libro en la base de datos
                    query = """
                    INSERT INTO libros (isbn, titulo, genero, ano_publicacion, id_autor, cantidad_disponible)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    params = (libro.code_isbn, libro.titulo, libro.genero, libro.anio_publicacion, libro.autor.id, libro.cant_disponible)
                    
                    try:
                    # Ejecuta la consulta y realiza el commit
                        self.db.execute_query(query, params)
                        print(f"-----Libro registrado con exito-----")
                        
                    except Exception as e:
                        print(f"Error al registrar libro: {e}")
                else: print(f" ERROR - El año de publicacion ingresado del libro es: {libro.anio_publicacion} y se registra con: {libro.cant_disponible} ejemplares")
            else:
                print("No se encontro el autor.")
        else:
            print("El libro ya se encuentra registrado en la base de datos")
            print(f"Se encontro el libro: {libroEncontrado}")