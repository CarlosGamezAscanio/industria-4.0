# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: ventanas_analisis.py
# Descripción: Ventanas de análisis - Registro y Gráficas
# ===================================================================

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')  # Backend compatible con tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import Database
from datetime import datetime
import pandas as pd # IMPORTANTE: Librería para Excel

class VentanaRegistro(ctk.CTkToplevel):
    """
    VENTANA DE REPORTES CON FILTROS Y EXPORTACIÓN EXCEL
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("GENERADOR DE REPORTES Y HISTORIAL")
        self.geometry("900x700")
        self.transient(parent)
        self.grab_set()
        
        self.db = Database()
        self.registros_actuales = [] # Para guardar lo que se ve en pantalla
        
        self.crear_interfaz()
        
        # Cargar datos iniciales (del día actual o todos)
        self.filtrar_datos(cargar_todo=True)
    
    def crear_interfaz(self):
        # --- HEADER Y FILTROS ---
        frame_controles = ctk.CTkFrame(self, fg_color="#2B2B2B")
        frame_controles.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(frame_controles, text="📅 RANGO DE FECHAS (YYYY-MM-DD)", 
                    font=("Roboto", 12, "bold"), text_color="#CCCCCC").pack(pady=(10,5))
        
        # Contenedor de inputs de fecha
        frame_fechas = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_fechas.pack(pady=5)
        
        # Fecha Desde
        self.ent_desde = ctk.CTkEntry(frame_fechas, placeholder_text="Desde (ej: 2023-01-01)", width=150)
        self.ent_desde.pack(side="left", padx=10)
        
        # Fecha Hasta
        self.ent_hasta = ctk.CTkEntry(frame_fechas, placeholder_text="Hasta (ej: 2023-12-31)", width=150)
        self.ent_hasta.pack(side="left", padx=10)
        
        # Botones de Acción
        frame_botones = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_botones.pack(pady=15)
        
        self.btn_filtrar = ctk.CTkButton(frame_botones, text="🔍 FILTRAR", command=self.ejecutar_filtro,
                                       fg_color="#3498DB", width=120)
        self.btn_filtrar.pack(side="left", padx=10)

        self.btn_todos = ctk.CTkButton(frame_botones, text="🔄 VER TODO", command=lambda: self.filtrar_datos(cargar_todo=True),
                                       fg_color="#505050", width=120)
        self.btn_todos.pack(side="left", padx=10)
        
        self.btn_excel = ctk.CTkButton(frame_botones, text="📗 EXPORTAR EXCEL", command=self.generar_excel,
                                     fg_color="#27AE60", hover_color="#219150", width=150)
        self.btn_excel.pack(side="left", padx=10)

        # --- TABLA DE RESULTADOS ---
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.crear_tabla()
        
        # Barra de estado simple
        self.lbl_registros = ctk.CTkLabel(self, text="Registros encontrados: 0", font=("Roboto", 12))
        self.lbl_registros.pack(pady=5)

    def crear_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B", borderwidth=0)
        style.configure("Treeview.Heading", background="#1F538D", foreground="white", borderwidth=1)
        style.map("Treeview", background=[("selected", "#3498DB")])
        
        columnas = ("ID", "Fecha", "Temp", "Presion", "Estado")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=20)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha / Hora")
        self.tree.heading("Temp", text="Temperatura (°C)")
        self.tree.heading("Presion", text="Presión (PSI)")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Fecha", width=180, anchor="center")
        self.tree.column("Temp", width=120, anchor="center")
        self.tree.column("Presion", width=120, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")
        
        self.tree.tag_configure("ALERTA", background="#E74C3C")
        self.tree.tag_configure("NORMAL", background="#2ECC71", foreground="black")
        
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def ejecutar_filtro(self):
        f_inicio = self.ent_desde.get().strip()
        f_fin = self.ent_hasta.get().strip()
        
        if not self.validar_fechas(f_inicio, f_fin):
            return
            
        self.filtrar_datos(f_inicio, f_fin)

    def validar_fechas(self, f1, f2):
        try:
            datetime.strptime(f1, '%Y-%m-%d')
            datetime.strptime(f2, '%Y-%m-%d')
            return True
        except ValueError:
            messagebox.showerror("Error de Formato", "Las fechas deben tener el formato YYYY-MM-DD\nEjemplo: 2024-01-30")
            return False

    def filtrar_datos(self, f_inicio=None, f_fin=None, cargar_todo=False):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if cargar_todo:
            self.registros_actuales = self.db.obtener_historial_completo()
            self.ent_desde.delete(0, 'end')
            self.ent_hasta.delete(0, 'end')
        else:
            self.registros_actuales = self.db.obtener_historial_por_rango(f_inicio, f_fin)
        
        # Llenar tabla
        for reg in self.registros_actuales:
            # DB devuelve: (id, fecha, temp, presion, estado)
            # Treeview espera lo mismo
            self.tree.insert("", "end", values=reg, tags=(reg[4],))
            
        self.lbl_registros.configure(text=f"Registros encontrados: {len(self.registros_actuales)}")

    def generar_excel(self):
        if not self.registros_actuales:
            messagebox.showwarning("Sin datos", "No hay datos en pantalla para exportar.")
            return
            
        try:
            # Pedir dónde guardar el archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel file", "*.xlsx")],
                title="Guardar Reporte"
            )
            
            if filename:
                # Usamos PANDAS para crear el Excel profesionalmente
                columnas = ["ID", "Fecha y Hora", "Temperatura (°C)", "Presión (PSI)", "Estado"]
                df = pd.DataFrame(self.registros_actuales, columns=columnas)
                
                # Exportar
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Reporte exportado correctamente en:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo crear el archivo Excel:\n{str(e)}")


class VentanaGrafica(ctk.CTkToplevel):
    """
    VENTANA PARA MOSTRAR GRAFICA INTERACTIVA DE TEMPERATURA
    Incluye selector de registros, estadísticas y visualización temporal
    """
    
    def __init__(self, parent):
        """
        CONSTRUCTOR: Inicializa la ventana de gráfica
        
        Args:
            parent: Ventana padre (Dashboard)
        """
        super().__init__(parent)
        
        # CONFIGURACION DE LA VENTANA
        self.title("GRÁFICA DE TEMPERATURA")
        self.geometry("1000x700")
        self.transient(parent)
        self.grab_set()
        
        # INICIALIZAR BASE DE DATOS
        self.db = Database()
        
        # CREAR INTERFAZ
        self.crear_interfaz()
        
        # CARGAR GRAFICA INICIAL
        self.actualizar_grafica()
    
    def crear_interfaz(self):
        """CONSTRUYE LA INTERFAZ GRAFICA DE LA VENTANA"""
        
        # TITULO DE LA VENTANA
        titulo = ctk.CTkLabel(
            self, 
            text="📈 ANÁLISIS GRÁFICO DE TEMPERATURA", 
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=20)
        
        # PANEL DE CONTROLES
        self.crear_panel_controles()
        
        # CONTENEDOR PARA LA GRAFICA
        self.frame_grafica = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.frame_grafica.pack(fill="both", expand=True, padx=20, pady=20)
        
        # BOTON CERRAR VENTANA
        btn_cerrar = ctk.CTkButton(
            self, 
            text="CERRAR", 
            command=self.destroy,
            fg_color="#E74C3C", 
            hover_color="#C0392B"
        )
        btn_cerrar.pack(pady=20)
    
    def crear_panel_controles(self):
        """CREA EL PANEL DE CONTROLES SUPERIOR"""
        
        frame_controles = ctk.CTkFrame(self, fg_color="transparent")
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        # SELECTOR DE CANTIDAD DE REGISTROS
        lbl_limite = ctk.CTkLabel(
            frame_controles, 
            text="Mostrar últimos:", 
            font=("Roboto", 12)
        )
        lbl_limite.pack(side="left", padx=(0, 10))
        
        self.combo_limite = ctk.CTkComboBox(
            frame_controles,
            values=["10", "20", "50", "100", "TODOS"],
            width=120,
            command=self.on_combo_change
        )
        self.combo_limite.set("50")  # Valor por defecto
        self.combo_limite.pack(side="left", padx=5)
        
        # BOTON ACTUALIZAR
        btn_actualizar = ctk.CTkButton(
            frame_controles,
            text="🔄 ACTUALIZAR",
            command=self.actualizar_grafica,
            width=120,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        btn_actualizar.pack(side="left", padx=10)
    
    def on_combo_change(self, valor):
        """
        MANEJA EL CAMBIO EN EL SELECTOR DE REGISTROS
        
        Args:
            valor: Nuevo valor seleccionado
        """
        self.actualizar_grafica()
    
    def actualizar_grafica(self):
        """
        ACTUALIZA LA GRAFICA CON LOS DATOS SELECCIONADOS
        Se ejecuta al cambiar el selector o presionar actualizar
        """
        # LIMPIAR CONTENIDO ANTERIOR
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()
        
        # OBTENER LIMITE SELECCIONADO
        limite_str = self.combo_limite.get()
        limite = None if limite_str == "TODOS" else int(limite_str)
        
        # OBTENER DATOS DE LA BASE DE DATOS
        registros = self.db.obtener_historial_completo()
        
        if registros:
            # APLICAR LIMITE SI ES NECESARIO
            if limite:
                registros = registros[:limite]
            
            # EXTRAER DATOS PARA LA GRAFICA
            ids = [reg[0] for reg in registros]
            temperaturas = [float(reg[2]) for reg in registros]
            
            # CALCULAR ESTADISTICAS
            temp_max = max(temperaturas)
            temp_min = min(temperaturas)
            temp_prom = sum(temperaturas) / len(temperaturas)
            
            # CREAR GRAFICA CON MATPLOTLIB
            self.crear_grafica_matplotlib(ids, temperaturas, temp_max, temp_min, temp_prom)
            
            # MOSTRAR ESTADISTICAS DEBAJO DE LA GRAFICA
            self.mostrar_estadisticas_grafica(temp_max, temp_min, temp_prom, len(registros))
            
        else:
            # MOSTRAR MENSAJE SI NO HAY DATOS
            self.mostrar_mensaje_sin_datos()
    
    def crear_grafica_matplotlib(self, ids, temperaturas, temp_max, temp_min, temp_prom):
        """
        CREA LA GRAFICA DE MATPLOTLIB CON TODOS LOS ELEMENTOS VISUALES
        
        Args:
            ids: Lista de IDs de registros
            temperaturas: Lista de valores de temperatura
            temp_max, temp_min, temp_prom: Estadísticas calculadas
        """
        # CREAR FIGURA DE MATPLOTLIB
        fig = Figure(figsize=(12, 6), facecolor='#2B2B2B')
        ax = fig.add_subplot(111)
        
        # CONFIGURAR APARIENCIA OSCURA
        ax.set_facecolor('#1E1E1E')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.tick_params(colors='white')
        
        # GRAFICAR LINEA PRINCIPAL DE TEMPERATURA
        ax.plot(ids, temperaturas, 
               color='#3498DB', 
               linewidth=2, 
               marker='o', 
               markersize=4,
               label='Temperatura')
        
        # LINEAS DE REFERENCIA
        ax.axhline(y=90, color='#E74C3C', linestyle='--', 
                  linewidth=2, label='Umbral Crítico (90°C)')
        ax.axhline(y=temp_prom, color='#2ECC71', linestyle=':', 
                  linewidth=2, label=f'Promedio ({temp_prom:.2f}°C)')
        
        # AREA DE ALERTA (zona crítica)
        ax.fill_between(ids, 90, max(temperaturas + [100]), 
                       alpha=0.2, color='#E74C3C')
        
        # ETIQUETAS Y TITULO
        ax.set_xlabel('ID de Registro', color='white', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperatura (°C)', color='white', fontsize=12, fontweight='bold')
        ax.set_title('EVOLUCIÓN DE TEMPERATURA EN EL TIEMPO', 
                   color='white', fontsize=14, fontweight='bold', pad=20)
        
        # GRID Y LEYENDA
        ax.grid(True, alpha=0.3, color='gray', linestyle='--')
        ax.legend(facecolor='#2B2B2B', edgecolor='white', 
                 labelcolor='white', loc='upper left')
        
        # AJUSTAR DISEÑO
        fig.tight_layout()
        
        # INTEGRAR EN TKINTER
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def mostrar_estadisticas_grafica(self, temp_max, temp_min, temp_prom, total_registros):
        """
        MUESTRA LAS ESTADISTICAS DEBAJO DE LA GRAFICA
        
        Args:
            temp_max, temp_min, temp_prom: Valores estadísticos
            total_registros: Número total de registros
        """
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # TEMPERATURA MAXIMA (rojo)
        lbl_max = ctk.CTkLabel(
            stats_frame, 
            text=f"Máxima: {temp_max}°C", 
            font=("Roboto", 12, "bold"), 
            text_color="#E74C3C"
        )
        lbl_max.pack(side="left", padx=20)
        
        # TEMPERATURA MINIMA (azul)
        lbl_min = ctk.CTkLabel(
            stats_frame, 
            text=f"Mínima: {temp_min}°C", 
            font=("Roboto", 12, "bold"), 
            text_color="#3498DB"
        )
        lbl_min.pack(side="left", padx=20)
        
        # TEMPERATURA PROMEDIO (verde)
        lbl_prom = ctk.CTkLabel(
            stats_frame, 
            text=f"Promedio: {temp_prom:.2f}°C", 
            font=("Roboto", 12, "bold"), 
            text_color="#2ECC71"
        )
        lbl_prom.pack(side="left", padx=20)
        
        # TOTAL DE REGISTROS
        lbl_total = ctk.CTkLabel(
            stats_frame, 
            text=f"Total registros: {total_registros}", 
            font=("Roboto", 12, "bold")
        )
        lbl_total.pack(side="left", padx=20)
    
    def mostrar_mensaje_sin_datos(self):
        """MUESTRA MENSAJE CUANDO NO HAY DATOS DISPONIBLES"""
        lbl_sin_datos = ctk.CTkLabel(
            self.frame_grafica,
            text="⚠️ NO HAY DATOS DISPONIBLES\n\nEl sistema aún no ha registrado mediciones.",
            font=("Roboto", 16),
            text_color="#E74C3C"
        )
        lbl_sin_datos.pack(expand=True)