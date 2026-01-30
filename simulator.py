# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: simulator.py
# Descripción: Simulador de sensores industriales
# ===================================================================

import random

class SimuladorSensor:
    """
    CLASE PARA SIMULAR SENSORES DE TEMPERATURA Y PRESION
    Genera valores aleatorios dentro de rangos realistas
    """
    
    def __init__(self):
        """CONSTRUCTOR: Define los rangos de operación de los sensores"""
        # RANGOS DE TEMPERATURA (en grados Celsius)
        self.temp_min = 0.0
        self.temp_max = 100.0
        
        # RANGOS DE PRESION (en PSI)
        self.press_min = 0.0
        self.press_max = 20.0
        
    def leer_sensores(self):
        """
        SIMULA LA LECTURA DE SENSORES
        
        Returns:
            tuple: (temperatura, presion, estado)
                - temperatura (float): Valor en grados Celsius
                - presion (float): Valor en PSI
                - estado (str): "NORMAL" o "ALERTA"
        """
        # GENERAR VALORES ALEATORIOS
        temperatura = round(random.uniform(self.temp_min, self.temp_max), 2)
        presion = round(random.uniform(self.press_min, self.press_max), 2)
        
        # DETERMINAR ESTADO SEGUN UMBRALES CRITICOS
        estado = "NORMAL"
        if temperatura > 85.0 or presion > 12.0:
            estado = "ALERTA"
            
        return temperatura, presion, estado