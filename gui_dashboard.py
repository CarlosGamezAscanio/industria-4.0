import customtkinter as ctk
from tkinter import messagebox
from simulator import SimuladorSensor
from database import Database

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SISTEMA INDUSTRIAL 4.0")
        self.geometry("600x650") # Un poco más alto para el nuevo diseño
        
        # 1. Herramientas
        self.simulador = SimuladorSensor()
        self.db = Database()

        # 2. Inicializar variables de UI como None para evitar el AttributeError
        self.sensor_container = None
        
        # 3. Dibujar Interfaz
        self.setup_ui()

        # 4. Iniciar monitoreo con un pequeño retraso
        self.after(1000, self.actualizar_automaticamente)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=15, width=580, height=580)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        self.main_frame.grid_propagate(False)

        self.lbl_titulo = ctk.CTkLabel(self.main_frame, text="PANEL DE CONTROL", font=("Roboto", 28, "bold"))
        self.lbl_titulo.pack(pady=(20, 10))

        # --- AQUÍ DEFINIMOS EL CONTENEDOR CORRECTAMENTE ---
        self.sensor_container = ctk.CTkFrame(self.main_frame, 
                                            fg_color="#212121", 
                                            border_width=2, 
                                            border_color="#34495E")
        self.sensor_container.pack(fill="x", padx=40, pady=20, ipady=40)

        self.lbl_status = ctk.CTkLabel(self.sensor_container, text="● SISTEMA EN VIVO", 
                                       text_color="#00FFFF", font=("Roboto", 14, "bold"))
        self.lbl_status.pack(pady=(15, 0))

        self.lbl_temp = ctk.CTkLabel(self.sensor_container, text="-- °C", font=("Roboto", 20, "bold"))
        self.lbl_temp.pack(pady=10)

        self.lbl_pres = ctk.CTkLabel(self.sensor_container, text="-- PSI", font=("Roboto", 20, "bold"))
        self.lbl_pres.pack(pady=10)

        self.btn_salir = ctk.CTkButton(self.main_frame, text="CERRAR SESIÓN", command=self.destroy,
                                       fg_color="#E74C3C", hover_color="#C0392B", width=200)
        self.btn_salir.pack(side="bottom", pady=20)

    def actualizar_automaticamente(self):
        self.actualizar_datos()
        self.after(2000, self.actualizar_automaticamente)

    def actualizar_datos(self):
        # Seguridad: Si por alguna razón el container no se ha creado, no hacemos nada
        if self.sensor_container is None:
            return

        temp, pres, estado_sim = self.simulador.leer_sensores()
        self.db.guardar_lectura(temp, pres, estado_sim)
        
        self.lbl_temp.configure(text=f"{temp} °C")
        self.lbl_pres.configure(text=f"{pres} PSI")

        # Lógica de Alerta Combinada
        if temp > 90 or pres > 40:
            color = "#FF4444"
            self.lbl_temp.configure(text_color=color)
            self.lbl_pres.configure(text_color=color)
            self.lbl_status.configure(text="● ALERTA DE SISTEMA", text_color=color)
            self.sensor_container.configure(border_color=color)
            
            self.update_idletasks()
            messagebox.showwarning("⚠️ ALERTA", f"Valores Críticos:\nTemp: {temp}°C\nPres: {pres} PSI")
        else:
            color_ok = "#2ECC71"
            self.lbl_temp.configure(text_color=color_ok)
            self.lbl_pres.configure(text_color=color_ok)
            self.lbl_status.configure(text="● MONITOREO EN PROCESO", text_color="yellow")
            self.sensor_container.configure(border_color="#34495E")

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()