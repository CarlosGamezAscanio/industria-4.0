import customtkinter as ctk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database


class GestorRecurrencias(ctk.CTkToplevel):
    """VENTANA PARA MOSTRAR HISTORIAL DE RECURRENCIAS"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self.title("HISTORIAL DE RECURRENCIAS")
        self.geometry("900x600")
        self.transient(parent)
        self.grab_set()
        
        titulo = ctk.CTkLabel(self, text="HISTORIAL DE ALERTAS", font=("Roboto", 20, "bold"))
        titulo.pack(pady=20)
        
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=20)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B")
        style.configure("Treeview.Heading", background="#1F538D", foreground="white")
        
        columnas = ("ID", "Fecha", "Temperatura", "Presion", "Estado")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Temperatura", text="Temp (°C)")
        self.tree.heading("Presion", text="Presion (PSI)")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50)
        self.tree.column("Fecha", width=150)
        self.tree.column("Temperatura", width=150)
        self.tree.column("Presion", width=150)
        self.tree.column("Estado", width=100)
        
        self.tree.tag_configure("ALERTA", background="#E74C3C", foreground="white")
        self.tree.tag_configure("NORMAL", background="#2ECC71", foreground="white")
        
        self.tree.pack(fill="both", expand=True)
        
        self.cargar_datos()
        
        btn_cerrar = ctk.CTkButton(self, text="CERRAR", command=self.destroy, fg_color="#E74C3C")
        btn_cerrar.pack(pady=20)
    
    def cargar_datos(self):
        registros = self.db.obtener_historial_completo()
        for reg in registros:
            id_reg, fecha, temp, pres, estado = reg
            self.tree.insert("", "end", values=(id_reg, fecha, temp, pres, estado), tags=(estado,))
