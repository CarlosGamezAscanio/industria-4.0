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
        u_limpio = usuario.strip()
        p_limpio = password.strip()
        
        if not u_limpio or not p_limpio:
            # Enviamos 3 cosas: (Exito, Mensaje, Rol)
            return False, "Campos vacíos", None
        
        # Aquí database devuelve "administrador", "operador" o None
        rol_db = self.db.validar_usuario(u_limpio, p_limpio)

        if rol_db:
            # IMPORTANTE: Devolvemos 3 valores siempre
            # Exito = True
            # Mensaje = "Acceso correcto"
            # Rol = El que vino de la DB (administrador u operador)
            return True, "Acceso correcto", rol_db
        else:
            return False, "Credenciales incorrectas", None