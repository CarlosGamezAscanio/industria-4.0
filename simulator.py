import random

class SimuladorSensor:
    def __init__(self):
        #DEFINICION DE RANGOS "NORMALES" DE NUESTRA MAQUINARIA
        self.temp_min = 20.0
        self.temp_max = 100.0
        self.press_min = 1.0
        self.press_max = 15.0
        
    def leer_sensores(self):
        #GENERADOR DE DATOS ALEATORIOS DE TEMPERATURA Y PRESION
        #GENERAR UN NUMERO DECIMAL ALEATORIO ENTRE LOS RANGOS
        
        temperatura = round(random.uniform(self.temp_min, self.temp_max), 2)
        presion = round(random.uniform(self.press_min, self.press_max), 2)
        
        #LOGICA DE DEFINICION DE ESTADOS: SI SUPERA EL LIMITE, GENERA ALERTA
        estado = "NORMAL"
        if temperatura > 85.0 or presion > 12.0:
            estado = "ALERTA"
            
        return temperatura, presion, estado
    
""" if __name__ == "__main__":
    sim = SimuladorSensor()
    t, p, e = sim.leer_sensores()
    print(f"---PRUEBA DE SIMULADOR---")
    print(f"Temperatura:{t}°C")
    print(f"Presion:{p}psi")
    print(f"Estado:{e}") """