import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2  # Para conectarse a PostgreSQL
from psycopg2 import sql

# Funciones para botones (sin funcionalidad completa)
def nuevo_registro():
    entry_nombre.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    messagebox.showinfo("Nuevo", "Listo para agregar un nuevo registro.")

def registrar_usuario():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()
    identificador = entry_id.get()

    if nombre and correo and contraseña and identificador:
        messagebox.showinfo("Registro exitoso", f"Usuario {nombre} con ID {identificador} registrado con éxito.")
        entry_nombre.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        entry_id.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Todos los campos son obligatorios.")

def eliminar_usuario():
    messagebox.showinfo("Eliminar", "Funcionalidad de eliminar usuario (por implementar).")

def buscar_usuario():
    messagebox.showinfo("Buscar", "Funcionalidad de buscar usuario por ID (por implementar).")

def editar_usuario():
    messagebox.showinfo("Editar", "Funcionalidad de editar usuario (por implementar).")

# Funciones para abrir nuevas ventanas desde el menú
def abrir_ventana_medicos():
    ventana_medicos = tk.Toplevel()
    ventana_medicos.title("Médicos")
    ventana_medicos.geometry("400x450")
    ventana_medicos.configure(bg="#FEFCFD")
  
    frame_campos = tk.Frame(ventana_medicos, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Etiquetas y entradas de texto
    label_id = tk.Label(frame_campos, text="ID (Identificador):", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_id = tk.Entry(frame_campos)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    label_nombre = tk.Label(frame_campos, text="Nombre:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_nombre = tk.Entry(frame_campos)
    entry_nombre.grid(row=1, column=1, padx=10, pady=10)

    label_apellido = tk.Label(frame_campos, text="Apellido:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_apellido = tk.Entry(frame_campos)
    entry_apellido.grid(row=2, column=1, padx=10, pady=10)

    label_correo = tk.Label(frame_campos, text="Correo:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_correo.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_correo = tk.Entry(frame_campos)
    entry_correo.grid(row=3, column=1, padx=10, pady=10)

    label_cedula = tk.Label(frame_campos, text="Numero de Cedula:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_cedula.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_cedula = tk.Entry(frame_campos, show="*")
    entry_cedula.grid(row=4, column=1, padx=10, pady=10)

    label_especialidad = tk.Label(frame_campos, text="Especialidad:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_especialidad.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_especialidad = tk.Entry(frame_campos, show="*")
    entry_especialidad.grid(row=5, column=1, padx=10, pady=10)

    # Frame para los botones
    frame_botones = tk.Frame(ventana_medicos, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)

    # Botones de la interfaz
    boton_nuevo = tk.Button(frame_botones, text="Nuevo", command=nuevo_registro, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_nuevo.grid(row=0, column=0, padx=10, pady=5)

    boton_registrar = tk.Button(frame_botones, text="Registrar", command=registrar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_registrar.grid(row=0, column=1, padx=10, pady=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_eliminar.grid(row=1, column=0, padx=10, pady=5)

    boton_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_buscar.grid(row=1, column=2, padx=10, pady=5)

    boton_editar = tk.Button(frame_botones, text="Editar", command=editar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_editar.grid(row=1, column=1,  padx=10, pady=5)



    entry_buscar = tk.Entry(frame_botones, show="*")
    entry_buscar.grid(row=0, column=2, padx=10, pady=10)




def abrir_ventana_pacientes():
    ventana_pacientes = tk.Toplevel()
    ventana_pacientes.title("Pacientes")
    ventana_pacientes.geometry("400x450")
    ventana_pacientes.configure(bg="#FEFCFD")
    frame_campos = tk.Frame(ventana_pacientes, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Etiquetas y entradas de texto
    label_id = tk.Label(frame_campos, text="ID (Identificador):", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_id = tk.Entry(frame_campos)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    label_nombre = tk.Label(frame_campos, text="Nombre:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_nombre = tk.Entry(frame_campos)
    entry_nombre.grid(row=1, column=1, padx=10, pady=10)

    label_apellido = tk.Label(frame_campos, text="Apellido:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_apellido = tk.Entry(frame_campos)
    entry_apellido.grid(row=2, column=1, padx=10, pady=10)
    
    label_nacimiento = tk.Label(frame_campos, text="Fecha De Nacimiento:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_nacimiento.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_nacimiento = tk.Entry(frame_campos)
    entry_nacimiento.grid(row=3, column=1, padx=10, pady=10)

    label_genero = tk.Label(frame_campos, text="Genero:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_genero.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_genero = tk.Entry(frame_campos)
    entry_genero.grid(row=4, column=1, padx=10, pady=10)

    label_correo = tk.Label(frame_campos, text="Correo:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_correo.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_correo = tk.Entry(frame_campos)
    entry_correo.grid(row=5, column=1, padx=10, pady=10)

    label_celular = tk.Label(frame_campos, text="Numero de Celular:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_celular.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    entry_celular = tk.Entry(frame_campos, show="*")
    entry_celular.grid(row=6, column=1, padx=10, pady=10)

    label_especialidad = tk.Label(frame_campos, text="Alergias:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_especialidad.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    entry_especialidad = tk.Entry(frame_campos, show="*")
    entry_especialidad.grid(row=7, column=1, padx=10, pady=10)

    label_observaciones = tk.Label(frame_campos, text="Observaciones:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_observaciones.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    entry_observaciones = tk.Entry(frame_campos, show="*")
    entry_observaciones.grid(row=7, column=1, padx=10, pady=10)


    # Frame para los botones
    frame_botones = tk.Frame(ventana_pacientes, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)

    # Botones de la interfaz
    boton_nuevo = tk.Button(frame_botones, text="Nuevo", command=nuevo_registro, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_nuevo.grid(row=0, column=0, padx=10, pady=5)

    boton_registrar = tk.Button(frame_botones, text="Registrar", command=registrar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_registrar.grid(row=0, column=1, padx=10, pady=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_eliminar.grid(row=1, column=0, padx=10, pady=5)

    boton_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_buscar.grid(row=1, column=2, padx=10, pady=5)

    boton_editar = tk.Button(frame_botones, text="Editar", command=editar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_editar.grid(row=1, column=1,  padx=10, pady=5)



    entry_buscar = tk.Entry(frame_botones, show="*")
    entry_buscar.grid(row=0, column=2, padx=10, pady=10)




def abrir_ventana_enfermedades():
    ventana_enfermedades = tk.Toplevel()
    ventana_enfermedades.title("Enfermedades")
    ventana_enfermedades.geometry("300x400")
    tk.Label(ventana_enfermedades, text="Ventana de Enfermedades").pack(pady=20)

    ventana_enfermedades.configure(bg="#FEFCFD")
    frame_campos = tk.Frame(ventana_enfermedades, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Etiquetas y entradas de texto
    label_id = tk.Label(frame_campos, text="ID (Identificador):", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_id = tk.Entry(frame_campos)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    label_nombreE = tk.Label(frame_campos, text="Nombre Enfermedad:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_nombreE.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_nombreE = tk.Entry(frame_campos)
    entry_nombreE.grid(row=1, column=1, padx=10, pady=10)

    label_tipoe = tk.Label(frame_campos, text="Tipo de enfermedad:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_tipoe.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_tipoe = tk.Entry(frame_campos)
    entry_tipoe.grid(row=2, column=1, padx=10, pady=10)
    
    label_descripcion = tk.Label(frame_campos, text="Descripcion:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_descripcion.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_descripcion = tk.Entry(frame_campos)
    entry_descripcion.grid(row=3, column=1, padx=10, pady=10)

    label_sintomas = tk.Label(frame_campos, text="Sintomas:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_sintomas.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_sintomas = tk.Entry(frame_campos)
    entry_sintomas.grid(row=4, column=1, padx=10, pady=10)

    label_causas = tk.Label(frame_campos, text="Causas:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_causas.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_causas = tk.Entry(frame_campos)
    entry_causas.grid(row=5, column=1, padx=10, pady=10)

    label_compli = tk.Label(frame_campos, text="Complicaciones:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_compli.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    entry_compli = tk.Entry(frame_campos, show="*")
    entry_compli.grid(row=6, column=1, padx=10, pady=10)

    label_tratamiento = tk.Label(frame_campos, text="Tratamiento recomendado:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_tratamiento.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    entry_tratamiento = tk.Entry(frame_campos, show="*")
    entry_tratamiento.grid(row=7, column=1, padx=10, pady=10)

    # Frame para los botones
    frame_botones = tk.Frame(ventana_enfermedades, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)

    # Botones de la interfaz
    boton_nuevo = tk.Button(frame_botones, text="Nuevo", command=nuevo_registro, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_nuevo.grid(row=0, column=0, padx=10, pady=5)

    boton_registrar = tk.Button(frame_botones, text="Registrar", command=registrar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_registrar.grid(row=0, column=1, padx=10, pady=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_eliminar.grid(row=1, column=0, padx=10, pady=5)

    boton_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_buscar.grid(row=1, column=2, padx=10, pady=5)

    boton_editar = tk.Button(frame_botones, text="Editar", command=editar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_editar.grid(row=1, column=1,  padx=10, pady=5)



    entry_buscar = tk.Entry(frame_botones, show="*")
    entry_buscar.grid(row=0, column=2, padx=10, pady=10)

def abrir_ventana_signos():
    ventana_signos = tk.Toplevel()
    ventana_signos.title("Signos")
    ventana_signos.geometry("300x400")
    tk.Label(ventana_signos, text="Ventana de Signos").pack(pady=20)

    ventana_signos.configure(bg="#FEFCFD")
    frame_campos = tk.Frame(ventana_signos, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Etiquetas y entradas de texto
    label_id = tk.Label(frame_campos, text="ID (Identificador):", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_id = tk.Entry(frame_campos)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    label_fecha = tk.Label(frame_campos, text="Fecha:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_fecha.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_fecha = tk.Entry(frame_campos)
    entry_fecha.grid(row=1, column=1, padx=10, pady=10)

    label_hora = tk.Label(frame_campos, text="Hora:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_hora.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_hora = tk.Entry(frame_campos)
    entry_hora.grid(row=2, column=1, padx=10, pady=10)
    
    label_temperatura = tk.Label(frame_campos, text="Temperatura Corporal:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_temperatura.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_temperatura = tk.Entry(frame_campos)
    entry_temperatura.grid(row=3, column=1, padx=10, pady=10)
    
    label_freC = tk.Label(frame_campos, text="Frecuencia cardiaca:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_freC.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_freC = tk.Entry(frame_campos)
    entry_freC.grid(row=4, column=1, padx=10, pady=10)

    label_freR = tk.Label(frame_campos, text="Frecuencia respiratoria:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_freR.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_freR = tk.Entry(frame_campos)
    entry_freR.grid(row=5, column=1, padx=10, pady=10)

    label_presion = tk.Label(frame_campos, text="Presion Arterial:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_presion.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    entry_presion = tk.Entry(frame_campos)
    entry_presion.grid(row=6, column=1, padx=10, pady=10)

    label_saturacion = tk.Label(frame_campos, text="Saturacion Oxigeno:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_saturacion.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    entry_saturacion = tk.Entry(frame_campos, show="*")
    entry_saturacion.grid(row=7, column=1, padx=10, pady=10)

    label_peso = tk.Label(frame_campos, text="Peso:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_peso.grid(row=8, column=0, padx=10, pady=10, sticky="w")
    entry_peso = tk.Entry(frame_campos, show="*")
    entry_peso.grid(row=8, column=1, padx=10, pady=10)

    label_estatura = tk.Label(frame_campos, text="Estatura:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_estatura.grid(row=9, column=0, padx=10, pady=10, sticky="w")
    entry_estatura = tk.Entry(frame_campos, show="*")
    entry_estatura.grid(row=9, column=1, padx=10, pady=10)

    label_imc = tk.Label(frame_campos, text="IMC:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_imc.grid(row=10, column=0, padx=10, pady=10, sticky="w")
    entry_imc = tk.Entry(frame_campos, show="*")
    entry_imc.grid(row=10, column=1, padx=10, pady=10)

    # Frame para los botones
    frame_botones = tk.Frame(ventana_signos, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)

    # Botones de la interfaz
    boton_nuevo = tk.Button(frame_botones, text="Nuevo", command=nuevo_registro, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_nuevo.grid(row=0, column=0, padx=10, pady=5)

    boton_registrar = tk.Button(frame_botones, text="Registrar", command=registrar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_registrar.grid(row=0, column=1, padx=10, pady=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_eliminar.grid(row=1, column=0, padx=10, pady=5)

    boton_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_buscar.grid(row=1, column=2, padx=10, pady=5)

    boton_editar = tk.Button(frame_botones, text="Editar", command=editar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_editar.grid(row=1, column=1,  padx=10, pady=5)



    entry_buscar = tk.Entry(frame_botones, show="*")
    entry_buscar.grid(row=0, column=2, padx=10, pady=10)


def verificar_credenciales(entry_correo, entry_contraseña, ventana_login,ventana_principal):
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()
    
    try:
        # Conectar a la base de datos
        conexion = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="example",
            host="localhost",
            port="5555"
        )
        
        cursor = conexion.cursor()
        
        # Consulta para verificar el correo y la contraseña
        consulta = sql.SQL("SELECT rol FROM usuarios WHERE correo = %s AND contraseña = %s")
        cursor.execute(consulta, (correo, contraseña))
        resultado = cursor.fetchone()
        resultado = ['Administrador'] # Eliminar esta línea para probar el login con la base de datos
        if resultado:
            rol = resultado[0]
            messagebox.showinfo("Login exitoso", f"Bienvenido, {rol}")
            cursor.close()
            conexion.close()
            ventana_login.destroy()
            ventana_principal.deiconify()
            return 0
            
            # Aquí podrías abrir la ventana específica del rol
            # abrir_ventana_administrador() o abrir_ventana_medico()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")
            cursor.close()
            conexion.close()
            return 1        

    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")

def abrir_ventana_login(ventana_principal):
    ventana_login = tk.Toplevel()
    ventana_login.title("Login")
    ventana_login.geometry("300x200")
    ventana_login.configure(bg="#FEFCFD")
    
    frame_campos = tk.Frame(ventana_login, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)
    
    # Etiquetas y campos de entrada
    label_correo = tk.Label(frame_campos, text="Correo:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_correo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_correo = tk.Entry(frame_campos)
    entry_correo.grid(row=0, column=1, padx=10, pady=10)
    
    label_contraseña = tk.Label(frame_campos, text="Contraseña:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_contraseña.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_contraseña = tk.Entry(frame_campos, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)
    
    # Botón de login
    boton_login = tk.Button(ventana_login, text="Iniciar sesión", command=lambda: verificar_credenciales(entry_correo, entry_contraseña,ventana_login,ventana_principal), bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    boton_login.pack(pady=10)
    
    ventana_login.mainloop()

# Ejecutar la ventana de login



def abrir_ventana_diagnostico():
    ventana_diagnostico = tk.Toplevel()
    ventana_diagnostico.title("Diagnóstico")
    ventana_diagnostico.geometry("300x400")
    
    ventana_diagnostico.configure(bg="#FEFCFD")
    frame_campos = tk.Frame(ventana_diagnostico, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Etiquetas y entradas de texto
    label_id = tk.Label(frame_campos, text="ID (Identificador):", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_id.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_id = tk.Entry(frame_campos)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    label_nom = tk.Label(frame_campos, text="Nombre Paciente:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_nom.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_nom = tk.Entry(frame_campos)
    entry_nom.grid(row=2, column=1, padx=10, pady=10)
    
    label_fechaD = tk.Label(frame_campos, text="Fecha Diagnostico:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_fechaD.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_fechaD = tk.Entry(frame_campos)
    entry_fechaD.grid(row=1, column=1, padx=10, pady=10)
    
    label_temperatura = tk.Label(frame_campos, text="Sintomas Presentados:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_temperatura.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_temperatura = tk.Entry(frame_campos)
    entry_temperatura.grid(row=3, column=1, padx=10, pady=10)
    
    label_freC = tk.Label(frame_campos, text="Diagnostico Principal:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_freC.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_freC = tk.Entry(frame_campos)
    entry_freC.grid(row=4, column=1, padx=10, pady=10)

    label_freR = tk.Label(frame_campos, text="Diagnostico Secundario:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_freR.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    entry_freR = tk.Entry(frame_campos)
    entry_freR.grid(row=5, column=1, padx=10, pady=10)

    label_presion = tk.Label(frame_campos, text="Pruebas Realizadas:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_presion.grid(row=6, column=0, padx=10, pady=10, sticky="w")
    entry_presion = tk.Entry(frame_campos)
    entry_presion.grid(row=6, column=1, padx=10, pady=10)

    label_saturacion = tk.Label(frame_campos, text="Resultado De Pruebas:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_saturacion.grid(row=7, column=0, padx=10, pady=10, sticky="w")
    entry_saturacion = tk.Entry(frame_campos, show="*")
    entry_saturacion.grid(row=7, column=1, padx=10, pady=10)

    label_peso = tk.Label(frame_campos, text="Tratamiento recomendado:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_peso.grid(row=8, column=0, padx=10, pady=10, sticky="w")
    entry_peso = tk.Entry(frame_campos, show="*")
    entry_peso.grid(row=8, column=1, padx=10, pady=10)

    label_estatura = tk.Label(frame_campos, text="Duracion de tratamiento:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_estatura.grid(row=9, column=0, padx=10, pady=10, sticky="w")
    entry_estatura = tk.Entry(frame_campos, show="*")
    entry_estatura.grid(row=9, column=1, padx=10, pady=10)

    label_imc = tk.Label(frame_campos, text="Comentarios/Observaciones:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_imc.grid(row=10, column=0, padx=10, pady=10, sticky="w")
    entry_imc = tk.Entry(frame_campos, show="*")
    entry_imc.grid(row=10, column=1, padx=10, pady=10)

    
    label_imc = tk.Label(frame_campos, text="Estado del paciente:", bg="#FEFCFD", font=("Arial", 10, "bold"))
    label_imc.grid(row=11, column=0, padx=10, pady=10, sticky="w")
    entry_imc = tk.Entry(frame_campos, show="*")
    entry_imc.grid(row=11, column=1, padx=10, pady=10)

    # Frame para los botones
    frame_botones = tk.Frame(ventana_diagnostico, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)

    # Botones de la interfaz
    boton_nuevo = tk.Button(frame_botones, text="Nuevo", command=nuevo_registro, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_nuevo.grid(row=0, column=0, padx=10, pady=5)

    boton_registrar = tk.Button(frame_botones, text="Registrar", command=registrar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_registrar.grid(row=0, column=1, padx=10, pady=5)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_eliminar.grid(row=1, column=0, padx=10, pady=5)

    boton_buscar = tk.Button(frame_botones, text="Buscar", command=buscar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_buscar.grid(row=1, column=2, padx=10, pady=5)

    boton_editar = tk.Button(frame_botones, text="Editar", command=editar_usuario, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
    boton_editar.grid(row=1, column=1,  padx=10, pady=5)



    entry_buscar = tk.Entry(frame_botones, show="*")
    entry_buscar.grid(row=0, column=2, padx=10, pady=10)


# Configuración de la ventana principal
def configurar_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("400x450")
    ventana.configure(bg="#FEFCFD")
    configurar_menu(ventana)
    configurar_frame_campos(ventana)
    configurar_frame_botones(ventana)
    return ventana

def configurar_menu(ventana):
    menu_bar = tk.Menu(ventana)
    ventana.config(menu=menu_bar)
    
    # Menú "Opciones"
    menu_opciones = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Opciones", menu=menu_opciones)
    menu_opciones.add_command(label="Médicos", command=abrir_ventana_medicos)
    menu_opciones.add_command(label="Pacientes", command=abrir_ventana_pacientes)
    menu_opciones.add_command(label="Enfermedades", command=abrir_ventana_enfermedades)
    menu_opciones.add_command(label="Signos", command=abrir_ventana_signos)
    menu_opciones.add_command(label="Diagnóstico", command=abrir_ventana_diagnostico)

def configurar_frame_campos(ventana):
    frame_campos = tk.Frame(ventana, bg="#FEFCFD", bd=2, relief=tk.GROOVE)
    frame_campos.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)
    
    # Etiquetas y entradas de texto
    campos = [
        ("ID (Identificador):", "entry_id"),
        ("Nombre:", "entry_nombre"),
        ("Apellido:", "entry_apellido"),
        ("Correo:", "entry_correo"),
        ("Contraseña:", "entry_contraseña", "*")
    ]
    
    for i, (label_text, entry_var, *show) in enumerate(campos):
        label = tk.Label(frame_campos, text=label_text, bg="#FEFCFD", font=("Arial", 10, "bold"))
        label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
        entry = tk.Entry(frame_campos, show=show[0] if show else "")
        entry.grid(row=i, column=1, padx=10, pady=10)
        globals()[entry_var] = entry  # Guardamos las referencias globales de las entradas

def configurar_frame_botones(ventana):
    frame_botones = tk.Frame(ventana, bg="#fefcfd")
    frame_botones.pack(pady=10, padx=10, fill=tk.BOTH)
    
    # Configuración de botones
    botones = [
        ("Nuevo", nuevo_registro),
        ("Registrar", registrar_usuario),
        ("Eliminar", eliminar_usuario),
        ("Buscar", buscar_usuario),
        ("Editar", editar_usuario)
    ]
    
    for i, (text, command) in enumerate(botones):
        boton = tk.Button(frame_botones, text=text, command=command, bg="#8fbfec", fg="#fff", width=12, font=("Arial", 10, "bold"))
        boton.grid(row=i // 2, column=i % 2, padx=10, pady=5)
        
    # Campo de búsqueda
    global entry_buscar
    entry_buscar = tk.Entry(frame_botones, show="*")
 

ventana = configurar_ventana_principal()
ventana.withdraw()
abrir_ventana_login(ventana)
ventana.mainloop()
