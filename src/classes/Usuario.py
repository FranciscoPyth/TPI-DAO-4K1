class Usuario():
    def __init__(self, nombre, apellido, direccion, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono


class Estudiante(Usuario):
    def __init__(self, nombre, apellido, direccion, telefono):
        super().__init__(nombre, apellido, direccion, telefono)

class Profesor(Usuario):
    def __init__(self, nombre, apellido, direccion, telefono):
        super().__init__(nombre, apellido, direccion, telefono)