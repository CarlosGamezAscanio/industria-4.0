from database import Database

class AuthManager:
    def __init__(self):
        #AL NACER, EL GUARDIAN CREA UNA CONEXION A LA BASE DE DATOS
        self.db = Database()
    
    def verificar_acceso(self, usuario, password):
        #ESTA FUNCION ES UN FILTRO QUE SE ENCARGA DE RETORNAR TRUE,MENSAJE SI EL ACCESO ES CORRECTO O FALSE,MENSAJE SI ES INCORRECTO
        
        #1.LIMPIEZA DE DATOS(QUITAMOS ESPACIOS ACCIDENTALES)
        u_limpio = usuario.strip()
        p_limpio = password.strip()
        
        #2.VALIDACION BASICA PREGUNTA SI ESCRIBIO ALGO EL USUARIO
        if not u_limpio or not p_limpio:
            return False, "____ERROR:LOS CAMPOS NO PUEDEN ESTAR VACIOS____"
        
        #3.CONSULTA A LA BASE DE DATOS
        #RECORDANDO QUE EN DATABASE.PY YA CREAMOS 'VALIDAR_USUARIO'
        es_valido = self.db.validar_usuario(u_limpio, p_limpio)
        
        if es_valido:
            return True, f"BIENVENIDO {u_limpio}"
        else:
            return False, f"USUARIO O PASSWORD INCORRECTOS"
        
""" if __name__ == "__main__":
    auth = AuthManager()
    #PRUEBA CON LOS DATOS QUE INSERTAMOS POR DEFECTO EN DATABASE.PY
    resultado, mensaje = auth.verificar_acceso(" admin", "1234")
    print(f"RESULTADO:{resultado} // Mensaje:{mensaje}") """