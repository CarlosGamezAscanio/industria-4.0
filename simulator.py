# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: simulator.py
# ===================================================================

import random

# --- DEFINICIÓN DE UMBRALES (Reglas de Negocio) ---
# Importaremos estas variables desde el dashboard para que coincidan siempre
TEMP_MAX_ALERTA = 70.0
TEMP_MIN_ALERTA = 20.0

PRESS_MAX_ALERTA = 30.0
PRESS_MIN_ALERTA = 3.0   # Corregido a 3 PSI según tu requerimiento

class SimuladorSensor:
    """
    CLASE PARA SIMULAR SENSORES DE TEMPERATURA Y PRESION
    """
    
    def __init__(self):
        # RANGOS FISICOS DE LOS SENSORES
        self.temp_min_fisico, self.press_min_fisico = 0.0, 0.0
        self.temp_max_fisico, self.press_max_fisico = 100.0, 45.0 

        # VALORES INICIALES
        self.temp_actual, self.press_actual = 25.0, 10.0 
        self.factor_suavizado = 0.2 
        
        # MODO DE PRUEBA DE ALERTAS
        self.modo_alerta_forzada = False
        self.contador_alerta = 0 

    def leer_sensores(self):
        """
        Genera valores y determina el estado basado en los umbrales
        """
        # SI ESTAMOS EN MODO ALERTA FORZADA
        if self.modo_alerta_forzada:
            self.contador_alerta += 1
            
            # Forzar valores críticos alternados
            if self.contador_alerta % 2 == 0:
                # Temperatura alta crítica
                temp = round(random.uniform(90, 98), 2)
                press = round(random.uniform(40, 44), 2)
            else:
                # Temperatura baja crítica (opcional)
                temp = round(random.uniform(5, 15), 2)
                press = round(random.uniform(1, 2.5), 2)
            
            # Después de 10 lecturas (20 segundos), volver a normal
            if self.contador_alerta >= 10:
                self.modo_alerta_forzada = False
                self.contador_alerta = 0
                self.temp_actual = 25.0
                self.press_actual = 10.0
            
            estado = "ALERTA"
            return temp, press, estado
        
        # MODO NORMAL
        # GENERAR VARIACION ALEATORIA
        paso_temp = random.uniform(-3.0, 3.5) # Aumenté la variación para probar las alertas más rápido
        paso_press = random.uniform(-2.0, 2.0)

        # CALCULAR NUEVO OBJETIVO
        objetivo_temp = self.temp_actual + paso_temp
        objetivo_press = self.press_actual + paso_press

        # SUAVIZADO
        self.temp_actual = self.temp_actual + (objetivo_temp - self.temp_actual) * self.factor_suavizado
        self.press_actual = self.press_actual + (objetivo_press - self.press_actual) * self.factor_suavizado

        # MANTENER DENTRO DE RANGOS FÍSICOS
        self.temp_actual = max(self.temp_min_fisico, min(self.temp_max_fisico, self.temp_actual))
        self.press_actual = max(self.press_min_fisico, min(self.press_max_fisico, self.press_actual))
        
        # --- LÓGICA DE ESTADO GENERAL ---
        estado = "NORMAL"
        
        # Verificamos si ALGO está mal para el registro en base de datos
        if (self.temp_actual > TEMP_MAX_ALERTA or self.temp_actual < TEMP_MIN_ALERTA or
            self.press_actual > PRESS_MAX_ALERTA or self.press_actual < PRESS_MIN_ALERTA):
            estado = "ALERTA"
            
        return round(self.temp_actual, 2), round(self.press_actual, 2), estado
    
    def activar_alerta_prueba(self):
        """
        Activa el modo de alerta forzada por unos segundos
        """
        self.modo_alerta_forzada = True
        self.contador_alerta = 0