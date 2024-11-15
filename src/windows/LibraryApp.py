import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.BibliotecaService import BibliotecaService
from classes.Autor import Autor
from classes.Libro import Libro
from classes.Usuario import Usuario, Estudiante, Profesor
from services.UsuarioService import UsuarioService
from classes.Prestamo import Prestamo
from services.LibroService import LibroService
from services.AutorService import AutorService
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageEnhance, ImageDraw


class LibraryApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("BibliotecApp")
        self.geometry("1950x1024")
        self.iconbitmap(r"C:/Users/Usuario/Desktop/TPDAO2/TPI-DAO-4K1/src/images/logo_app.ico")


        # Cargar y colocar la imagen de fondo con transparencia
        background_image = Image.open(r"C:/Users/Usuario/Desktop/TPDAO2/TPI-DAO-4K1/src/images/fondo.jpg")
        background_image = background_image.resize((1950, 1024), Image.LANCZOS)
        background_image = self.apply_transparency(background_image, alpha=0.4)
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        tk.Label(self, text="BibliotecApp", font=("Helvetica", 26, "bold")).pack(pady=20)

        # Botones de opciones redondeados con color personalizado
        self.create_rounded_button("Autores", self.abrir_autores, "#DA9A9A").pack(pady=15)
        self.create_rounded_button("Usuarios", self.abrir_usuarios, "#DA9A9A").pack(pady=15)
        self.create_rounded_button("Libros", self.abrir_libros, "#DA9A9A").pack(pady=15)
        self.create_rounded_button("Reportes", self.abrir_reportes, "#DA9A9A").pack(pady=15)

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
                nacionalidades = ["Argentina", "Chile", "Brasil", "Uruguay", "Paraguay", "Bolivia", "Perú"]
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
        ventana_libros.title("Libros")
        ventana_libros.geometry("400x300")
        tk.Label(ventana_libros, text="Gestión de Libros", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(ventana_libros, text="Volver", command=ventana_libros.destroy).pack(pady=10)

    def abrir_reportes(self):
        ventana_reportes = tk.Toplevel(self)
        ventana_reportes.title("Reportes")
        ventana_reportes.geometry("400x300")
        tk.Label(ventana_reportes, text="Gestión de Reportes", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(ventana_reportes, text="Volver", command=ventana_reportes.destroy).pack(pady=10)

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
