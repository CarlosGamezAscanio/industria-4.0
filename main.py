# ===================================================================
# SISTEMA DE MONITOREO INDUSTRIAL 4.0
# Archivo: main.py
# Descripción: Punto de entrada principal de la aplicación
# ===================================================================

from gui_login import LoginWindow

def main():
    """
    FUNCION PRINCIPAL QUE INICIA LA APLICACION
    Crea y ejecuta la ventana de login
    """
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
