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

    def leer_sensores(self):
        """
        Genera valores y determina el estado basado en los umbrales
        """
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