import customtkinter as ctk
from auth import AuthManager
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