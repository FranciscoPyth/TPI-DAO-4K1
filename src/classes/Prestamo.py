class Prestamo():
    def __init__(self, usuario, libro, fecha_prestamo, fecha_devolucion):
        self.id = None
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.fecha_devolucion_real = None
    
    def setFechaDevolucionReal(self, fecha):
        self.fecha_devolucion_real = fecha