# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: gui_login.py
# Descripción: Interfaz gráfica de inicio de sesión
# ===================================================================

import customtkinter as ctk
from auth import AuthManager
from gui_dashboard import Dashboard
from tkinter import messagebox
from gui_admin import AdminWindow

# CONFIGURACION GLOBAL DEL TEMA VISUAL
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema azul

class LoginWindow(ctk.CTk):
    """
    VENTANA DE INICIO DE SESION
    Permite a los usuarios autenticarse para acceder al sistema
    """
    
    def __init__(self):
        """CONSTRUCTOR: Configura la ventana de login"""
        super().__init__()
        
        # INICIALIZAR GESTOR DE AUTENTICACION
        self.auth = AuthManager()
        
        # CONFIGURACION DE LA VENTANA
        self.title("CONTROL INDUSTRIAL - INICIO DE SESIÓN")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # CREAR INTERFAZ GRAFICA
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """CREA TODOS LOS ELEMENTOS VISUALES DE LA VENTANA"""
        
        # TITULO PRINCIPAL
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="INDUSTRIA 4.0", 
            font=("Roboto", 26, "bold")
        )
        self.label_titulo.pack(pady=(50, 30))
        
        # CAMPO DE USUARIO
        self.entry_user = ctk.CTkEntry(
            self, 
            placeholder_text="USUARIO", 
            width=250, 
            height=35
        )
        self.entry_user.pack(pady=10)
        
        # CAMPO DE CONTRASEÑA
        self.entry_pass = ctk.CTkEntry(
            self, 
            placeholder_text="CONTRASEÑA", 
            show="*", 
            width=250, 
            height=35
        )
        self.entry_pass.pack(pady=10)
        
        # BOTON DE ACCESO
        self.btn_login = ctk.CTkButton(
            self, 
            text="ENTRAR", 
            command=self.intentar_login, 
            width=250, 
            height=40
        )
        self.btn_login.pack(pady=40)
        
        # PERMITIR LOGIN CON ENTER
        self.bind('<Return>', lambda event: self.intentar_login())
        self.entry_user.bind('<Return>', lambda event: self.entry_pass.focus())
        self.entry_pass.bind('<Return>', lambda event: self.intentar_login())
        
    def intentar_login(self):
        """
        PROCESA EL INTENTO DE INICIO DE SESION
        Valida credenciales y abre el dashboard si son correctas
        """
        # OBTENER DATOS INGRESADOS
        usuario = self.entry_user.get()
        password = self.entry_pass.get()
        
        # VALIDAR CON EL GESTOR DE AUTENTICACION
        exito, resultado = self.auth.verificar_acceso(usuario, password)
        
        if exito:
            self.destroy()  # Cerrar ventana de login
            #SI ES ADMIN, SE APERTURA LA VISTA ADMIN
            if resultado == "administrador":
                app_dashboard = AdminWindow() 
            else:    
                app_dashboard = Dashboard()
                
            app_dashboard.mainloop()
        else:
            # LOGIN FALLIDO: Mostrar error
            messagebox.showerror("Error de Acceso", resultado)
            # Limpiar campos para nuevo intento
            self.entry_pass.delete(0, 'end')
            self.entry_user.focus()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()