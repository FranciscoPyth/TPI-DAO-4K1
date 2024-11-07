import sqlite3
from sqlite3 import Error

class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        try:
            self.connection = sqlite3.connect("biblioteca.db")
            self.cursor = self.connection.cursor()
            print("Conexión a SQLite establecida")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def test_connection(self):
        if not self.connection:
            self._initialize_connection()

    def execute_query(self, query, parameters=()):
        try:
            self.test_connection()
            self.cursor.execute(query, parameters)
            
            # Si la consulta es un SELECT, devolvemos los resultados
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()  # Devuelve todos los resultados
            else:
                self.connection.commit()  # Si no es SELECT, solo ejecutamos commit
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")


    def fetch_query(self, query, parameters=()):
        try:
            self.test_connection()
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al obtener datos: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Conexión cerrada")