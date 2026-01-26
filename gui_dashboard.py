# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: gui_dashboard.py
# Descripción: Panel principal de monitoreo simplificado
# ===================================================================

import customtkinter as ctk
from tkinter import messagebox
from simulator import SimuladorSensor
from database import Database
from ventanas_analisis import VentanaRegistro, VentanaGrafica

class Dashboard(ctk.CTk):
    """
    PANEL PRINCIPAL DE MONITOREO
    Muestra datos en tiempo real, gestiona alertas y proporciona
    acceso a historial y gráficas de temperatura
    """
    
    def __init__(self):
        """CONSTRUCTOR: Inicializa el dashboard y sus componentes"""
        super().__init__()
        
        # CONFIGURACION DE LA VENTANA
        self.title("SISTEMA INDUSTRIAL 4.0")
        self.geometry("600x550")
        
        # INICIALIZAR HERRAMIENTAS
        self.simulador = SimuladorSensor()
        self.db = Database()
        self.sensor_container = None  # Contenedor de sensores
        
        # CREAR INTERFAZ Y INICIAR MONITOREO
        self.setup_ui()
        self.after(1000, self.actualizar_automaticamente)  # Iniciar después de 1 segundo

    def setup_ui(self):
        """CONSTRUYE LA INTERFAZ GRAFICA DEL DASHBOARD"""
        
        # CONFIGURACION DE GRID
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # FRAME PRINCIPAL
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, width=580, height=530)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.main_frame.grid_propagate(False)

        # TITULO DEL PANEL
        self.lbl_titulo = ctk.CTkLabel(
            self.main_frame, 
            text="PANEL DE CONTROL", 
            font=("Roboto", 28, "bold")
        )
        self.lbl_titulo.pack(pady=(20, 10))

        # CONTENEDOR DE DATOS DE SENSORES
        self.sensor_container = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#212121", 
            border_width=2, 
            border_color="#34495E"
        )
        self.sensor_container.pack(fill="x", padx=40, pady=20, ipady=40)

        # INDICADOR DE ESTADO DEL SISTEMA
        self.lbl_status = ctk.CTkLabel(
            self.sensor_container, 
            text="● SISTEMA EN VIVO", 
            text_color="#00FFFF", 
            font=("Roboto", 14, "bold")
        )
        self.lbl_status.pack(pady=(15, 0))

        # DISPLAY DE TEMPERATURA
        self.lbl_temp = ctk.CTkLabel(
            self.sensor_container, 
            text="-- °C", 
            font=("Roboto", 20, "bold")
        )
        self.lbl_temp.pack(pady=10)

        # DISPLAY DE PRESION
        self.lbl_pres = ctk.CTkLabel(
            self.sensor_container, 
            text="-- PSI", 
            font=("Roboto", 20, "bold")
        )
        self.lbl_pres.pack(pady=10)

        # FRAME PARA BOTONES DE FUNCIONES
        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_botones.pack(pady=20)

        # BOTON PARA VER REGISTRO TABULAR
        self.btn_registro = ctk.CTkButton(
            frame_botones,
            text="📊 VER REGISTRO",
            command=self.mostrar_registro_temperatura,
            width=200,
            height=40,
            fg_color="#16A085",
            hover_color="#138D75"
        )
        self.btn_registro.pack(side="left", padx=10)

        # BOTON PARA VER GRAFICA
        self.btn_grafica = ctk.CTkButton(
            frame_botones,
            text="📈 VER GRÁFICA",
            command=self.mostrar_grafica_temperatura,
            width=200,
            height=40,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        self.btn_grafica.pack(side="left", padx=10)

        # BOTON CERRAR SESION
        self.btn_salir = ctk.CTkButton(
            self.main_frame, 
            text="CERRAR SESIÓN", 
            command=self.destroy,
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            width=200
        )
        self.btn_salir.pack(side="bottom", pady=20)

    def actualizar_automaticamente(self):
        """
        CICLO DE ACTUALIZACION AUTOMATICA
        Se ejecuta cada 2 segundos para actualizar los datos
        """
        self.actualizar_datos()
        self.after(2000, self.actualizar_automaticamente)  # Repetir cada 2 segundos

    def actualizar_datos(self):
        """
        ACTUALIZA LOS DATOS DE LOS SENSORES Y LA INTERFAZ
        Lee sensores, guarda en BD y actualiza displays
        """
        # VERIFICAR QUE LA INTERFAZ ESTE LISTA
        if self.sensor_container is None:
            return

        # LEER DATOS DE LOS SENSORES
        temp, pres, estado_sim = self.simulador.leer_sensores()
        
        # GUARDAR EN BASE DE DATOS
        self.db.guardar_lectura(temp, pres, estado_sim)
        
        # ACTUALIZAR DISPLAYS
        self.lbl_temp.configure(text=f"{temp} °C")
        self.lbl_pres.configure(text=f"{pres} PSI")

        # LOGICA DE ALERTAS Y COLORES
        if temp > 90 or pres > 40:
            # ESTADO DE ALERTA: Valores críticos
            color_alerta = "#FF4444"
            self.lbl_temp.configure(text_color=color_alerta)
            self.lbl_pres.configure(text_color=color_alerta)
            self.lbl_status.configure(text="● ALERTA DE SISTEMA", text_color=color_alerta)
            self.sensor_container.configure(border_color=color_alerta)
            
            # MOSTRAR ALERTA AL USUARIO
            self.update_idletasks()
            messagebox.showwarning(
                "⚠️ ALERTA", 
                f"Valores Críticos:\nTemp: {temp}°C\nPres: {pres} PSI"
            )
        else:
            # ESTADO NORMAL: Valores dentro de rango
            color_normal = "#2ECC71"
            self.lbl_temp.configure(text_color=color_normal)
            self.lbl_pres.configure(text_color=color_normal)
            self.lbl_status.configure(text="● MONITOREO EN PROCESO", text_color="yellow")
            self.sensor_container.configure(border_color="#34495E")
    
    def mostrar_registro_temperatura(self):
        """
        ABRE VENTANA CON TABLA DE HISTORIAL DE TEMPERATURA
        Utiliza el módulo ventanas_analisis
        """
        try:
            VentanaRegistro(self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro:\n{str(e)}")
    
    def mostrar_grafica_temperatura(self):
        """
        ABRE VENTANA CON GRAFICA INTERACTIVA DE TEMPERATURA
        Utiliza el módulo ventanas_analisis
        """
        try:
            VentanaGrafica(self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la gráfica:\n{str(e)}")

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
