# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: simulator.py
# Descripción: Simulador de sensores industriales
# ===================================================================

import random

class Sensores:
    """
    CLASE PARA SIMULAR SENSORES DE TEMPERATURA Y PRESION
    Genera valores aleatorios dentro de rangos realistas
    """
    
    def __init__(self):
        """CONSTRUCTOR: Define los rangos de operación de los sensores"""
        #RANGOS DE TEMPERATURA (en grados Celsius) # RANGOS DE PRESION (en PSI)
        self.temp_min, self.press_min = 0.0, 0.0
        self.temp_max, self.press_max = 100.0, 20.0

        #VALORES INICIALES (PUNTO DE PARTIDA DE LA SIMULACIÓN)
        self.temp_actual, self.press_actual = 25.0, 5.0 

        #VALOR SUAVIZADO
        self.factor_suavizado = 0.1

    def leer_sensores(self):
        """
        SIMULA LA LECTURA ESTABLE BASADA EN VALORES ANTERIORES
        
        Returns:
            tuple: (temperatura, presion, estado)
                - temperatura (float): Valor en grados Celsius
                - presion (float): Valor en PSI
                - estado (str): "NORMAL" o "ALERTA"
        """
        #DEFINIR UN PASO MÁXIMO DE CAMBIO QUE PUEDE REALIZAR EL SISTEMA
        paso_temp = random.uniform(-1.5, 1.5)
        paso_press = random.uniform(-0.3 , 0.3)

        #APLICACION DE UNA VARIACIÓN AL VALOR ACTUAL (VALOR OBJETIVO)
        objetivo_temp = self.temp_actual + paso_temp
        objetivo_press = self.press_actual + paso_press

        #SUAVIZADO DE LECTURAS PARA EVITAR CAMBIOS BRUSCOS
        #NUEVO = ANTERIOR + (OBJETIVO - ANTERIOR) * FACTOR_SUAVIZADO
        self.temp_actual = self.temp_actual + (objetivo_temp - self.temp_actual) * self.factor_suavizado
        self.press_actual = self.press_actual + (objetivo_press - self.press_actual) * self.factor_suavizado

        #RESTRICCION PARA EVITAR QUE SE SALGA DE LOS RANGOS DEFINIDOS
        self.temp_actual = max(self.temp_min, min(self.temp_max, self.temp_actual))
        self.press_actual = max(self.press_min, min(self.press_max, self.press_actual))
        
        # DETERMINAR ESTADO SEGUN UMBRALES CRITICOS
        estado = "NORMAL"
        if self.temp_actual > 85.0 or self.press_actual > 12.0:
            estado = "ALERTA"
            
        return round(self.temp_actual,2), round(self.press_actual,2), estado
    
    def generar_falla_critica(self):
        """Salto brusco para forzar una alerta inmediata"""
        self.temp_actual = random.uniform(86.0, 95.0)
        self.press_actual = random.uniform(13.0, 18.0)

    def estabilizar_sistema(self):
        """Regresa los valores a niveles normales de operación"""
        self.temp_actual = 25.0
        self.press_actual = 5.0
        print(">>> REPELEANDO VALORES SEGUROS <<<")