import customtkinter as ctk
from auth import AuthManager
from gui_dashboard import Dashboard
from tkinter import messagebox

#CONFIGURACION DEL ESTILO VISUAL
ctk.set_appearance_mode("dark")#MODO OBSCURO
ctk.set_default_color_theme("blue")#COLOR BOTONES

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #CONEXION CON EL GUARDIAN DE ACCESO AUTH.PY
        self.auth = AuthManager()
        
        #CONFIGURACION BASICA DE LA VENTANA
        self.title("CONTROL INDUSTRIAL - INICIO DE SESION")
        self.geometry("400x450")
        self.resizable(False, False)
        
        #CREACION DE ELEMENTOS VISUALES (WIDGETS)
        self.label_titulo = ctk.CTkLabel(self, text="INDUSTRIA 4.0", font=("Roboto",26 , "bold"))
        self.label_titulo.pack(pady=(50,30))
        
        #CAMPO DE USUARIO
        self.entry_user = ctk.CTkEntry(self, placeholder_text="USUARIO", width=250, height=35)
        self.entry_user.pack(pady=10)
        
        #CAMPO DE PASSWORD
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="PASSWORD", show="*", width=250, height=35)
        self.entry_pass.pack(pady=10)
        
        #BOTON DE ENTRADA
        self.btn_login = ctk.CTkButton(self, text="ENTRAR", command=self.intentar_login, width=250, height=40)
        self.btn_login.pack(pady=40)
        
    def intentar_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        
        #LLAMADA A LA LOGICA DE AUTH.PY
        exito, mensaje = self.auth.verificar_acceso(u, p)
        
        if exito:
            #SI EL LOGIN ES CORRECTO, CERRAMOS ESTA VENTANA
            self.destroy()
            #ABRIMOS EL DASHBOARD (LA VENTANA DE SIMULACION)
            app_dashboard = Dashboard()
            app_dashboard.mainloop()
        
        else:
            messagebox.showerror("ERROR DE ACCESO, VERIFIQUE", mensaje)
            
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()