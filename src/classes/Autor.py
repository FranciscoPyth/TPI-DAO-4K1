class Autor():
    def __init__(self, identificador, nombre, apellido, nacionalidad) -> None:
        self.id = identificador # No pongo ID porque es una palabra reservada de Python 
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad
        