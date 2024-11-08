class Usuario:
    def __init__(self, nombre, apellido, tipo_usuario, direccion, telefono):
        if tipo_usuario not in ["Profesor", "Estudiante"]:
            raise ValueError("El tipo de usuario no es válido. Debe ser 'Profesor' o 'Estudiante'.")
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.direccion = direccion
        self.telefono = telefono

class Estudiante(Usuario):
    def __init__(self, nombre, apellido, direccion, telefono):
        super().__init__(nombre, apellido, direccion, telefono, tipo_usuario="Estudiante")

class Profesor(Usuario):
    def __init__(self, nombre, apellido, direccion, telefono):
        super().__init__(nombre, apellido, direccion, telefono, tipo_usuario="Profesor")
