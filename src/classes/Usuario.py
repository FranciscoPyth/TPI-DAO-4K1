class Usuario():
    def __init__(self, id_usuario, nombre, apellido, direccion, telefono):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono


class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, apellido, direccion, telefono):
        super().__init__(id_usuario, nombre, apellido, direccion, telefono)

class Profesor(Usuario):
    def __init__(self, id_usuario, nombre, apellido, direccion, telefono):
        super().__init__(id_usuario, nombre, apellido, direccion, telefono)