# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: gui_login.py
# Descripción: Interfaz gráfica de inicio de sesión
# ===================================================================
import customtkinter as ctk
from auth import AuthManager
from gui_admin import AdminWindow  # Cambiado de Dashboard a AdminWindow
from tkinter import messagebox
from PIL import Image, ImageDraw
import os

# Constantes para diseño mejorado
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
TITLE_FONT = ("Segoe UI", 32, "bold")
SUBTITLE_FONT = ("Segoe UI", 14)
LABEL_FONT = ("Segoe UI", 13)
BUTTON_FONT = ("Segoe UI", 16, "bold")
ENTRY_WIDTH = 350
ENTRY_HEIGHT = 45
BUTTON_WIDTH = 350
BUTTON_HEIGHT = 50

# Paleta de colores
COLOR_AMARILLO = "#FFD700"
COLOR_AMARILLO_HOVER = "#FFC700"
COLOR_GRIS_OSCURO = "#2B2B2B"
COLOR_GRIS_MEDIO = "#3D3D3D"
COLOR_GRIS_CLARO = "#505050"
COLOR_NEGRO = "#1A1A1A"
COLOR_BLANCO = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Activar pantalla completa al inicio
        self.attributes('-fullscreen', True)
        
        # Conexión con el gestor de autenticación
        self.auth = AuthManager()
        
        # Configuración básica de la ventana
        self.title("CONTROL INDUSTRIAL - INICIO DE SESIÓN")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        # Configuración de apariencia
        ctk.set_appearance_mode("dark")
        
        # Centrar ventana en pantalla
        self.center_window()
        
        # Crear imagen de placeholder si no existe
        self.create_placeholder_image()
        
        # Crear el layout principal
        self.create_ui()
        
        # Enfocar el campo de usuario al iniciar
        self.entry_user.focus_set()
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_placeholder_image(self):
        """Crear una imagen de placeholder si no existe login_image.png"""
        if not os.path.exists("login_image.png"):
            # Crear una imagen moderna con degradado
            img = Image.new('RGB', (500, 600), COLOR_GRIS_OSCURO)
            draw = ImageDraw.Draw(img)
            
            # Agregar elementos visuales
            # Círculos decorativos
            draw.ellipse([50, 100, 200, 250], fill=COLOR_AMARILLO, outline=COLOR_AMARILLO)
            draw.ellipse([300, 350, 450, 500], fill=COLOR_GRIS_CLARO, outline=COLOR_GRIS_CLARO)
            draw.ellipse([100, 400, 180, 480], fill=COLOR_AMARILLO, outline=COLOR_AMARILLO)
            
            img.save("login_image.png")
    
    def create_ui(self):
        # Contenedor principal que divide la pantalla
        main_container = ctk.CTkFrame(self, fg_color=COLOR_NEGRO, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # ========== LADO IZQUIERDO - IMAGEN ==========
        left_frame = ctk.CTkFrame(main_container, fg_color=COLOR_GRIS_OSCURO, corner_radius=0, width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)
        
        # Cargar y mostrar imagen
        try:
            img = Image.open("login_image.png")
            img = img.resize((700, 800), Image.Resampling.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(800, 700))
            
            img_label = ctk.CTkLabel(left_frame, image=photo_img, text="")
            img_label.pack(fill="both", expand=True)
        except:
            # Si no se puede cargar la imagen, mostrar un frame con texto
            branding_frame = ctk.CTkFrame(left_frame, fg_color=COLOR_GRIS_OSCURO)
            branding_frame.pack(fill="both", expand=True, padx=40, pady=40)
            
            ctk.CTkLabel(
                branding_frame, 
                text="🏭", 
                font=("Segoe UI", 120),
                text_color=COLOR_AMARILLO
            ).pack(expand=True)
            
            ctk.CTkLabel(
                branding_frame, 
                text="INDUSTRIA 4.0", 
                font=("Segoe UI", 36, "bold"),
                text_color=COLOR_AMARILLO
            ).pack(pady=20)
            
            ctk.CTkLabel(
                branding_frame, 
                text="Sistema de Control\nIndustrial Avanzado", 
                font=("Segoe UI", 16),
                text_color=COLOR_TEXTO_SECUNDARIO,
                justify="center"
            ).pack()
        
        # ========== LADO DERECHO - FORMULARIO LOGIN ==========
        right_frame = ctk.CTkFrame(main_container, fg_color=COLOR_NEGRO, corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Frame interno para centrar el formulario
        login_frame = ctk.CTkFrame(right_frame, fg_color=COLOR_NEGRO)
        login_frame.pack(expand=True, pady=50)
        
        # Título principal
        self.label_titulo = ctk.CTkLabel(
            login_frame, 
            text="Iniciar Sesión", 
            font=TITLE_FONT,
            text_color=COLOR_AMARILLO
        )
        self.label_titulo.pack(pady=(0, 10))
        
        # Subtítulo
        self.label_subtitulo = ctk.CTkLabel(
            login_frame, 
            text="Ingrese sus credenciales para continuar", 
            font=SUBTITLE_FONT,
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        self.label_subtitulo.pack(pady=(0, 40))
        
        # Label Usuario
        label_user = ctk.CTkLabel(
            login_frame,
            text="USUARIO",
            font=LABEL_FONT,
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        label_user.pack(anchor="w", pady=(0, 5))
        
        # Campo de usuario
        self.entry_user = ctk.CTkEntry(
            login_frame, 
            placeholder_text="Ingrese su usuario",
            width=ENTRY_WIDTH, 
            height=ENTRY_HEIGHT, 
            font=LABEL_FONT,
            fg_color=COLOR_GRIS_MEDIO,
            border_color=COLOR_GRIS_CLARO,
            border_width=2,
            text_color=COLOR_BLANCO,
            placeholder_text_color=COLOR_TEXTO_SECUNDARIO
        )
        self.entry_user.pack(pady=(0, 20))
        
        # Label Password
        label_pass = ctk.CTkLabel(
            login_frame,
            text="CONTRASEÑA",
            font=LABEL_FONT,
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        label_pass.pack(anchor="w", pady=(0, 5))
        
        # Campo de password
        self.entry_pass = ctk.CTkEntry(
            login_frame, 
            placeholder_text="Ingrese su contraseña",
            show="●", 
            width=ENTRY_WIDTH, 
            height=ENTRY_HEIGHT, 
            font=LABEL_FONT,
            fg_color=COLOR_GRIS_MEDIO,
            border_color=COLOR_GRIS_CLARO,
            border_width=2,
            text_color=COLOR_BLANCO,
            placeholder_text_color=COLOR_TEXTO_SECUNDARIO
        )
        self.entry_pass.pack(pady=(0, 15))
        
        # Etiqueta para mensajes de error
        self.error_label = ctk.CTkLabel(
            login_frame, 
            text="", 
            text_color="#FF4444", 
            font=LABEL_FONT,
            wraplength=ENTRY_WIDTH
        )
        self.error_label.pack(pady=(5, 20))
        
        # Botón de entrada con estilo amarillo
        self.btn_login = ctk.CTkButton(
            login_frame, 
            text="ENTRAR", 
            command=self.intentar_login, 
            width=BUTTON_WIDTH, 
            height=BUTTON_HEIGHT, 
            font=BUTTON_FONT,
            fg_color=COLOR_AMARILLO,
            hover_color=COLOR_AMARILLO_HOVER,
            text_color=COLOR_NEGRO,
            corner_radius=8
        )
        self.btn_login.pack(pady=(0, 20))
        
        # Footer con información adicional
        footer_label = ctk.CTkLabel(
            login_frame,
            text="¿Olvidó su contraseña? Contacte al administrador",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        footer_label.pack(pady=(20, 0))
        
        # Bind para Enter en campos
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus_set())
        self.entry_pass.bind("<Return>", lambda e: self.intentar_login())
    
    def intentar_login(self):
        # Limpiar mensaje de error previo
        self.error_label.configure(text="")
        
        u = self.entry_user.get().strip()
        p = self.entry_pass.get().strip()
        
        # Validaciones básicas
        if not u or not p:
            self.error_label.configure(text="⚠ Por favor, complete todos los campos.")
            return
        
        # Cambiar botón a estado de carga
        self.btn_login.configure(state="disabled", text="VERIFICANDO...", fg_color=COLOR_GRIS_CLARO)
        self.update()
        
        try:
            # Llamada a la lógica de auth.py
            exito, mensaje = self.auth.verificar_acceso(u, p)
            
            if exito:
                # Si el login es correcto, cerramos esta ventana
                self.destroy()
                # Abrimos la ventana de Administración
                app_admin = AdminWindow()
                app_admin.mainloop()
            else:
                self.error_label.configure(text=f"⚠ {mensaje}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
        finally:
            # Restaurar botón
            self.btn_login.configure(state="normal", text="ENTRAR", fg_color=COLOR_AMARILLO)

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()