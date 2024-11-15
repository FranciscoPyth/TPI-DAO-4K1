from classes.Libro import Libro

class LibroService:
    def __init__(self, db):
        self.db = db

    def get_all_libros(self):
        """Obtiene todos los libros de la base de datos"""
        query = """
        SELECT isbn, titulo, genero, ano_publicacion, id_autor, cantidad_disponible 
        FROM libros
        ORDER BY titulo
        """
        return self.db.fetch_query(query)

    def findLibroByIsdn(self, libro: Libro):
        """Busca un libro por su ISBN"""
        query = "SELECT * FROM libros WHERE isbn = ?"
        return self.db.fetch_query(query, (libro.code_isbn,), single=True)

    def registrar_libro(self, libro: Libro):
        """Registra un nuevo libro en la base de datos"""
        if self.findLibroByIsdn(libro):
            raise ValueError(f"Ya existe un libro con el ISBN {libro.code_isbn}")

        if libro.anio_publicacion > 2024 or libro.cant_disponible <= 0:
            raise ValueError("Año de publicación inválido o cantidad disponible debe ser mayor a 0")

        query = """
        INSERT INTO libros (isbn, titulo, genero, ano_publicacion, id_autor, cantidad_disponible)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (libro.code_isbn, libro.titulo, libro.genero, libro.anio_publicacion, 
                 libro.autor, libro.cant_disponible)
        self.db.execute_query(query, params)

    def update_libro(self, isbn, libro_data):
        """Actualiza un libro existente"""
        query = """
        UPDATE libros 
        SET titulo=?, genero=?, ano_publicacion=?, id_autor=?, cantidad_disponible=?
        WHERE isbn=?
        """
        params = (
            libro_data['titulo'],
            libro_data['genero'],
            libro_data['ano_publicacion'],
            libro_data['id_autor'],
            libro_data['cantidad_disponible'],
            isbn
        )
        self.db.execute_query(query, params)

    def delete_libro(self, isbn):
        """Elimina un libro por su ISBN"""
        query = "DELETE FROM libros WHERE isbn=?"
        self.db.execute_query(query, (isbn,))

    def consultarDispinibilidadLibro(self, libro: Libro):
        """Consulta la disponibilidad de un libro"""
        query = """
        SELECT COUNT(*) FROM libros L 
        JOIN prestamos P ON L.isbn = P.isbn_libro 
        WHERE L.isbn = ? AND P.fecha_devolucion_real IS NULL
        """
        params = (libro.code_isbn,)
        cantPrestamosLibro = self.db.fetch_query(query, params, single=True)
        
        if cantPrestamosLibro is None:
            return True
        elif cantPrestamosLibro[0] < libro.cant_disponible:
            return True
        return False