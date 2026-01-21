import sqlite3
from datetime import datetime

class Database:
    def __init__(self,db_name="sistema_monitoreo.db"):
        self.db_name = db_name
        self.crear_tablas()
        
    def conectar(self):
        "Establecida la conexion con el archivo .db"
        return sqlite3.connect(self.db_name)
    
    def crear_tablas(self):
        "Crea las tablas de usuarios y sensores si no existen"
        conn = self.conectar()
        cursor = conn.cursor()
        
        #TABLA DE USUARIOS (PARA EL INICIO DE SESION)
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)''')
        
        #TABLA DE USUARIOS HISTORIAL (PARA TEMPERATURA Y PRESION)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS historial(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           fecha TIMESTAMP NOT NULL,
                           temperatura REAL NOT NULL,
                           presion REAL NOT NULL,
                           estado TEXT NOT NULL)''')
        
        #INSERTAR UN USUARIO DE PRUEBA SI LA TABLA ESTA VACIA
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (?,?)",("admin","1234"))
            
        conn.commit()
        conn.close()
        
    def guardar_lectura(self, temp, press, estado):
        #GUARDA NUEVAS MEDICIONES DE SENSORES
        conn = self.conectar()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
                       INSERT INTO historial (fecha, temperatura, presion, estado)
                       VALUES (?,?,?,?)''', (fecha_actual, temp, press, estado))
        
        conn.commit()
        conn.close()
    
    def validar_usuario(self, usuario, password):
        #VERIFICA SI LAS CREDENCIALES SON CORRECTAS
        
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (usuario,password))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado is not None #RETORNA TRUE SI EXISTE, FALSE SI NO
    
""" #PRUEBA DE FUNCIONAMIENTO
if __name__ == "__main__":
    #CREACION DE INSTANCIA
    db = Database()
    print("---PRUEBA BASE DE DATOS---")
    
    #PRUEBA GUARDAR DATOS
    db.guardar_lectura(30.5, 12.0, "NORMAL")
    print("DATOS GUARDADOS")
    
    #PRUEBA DE LOGIN CON EL USUARIO POR DEFECTO
    
    exito = db.validar_usuario("admin","1234")
    if exito:
        print("LOGIN EXITOSO")
    else:
        print("LOGIN FALLIDO") """