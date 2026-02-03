# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: gui_dashboard.py
# Descripción: Panel principal de monitoreo corregido
# ===================================================================

import customtkinter as ctk
from tkinter import messagebox
# Importamos las constantes del simulador para no tener números mágicos
from simulator import SimuladorSensor, TEMP_MAX_ALERTA, TEMP_MIN_ALERTA, PRESS_MAX_ALERTA, PRESS_MIN_ALERTA
from database import Database
from ventanas_analisis import VentanaRegistro, VentanaGrafica
from PIL import Image

# Paleta de colores 
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
COLOR_AZUL = "#3498DB" # Agregado para temperaturas bajas

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # CONFIGURACION DE LA VENTANA
        self.title("SISTEMA INDUSTRIAL 4.0 - PANEL DE CONTROL")
        self.geometry("1200x700")
        self.resizable(True, True)  # Permitir redimensionar
        ctk.set_appearance_mode("dark")
        
        # Vincular tecla F11 para alternar pantalla completa
        self.bind("<F11>", self.toggle_fullscreen)
        # Vincular tecla Escape para salir de pantalla completa
        self.bind("<Escape>", self.exit_fullscreen)
        
        self.is_fullscreen = True
        
        # INICIALIZAR HERRAMIENTAS
        self.simulador = SimuladorSensor()
        self.db = Database()
        
        # --- CONTROL DE ALERTAS (Para evitar spam de popups) ---
        self.alerta_temp_activa = False
        self.alerta_pres_activa = False
        
        # CREAR INTERFAZ Y INICIAR MONITOREO
        self.setup_ui()
        self.after(1000, self.actualizar_automaticamente)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def toggle_fullscreen(self, event=None):
        """Alternar entre pantalla completa y ventana normal (F11)"""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes('-fullscreen', self.is_fullscreen)
        return "break"
    
    def exit_fullscreen(self, event=None):
        """Salir de pantalla completa (Escape)"""
        self.is_fullscreen = False
        self.attributes('-fullscreen', False)
        return "break"

    def setup_ui(self):
        # FRAME PRINCIPAL
        main_container = ctk.CTkFrame(self, fg_color=COLOR_NEGRO, corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # HEADER
        header_frame = ctk.CTkFrame(main_container, fg_color=COLOR_GRIS_OSCURO, height=80, corner_radius=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(header_frame, text="PANEL DE CONTROL INDUSTRIAL", 
                                 font=("Segoe UI", 32, "bold"), text_color=COLOR_AMARILLO)
        title_label.pack(side="left", padx=30, pady=20)
        
        # Frame para botones del header
        header_buttons = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_buttons.pack(side="right", padx=30, pady=20)
        
        # Botón para simular alerta (demostración)
        self.btn_simular_alerta = ctk.CTkButton(header_buttons, text="⚠ SIMULAR ALERTA", 
                                               command=self.simular_alerta_demo,
                                               fg_color=COLOR_NARANJA, hover_color=COLOR_ROJO, 
                                               width=180, height=40, font=("Segoe UI", 13, "bold"))
        self.btn_simular_alerta.pack(side="left", padx=10)
        
        # Botón para alternar pantalla completa
        self.btn_fullscreen = ctk.CTkButton(header_buttons, text="⛶ PANTALLA COMPLETA", 
                                           command=self.toggle_fullscreen,
                                           fg_color=COLOR_GRIS_CLARO, hover_color=COLOR_AMARILLO, 
                                           width=200, height=40, font=("Segoe UI", 13, "bold"))
        self.btn_fullscreen.pack(side="left", padx=10)
        
        self.btn_salir = ctk.CTkButton(header_buttons, text="⏻ CERRAR SESIÓN", command=self.destroy,
                                     fg_color=COLOR_GRIS_CLARO, hover_color=COLOR_ROJO, width=160, height=40,
                                     font=("Segoe UI", 13, "bold"))
        self.btn_salir.pack(side="left")
        
        # CONTENIDO
        content_frame = ctk.CTkFrame(main_container, fg_color=COLOR_NEGRO)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # MONITOR FRAME
        monitor_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_GRIS_OSCURO, corner_radius=15)
        monitor_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        ctk.CTkLabel(monitor_frame, text="MONITOREO EN TIEMPO REAL", 
                   font=("Segoe UI", 20, "bold"), text_color=COLOR_AMARILLO).pack(pady=(25, 20))
        
        self.lbl_status = ctk.CTkLabel(monitor_frame, text="● SISTEMA INICIALIZANDO", 
                                     text_color=COLOR_NARANJA, font=("Segoe UI", 16, "bold"))
        self.lbl_status.pack(pady=(0, 30))
        
        sensors_container = ctk.CTkFrame(monitor_frame, fg_color="transparent")
        sensors_container.pack(fill="x", padx=40, pady=(0, 30))
        
        # --- TARJETA TEMPERATURA ---
        self.temp_card = ctk.CTkFrame(sensors_container, fg_color=COLOR_GRIS_MEDIO, 
                                    corner_radius=12, border_width=3, border_color=COLOR_GRIS_CLARO)
        self.temp_card.pack(side="left", fill="both", expand=True, padx=10)
        
        try:
            temp_img = Image.open("temperatura.png").resize((60, 60), Image.Resampling.LANCZOS)
            temp_photo = ctk.CTkImage(light_image=temp_img, dark_image=temp_img, size=(60, 60))
            ctk.CTkLabel(self.temp_card, image=temp_photo, text="").pack(pady=(20, 5))
        except:
            pass # Si no hay imagen, no falla

        ctk.CTkLabel(self.temp_card, text="TEMPERATURA", font=("Segoe UI", 16, "bold"), 
                   text_color=COLOR_TEXTO_SECUNDARIO).pack()
        
        self.lbl_temp = ctk.CTkLabel(self.temp_card, text="-- °C", font=("Segoe UI", 48, "bold"), 
                                   text_color=COLOR_BLANCO)
        self.lbl_temp.pack(pady=10)
        
        ctk.CTkLabel(self.temp_card, text=f"Rango: {TEMP_MIN_ALERTA}°C - {TEMP_MAX_ALERTA}°C", 
                   font=("Segoe UI", 12), text_color=COLOR_TEXTO_SECUNDARIO).pack(pady=(5, 20))
        
        # --- TARJETA PRESIÓN ---
        self.pres_card = ctk.CTkFrame(sensors_container, fg_color=COLOR_GRIS_MEDIO, 
                                    corner_radius=12, border_width=3, border_color=COLOR_GRIS_CLARO)
        self.pres_card.pack(side="left", fill="both", expand=True, padx=10)
        
        try:
            pres_img = Image.open("presion.png").resize((60, 60), Image.Resampling.LANCZOS)
            pres_photo = ctk.CTkImage(light_image=pres_img, dark_image=pres_img, size=(60, 60))
            ctk.CTkLabel(self.pres_card, image=pres_photo, text="").pack(pady=(20, 5))
        except:
            pass

        ctk.CTkLabel(self.pres_card, text="PRESIÓN", font=("Segoe UI", 16, "bold"), 
                   text_color=COLOR_TEXTO_SECUNDARIO).pack()
        
        self.lbl_pres = ctk.CTkLabel(self.pres_card, text="-- PSI", font=("Segoe UI", 48, "bold"), 
                                   text_color=COLOR_BLANCO)
        self.lbl_pres.pack(pady=10)
        
        ctk.CTkLabel(self.pres_card, text=f"Rango: {PRESS_MIN_ALERTA} PSI - {PRESS_MAX_ALERTA} PSI", 
                   font=("Segoe UI", 12), text_color=COLOR_TEXTO_SECUNDARIO).pack(pady=(5, 20))
        
        # --- BOTONES INFERIORES ---
        actions_frame = ctk.CTkFrame(content_frame, fg_color=COLOR_GRIS_OSCURO, corner_radius=15, height=180)
        actions_frame.pack(fill="x")
        actions_frame.pack_propagate(False)
        
        ctk.CTkLabel(actions_frame, text="ANÁLISIS Y REPORTES", font=("Segoe UI", 20, "bold"), 
                   text_color=COLOR_AMARILLO).pack(pady=(25, 20))
        
        buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_container.pack(expand=True)
        
        self.btn_registro = ctk.CTkButton(buttons_container, text="VER REGISTRO HISTÓRICO", 
                                        command=self.mostrar_registro_temperatura, width=280, height=55,
                                        font=("Segoe UI", 16, "bold"), fg_color=COLOR_AMARILLO, 
                                        text_color=COLOR_NEGRO, hover_color=COLOR_AMARILLO_HOVER)
        self.btn_registro.pack(side="left", padx=15)
        
        self.btn_grafica = ctk.CTkButton(buttons_container, text="VER GRÁFICA DE TENDENCIAS", 
                                       command=self.mostrar_grafica_temperatura, width=280, height=55,
                                       font=("Segoe UI", 16, "bold"), fg_color=COLOR_AMARILLO, 
                                       text_color=COLOR_NEGRO, hover_color=COLOR_AMARILLO_HOVER)
        self.btn_grafica.pack(side="left", padx=15)

    def actualizar_automaticamente(self):
        self.actualizar_datos()
        self.after(2000, self.actualizar_automaticamente)

    def actualizar_datos(self):
        # 1. LEER DATOS
        temp, pres, estado_sim = self.simulador.leer_sensores()
        
        # 2. GUARDAR EN BD
        self.db.guardar_lectura(temp, pres, estado_sim)
        
        # 3. ACTUALIZAR INTERFAZ
        self.lbl_temp.configure(text=f"{temp} °C")
        self.lbl_pres.configure(text=f"{pres} PSI")

        # --- LÓGICA DE DETECCIÓN DE ALERTAS ---
        # Usamos las constantes importadas de simulator.py
        
        # Temperatura
        es_temp_alta = temp > TEMP_MAX_ALERTA
        es_temp_baja = temp < TEMP_MIN_ALERTA
        hay_problema_temp = es_temp_alta or es_temp_baja
        
        # Presión
        es_pres_alta = pres > PRESS_MAX_ALERTA
        es_pres_baja = pres < PRESS_MIN_ALERTA
        hay_problema_pres = es_pres_alta or es_pres_baja
        
        mensaje_estado = "✓ SISTEMA OPERANDO NORMALMENTE"
        color_estado = COLOR_VERDE

        # --- GESTIÓN VISUAL Y POP-UPS DE TEMPERATURA ---
        if hay_problema_temp:
            mensaje_estado = "⚠ ALERTA EN TEMPERATURA"
            color_estado = COLOR_ROJO
            
            # Cambiar colores tarjeta
            color_borde = COLOR_ROJO if es_temp_alta else COLOR_AZUL
            color_texto = COLOR_ROJO if es_temp_alta else COLOR_AZUL
            self.temp_card.configure(border_color=color_borde, border_width=4)
            self.lbl_temp.configure(text_color=color_texto)
            
            # POPUP (Solo si no estaba activa la alerta para no spammear)
            if not self.alerta_temp_activa:
                tipo = "ALTA" if es_temp_alta else "BAJA"
                messagebox.showwarning("ALERTA DE TEMPERATURA", 
                                     f"La temperatura ha salido del rango seguro.\n\n"
                                     f"Valor actual: {temp}°C\n"
                                     f"Tipo: Temperatura Crítica {tipo}")
                self.alerta_temp_activa = True # Marcamos como vista
        else:
            # Regresar a normalidad
            self.temp_card.configure(border_color=COLOR_GRIS_CLARO, border_width=3)
            self.lbl_temp.configure(text_color=COLOR_BLANCO)
            self.alerta_temp_activa = False # Reseteamos bandera

        # --- GESTIÓN VISUAL Y POP-UPS DE PRESIÓN ---
        if hay_problema_pres:
            if "ALERTA" in mensaje_estado:
                mensaje_estado += " Y PRESIÓN"
            else:
                mensaje_estado = "⚠ ALERTA EN PRESIÓN"
                color_estado = COLOR_ROJO

            # Cambiar colores tarjeta
            self.pres_card.configure(border_color=COLOR_ROJO, border_width=4)
            self.lbl_pres.configure(text_color=COLOR_ROJO)
            
            # POPUP (Controlado)
            if not self.alerta_pres_activa:
                tipo = "ALTA" if es_pres_alta else "BAJA"
                messagebox.showwarning("ALERTA DE PRESIÓN", 
                                     f"La presión ha salido del rango seguro.\n\n"
                                     f"Valor actual: {pres} PSI\n"
                                     f"Tipo: Presión Crítica {tipo}")
                self.alerta_pres_activa = True
        else:
            # Regresar a normalidad
            self.pres_card.configure(border_color=COLOR_GRIS_CLARO, border_width=3)
            self.lbl_pres.configure(text_color=COLOR_BLANCO)
            self.alerta_pres_activa = False

        # Actualizar barra inferior
        self.lbl_status.configure(text=mensaje_estado, text_color=color_estado)
    
    def mostrar_registro_temperatura(self):
        VentanaRegistro(self)
    
    def mostrar_grafica_temperatura(self):
        VentanaGrafica(self)
    
    def simular_alerta_demo(self):
        """
        Activa el modo de alerta en el simulador para demostración
        """
        self.simulador.activar_alerta_prueba()
        
        # Deshabilitar el botón temporalmente
        self.btn_simular_alerta.configure(
            state="disabled",
            text="⏳ SIMULANDO...",
            fg_color=COLOR_GRIS_CLARO
        )
        
        # Reactivar el botón después de 20 segundos
        self.after(20000, self.reactivar_boton_alerta)
    
    def reactivar_boton_alerta(self):
        """
        Reactiva el botón de simular alerta
        """
        self.btn_simular_alerta.configure(
            state="normal",
            text="⚠ SIMULAR ALERTA",
            fg_color=COLOR_NARANJA
        )

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()