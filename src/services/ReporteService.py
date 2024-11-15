import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class ReporteService:
    def __init__(self, db):
        self.db = db


    def listar_prestamos_vencidos(self):
        """
        Genera un reporte en PDF de los préstamos vencidos con tabla y gráfico.
        """
        query = """
        SELECT libros.titulo, prestamos.fecha_devolucion
        FROM prestamos
        JOIN libros ON prestamos.isbn_libro = libros.isbn
        WHERE prestamos.fecha_devolucion < CURRENT_TIMESTAMP
        AND prestamos.fecha_devolucion_real IS NULL
        """
        
        try:
            prestamos_vencidos = self.db.execute_query(query)
            if prestamos_vencidos is None:
                raise ValueError("La consulta no devolvió resultados.")
            
            # Crear el gráfico de los préstamos vencidos
            libros = [prestamo[0] for prestamo in prestamos_vencidos]
            fechas = [prestamo[1] for prestamo in prestamos_vencidos]
            
            plt.figure(figsize=(8, 6))
            plt.barh(libros, [datetime.strptime(fecha, "%Y-%m-%d").date() for fecha in fechas], color='red')
            plt.xlabel('Fecha de Devolución')
            plt.ylabel('Libros')
            plt.title('Préstamos Vencidos')
            plt.tight_layout()
            
            # Guardar el gráfico como archivo PNG
            plt.savefig('prestamos_vencidos.png')
            plt.close()

            # Crear el PDF
            pdf_filename = 'reporte_prestamos_vencidos.pdf'
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 10)

            # Título del reporte
            c.drawString(200, 770, "Reporte de Préstamos Vencidos")

            # Crear la tabla con líneas
            c.setFont("Helvetica-Bold", 10)
            c.drawString(100, 720, "Libro")
            c.drawString(400, 720, "Fecha de Devolución")
            
            c.setFont("Helvetica", 10)
            
            # Dibujar las líneas horizontales y verticales para la tabla
            y_position = 700
            line_height = 15
            for i, prestamo in enumerate(prestamos_vencidos):
                # Dibujar contenido de las celdas
                c.drawString(100, y_position, prestamo[0])
                c.drawString(400, y_position, prestamo[1])
                
                # Línea horizontal
                c.line(90, y_position - 5, 500, y_position - 5)
                y_position -= line_height
            
            # Última línea horizontal después de la tabla
            c.line(90, y_position - 5, 500, y_position - 5)

            # Calcular el espacio dinámico entre la tabla y el gráfico
            # Si la tabla tiene muchas filas, ajustamos el espacio
            espacio_entre_tabla_y_grafico = 50 + (len(prestamos_vencidos) * line_height)
            y_position -= espacio_entre_tabla_y_grafico

            # Incluir el gráfico de préstamos vencidos en el PDF
            c.drawImage('prestamos_vencidos.png', 100, y_position, width=400, height=200)

            # Guardar el PDF
            c.save()
            
            # Abrir el PDF generado
            self.abrir_pdf(pdf_filename)

        except Exception as e:
            print(f"Error al listar préstamos vencidos: {e}")


    def libros_mas_prestados(self):
        """
        Genera un reporte de los libros más prestados durante el último mes, con gráfico.
        """
        fecha_limite = datetime.now() - timedelta(days=30)
        print(fecha_limite)
        query = f"""
        SELECT libros.titulo, COUNT(prestamos.isbn_libro) AS cantidad_prestamos
        FROM prestamos
        JOIN libros ON prestamos.isbn_libro = libros.isbn
        WHERE prestamos.fecha_prestamo > '{fecha_limite.strftime('%Y-%m-%d')}'
        GROUP BY libros.titulo
        ORDER BY cantidad_prestamos DESC
        """
        
        try:
            libros_mas_prestados = self.db.execute_query(query)
            if libros_mas_prestados is None:
                raise ValueError("La consulta no devolvió resultados.")
            
            # Crear el gráfico de los libros más prestados
            libros = [libro[0] for libro in libros_mas_prestados]
            cantidad = [libro[1] for libro in libros_mas_prestados]
            
            # Cambiar x por y en el gráfico: cantidad en el eje vertical (y) y libros en el eje horizontal (x)
            plt.figure(figsize=(8, 6))
            plt.bar(libros, cantidad, color='blue')  # Usamos plt.bar en lugar de plt.barh
            plt.ylabel('Cantidad de Préstamos')     # Etiqueta para el eje y
            plt.xlabel('Libros')                    # Etiqueta para el eje x
            plt.title('Libros Más Prestados del Último Mes')
            plt.xticks(rotation=45, ha='right')     # Rotar los títulos de los libros para que no se solapen
            plt.tight_layout()
            
            # Guardar el gráfico como archivo PNG
            plt.savefig('libros_mas_prestados.png')
            plt.close()

            # Crear el PDF
            pdf_filename = 'reporte_libros_mas_prestados.pdf'
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 10)

            # Título del reporte
            c.drawString(200, 750, "Reporte de Libros Más Prestados del Último Mes")

            # Agregar el gráfico de libros más prestados
            c.drawImage('libros_mas_prestados.png', 100, 400, width=400, height=200)

            # Guardar el PDF
            c.save()
            
            # Abrir el PDF generado
            self.abrir_pdf(pdf_filename)

        except Exception as e:
            print(f"Error al listar libros más prestados: {e}")


    def usuarios_mas_activos(self):
        """
        Genera un reporte de los usuarios más activos, con gráfico.
        """
        query = """
        SELECT usuarios.nombre || ' ' || usuarios.apellido AS nombre_completo, COUNT(prestamos.id_usuario) AS cantidad_prestamos
        FROM prestamos
        JOIN usuarios ON prestamos.id_usuario = usuarios.id
        GROUP BY nombre_completo
        ORDER BY cantidad_prestamos DESC
        """
        
        try:
            usuarios_mas_activos = self.db.execute_query(query)
            if usuarios_mas_activos is None:
                raise ValueError("La consulta no devolvió resultados.")
            
            # Crear el gráfico de los usuarios más activos
            usuarios = [usuario[0] for usuario in usuarios_mas_activos]
            cantidad = [usuario[1] for usuario in usuarios_mas_activos]
            
            plt.figure(figsize=(8, 6))
            plt.barh(usuarios, cantidad, color='green')
            plt.xlabel('Cantidad de Préstamos')
            plt.ylabel('Usuarios')
            plt.title('Usuarios Más Activos')
            plt.tight_layout()
            
            # Guardar el gráfico como archivo PNG
            plt.savefig('usuarios_mas_activos.png')
            plt.close()

            # Crear el PDF
            pdf_filename = 'reporte_usuarios_mas_activos.pdf'
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 10)

            # Título del reporte
            c.drawString(200, 750, "Reporte de Usuarios Más Activos")

            # Agregar el gráfico de usuarios más activos
            c.drawImage('usuarios_mas_activos.png', 100, 400, width=400, height=200)

            # Guardar el PDF
            c.save()
            
            # Abrir el PDF generado
            self.abrir_pdf(pdf_filename)

        except Exception as e:
            print(f"Error al listar usuarios más activos: {e}")

    def abrir_pdf(self, filename):
        """
        Abre automáticamente el archivo PDF generado.
        """
        if os.name == 'nt':  # Para Windows
            os.startfile(filename)
