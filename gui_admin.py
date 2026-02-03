import customtkinter as ctk
from tkinter import messagebox
from database import Database

# Paleta de colores consistente
COLOR_AMARILLO = "#FFD700"
COLOR_AMARILLO_HOVER = "#FFC700"
COLOR_GRIS_OSCURO = "#2B2B2B"
COLOR_GRIS_MEDIO = "#3D3D3D"
COLOR_GRIS_CLARO = "#505050"
COLOR_NEGRO = "#1A1A1A"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"
COLOR_VERDE = "#00FF88"
COLOR_ROJO = "#FF4444"
COLOR_NARANJA = "#FF8C00"
COLOR_AZUL = "#3498DB"

class AdminWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        self.usuario_seleccionado_id = None  # Para saber si estamos editando
        
        # CONFIGURACIÓN DE VENTANA
        self.title("SISTEMA INDUSTRIAL 4.0 - ADMINISTRACIÓN DE USUARIOS")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Configuración de apariencia
        ctk.set_appearance_mode("dark")
        
        # Centrar ventana
        self.center_window()
        
        self.setup_ui()
        self.cargar_usuarios()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        # FRAME PRINCIPAL
        main_container = ctk.CTkFrame(self, fg_color=COLOR_NEGRO, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # ========== HEADER ==========
        header_frame = ctk.CTkFrame(main_container, fg_color=COLOR_GRIS_OSCURO, height=80, corner_radius=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame, 
            text="👥 GESTIÓN DE USUARIOS", 
            font=("Segoe UI", 32, "bold"), 
            text_color=COLOR_AMARILLO
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        # Botón volver
        self.btn_volver = ctk.CTkButton(
            header_frame, 
            text="← VOLVER AL LOGIN", 
            command=self.ir_al_login,
            fg_color=COLOR_GRIS_CLARO, 
            hover_color=COLOR_AMARILLO,
            width=180,
            height=40,
            font=("Segoe UI", 13, "bold")
        )
        self.btn_volver.pack(side="right", padx=30, pady=20)
        
        # ========== CONTENIDO ==========
        content_frame = ctk.CTkFrame(main_container, fg_color=COLOR_NEGRO)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ========== SECCIÓN FORMULARIO ==========
        form_section = ctk.CTkFrame(content_frame, fg_color=COLOR_GRIS_OSCURO, corner_radius=15)
        form_section.pack(fill="x", pady=(0, 20))
        
        # Título de sección
        ctk.CTkLabel(
            form_section,
            text="FORMULARIO DE USUARIO",
            font=("Segoe UI", 20, "bold"),
            text_color=COLOR_AMARILLO
        ).pack(pady=(25, 20))
        
        # Frame para el formulario
        self.frame_form = ctk.CTkFrame(form_section, fg_color="transparent")
        self.frame_form.pack(pady=(0, 25), padx=40)
        
        # Campo Nombre de Usuario
        ctk.CTkLabel(
            self.frame_form,
            text="NOMBRE DE USUARIO",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5), padx=10)
        
        self.entry_nombre = ctk.CTkEntry(
            self.frame_form, 
            placeholder_text="Ingrese el nombre de usuario",
            width=250,
            height=40,
            font=("Segoe UI", 13),
            fg_color=COLOR_GRIS_MEDIO,
            border_color=COLOR_GRIS_CLARO,
            border_width=2
        )
        self.entry_nombre.grid(row=1, column=0, padx=10, pady=(0, 15))
        
        # Campo Contraseña
        ctk.CTkLabel(
            self.frame_form,
            text="CONTRASEÑA",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).grid(row=0, column=1, sticky="w", pady=(0, 5), padx=10)
        
        self.entry_pass = ctk.CTkEntry(
            self.frame_form, 
            placeholder_text="Ingrese la contraseña",
            show="●",
            width=250,
            height=40,
            font=("Segoe UI", 13),
            fg_color=COLOR_GRIS_MEDIO,
            border_color=COLOR_GRIS_CLARO,
            border_width=2
        )
        self.entry_pass.grid(row=1, column=1, padx=10, pady=(0, 15))
        
        # Campo Rol
        ctk.CTkLabel(
            self.frame_form,
            text="ROL DE USUARIO",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        ).grid(row=0, column=2, sticky="w", pady=(0, 5), padx=10)
        
        self.combo_rol = ctk.CTkOptionMenu(
            self.frame_form, 
            values=["operador", "admin"],
            width=200,
            height=40,
            font=("Segoe UI", 13),
            fg_color=COLOR_GRIS_MEDIO,
            button_color=COLOR_AMARILLO,
            button_hover_color=COLOR_AMARILLO_HOVER,
            dropdown_fg_color=COLOR_GRIS_MEDIO
        )
        self.combo_rol.grid(row=1, column=2, padx=10, pady=(0, 15))
        
        # Frame para botones de acción
        buttons_frame = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(
            buttons_frame, 
            text="✓ REGISTRAR USUARIO", 
            command=self.guardar_usuario,
            fg_color=COLOR_VERDE,
            hover_color="#00DD70",
            text_color=COLOR_NEGRO,
            width=250,
            height=45,
            font=("Segoe UI", 15, "bold"),
            corner_radius=8
        )
        self.btn_guardar.pack(side="left", padx=10)
        
        # Botón Limpiar
        self.btn_limpiar = ctk.CTkButton(
            buttons_frame, 
            text="⟲ LIMPIAR FORMULARIO", 
            command=self.limpiar_campos,
            fg_color=COLOR_GRIS_CLARO,
            hover_color=COLOR_GRIS_MEDIO,
            width=250,
            height=45,
            font=("Segoe UI", 15, "bold"),
            corner_radius=8
        )
        self.btn_limpiar.pack(side="left", padx=10)
        
        # ========== SECCIÓN LISTA DE USUARIOS ==========
        list_section = ctk.CTkFrame(content_frame, fg_color=COLOR_GRIS_OSCURO, corner_radius=15)
        list_section.pack(fill="both", expand=True)
        
        # Título de sección
        ctk.CTkLabel(
            list_section,
            text="USUARIOS REGISTRADOS EN EL SISTEMA",
            font=("Segoe UI", 20, "bold"),
            text_color=COLOR_AMARILLO
        ).pack(pady=(25, 15))
        
        # Frame scrollable para la lista
        self.lista_usuarios_frame = ctk.CTkScrollableFrame(
            list_section,
            fg_color=COLOR_GRIS_MEDIO,
            corner_radius=10,
            border_width=2,
            border_color=COLOR_GRIS_CLARO
        )
        self.lista_usuarios_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

    def cargar_usuarios(self):
        """Limpia la lista y la vuelve a llenar desde la DB"""
        # Limpiar widgets previos en el frame de la lista
        for widget in self.lista_usuarios_frame.winfo_children():
            widget.destroy()

        usuarios = self.db.obtener_usuarios()
        
        if not usuarios:
            # Mensaje si no hay usuarios
            ctk.CTkLabel(
                self.lista_usuarios_frame,
                text="No hay usuarios registrados en el sistema",
                font=("Segoe UI", 14),
                text_color=COLOR_TEXTO_SECUNDARIO
            ).pack(pady=20)
            return
        
        for user in usuarios:
            user_id, nombre, rol = user
            
            # Tarjeta de usuario
            fila = ctk.CTkFrame(
                self.lista_usuarios_frame,
                fg_color=COLOR_GRIS_OSCURO,
                corner_radius=10,
                border_width=2,
                border_color=COLOR_GRIS_CLARO
            )
            fila.pack(fill="x", pady=8, padx=10)
            
            # Icono según el rol
            icono = "👑" if rol == "admin" else "👤"
            color_rol = COLOR_AMARILLO if rol == "admin" else COLOR_TEXTO_SECUNDARIO
            
            # Frame izquierdo con info
            info_frame = ctk.CTkFrame(fila, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            
            # Nombre del usuario
            ctk.CTkLabel(
                info_frame,
                text=f"{icono}  {nombre}",
                font=("Segoe UI", 16, "bold"),
                text_color=COLOR_BLANCO,
                anchor="w"
            ).pack(side="left")
            
            # Etiqueta de rol
            rol_label = ctk.CTkLabel(
                info_frame,
                text=rol.upper(),
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_NEGRO,
                fg_color=color_rol,
                corner_radius=5,
                width=80,
                height=25
            )
            rol_label.pack(side="left", padx=15)
            
            # Frame derecho con botones
            buttons_frame = ctk.CTkFrame(fila, fg_color="transparent")
            buttons_frame.pack(side="right", padx=15, pady=8)
            
            # Botón Editar
            ctk.CTkButton(
                buttons_frame,
                text="✎ Editar",
                fg_color=COLOR_AZUL,
                hover_color="#2980B9",
                width=100,
                height=35,
                font=("Segoe UI", 13, "bold"),
                corner_radius=6,
                command=lambda u=user: self.preparar_edicion(u)
            ).pack(side="left", padx=5)
            
            # Botón Eliminar
            ctk.CTkButton(
                buttons_frame,
                text="🗑 Eliminar",
                fg_color=COLOR_ROJO,
                hover_color="#C0392B",
                width=100,
                height=35,
                font=("Segoe UI", 13, "bold"),
                corner_radius=6,
                command=lambda i=user_id: self.eliminar(i)
            ).pack(side="left", padx=5)

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        password = self.entry_pass.get()
        rol = self.combo_rol.get()

        if not nombre or not password:
            messagebox.showwarning("Atención", "Completa todos los campos")
            return

        if self.usuario_seleccionado_id:
            # ACTUALIZAR
            exito, msg = self.db.actualizar_usuario(self.usuario_seleccionado_id, nombre, password, rol)
        else:
            # CREAR
            exito, msg = self.db.agregar_usuario(nombre, password, rol)

        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", msg)

    def preparar_edicion(self, datos_user):
        self.usuario_seleccionado_id, nombre, rol = datos_user
        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, nombre)
        self.combo_rol.set(rol)
        self.btn_guardar.configure(
            text="💾 GUARDAR CAMBIOS",
            fg_color=COLOR_NARANJA,
            hover_color="#FF7700"
        )

    def eliminar(self, user_id):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este usuario?"):
            self.db.eliminar_usuario(user_id)
            self.cargar_usuarios()

    def limpiar_campos(self):
        self.usuario_seleccionado_id = None
        self.entry_nombre.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.btn_guardar.configure(
            text="✓ REGISTRAR USUARIO",
            fg_color=COLOR_VERDE,
            hover_color="#00DD70"
        )

    def ir_al_login(self):
        self.destroy()
        from gui_login import LoginWindow
        app = LoginWindow()
        app.mainloop()

# Activar pantalla completa al inicio
        self.attributes('-fullscreen', True)

if __name__ == "__main__":
    app = AdminWindow()
    app.mainloop()