import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.BibliotecaService import BibliotecaService
from classes.Autor import Autor
from classes.Libro import Libro
from classes.Prestamo import Prestamo
from classes.Usuario import Usuario, Estudiante, Profesor
from services.UsuarioService import UsuarioService
from services.LibroService import LibroService
from services.AutorService import AutorService
from services.PrestamoService import PrestamoService
from services.ReporteService import ReporteService
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import services.ApiPaises


class LibraryApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("BibliotecApp")
        self.geometry("1950x1024")
        self.iconbitmap(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")


        # Cargar y colocar la imagen de fondo con transparencia
        background_image = Image.open(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/fondo.jpg")
        background_image = background_image.resize((1950, 1024), Image.LANCZOS)
        background_image = self.apply_transparency(background_image, alpha=0.4)
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        tk.Label(self, text="BibliotecApp", font=("Helvetica", 26, "bold")).pack(pady=20)

        # Botones de opciones redondeados con color personalizado
        self.create_rounded_button("Autores", self.abrir_autores, "#DA9A9A").pack(pady=10)
        self.create_rounded_button("Usuarios", self.abrir_usuarios, "#DA9A9A").pack(pady=10)
        self.create_rounded_button("Libros", self.abrir_libros, "#DA9A9A").pack(pady=10)
        self.create_rounded_button("Prestamos", self.abrir_prestamos, "#DA9A9A").pack(pady=10)
        self.create_rounded_button("Reportes", self.abrir_reportes, "#DA9A9A").pack(pady=10)

        # Botón de salir
        tk.Button(self, text="SALIR", width=30, height=2, bg="#FF6565", font=("Helvetica", 14, "bold"), command=self.salir).pack(pady=30)

    def apply_transparency(self, image, alpha):
        """Aplica transparencia a una imagen."""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(alpha)

    def create_rounded_button(self, text, command, bg_color):
        """Crea un botón redondeado con texto e imagen de fondo con color especificado."""
        # Dimensiones del botón
        button_width = 566
        button_height = 92
        
        # Calcular el radio de los bordes como el 30% de la altura
        radius = int(0.3 * min(button_width, button_height))

        # Crear una imagen de botón redondeado con el color especificado
        button_image = Image.new("RGBA", (button_width, button_height), bg_color)
        draw = ImageDraw.Draw(button_image)
        
        # Dibuja el rectángulo redondeado con el nuevo radio
        draw.rounded_rectangle((0, 0, button_width, button_height), radius=radius, fill=bg_color)

        # Convertir la imagen a formato tkinter
        button_photo = ImageTk.PhotoImage(button_image)

        # Crear un botón usando la imagen
        button = tk.Button(self, text=text, image=button_photo, compound="center",
                        font=("Helvetica", 22), command=command, borderwidth=0, width=button_width, height=button_height)
        button.image = button_photo  # Mantener referencia a la imagen
        return button


    # Métodos para abrir cada ventana
    def abrir_autores(self):
        ventana_autores = tk.Toplevel(self)
        ventana_autores.title("Gestión de Autores")
        ventana_autores.geometry("900x600")
        ventana_autores.iconbitmap(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")

        pantalla_ancho = ventana_autores.winfo_screenwidth()
        pantalla_alto = ventana_autores.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (pantalla_ancho // 2) - (900 // 2)
        y = (pantalla_alto // 2) - (600 // 2)

        ventana_autores.geometry(f"{900}x{600}+{x}+{y}")

        # Frame principal
        main_frame = ttk.Frame(ventana_autores, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Autor", padding="10")
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Variables del formulario
        self.vars_autor = {
            'id': tk.StringVar(),
            'nombre': tk.StringVar(),
            'apellido': tk.StringVar(),
            'telefono': tk.StringVar(),
            'nacionalidad': tk.StringVar()
        }

        # Funciones de validación
        def solo_letras(char):
            return char.isalpha() or char.isspace()  # Permite letras y espacios

        def solo_numeros(char):
            return char.isdigit()  # Permite solo números

        # Crear campos del formulario
        campos = [
            ("Nombre:", 'nombre', 0),
            ("Apellido:", 'apellido', 2),
            ("Teléfono:", 'telefono', 4),
            ("Nacionalidad:", 'nacionalidad', 6)
        ]

        for label_text, var_name, col in campos:
            ttk.Label(form_frame, text=label_text).grid(row=0, column=col, padx=5, pady=5)

            if var_name == 'nacionalidad':
                nacionalidades = services.ApiPaises.obtener_nombres_de_paises()
                ttk.Combobox(form_frame, textvariable=self.vars_autor[var_name], values=nacionalidades, state="readonly").grid(
                    row=0, column=col+1, padx=5, pady=5
                )
            else:
                entry = ttk.Entry(form_frame, textvariable=self.vars_autor[var_name])
                
                # Configurar validación
                if var_name in ('nombre', 'apellido'):
                    # Validación para solo letras
                    entry.config(validate="key", validatecommand=(ventana_autores.register(solo_letras), '%S'))
                elif var_name == 'telefono':
                    # Validación para solo números
                    entry.config(validate="key", validatecommand=(ventana_autores.register(solo_numeros), '%S'))

                entry.grid(row=0, column=col+1, padx=5, pady=5)

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=1, column=0, columnspan=8, pady=10)

        # Botones
        ttk.Button(button_frame, text="Guardar", command=lambda: self._guardar_autor(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=lambda: self._actualizar_autor(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=lambda: self._eliminar_autor(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self._limpiar_campos_autor).pack(side=tk.LEFT, padx=5)

        # Frame para la tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear tabla
        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Nacionalidad")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Vincular evento de selección
        tree.bind('<<TreeviewSelect>>', lambda event: self._seleccionar_autor(event, tree))

        # Cargar datos iniciales
        self._cargar_autores(tree)

    def _cargar_autores(self, tree):
        """Carga los autores en la tabla"""
        # Limpiar la tabla
        for item in tree.get_children():
            tree.delete(item)
        
        # Obtener autores
        autor_service = AutorService(self.db)
        autores = autor_service.get_all_autores()
        
        # Insertar autores en la tabla
        for autor in autores:
            tree.insert("", tk.END, values=autor)

    def _guardar_autor(self, tree):
        """Guarda un nuevo autor"""
        try:
            autor = Autor(
                nombre=self.vars_autor['nombre'].get(),
                apellido=self.vars_autor['apellido'].get(),
                telefono=self.vars_autor['telefono'].get(),
                nacionalidad=self.vars_autor['nacionalidad'].get()
            )
            autor_service = AutorService(self.db)
            autor_service.create_autor(autor)
            self._limpiar_campos_autor()
            self._cargar_autores(tree)
            messagebox.showinfo("Éxito", "Autor guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _actualizar_autor(self, tree):
        """Actualiza un autor existente"""
        if not self.vars_autor['id'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un autor para actualizar")
            return
        
        try:
            autor_service = AutorService(self.db)
            autor_data = {
                'nombre': self.vars_autor['nombre'].get(),
                'apellido': self.vars_autor['apellido'].get(),
                'telefono': self.vars_autor['telefono'].get(),
                'nacionalidad': self.vars_autor['nacionalidad'].get()
            }
            autor_service.update_autor(self.vars_autor['id'].get(), autor_data)
            self._limpiar_campos_autor()
            self._cargar_autores(tree)
            messagebox.showinfo("Éxito", "Autor actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_autor(self, tree):
        """Elimina un autor"""
        if not self.vars_autor['id'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un autor para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este autor?"):
            try:
                autor_service = AutorService(self.db)
                autor_service.delete_autor(self.vars_autor['id'].get())
                self._limpiar_campos_autor()
                self._cargar_autores(tree)
                messagebox.showinfo("Éxito", "Autor eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _seleccionar_autor(self, event, tree):
        """Maneja la selección de un autor en la tabla"""
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])
            autor = item['values']
            self.vars_autor['id'].set(autor[0])
            self.vars_autor['nombre'].set(autor[1])
            self.vars_autor['apellido'].set(autor[2])
            self.vars_autor['telefono'].set(autor[3])
            self.vars_autor['nacionalidad'].set(autor[4])

    def _limpiar_campos_autor(self):
        """Limpia los campos del formulario"""
        for var in self.vars_autor.values():
            var.set("")
    
    def abrir_usuarios(self):
        """Abre la ventana de gestión de usuarios"""
        ventana_usuarios = tk.Toplevel(self)
        ventana_usuarios.title("Usuarios")
        ventana_usuarios.geometry("800x600")
        ventana_usuarios.iconbitmap(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")


        pantalla_ancho = ventana_usuarios.winfo_screenwidth()
        pantalla_alto = ventana_usuarios.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (pantalla_ancho // 2) - (800 // 2)
        y = (pantalla_alto // 2) - (600 // 2)

        ventana_usuarios.geometry(f"{800}x{600}+{x}+{y}")
        
        # Variables para los campos del usuario
        self.vars_usuario = {
            'id': tk.StringVar(),
            'nombre': tk.StringVar(),
            'apellido': tk.StringVar(),
            'tipo_usuario': tk.StringVar(),
            'direccion': tk.StringVar(),
            'telefono': tk.StringVar()
        }
        
        # Frame para el formulario
        frame_form = ttk.LabelFrame(ventana_usuarios, text="Datos del Usuario")
        frame_form.pack(padx=10, pady=10, fill="x")
        
        # Campos del formulario
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.vars_usuario['nombre']).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Apellido:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.vars_usuario['apellido']).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Tipo Usuario:").grid(row=1, column=0, padx=5, pady=5)
        tipo_combo = ttk.Combobox(frame_form, textvariable=self.vars_usuario['tipo_usuario'], values=['Estudiante', 'Profesor'])
        tipo_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Dirección:").grid(row=1, column=2, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.vars_usuario['direccion']).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame_form, textvariable=self.vars_usuario['telefono']).grid(row=2, column=1, padx=5, pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(ventana_usuarios)
        frame_botones.pack(pady=10)
        
        # Botones CRUD
        ttk.Button(frame_botones, text="Guardar", command=lambda: self._guardar_usuario(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Actualizar", command=lambda: self._actualizar_usuario(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=lambda: self._eliminar_usuario(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_campos_usuario).pack(side=tk.LEFT, padx=5)
        
        # Tabla de usuarios
        columns = ('ID', 'Nombre', 'Apellido', 'Tipo', 'Dirección', 'Teléfono')
        tree = ttk.Treeview(ventana_usuarios, columns=columns, show='headings')
        
        # Configurar las columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(ventana_usuarios, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Vincular evento de selección
        tree.bind('<<TreeviewSelect>>', lambda event: self._seleccionar_usuario(event, tree))
        
        # Cargar datos iniciales
        self._cargar_usuarios(tree)

    def _cargar_usuarios(self, tree):
        """Carga los usuarios en la tabla"""
        # Limpiar la tabla
        for item in tree.get_children():
            tree.delete(item)
        
        # Obtener usuarios
        usuario_service = UsuarioService(self.db)
        query = "SELECT id, nombre, apellido, tipo_usuario, direccion, telefono FROM usuarios"
        usuarios = self.db.fetch_query(query)
        
        # Insertar usuarios en la tabla
        for usuario in usuarios:
            tree.insert("", tk.END, values=usuario)

    def _guardar_usuario(self, tree):
        """Guarda un nuevo usuario"""
        try:
            tipo = self.vars_usuario['tipo_usuario'].get()
            if tipo == 'estudiante':
                usuario = Estudiante(
                    nombre=self.vars_usuario['nombre'].get(),
                    apellido=self.vars_usuario['apellido'].get(),
                    direccion=self.vars_usuario['direccion'].get(),
                    telefono=self.vars_usuario['telefono'].get()
                )
            else:
                usuario = Profesor(
                    nombre=self.vars_usuario['nombre'].get(),
                    apellido=self.vars_usuario['apellido'].get(),
                    direccion=self.vars_usuario['direccion'].get(),
                    telefono=self.vars_usuario['telefono'].get()
                )
            
            usuario_service = UsuarioService(self.db)
            usuario_service.registrar_usuario(usuario)
            self._limpiar_campos_usuario()
            self._cargar_usuarios(tree)
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _actualizar_usuario(self, tree):
        """Actualiza un usuario existente"""
        if not self.vars_usuario['id'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para actualizar")
            return
        
        try:
            query = """
            UPDATE usuarios 
            SET nombre=?, apellido=?, tipo_usuario=?, direccion=?, telefono=?
            WHERE id=?
            """
            params = (
                self.vars_usuario['nombre'].get(),
                self.vars_usuario['apellido'].get(),
                self.vars_usuario['tipo_usuario'].get(),
                self.vars_usuario['direccion'].get(),
                self.vars_usuario['telefono'].get(),
                self.vars_usuario['id'].get()
            )
            self.db.execute_query(query, params)
            self._limpiar_campos_usuario()
            self._cargar_usuarios(tree)
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_usuario(self, tree):
        """Elimina un usuario"""
        if not self.vars_usuario['id'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            try:
                query = "DELETE FROM usuarios WHERE id=?"
                self.db.execute_query(query, (self.vars_usuario['id'].get(),))
                self._limpiar_campos_usuario()
                self._cargar_usuarios(tree)
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _seleccionar_usuario(self, event, tree):
        """Maneja la selección de un usuario en la tabla"""
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])
            usuario = item['values']
            self.vars_usuario['id'].set(usuario[0])
            self.vars_usuario['nombre'].set(usuario[1])
            self.vars_usuario['apellido'].set(usuario[2])
            self.vars_usuario['tipo_usuario'].set(usuario[3])
            self.vars_usuario['direccion'].set(usuario[4])
            self.vars_usuario['telefono'].set(usuario[5])

    def _limpiar_campos_usuario(self):
        """Limpia los campos del formulario"""
        for var in self.vars_usuario.values():
            var.set("")

    
    def abrir_libros(self):
        ventana_libros = tk.Toplevel(self)
        ventana_libros.title("Gestión de Libros")
        ventana_libros.geometry("1000x600")
        ventana_libros.iconbitmap(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")


        pantalla_ancho = ventana_libros.winfo_screenwidth()
        pantalla_alto = ventana_libros.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (pantalla_ancho // 2) - (1000 // 2)
        y = (pantalla_alto // 2) - (600 // 2)

        ventana_libros.geometry(f"{1000}x{600}+{x}+{y}")

        # Frame principal
        main_frame = ttk.Frame(ventana_libros, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Libro", padding="10")
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Variables del formulario
        self.vars_libro = {
            'isbn': tk.StringVar(),
            'titulo': tk.StringVar(),
            'genero': tk.StringVar(),
            'ano_publicacion': tk.StringVar(),
            'autor_id': tk.StringVar(),
            'cantidad_disponible': tk.StringVar()
        }

        # Funciones de validación
        def solo_numeros(char):
            return char.isdigit()

        def validar_isbn(char):
            return char.isdigit() or char == '-'

        # Crear campos del formulario
        campos = [
            ("ISBN:", 'isbn', 0),
            ("Título:", 'titulo', 2),
            ("Género:", 'genero', 4),
            ("Año:", 'ano_publicacion', 0, 1),
            ("Autor:", 'autor_id', 2, 1),
            ("Cantidad:", 'cantidad_disponible', 4, 1)
        ]

        for campo in campos:
            if len(campo) == 3:
                label_text, var_name, col = campo
                row = 0
            else:
                label_text, var_name, col, row = campo

            ttk.Label(form_frame, text=label_text).grid(row=row, column=col, padx=5, pady=5)

            if var_name == 'genero':
                generos = ["Ficción", "No Ficción", "Novela", "Poesía", "Historia", "Ciencia", "Tecnología"]
                ttk.Combobox(form_frame, textvariable=self.vars_libro[var_name], 
                            values=generos, state="readonly").grid(
                    row=row, column=col+1, padx=5, pady=5)
            elif var_name == 'autor_id':
                # Obtener lista de autores
                autor_service = AutorService(self.db)
                autores = autor_service.get_all_autores()
                autores_lista = [f"{autor[0]} - {autor[1]} {autor[2]}" for autor in autores]
                ttk.Combobox(form_frame, textvariable=self.vars_libro[var_name],
                            values=autores_lista, state="readonly").grid(
                    row=row, column=col+1, padx=5, pady=5)
            else:
                entry = ttk.Entry(form_frame, textvariable=self.vars_libro[var_name])
                
                # Configurar validación
                if var_name in ('ano_publicacion', 'cantidad_disponible'):
                    entry.config(validate="key", validatecommand=(ventana_libros.register(solo_numeros), '%S'))
                elif var_name == 'isbn':
                    entry.config(validate="key", validatecommand=(ventana_libros.register(validar_isbn), '%S'))

                entry.grid(row=row, column=col+1, padx=5, pady=5)

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=8, pady=10)

        # Botones
        ttk.Button(button_frame, text="Guardar", command=lambda: self._guardar_libro(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=lambda: self._actualizar_libro(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=lambda: self._eliminar_libro(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self._limpiar_campos_libro).pack(side=tk.LEFT, padx=5)

        # Frame para la tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear tabla
        columns = ("ISBN", "Título", "Género", "Año", "Autor", "Cantidad")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Vincular evento de selección
        tree.bind('<<TreeviewSelect>>', lambda event: self._seleccionar_libro(event, tree))

        # Cargar datos iniciales
        self._cargar_libros(tree)

    def _cargar_libros(self, tree):
        """Carga los libros en la tabla"""
        for item in tree.get_children():
            tree.delete(item)
        
        libro_service = LibroService(self.db)
        libros = libro_service.get_all_libros()
        
        for libro in libros:
            # Obtener nombre del autor
            autor_service = AutorService(self.db)
            autor = autor_service.find_autor_by_id(libro[4])
            nombre_autor = f"{autor[1]} {autor[2]}" if autor else "Desconocido"
            
            # Mostrar en la tabla
            tree.insert("", tk.END, values=(libro[0], libro[1], libro[2], libro[3], nombre_autor, libro[5]))

    def _guardar_libro(self, tree):
        """Guarda un nuevo libro"""
        try:
            # Extraer ID del autor del string "id - nombre apellido"
            autor_id = self.vars_libro['autor_id'].get().split(' - ')[0]
            
            libro = Libro(
                code_isbn=self.vars_libro['isbn'].get(),
                titulo=self.vars_libro['titulo'].get(),
                genero=self.vars_libro['genero'].get(),
                anio_publicacion=int(self.vars_libro['ano_publicacion'].get()),
                autor=autor_id,
                cant_disponible=int(self.vars_libro['cantidad_disponible'].get())
            )
            libro_service = LibroService(self.db)
            libro_service.registrar_libro(libro)
            self._limpiar_campos_libro()
            self._cargar_libros(tree)
            messagebox.showinfo("Éxito", "Libro guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _actualizar_libro(self, tree):
        """Actualiza un libro existente"""
        if not self.vars_libro['isbn'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un libro para actualizar")
            return
        
        try:
            autor_id = self.vars_libro['autor_id'].get().split(' - ')[0]
            libro_service = LibroService(self.db)
            libro_data = {
                'titulo': self.vars_libro['titulo'].get(),
                'genero': self.vars_libro['genero'].get(),
                'ano_publicacion': int(self.vars_libro['ano_publicacion'].get()),
                'id_autor': autor_id,
                'cantidad_disponible': int(self.vars_libro['cantidad_disponible'].get())
            }
            libro_service.update_libro(self.vars_libro['isbn'].get(), libro_data)
            self._limpiar_campos_libro()
            self._cargar_libros(tree)
            messagebox.showinfo("Éxito", "Libro actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_libro(self, tree):
        """Elimina un libro"""
        if not self.vars_libro['isbn'].get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un libro para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este libro?"):
            try:
                libro_service = LibroService(self.db)
                libro_service.delete_libro(self.vars_libro['isbn'].get())
                self._limpiar_campos_libro()
                self._cargar_libros(tree)
                messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _seleccionar_libro(self, event, tree):
        """Maneja la selección de un libro en la tabla"""
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])
            libro = item['values']
            self.vars_libro['isbn'].set(libro[0])
            self.vars_libro['titulo'].set(libro[1])
            self.vars_libro['genero'].set(libro[2])
            self.vars_libro['ano_publicacion'].set(libro[3])
            self.vars_libro['autor_id'].set(libro[4])
            self.vars_libro['cantidad_disponible'].set(libro[5])

    def _limpiar_campos_libro(self):
        """Limpia los campos del formulario"""
        for var in self.vars_libro.values():
            var.set("")


    def abrir_prestamos(self):
        ventana_prestamos = tk.Toplevel(self)
        ventana_prestamos.title("Gestión de Préstamos")
        ventana_prestamos.geometry("1000x600")
        ventana_prestamos.iconbitmap(
            r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")

        # Centrar ventana
        pantalla_ancho = ventana_prestamos.winfo_screenwidth()
        pantalla_alto = ventana_prestamos.winfo_screenheight()
        x = (pantalla_ancho // 2) - (1000 // 2)
        y = (pantalla_alto // 2) - (600 // 2)
        ventana_prestamos.geometry(f"{1000}x{600}+{x}+{y}")

        # Frame principal
        main_frame = ttk.Frame(ventana_prestamos, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Préstamo", padding="10")
        form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Variables del formulario
        self.vars_prestamo = {
            'id_usuario': tk.StringVar(),
            'isbn_libro': tk.StringVar(),
            'fecha_prestamo': tk.StringVar(),
            'fecha_devolucion': tk.StringVar(),
            'fecha_devolucion_real': tk.StringVar(),
        }

        # Obtener datos de usuarios y libros

        usuario_service = UsuarioService(self.db)
        libros_service = LibroService(self.db)

        usuarios = usuario_service.get_all_usuarios()
        libros = libros_service.get_all_libros()

        # Crear listas desplegables
        usuarios_lista = [f"{usuario[0]} - {usuario[1]} {usuario[2]}" for usuario in usuarios]
        libros_lista = [f"{libro[0]} - {libro[1]}" for libro in libros]

        # Crear campos del formulario
        campos = [
            ("Usuario:", 'id_usuario', 0),
            ("Libro:", 'isbn_libro', 2),
            ("Fecha Préstamo:", 'fecha_prestamo', 4),
            ("Fecha Devolución:", 'fecha_devolucion', 0, 1),
            ("Fecha Devolución Real:", 'fecha_devolucion_real', 2, 1),
        ]

        for campo in campos:
            label_text, var_name, col = campo[:3]
            row = campo[3] if len(campo) > 3 else 0

            ttk.Label(form_frame, text=label_text).grid(row=row, column=col, padx=5, pady=5)

            if var_name == 'id_usuario':
                # Desplegable para usuarios
                ttk.Combobox(form_frame, textvariable=self.vars_prestamo[var_name], values=usuarios_lista).grid(
                    row=row, column=col + 1, padx=5, pady=5)
            elif var_name == 'isbn_libro':
                # Desplegable para libros
                ttk.Combobox(form_frame, textvariable=self.vars_prestamo[var_name], values=libros_lista).grid(
                    row=row, column=col + 1, padx=5, pady=5)
            else:
                # Entrada normal
                ttk.Entry(form_frame, textvariable=self.vars_prestamo[var_name]).grid(row=row, column=col + 1, padx=5, pady=5)

        # Frame para botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=8, pady=10)

        # Botones
        ttk.Button(button_frame, text="Registrar", command=lambda: self._registrar_prestamo(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=lambda: self._actualizar_prestamo(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=lambda: self._eliminar_prestamo(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self._limpiar_campos_prestamo).pack(side=tk.LEFT, padx=5)

        # Frame para la tabla
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear tabla
        columns = ("Usuario", "ISBN", "Fecha Préstamo", "Fecha Devolución", "Fecha Devolución Real")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Vincular evento de selección
        tree.bind('<<TreeviewSelect>>', lambda event: self._seleccionar_prestamo(event, tree))

        # Cargar datos iniciales
        self._cargar_prestamos(tree)


    def _cargar_prestamos(self, tree):
        """Carga los préstamos en la tabla."""
        # Limpiar la tabla
        for item in tree.get_children():
            tree.delete(item)

        prestamos_service = PrestamoService(self.db)
        prestamos = prestamos_service.get_all_prestamos()
        print("Préstamos recuperados:", prestamos)

        # Verificar si se obtuvieron datos
        if not prestamos:
            print("No hay préstamos para mostrar.")
            return

        # Insertar los datos en la tabla
        for prestamo in prestamos:
            # Ajustar según la estructura de las tuplas devueltas
            tree.insert(
                "",
                "end",
                values=(
                    prestamo[1],  # usuario
                    prestamo[2],  # libro
                    prestamo[3],  # fecha_prestamo
                    prestamo[4],  # fecha_devolucion
                ),
            )




    def _registrar_prestamo(self, tree):
        """Registra un nuevo préstamo"""
        try:
            # Extraer valores del formulario
            usuario_id = self.vars_prestamo['id_usuario'].get().split(" - ")[0]
            isbn = self.vars_prestamo['isbn_libro'].get().split(" - ")[0]

            fecha_prestamo = self.vars_prestamo['fecha_prestamo'].get()
            fecha_devolucion = self.vars_prestamo['fecha_devolucion'].get()

            # Instancias de usuario y libro
            usuario_service = UsuarioService(self.db)
            libro_service = LibroService(self.db)

            usuario = usuario_service.find_usuario_by_id(usuario_id)
            libro = libro_service.findLibroByIsdn(isbn)

            if usuario is None:
                raise Exception(f"Usuario con ID {usuario_id} no encontrado")
            if libro is None:
                raise Exception(f"Libro con ISBN {isbn} no encontrado")

            # Crear objeto de préstamo
            prestamo = Prestamo(
                usuario=usuario,
                libro=libro,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion=fecha_devolucion,
            )

            # Registrar en la base de datos
            prestamo_service = PrestamoService(self.db)
            prestamo_service.registrar_prestamo(prestamo)

            # Actualizar interfaz
            self._limpiar_campos_prestamo()
            self._cargar_prestamos(tree)
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el préstamo: {e}")


    def _actualizar_prestamo(self, tree):
        """Actualiza un préstamo existente"""
        # Implementar funcionalidad similar al registro

    def _eliminar_prestamo(self, tree):
        """Elimina un préstamo"""
        # Implementar funcionalidad similar al registro

    def _seleccionar_prestamo(self, event, tree):
        """Selecciona un préstamo de la tabla"""
        # Implementar funcionalidad similar a selección de libros

    def _limpiar_campos_prestamo(self):
        """Limpia los campos del formulario"""
        for var in self.vars_prestamo.values():
            var.set("")


    def salir(self):
        self.destroy()

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

        tk.Label(self.nuevo_libro_frame, text="Cantidad:", bg="#f5f5f5", font=("Helvetica", 10)).pack(pady=5)
        self.cantidad_entry = tk.Entry(self.nuevo_libro_frame, font=("Helvetica", 10))
        self.cantidad_entry.pack(pady=5)

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
        
    
    def abrir_reportes(self):
        # Crear la ventana
        ventana_reportes = tk.Toplevel(self)
        ventana_reportes.title("Reportes")

        ventana_reportes.iconbitmap(r"C:/Users/Usuario/General/Archivos Fran Dell/Ingeniería en Sistemas/4° Cuarto Año/Desarrollo de Aplicaciones con Objetos (DAO)/TPI-DAO-4K1/src/images/logo_app.ico")

        
        # Establecer tamaño de la ventana
        ancho_ventana = 975
        alto_ventana = 512
        
        # Obtener las dimensiones de la pantalla
        pantalla_ancho = ventana_reportes.winfo_screenwidth()
        pantalla_alto = ventana_reportes.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (pantalla_ancho // 2) - (ancho_ventana // 2)
        y = (pantalla_alto // 2) - (alto_ventana // 2)

        # Establecer la posición de la ventana en el centro de la pantalla
        ventana_reportes.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Configurar el fondo de la ventana
        ventana_reportes.config(bg="#CFCADC")  # Fondo gris claro
        
        # Título con estilo mejorado y texto en blanco
        tk.Label(ventana_reportes, text="Gestión de Reportes", font=("Helvetica", 22, "bold"), bg="#DA9A9A", fg="black", relief="solid", padx=10, pady=10).pack(pady=20)
        
        # Función para personalizar los botones
        def crear_boton(texto, comando, color_fondo, color_hover):
            boton = tk.Button(ventana_reportes, text=texto, font=("Helvetica", 14), bg=color_fondo, fg="black", relief="flat", 
                            height=2, width=25, bd=3, command=comando)
            boton.pack(pady=12)
            boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))  # Efecto hover
            boton.bind("<Leave>", lambda e: boton.config(bg=color_fondo))  # Efecto hover
            return boton

        # Botones para generar reportes, con texto blanco
        crear_boton("Préstamos Vencidos", self.generar_prestamos_vencidos, "#DA9A9A", "#FF6565")
        crear_boton("Libros Más Prestados", self.generar_libros_mas_prestados, "#DA9A9A", "#FF6565")
        crear_boton("Usuarios Más Activos", self.generar_usuarios_mas_activos, "#DA9A9A", "#FF6565")
        
        # Botón de volver con otro color, texto blanco
        crear_boton("Volver", ventana_reportes.destroy, "#FF6565", "#e53935")
        
        # Se puede agregar un borde o sombreado a la ventana para dar más profundidad
        ventana_reportes.update_idletasks()  # Asegura que se actualicen los tamaños de los widgets
        ventana_reportes.attributes("-topmost", True)  # Mantener la ventana al frente

    def generar_prestamos_vencidos(self):
        # Crear el servicio de reportes y generar el reporte
        reporte_service = ReporteService(self.db)
        reporte_service.listar_prestamos_vencidos()

    def generar_libros_mas_prestados(self):
        # Crear el servicio de reportes y generar el reporte
        reporte_service = ReporteService(self.db)
        reporte_service.libros_mas_prestados()

    def generar_usuarios_mas_activos(self):
        # Crear el servicio de reportes y generar el reporte
        reporte_service = ReporteService(self.db)
        reporte_service.usuarios_mas_activos()


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
                autor_service = AutorService(self.db)  # Asegúrate de tener una instancia o método accesible para interactuar con la BD
                autor_service.registrar_autor(autor)
            except Exception as e:
                print(f"Error al guardar el autor: {e}")
        else:
            print("Por favor, completa todos los campos.")

    
    def save_libro(self):
        # Capturamos los valores ingresados por el usuario
        codigo_isbn = self.code_isbn_entry.get()
        titulo = self.titulo_entry.get()
        genero = self.genero_combobox.get()
        anio_publicacion = self.anio_entry.get()
        autor = self.autor_combobox.get()
        cantidad = self.cantidad_entry.get()

        # Crear el objeto Libro con los nuevos atributos
        libro = Libro(codigo_isbn, titulo, genero, anio_publicacion, autor, cantidad)

        # Aquí deberías llamar a un método en tu servicio de base de datos para insertar estos datos
        if libro:
            # Usando un método de biblioteca para insertar el autor en la base de datos
            try:
                libro_service = LibroService(self.db)
                libro_service.registrar_libro(libro)
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


    def save_prestamo(self):
        print("Préstamo guardado")
        self.prestamo_form_frame.pack_forget()
