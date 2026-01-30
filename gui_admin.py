import customtkinter as ctk
from tkinter import messagebox
from database import Database

class AdminWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        self.usuario_seleccionado_id = None  # Para saber si estamos editando
        
        # CONFIGURACIÓN DE VENTANA
        self.title("ADMINISTRACIÓN DE USUARIOS - INDUSTRIA 4.0")
        self.geometry("700x600")
        
        self.setup_ui()
        self.cargar_usuarios()

    def setup_ui(self):
        # TÍTULO
        self.lbl_titulo = ctk.CTkLabel(self, text="GESTIÓN DE USUARIOS", font=("Roboto", 24, "bold"))
        self.lbl_titulo.pack(pady=20)

        # --- FORMULARIO (CREATE / UPDATE) ---
        self.frame_form = ctk.CTkFrame(self)
        self.pack_pady = 5
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_nombre = ctk.CTkEntry(self.frame_form, placeholder_text="Nombre de Usuario", width=200)
        self.entry_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.entry_pass = ctk.CTkEntry(self.frame_form, placeholder_text="Contraseña", show="*", width=200)
        self.entry_pass.grid(row=0, column=1, padx=10, pady=10)

        self.combo_rol = ctk.CTkOptionMenu(self.frame_form, values=["operador", "admin"])
        self.combo_rol.grid(row=0, column=2, padx=10, pady=10)

        # BOTONES DE ACCIÓN
        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Registrar Usuario", fg_color="green", command=self.guardar_usuario)
        self.btn_guardar.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew", padx=10)

        self.btn_limpiar = ctk.CTkButton(self.frame_form, text="Limpiar", fg_color="gray", command=self.limpiar_campos)
        self.btn_limpiar.grid(row=1, column=2, pady=10, padx=10)

        # --- LISTA DE USUARIOS (READ / DELETE) ---
        self.lista_usuarios_frame = ctk.CTkScrollableFrame(self, label_text="Usuarios en el Sistema")
        self.lista_usuarios_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # BOTÓN VOLVER
        self.btn_volver = ctk.CTkButton(self, text="Volver al login", command=self.ir_al_login)
        self.btn_volver.pack(pady=10)

    def cargar_usuarios(self):
        """Limpia la lista y la vuelve a llenar desde la DB"""
        # Limpiar widgets previos en el frame de la lista
        for widget in self.lista_usuarios_frame.winfo_children():
            widget.destroy()

        usuarios = self.db.obtener_usuarios()
        for user in usuarios:
            user_id, nombre, rol = user
            
            fila = ctk.CTkFrame(self.lista_usuarios_frame)
            fila.pack(fill="x", pady=2, padx=5)

            ctk.CTkLabel(fila, text=f"{nombre} ({rol})", width=200, anchor="w").pack(side="left", padx=10)
            
            # Botón Eliminar
            ctk.CTkButton(fila, text="Eliminar", fg_color="#E74C3C", width=80, 
                          command=lambda i=user_id: self.eliminar(i)).pack(side="right", padx=5)
            
            # Botón Editar
            ctk.CTkButton(fila, text="Editar", fg_color="#3498DB", width=80, 
                          command=lambda u=user: self.preparar_edicion(u)).pack(side="right", padx=5)

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        password = self.entry_pass.get()
        rol = self.combo_rol.get()

        if not nombre or not password:
            messagebox.showwarning("Atención", "Completa todos los campos")
            return

        if self.usuario_seleccionado_id:
            # ACTUALIZAR
            exito, msg = self.db.actualizar_usuario(self.usuario_seleccionado_id, nombre, password, rol)
        else:
            # CREAR
            exito, msg = self.db.agregar_usuario(nombre, password, rol)

        if exito:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_campos()
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", msg)

    def preparar_edicion(self, datos_user):
        self.usuario_seleccionado_id, nombre, rol = datos_user
        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, nombre)
        self.combo_rol.set(rol)
        self.btn_guardar.configure(text="Guardar Cambios", fg_color="orange")

    def eliminar(self, user_id):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este usuario?"):
            self.db.eliminar_usuario(user_id)
            self.cargar_usuarios()

    def limpiar_campos(self):
        self.usuario_seleccionado_id = None
        self.entry_nombre.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.btn_guardar.configure(text="Registrar Usuario", fg_color="green")

    def ir_al_login(self):
        self.destroy()
        from gui_login import LoginWindow
        app = LoginWindow()
        app.mainloop()

if __name__ == "__main__":
    app = AdminWindow()
    app.mainloop()