# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: auth.py
# Descripción: Gestión de autenticación de usuarios
# ===================================================================

from database import Database

class AuthManager:
    """
    CLASE PARA MANEJAR LA AUTENTICACION DE USUARIOS
    Se encarga de validar credenciales contra la base de datos
    """
    
    def __init__(self):
        """CONSTRUCTOR: Inicializa la conexión a la base de datos"""
        self.db = Database()
    
    def verificar_acceso(self, usuario, password):
        """
        VERIFICA SI LAS CREDENCIALES SON VALIDAS
        
        Args:
            usuario (str): Nombre de usuario
            password (str): Contraseña del usuario
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        # LIMPIAR DATOS DE ENTRADA (quitar espacios)
        u_limpio = usuario.strip()
        p_limpio = password.strip()
        
        # VALIDAR QUE NO ESTEN VACIOS
        if not u_limpio or not p_limpio:
            return False, "ERROR: Los campos no pueden estar vacíos"
        
        # CONSULTAR BASE DE DATOS
        es_valido = self.db.validar_usuario(u_limpio, p_limpio)
        
        if es_valido:
            return True, f"Bienvenido {u_limpio}"
        else:
            return False, "Usuario o contraseña incorrectos"