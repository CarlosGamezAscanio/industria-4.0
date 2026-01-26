# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: ventanas_analisis.py
# Descripción: Ventanas de análisis - Registro y Gráficas
# ===================================================================

import customtkinter as ctk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')  # Backend compatible con tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import Database


class VentanaRegistro(ctk.CTkToplevel):
    """
    VENTANA PARA MOSTRAR TABLA DE HISTORIAL DE TEMPERATURA
    Muestra todos los registros en formato tabular con estadísticas
    """
    
    def __init__(self, parent):
        """
        CONSTRUCTOR: Inicializa la ventana de registro
        
        Args:
            parent: Ventana padre (Dashboard)
        """
        super().__init__(parent)
        
        # CONFIGURACION DE LA VENTANA
        self.title("REGISTRO DE TEMPERATURA")
        self.geometry("800x600")
        self.transient(parent)  # Mantener al frente
        self.grab_set()  # Modal
        
        # INICIALIZAR BASE DE DATOS
        self.db = Database()
        
        # CREAR INTERFAZ
        self.crear_interfaz()
        
        # CARGAR DATOS
        self.cargar_datos()
    
    def crear_interfaz(self):
        """CONSTRUYE LA INTERFAZ GRAFICA DE LA VENTANA"""
        
        # TITULO DE LA VENTANA
        titulo = ctk.CTkLabel(
            self, 
            text="📊 HISTORIAL DE TEMPERATURA", 
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=20)
        
        # CONTENEDOR PARA LA TABLA
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(fill="both", expand=True, padx=20, pady=20)
        
        # CONFIGURAR ESTILO DE LA TABLA
        self.configurar_estilo_tabla()
        
        # CREAR TABLA
        self.crear_tabla()
        
        # LABEL PARA ESTADISTICAS (se actualiza en cargar_datos)
        self.lbl_stats = ctk.CTkLabel(self, text="", font=("Roboto", 12))
        self.lbl_stats.pack(pady=10)
        
        # BOTON CERRAR
        btn_cerrar = ctk.CTkButton(
            self, 
            text="CERRAR", 
            command=self.destroy,
            fg_color="#E74C3C", 
            hover_color="#C0392B"
        )
        btn_cerrar.pack(pady=20)
    
    def configurar_estilo_tabla(self):
        """CONFIGURA EL ESTILO VISUAL DE LA TABLA"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2B2B2B",
                       foreground="white",
                       fieldbackground="#2B2B2B",
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background="#1F538D",
                       foreground="white",
                       borderwidth=1)
        style.map("Treeview", background=[("selected", "#3498DB")])
    
    def crear_tabla(self):
        """CREA LA TABLA CON COLUMNAS Y SCROLLBAR"""
        
        # DEFINIR COLUMNAS DE LA TABLA
        columnas = ("ID", "Fecha", "Hora", "Temperatura", "Estado")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=20)
        
        # CONFIGURAR ENCABEZADOS
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Temperatura", text="Temperatura (°C)")
        self.tree.heading("Estado", text="Estado")
        
        # CONFIGURAR ANCHOS DE COLUMNAS
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Fecha", width=120, anchor="center")
        self.tree.column("Hora", width=120, anchor="center")
        self.tree.column("Temperatura", width=150, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")
        
        # CONFIGURAR COLORES POR ESTADO
        self.tree.tag_configure("ALERTA", background="#E74C3C", foreground="white")
        self.tree.tag_configure("NORMAL", background="#2ECC71", foreground="white")
        
        # SCROLLBAR PARA LA TABLA
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # POSICIONAR TABLA Y SCROLLBAR
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def cargar_datos(self):
        """CARGA LOS DATOS DE LA BASE DE DATOS EN LA TABLA"""
        
        # OBTENER REGISTROS DE LA BASE DE DATOS
        registros = self.db.obtener_historial_completo()
        
        # INSERTAR DATOS EN LA TABLA
        for registro in registros:
            id_reg, fecha_completa, temp, pres, estado = registro
            
            # SEPARAR FECHA Y HORA
            try:
                fecha, hora = fecha_completa.split(" ")
            except:
                fecha = fecha_completa
                hora = "--"
            
            # INSERTAR FILA CON COLOR SEGÚN ESTADO
            self.tree.insert("", "end", 
                           values=(id_reg, fecha, hora, f"{temp}°C", estado),
                           tags=(estado,))
        
        # CALCULAR Y MOSTRAR ESTADISTICAS
        self.mostrar_estadisticas(registros)
    
    def mostrar_estadisticas(self, registros):
        """
        CALCULA Y MUESTRA LAS ESTADISTICAS DE LOS DATOS
        
        Args:
            registros: Lista de registros de la base de datos
        """
        total_registros = len(registros)
        
        if registros:
            temperaturas = [float(reg[2]) for reg in registros]
            temp_max = max(temperaturas)
            temp_min = min(temperaturas)
            temp_prom = sum(temperaturas) / len(temperaturas)
            
            stats_text = (f"Total: {total_registros} registros | "
                         f"Máx: {temp_max}°C | "
                         f"Mín: {temp_min}°C | "
                         f"Promedio: {temp_prom:.2f}°C")
        else:
            stats_text = "No hay registros disponibles"
        
        # ACTUALIZAR LABEL DE ESTADISTICAS
        self.lbl_stats.configure(text=stats_text)


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