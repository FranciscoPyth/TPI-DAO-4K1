import tkinter as tk
from tkinter import ttk
from services.BibliotecaService import BibliotecaService
from classes.Autor import Autor
from classes.Libro import Libro
from classes.Usuario import Usuario
from classes.Prestamo import Prestamo

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Biblioteca")
        self.geometry("600x500")
        self.configure(bg="#f5f5f5")

        # Título de la aplicación
        tk.Label(self, text="Gestión de Biblioteca", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        # Menú de opciones
        options_frame = tk.Frame(self, bg="#f5f5f5")
        options_frame.pack(pady=10)
        
        # Botones de opciones
        tk.Button(options_frame, text="Nuevo Autor", command=self.show_nuevo_autor, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Button(options_frame, text="Nuevo Libro", command=self.show_nuevo_libro, width=15, bg="#4CAF50", fg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Button(options_frame, text="Préstamo", command=self.show_prestamo, width=15, bg="#4CAF50", fg="white").grid(row=0, column=2, padx=10, pady=5)
        tk.Button(options_frame, text="Usuario nuevo", command=self.show_usuario, width=15, bg="#4CAF50", fg="white").grid(row=0, column=5, padx=10, pady=5)

        # Frame contenedor donde se mostrarán los formularios
        self.content_frame = tk.Frame(self, bg="#f5f5f5")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Inicialización de los formularios
        self.create_nuevo_autor_form()
        self.create_nuevo_libro_form()
        self.create_prestamo_form()
        self.create_usuario_form()

        # Mostrar el formulario de Nuevo Autor por defecto
        self.show_nuevo_autor()

    def clear_content_frame(self):
        # Oculta todos los frames de formularios
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def create_nuevo_autor_form(self):
        self.nuevo_autor_frame = tk.Frame(self.content_frame, bg="#f5f5f5")

        tk.Label(self.nuevo_autor_frame, text="Nombre:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.nombre_entry = tk.Entry(self.nuevo_autor_frame, font=("Helvetica", 10))
        self.nombre_entry.pack(pady=5)

        tk.Label(self.nuevo_autor_frame, text="Apellido:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.apellido_entry = tk.Entry(self.nuevo_autor_frame, font=("Helvetica", 10))
        self.apellido_entry.pack(pady=5)

        tk.Label(self.nuevo_autor_frame, text="Nacionalidad:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.nacionalidad_combobox = ttk.Combobox(self.nuevo_autor_frame, values=["Argentina", "Chile", "Perú", "Brasil"])
        self.nacionalidad_combobox.pack(pady=5)

        tk.Button(self.nuevo_autor_frame, text="Guardar", command=self.save_autor, bg="#4CAF50", fg="white").pack(pady=10)

    def create_nuevo_libro_form(self):
        self.nuevo_libro_frame = tk.Frame(self.content_frame, bg="#f5f5f5")

        tk.Label(self.nuevo_libro_frame, text="Código ISBN:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.code_isbn_entry = tk.Entry(self.nuevo_libro_frame, font=("Helvetica", 10))
        self.code_isbn_entry.pack(pady=5)

        tk.Label(self.nuevo_libro_frame, text="Título:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.titulo_entry = tk.Entry(self.nuevo_libro_frame, font=("Helvetica", 10))
        self.titulo_entry.pack(pady=5)

        tk.Label(self.nuevo_libro_frame, text="Género:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.genero_combobox = ttk.Combobox(self.nuevo_libro_frame, values=["Ficción", "No Ficción", "Misterio", "Ciencia Ficción"])
        self.genero_combobox.pack(pady=5)

        tk.Label(self.nuevo_libro_frame, text="Año de Publicación:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.anio_entry = tk.Entry(self.nuevo_libro_frame, font=("Helvetica", 10))
        self.anio_entry.pack(pady=5)

        tk.Label(self.nuevo_libro_frame, text="Autor:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.autor_combobox = ttk.Combobox(self.nuevo_libro_frame, values=["Autor 1", "Autor 2", "Autor 3"])
        self.autor_combobox.pack(pady=5)

        tk.Button(self.nuevo_libro_frame, text="Guardar", command=self.save_libro, bg="#4CAF50", fg="white").pack(pady=10)

    def create_prestamo_form(self):
        self.prestamo_frame = tk.Frame(self.content_frame, bg="#f5f5f5")
        
        # Tabla de préstamos
        self.prestamo_tree = ttk.Treeview(self.prestamo_frame, columns=("ID", "Usuario", "Fecha"), show="headings", height=5)
        self.prestamo_tree.heading("ID", text="ID")
        self.prestamo_tree.heading("Usuario", text="Usuario")
        self.prestamo_tree.heading("Fecha", text="Fecha de Préstamo")
        self.prestamo_tree.pack(pady=5)

        # Botón para agregar un nuevo préstamo
        tk.Button(self.prestamo_frame, text="+ Agregar Préstamo", command=self.show_prestamo_form, bg="#4CAF50", fg="white").pack(pady=10)

        # Formulario de nuevo préstamo
        self.prestamo_form_frame = tk.Frame(self.prestamo_frame, bg="#f5f5f5")
        tk.Label(self.prestamo_form_frame, text="Usuario:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.usuario_prestamo_entry = tk.Entry(self.prestamo_form_frame, font=("Helvetica", 10))
        self.usuario_prestamo_entry.pack(pady=5)

        tk.Label(self.prestamo_form_frame, text="Fecha de Préstamo:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.fecha_prestamo_entry = tk.Entry(self.prestamo_form_frame, font=("Helvetica", 10))
        self.fecha_prestamo_entry.pack(pady=5)

        tk.Button(self.prestamo_form_frame, text="Guardar", command=self.save_prestamo, bg="#4CAF50", fg="white").pack(pady=10)
        self.prestamo_form_frame.pack_forget()

    def create_usuario_form(self):
        self.usuario_frame = tk.Frame(self.content_frame, bg="#f5f5f5")

        tk.Label(self.usuario_frame, text="Nombre:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.nombre_usuario_entry = tk.Entry(self.usuario_frame, font=("Helvetica", 10))
        self.nombre_usuario_entry.pack(pady=5)

        tk.Label(self.usuario_frame, text="Apellido:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.apellido_usuario_entry = tk.Entry(self.usuario_frame, font=("Helvetica", 10))
        self.apellido_usuario_entry.pack(pady=5)

        tk.Label(self.usuario_frame, text="Profesor/Estudiante:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.tipo_usuario_combobox = ttk.Combobox(self.usuario_frame, values=["Profesor", "Estudiante"])
        self.tipo_usuario_combobox.pack(pady=5)
        
        tk.Label(self.usuario_frame, text="Dirección:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.direccion_usuario_entry = tk.Entry(self.usuario_frame, font=("Helvetica", 10))
        self.direccion_usuario_entry.pack(pady=5)

        tk.Label(self.usuario_frame, text="Teléfono:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.telefono_usuario_entry = tk.Entry(self.usuario_frame, font=("Helvetica", 10))
        self.telefono_usuario_entry.pack(pady=5)

        tk.Button(self.usuario_frame, text="Guardar", command=self.save_usuario, bg="#4CAF50", fg="white").pack(pady=10)
        
    
    
    # Funciones para mostrar formularios de Préstamo y Devolución
    def show_prestamo_form(self):
        self.prestamo_form_frame.pack()


    # Funciones para cambiar de formulario
    def show_nuevo_autor(self):
        self.clear_content_frame()
        self.nuevo_autor_frame.pack()

    def show_nuevo_libro(self):
        self.clear_content_frame()
        self.nuevo_libro_frame.pack()

    def show_prestamo(self):
        self.clear_content_frame()
        self.prestamo_frame.pack()
    
    def show_usuario(self):
        self.clear_content_frame()
        self.usuario_frame.pack()

    # Funciones para guardar datos
    def save_autor(self):
        # Capturamos los valores ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        nacionalidad = self.nacionalidad_combobox.get()
        autor = Autor(nombre, apellido, nacionalidad)
        # Aquí deberías llamar a un método en tu servicio de base de datos para insertar estos datos
        if autor:
            # Usando un método de biblioteca para insertar el autor en la base de datos
            try:
                biblioteca_service = BibliotecaService()  # Asegúrate de tener una instancia o método accesible para interactuar con la BD
                biblioteca_service.registrar_autor(autor)
            except Exception as e:
                print(f"Error al guardar el autor: {e}")
        else:
            print("Por favor, completa todos los campos.")
            
    
    def save_usuario(self):
        nombre = self.nombre_usuario_entry.get()
        apellido = self.apellido_usuario_entry.get()
        tipo_usuario = self.tipo_usuario_combobox.get()
        direccion = self.direccion_usuario_entry.get()
        telefono = self.telefono_usuario_entry.get()

        try:
            usuario = Usuario(nombre, apellido, tipo_usuario, direccion, telefono)
            biblioteca_service = BibliotecaService()
            biblioteca_service.registrar_usuario(usuario)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")

    def save_libro(self):
        print("Libro guardado")

    def save_prestamo(self):
        print("Préstamo guardado")
        self.prestamo_form_frame.pack_forget()

        
        
        

