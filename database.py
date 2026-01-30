# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: database.py
# Descripción: Gestión de base de datos SQLite
# ===================================================================

import sqlite3
from datetime import datetime

class Database:
    """
    CLASE PARA MANEJAR LA BASE DE DATOS SQLITE
    Gestiona usuarios, historial de sensores y operaciones CRUD
    """
    
    def __init__(self, db_name="registro_sensores.db"):
        """
        CONSTRUCTOR: Inicializa la base de datos
        
        Args:
            db_name (str): Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.crear_tablas()
        
    def conectar(self):
        """
        ESTABLECE CONEXION CON LA BASE DE DATOS
        
        Returns:
            sqlite3.Connection: Objeto de conexión
        """
        return sqlite3.connect(self.db_name)
    
    def crear_tablas(self):
        """
        CREA LAS TABLAS NECESARIAS SI NO EXISTEN
        - Tabla usuarios: Para autenticación
        - Tabla historial: Para registros de sensores
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        # TABLA DE USUARIOS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'operador'
            )
        ''')
        
        # TABLA DE HISTORIAL DE SENSORES
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL,
                temperatura REAL NOT NULL,
                presion REAL NOT NULL,
                estado TEXT NOT NULL
            )
        ''')
        
        # INSERTAR USUARIO POR DEFECTO SI NO EXISTE
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                ("admin", "1234", "administrador")
            )
            
        conn.commit()
        conn.close()
        
    def guardar_lectura(self, temp, press, estado):
        """
        GUARDA UNA NUEVA LECTURA DE SENSORES
        
        Args:
            temp (float): Temperatura en grados Celsius
            press (float): Presión en PSI
            estado (str): Estado del sistema ("NORMAL" o "ALERTA")
        """
        conn = self.conectar()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO historial (fecha, temperatura, presion, estado)
            VALUES (?, ?, ?, ?)
        ''', (fecha_actual, temp, press, estado))
        
        conn.commit()
        conn.close()
    
    def validar_usuario(self, usuario, password):
        """
        VERIFICA SI LAS CREDENCIALES SON CORRECTAS
        
        Args:
            usuario (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            bool: True si las credenciales son válidas, False en caso contrario
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT rol FROM usuarios WHERE usuario=? AND password=?", 
            (usuario, password)
        )
        resultado = cursor.fetchone()
        
        conn.close()

        #SI NO HAY NADA, DEVOLVEMOS NONE (QUE PAYTHON INTERPRETA COMO FALSO)
        return resultado[0] if resultado else None
    
    def obtener_usuarios(self):
        """[READ] Obtiene la lista de todos los usuarios registrados"""
        conn = self.conectar()
        cursor = conn.cursor()
        # Traemos ID para poder borrar, nombre y rol para mostrar
        cursor.execute("SELECT id, usuario, rol FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def agregar_usuario(self, usuario, password, rol='operador'):
        """[CREATE] Inserta un nuevo usuario"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                (usuario, password, rol)
            )
            conn.commit()
            conn.close()
            return True, "Usuario creado con éxito"
        except sqlite3.IntegrityError:
            return False, "Error: El nombre de usuario ya existe"

    def eliminar_usuario(self, id_usuario):
        """[DELETE] Borra un usuario definitivamente"""
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conn.commit()
        conn.close()
        return True
    
    def actualizar_usuario(self, id_usuario, nuevo_nombre, nuevo_password, nuevo_rol):
        """[UPDATE] Modifica los datos de un usuario existente"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios 
                SET usuario = ?, password = ?, rol = ?
                WHERE id = ?
            ''', (nuevo_nombre, nuevo_password, nuevo_rol, id_usuario))
            
            conn.commit()
            conn.close()
            return True, "Usuario actualizado correctamente"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"
    def obtener_historial_completo(self):
        """
        OBTIENE TODOS LOS REGISTROS DEL HISTORIAL
        
        Returns:
            list: Lista de tuplas con (id, fecha, temperatura, presion, estado)
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM historial ORDER BY fecha DESC")
        registros = cursor.fetchall()
        
        conn.close()
        return registros
    
    def obtener_historial_por_estado(self, estado):
        """
        OBTIENE REGISTROS FILTRADOS POR ESTADO
        
        Args:
            estado (str): Estado a filtrar ("NORMAL" o "ALERTA")
            
        Returns:
            list: Lista de registros que coinciden con el estado
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM historial WHERE estado=? ORDER BY fecha DESC", 
            (estado,)
        )
        registros = cursor.fetchall()
        
        conn.close()
        return registros
    
    def obtener_datos_temperatura(self, limite=None):
        """
        OBTIENE DATOS DE TEMPERATURA PARA GRAFICAS
        
        Args:
            limite (int, optional): Número máximo de registros a obtener
            
        Returns:
            list: Lista de tuplas con (id, fecha, temperatura)
        """
        conn = self.conectar()
        cursor = conn.cursor()
        
        if limite:
            cursor.execute(
                "SELECT id, fecha, temperatura FROM historial ORDER BY id DESC LIMIT ?", 
                (limite,)
            )
        else:
            cursor.execute(
                "SELECT id, fecha, temperatura FROM historial ORDER BY id DESC"
            )
        
        registros = cursor.fetchall()
        conn.close()
        
        # INVERTIR PARA ORDEN CRONOLOGICO
        return list(reversed(registros))