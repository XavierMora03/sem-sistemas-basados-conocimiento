import tkinter as tk
from tkinter import messagebox
import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="example",
            host="localhost",
            port="5555"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        tk.Label(root, text="Correo").pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        tk.Label(root, text="Contraseña").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack()

    def login(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            email = self.email_entry.get()
            password = self.password_entry.get()

            query = "SELECT * FROM usuarios WHERE correo=%s AND contraseña=%s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Login Success", "Welcome!")
                self.root.destroy()
                app = CRUDApp(tk.Tk())
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
            cursor.close()
            conn.close()

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD System")

        # Frame for Menu Options
        frame = tk.Frame(root)
        frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(frame, text="Usuarios", command=self.manage_users).pack(side=tk.LEFT)
        tk.Button(frame, text="Pacientes", command=self.manage_patients).pack(side=tk.LEFT)
        tk.Button(frame, text="Enfermedades", command=self.manage_diseases).pack(side=tk.LEFT)
        tk.Button(frame, text="Médicos", command=self.manage_medicos).pack(side=tk.LEFT)
        tk.Button(frame, text="Pacientes", command=self.manage_patients).pack(side=tk.LEFT)
        tk.Button(frame, text="Signos", command=self.manage_signos).pack(side=tk.LEFT)
        tk.Button(frame, text="Síntomas", command=self.manage_sintomas).pack(side=tk.LEFT)


        # Display frame
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

    def manage_users(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="User Management").pack()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, correo, rol FROM usuarios")
            users = cursor.fetchall()

            # Display each user with Edit and Delete options
            for user in users:
                user_frame = tk.Frame(self.display_frame)
                user_frame.pack(fill=tk.X, padx=5, pady=5)

                user_info = f"ID: {user[0]}, Nombre: {user[1]}, Correo: {user[2]}, Rol: {user[3]}"
                tk.Label(user_frame, text=user_info).pack(side=tk.LEFT)

                tk.Button(user_frame, text="Edit", command=lambda u=user: self.edit_user(u)).pack(side=tk.RIGHT, padx=5)
                tk.Button(user_frame, text="Delete", command=lambda u=user: self.delete_user(u[0])).pack(side=tk.RIGHT)

            cursor.close()
            conn.close()

        # Add a button to create a new user
        tk.Button(self.display_frame, text="Add New User", command=self.add_user).pack(pady=10)


    def edit_user(self, user):
        edit_user_window = tk.Toplevel(self.root)
        edit_user_window.title("Edit User")

        tk.Label(edit_user_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(edit_user_window)
        name_entry.insert(0, user[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_user_window, text="Correo").grid(row=1, column=0)
        email_entry = tk.Entry(edit_user_window)
        email_entry.insert(0, user[2])
        email_entry.grid(row=1, column=1)

        tk.Label(edit_user_window, text="Rol").grid(row=2, column=0)
        role_var = tk.StringVar(edit_user_window)
        role_var.set(user[3])  # Set current role as default
        role_dropdown = tk.OptionMenu(edit_user_window, role_var, "administrador", "medico")
        role_dropdown.grid(row=2, column=1)

        tk.Button(edit_user_window, text="Save Changes", command=lambda: self.save_edited_user(user[0], name_entry, email_entry, role_var)).grid(row=3, columnspan=2)

    def save_edited_user(self, user_id, name_entry, email_entry, role_var):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s WHERE id=%s"
            cursor.execute(query, (name_entry.get(), email_entry.get(), role_var.get(), user_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "User updated successfully!")
            self.manage_users()

    def add_user(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add User")

        tk.Label(add_user_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(add_user_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_user_window, text="Correo").grid(row=1, column=0)
        email_entry = tk.Entry(add_user_window)
        email_entry.grid(row=1, column=1)

        tk.Label(add_user_window, text="Rol").grid(row=2, column=0)
        role_var = tk.StringVar(add_user_window)
        role_var.set("medico")  # Set default role
        role_dropdown = tk.OptionMenu(add_user_window, role_var, "administrador", "medico")
        role_dropdown.grid(row=2, column=1)

        tk.Label(add_user_window, text="Contraseña").grid(row=3, column=0)
        password_entry = tk.Entry(add_user_window, show="*")
        password_entry.grid(row=3, column=1)

        tk.Button(add_user_window, text="Save", command=lambda: self.save_user(name_entry, email_entry, role_var, password_entry)).grid(row=4, columnspan=2)

    def save_user(self, name_entry, email_entry, role_var, password_entry):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO usuarios (nombre, correo, rol, contraseña) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name_entry.get(), email_entry.get(), role_var.get(), password_entry.get()))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "User added successfully!")
            self.manage_users()

    def manage_patients(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Patient Management").pack()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, fecha_nacimiento, genero, direccion, telefono FROM pacientes")
            patients = cursor.fetchall()

            for patient in patients:
                patient_frame = tk.Frame(self.display_frame)
                patient_frame.pack(fill=tk.X, padx=5, pady=5)

                patient_info = f"ID: {patient[0]}, Nombre: {patient[1]}, Fecha de Nacimiento: {patient[2]}, Género: {patient[3]}, Dirección: {patient[4]}, Teléfono: {patient[5]}"
                tk.Label(patient_frame, text=patient_info).pack(side=tk.LEFT)

                tk.Button(patient_frame, text="Edit", command=lambda p=patient: self.edit_patient(p)).pack(side=tk.RIGHT, padx=5)
                tk.Button(patient_frame, text="Delete", command=lambda p=patient: self.delete_patient(p[0])).pack(side=tk.RIGHT)

            cursor.close()
            conn.close()

        tk.Button(self.display_frame, text="Add Patient", command=self.add_patient).pack()

    def delete_patient(self, patient_id):
        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this patient?")
        if confirm:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pacientes WHERE id=%s", (patient_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.manage_patients()

    def add_patient(self):
        add_patient_window = tk.Toplevel(self.root)
        add_patient_window.title("Add Patient")

        tk.Label(add_patient_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(add_patient_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_patient_window, text="Fecha de Nacimiento (YYYY-MM-DD)").grid(row=1, column=0)
        dob_entry = tk.Entry(add_patient_window)
        dob_entry.grid(row=1, column=1)

        tk.Label(add_patient_window, text="Género").grid(row=2, column=0)
        gender_var = tk.StringVar(add_patient_window)
        gender_var.set("Masculino")  # Default selection
        gender_dropdown = tk.OptionMenu(add_patient_window, gender_var, "Masculino", "Femenino", "Otro")
        gender_dropdown.grid(row=2, column=1)

        tk.Label(add_patient_window, text="Dirección").grid(row=3, column=0)
        address_entry = tk.Entry(add_patient_window)
        address_entry.grid(row=3, column=1)

        tk.Label(add_patient_window, text="Teléfono").grid(row=4, column=0)
        phone_entry = tk.Entry(add_patient_window)
        phone_entry.grid(row=4, column=1)

        tk.Button(add_patient_window, text="Save", command=lambda: self.save_patient(name_entry, dob_entry, gender_var, address_entry, phone_entry)).grid(row=5, columnspan=2)

    def save_patient(self, name_entry, dob_entry, gender_var, address_entry, phone_entry):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO pacientes (nombre, fecha_nacimiento, genero, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name_entry.get(), dob_entry.get(), gender_var.get(), address_entry.get(), phone_entry.get()))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Patient added successfully!")
            self.manage_patients()

    def edit_patient(self, patient):
        edit_patient_window = tk.Toplevel(self.root)
        edit_patient_window.title("Edit Patient")

        tk.Label(edit_patient_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(edit_patient_window)
        name_entry.insert(0, patient[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_patient_window, text="Fecha de Nacimiento (YYYY-MM-DD)").grid(row=1, column=0)
        dob_entry = tk.Entry(edit_patient_window)
        dob_entry.insert(0, patient[2])
        dob_entry.grid(row=1, column=1)

        tk.Label(edit_patient_window, text="Género").grid(row=2, column=0)
        gender_var = tk.StringVar(edit_patient_window)
        gender_var.set(patient[3])  # Current gender as default
        gender_dropdown = tk.OptionMenu(edit_patient_window, gender_var, "Masculino", "Femenino", "Otro")
        gender_dropdown.grid(row=2, column=1)

        tk.Label(edit_patient_window, text="Dirección").grid(row=3, column=0)
        address_entry = tk.Entry(edit_patient_window)
        address_entry.insert(0, patient[4])
        address_entry.grid(row=3, column=1)

        tk.Label(edit_patient_window, text="Teléfono").grid(row=4, column=0)
        phone_entry = tk.Entry(edit_patient_window)
        phone_entry.insert(0, patient[5])
        phone_entry.grid(row=4, column=1)

        tk.Button(edit_patient_window, text="Save Changes", command=lambda: self.save_edited_patient(patient[0], name_entry, dob_entry, gender_var, address_entry, phone_entry)).grid(row=5, columnspan=2)

    def save_edited_patient(self, patient_id, name_entry, dob_entry, gender_var, address_entry, phone_entry):   
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "UPDATE pacientes SET nombre=%s, fecha_nacimiento=%s, genero=%s, direccion=%s, telefono=%s WHERE id=%s"
            cursor.execute(query, (name_entry.get(), dob_entry.get(), gender_var.get(), address_entry.get(), phone_entry.get(), patient_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.manage_patients()


    def manage_diseases(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Gestión de Enfermedades").pack()

        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, descripcion FROM enfermedades")
                diseases = cursor.fetchall()

                for disease in diseases:
                    disease_frame = tk.Frame(self.display_frame)
                    disease_frame.pack(fill=tk.X, padx=5, pady=5)

                    disease_info = f"ID: {disease[0]}, Nombre: {disease[1]}, Descripción: {disease[2]}"
                    tk.Label(disease_frame, text=disease_info).pack(side=tk.LEFT)

                    tk.Button(disease_frame, text="Editar", command=lambda d=disease: self.edit_disease(d)).pack(side=tk.RIGHT, padx=5)
                    tk.Button(disease_frame, text="Eliminar", command=lambda d=disease: self.delete_disease(d[0])).pack(side=tk.RIGHT)

                cursor.close()
                conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al conectarse a la base de datos: {str(e)}")

        tk.Button(self.display_frame, text="Añadir Enfermedad", command=self.add_disease).pack(pady=10)

    def add_disease(self):
        add_disease_window = tk.Toplevel(self.root)
        add_disease_window.title("Añadir Enfermedad")

        tk.Label(add_disease_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(add_disease_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_disease_window, text="Descripción").grid(row=1, column=0)
        description_entry = tk.Entry(add_disease_window)
        description_entry.grid(row=1, column=1)

        tk.Button(add_disease_window, text="Guardar", command=lambda: self.save_disease(name_entry, description_entry)).grid(row=2, columnspan=2)


    def edit_disease(self, disease):
        edit_disease_window = tk.Toplevel(self.root)
        edit_disease_window.title("Editar Enfermedad")

        tk.Label(edit_disease_window, text="Nombre").grid(row=0, column=0)
        name_entry = tk.Entry(edit_disease_window)
        name_entry.insert(0, disease[1])
        name_entry.grid(row=0, column=1)

        tk.Label(edit_disease_window, text="Descripción").grid(row=1, column=0)
        description_entry = tk.Entry(edit_disease_window)
        description_entry.insert(0, disease[2])
        description_entry.grid(row=1, column=1)

        tk.Button(edit_disease_window, text="Guardar Cambios", command=lambda: self.save_edited_disease(disease[0], name_entry, description_entry)).grid(row=2, columnspan=2)

    def save_edited_disease(self, disease_id, name_entry, description_entry):
        nombre = name_entry.get().strip()
        descripcion = description_entry.get().strip()

        if not nombre or not descripcion:
            messagebox.showwarning("Datos faltantes", "Por favor, complete todos los campos.")
            return

        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                query = "UPDATE enfermedades SET nombre=%s, descripcion=%s WHERE id=%s"
                cursor.execute(query, (nombre, descripcion, disease_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Enfermedad actualizada correctamente.")
                self.manage_diseases()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la enfermedad: {str(e)}")

    def save_disease(self, name_entry, description_entry):
        nombre = name_entry.get().strip()
        descripcion = description_entry.get().strip()

        if not nombre or not descripcion:
            messagebox.showwarning("Datos faltantes", "Por favor, complete todos los campos.")
            return

        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                query = "INSERT INTO enfermedades (nombre, descripcion) VALUES (%s, %s)"
                cursor.execute(query, (nombre, descripcion))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Enfermedad añadida correctamente.")
                self.manage_diseases()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir la enfermedad: {str(e)}")

    def delete_disease(self, disease_id):
        confirm = messagebox.askyesno("Confirmación de Eliminación", "¿Está seguro de que desea eliminar esta enfermedad?")
        if confirm:
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM enfermedades WHERE id=%s", (disease_id,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Éxito", "Enfermedad eliminada correctamente.")
                    self.manage_diseases()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la enfermedad: {str(e)}")

    #### MEdicos
    def manage_medicos(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Gestión de Médicos").pack()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT medicos.id, usuarios.nombre, usuarios.correo, medicos.especialidad
                FROM medicos
                JOIN usuarios ON medicos.usuario_id = usuarios.id
            """
            cursor.execute(query)
            medicos = cursor.fetchall()

            for medico in medicos:
                medico_frame = tk.Frame(self.display_frame)
                medico_frame.pack(fill=tk.X, padx=5, pady=5)

                medico_info = f"ID: {medico[0]}, Nombre: {medico[1]}, Correo: {medico[2]}, Especialidad: {medico[3]}"
                tk.Label(medico_frame, text=medico_info).pack(side=tk.LEFT)

                tk.Button(medico_frame, text="Editar", command=lambda m=medico: self.edit_medico(m)).pack(side=tk.RIGHT, padx=5)
                tk.Button(medico_frame, text="Eliminar", command=lambda m=medico: self.delete_medico(m[0])).pack(side=tk.RIGHT)

            cursor.close()
            conn.close()

        tk.Button(self.display_frame, text="Añadir Médico", command=self.add_medico).pack(pady=10)

    def add_medico(self):
        add_medico_window = tk.Toplevel(self.root)
        add_medico_window.title("Añadir Médico")

        tk.Label(add_medico_window, text="Usuario").grid(row=0, column=0)
        usuario_var = tk.StringVar(add_medico_window)
        
        # Obtener la lista de usuarios para seleccionar
        conn = connect_db()
        usuarios = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conn.close()
        
        usuario_options = [f"{usuario[0]} - {usuario[1]}" for usuario in usuarios]
        if not usuario_options:
            messagebox.showwarning("Sin Usuarios", "No hay usuarios disponibles. Por favor, añade un usuario primero.")
            add_medico_window.destroy()
            return
        
        usuario_var.set(usuario_options[0])
        usuario_dropdown = tk.OptionMenu(add_medico_window, usuario_var, *usuario_options)
        usuario_dropdown.grid(row=0, column=1)

        tk.Label(add_medico_window, text="Especialidad").grid(row=1, column=0)
        especialidad_entry = tk.Entry(add_medico_window)
        especialidad_entry.grid(row=1, column=1)

        tk.Button(add_medico_window, text="Guardar", command=lambda: self.save_medico(usuario_var, especialidad_entry, add_medico_window)).grid(row=2, columnspan=2)

    def save_medico(self, usuario_var, especialidad_entry, window):
        usuario_selected = usuario_var.get()
        usuario_id = int(usuario_selected.split(" - ")[0])
        especialidad = especialidad_entry.get().strip()

        if not especialidad:
            messagebox.showwarning("Datos Faltantes", "Por favor, complete todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO medicos (usuario_id, especialidad) VALUES (%s, %s)"
                cursor.execute(query, (usuario_id, especialidad))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Médico añadido correctamente.")
                window.destroy()
                self.manage_medicos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo añadir el médico: {str(e)}")
                conn.close()

    def edit_medico(self, medico):
        edit_medico_window = tk.Toplevel(self.root)
        edit_medico_window.title("Editar Médico")

        tk.Label(edit_medico_window, text="Usuario").grid(row=0, column=0)
        usuario_var = tk.StringVar(edit_medico_window)
        
        # Obtener la lista de usuarios para seleccionar
        conn = connect_db()
        usuarios = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conn.close()
        
        usuario_options = [f"{usuario[0]} - {usuario[1]}" for usuario in usuarios]
        usuario_actual = f"{medico[1]} - {medico[2]}"
        # Buscar el usuario correspondiente
        selected_usuario = None
        for usuario in usuarios:
            if usuario[0] == medico[1]:
                selected_usuario = f"{usuario[0]} - {usuario[1]}"
                break
        if selected_usuario:
            usuario_var.set(selected_usuario)
        else:
            usuario_var.set(usuario_options[0])

        usuario_dropdown = tk.OptionMenu(edit_medico_window, usuario_var, *usuario_options)
        usuario_dropdown.grid(row=0, column=1)

        tk.Label(edit_medico_window, text="Especialidad").grid(row=1, column=0)
        especialidad_entry = tk.Entry(edit_medico_window)
        especialidad_entry.insert(0, medico[3])
        especialidad_entry.grid(row=1, column=1)

        tk.Button(edit_medico_window, text="Guardar Cambios", command=lambda: self.save_edited_medico(medico[0], usuario_var, especialidad_entry, edit_medico_window)).grid(row=2, columnspan=2)

    def save_edited_medico(self, medico_id, usuario_var, especialidad_entry, window):
        usuario_selected = usuario_var.get()
        usuario_id = int(usuario_selected.split(" - ")[0])
        especialidad = especialidad_entry.get().strip()

        if not especialidad:
            messagebox.showwarning("Datos Faltantes", "Por favor, complete todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE medicos SET usuario_id=%s, especialidad=%s WHERE id=%s"
                cursor.execute(query, (usuario_id, especialidad, medico_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Éxito", "Médico actualizado correctamente.")
                window.destroy()
                self.manage_medicos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el médico: {str(e)}")
                conn.close()

    def delete_medico(self, medico_id):
        confirm = messagebox.askyesno("Confirmación de Eliminación", "¿Está seguro de que desea eliminar este médico?")
        if confirm:
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM medicos WHERE id=%s", (medico_id,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
                    self.manage_medicos()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el médico: {str(e)}")
                    conn.close()


    def manage_patients(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Gestión de Pacientes", font=("Arial", 16)).pack(pady=10)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, nombre, fecha_nacimiento, genero, direccion, telefono FROM pacientes")
                pacientes = cursor.fetchall()

                for paciente in pacientes:
                    paciente_frame = tk.Frame(self.display_frame, borderwidth=1, relief=tk.SOLID)
                    paciente_frame.pack(fill=tk.X, padx=10, pady=5)

                    paciente_info = (
                        f"ID: {paciente[0]}, Nombre: {paciente[1]}, "
                        f"Fecha de Nacimiento: {paciente[2]}, Género: {paciente[3]}, "
                        f"Dirección: {paciente[4]}, Teléfono: {paciente[5]}"
                    )
                    tk.Label(paciente_frame, text=paciente_info, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                    tk.Button(paciente_frame, text="Editar", command=lambda p=paciente: self.edit_patient(p)).pack(side=tk.RIGHT, padx=5)
                    tk.Button(paciente_frame, text="Eliminar", command=lambda p=paciente: self.delete_patient(p[0])).pack(side=tk.RIGHT)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de pacientes: {str(e)}")
            finally:
                cursor.close()
                conn.close()

        tk.Button(self.display_frame, text="Añadir Paciente", command=self.add_patient).pack(pady=10)

    def add_patient(self):
        add_patient_window = tk.Toplevel(self.root)
        add_patient_window.title("Añadir Paciente")
        add_patient_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0),
            ("Fecha de Nacimiento (YYYY-MM-DD)", 1),
            ("Género", 2),
            ("Dirección", 3),
            ("Teléfono", 4)
        ]

        entries = {}
        for label_text, row in fields:
            tk.Label(add_patient_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Género":
                gender_var = tk.StringVar(add_patient_window)
                gender_var.set("Masculino")
                gender_dropdown = tk.OptionMenu(add_patient_window, gender_var, "Masculino", "Femenino", "Otro")
                gender_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["genero"] = gender_var
            else:
                entry = tk.Entry(add_patient_window)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.split(" ")[0].lower()
                entries[key] = entry

        tk.Button(
            add_patient_window,
            text="Guardar",
            command=lambda: self.save_patient(entries, add_patient_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_patient(self, entries, window):
        nombre = entries["nombre"].get().strip()
        fecha_nacimiento = entries["fecha"].get().strip()
        genero = entries["genero"].get()
        direccion = entries["dirección"].get().strip()
        telefono = entries["teléfono"].get().strip()

        if not all([nombre, fecha_nacimiento, genero, direccion, telefono]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO pacientes (nombre, fecha_nacimiento, genero, direccion, telefono)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, fecha_nacimiento, genero, direccion, telefono))
                conn.commit()
                messagebox.showinfo("Éxito", "Paciente añadido correctamente.")
                window.destroy()
                self.manage_patients()
            except psycopg2.IntegrityError:
                conn.rollback()
                messagebox.showerror("Error", "El teléfono ingresado ya está en uso.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo añadir el paciente: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def edit_patient(self, paciente):
        edit_patient_window = tk.Toplevel(self.root)
        edit_patient_window.title("Editar Paciente")
        edit_patient_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0, paciente[1]),
            ("Fecha de Nacimiento (YYYY-MM-DD)", 1, paciente[2]),
            ("Género", 2, paciente[3]),
            ("Dirección", 3, paciente[4]),
            ("Teléfono", 4, paciente[5])
        ]

        entries = {}
        for label_text, row, value in fields:
            tk.Label(edit_patient_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Género":
                gender_var = tk.StringVar(edit_patient_window)
                gender_var.set(value)
                gender_dropdown = tk.OptionMenu(edit_patient_window, gender_var, "Masculino", "Femenino", "Otro")
                gender_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["genero"] = gender_var
            else:
                entry = tk.Entry(edit_patient_window)
                entry.insert(0, value)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.split(" ")[0].lower()
                entries[key] = entry

        tk.Button(
            edit_patient_window,
            text="Guardar Cambios",
            command=lambda: self.save_edited_patient(paciente[0], entries, edit_patient_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_edited_patient(self, paciente_id, entries, window):
        nombre = entries["nombre"].get().strip()
        fecha_nacimiento = entries["fecha"].get().strip()
        genero = entries["genero"].get()
        direccion = entries["dirección"].get().strip()
        telefono = entries["teléfono"].get().strip()

        if not all([nombre, fecha_nacimiento, genero, direccion, telefono]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE pacientes
                    SET nombre=%s, fecha_nacimiento=%s, genero=%s, direccion=%s, telefono=%s
                    WHERE id=%s
                """
                cursor.execute(query, (nombre, fecha_nacimiento, genero, direccion, telefono, paciente_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
                window.destroy()
                self.manage_patients()
            except psycopg2.IntegrityError:
                conn.rollback()
                messagebox.showerror("Error", "El teléfono ingresado ya está en uso.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo actualizar el paciente: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def delete_patient(self, paciente_id):
        confirm = messagebox.askyesno("Confirmación de Eliminación", "¿Está seguro de que desea eliminar este paciente?")
        if confirm:
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM pacientes WHERE id=%s", (paciente_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
                    self.manage_patients()
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"No se pudo eliminar el paciente: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()


    def manage_signos(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Gestión de Signos", font=("Arial", 16)).pack(pady=10)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = """
                    SELECT signos.id, signos.nombre, signos.descripcion, enfermedades.nombre
                    FROM signos
                    JOIN enfermedades ON signos.enfermedad_id = enfermedades.id
                """
                cursor.execute(query)
                signos = cursor.fetchall()

                for signo in signos:
                    signo_frame = tk.Frame(self.display_frame, borderwidth=1, relief=tk.SOLID)
                    signo_frame.pack(fill=tk.X, padx=10, pady=5)

                    signo_info = (
                        f"ID: {signo[0]}, Nombre: {signo[1]}, "
                        f"Descripción: {signo[2]}, Enfermedad: {signo[3]}"
                    )
                    tk.Label(signo_frame, text=signo_info, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                    tk.Button(signo_frame, text="Editar", command=lambda s=signo: self.edit_signo(s)).pack(side=tk.RIGHT, padx=5)
                    tk.Button(signo_frame, text="Eliminar", command=lambda s=signo: self.delete_signo(s[0])).pack(side=tk.RIGHT)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de signos: {str(e)}")
            finally:
                cursor.close()
                conn.close()

        tk.Button(self.display_frame, text="Añadir Signo", command=self.add_signo).pack(pady=10)

    def add_signo(self):
        add_signo_window = tk.Toplevel(self.root)
        add_signo_window.title("Añadir Signo")
        add_signo_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0),
            ("Descripción", 1),
            ("Enfermedad", 2)
        ]

        entries = {}
        for label_text, row in fields:
            tk.Label(add_signo_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Enfermedad":
                enfermedad_var = tk.StringVar(add_signo_window)
                # Obtener la lista de enfermedades para seleccionar
                conn = connect_db()
                enfermedades = []
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nombre FROM enfermedades")
                    enfermedades = cursor.fetchall()
                    cursor.close()
                    conn.close()

                enfermedad_options = [f"{enf[0]} - {enf[1]}" for enf in enfermedades]
                if not enfermedad_options:
                    messagebox.showwarning("Sin Enfermedades", "No hay enfermedades disponibles. Por favor, añade una enfermedad primero.")
                    add_signo_window.destroy()
                    return

                enfermedad_var.set(enfermedad_options[0])
                enfermedad_dropdown = tk.OptionMenu(add_signo_window, enfermedad_var, *enfermedad_options)
                enfermedad_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["enfermedad_id"] = enfermedad_var
            elif label_text == "Descripción":
                descripcion_text = tk.Text(add_signo_window, width=40, height=5)
                descripcion_text.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["descripcion"] = descripcion_text
            else:
                entry = tk.Entry(add_signo_window)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.lower()
                entries[key] = entry

        tk.Button(
            add_signo_window,
            text="Guardar",
            command=lambda: self.save_signo(entries, add_signo_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_signo(self, entries, window):
        nombre = entries["nombre"].get().strip()
        descripcion = entries["descripcion"].get("1.0", tk.END).strip()
        enfermedad_selected = entries["enfermedad_id"].get()
        enfermedad_id = int(enfermedad_selected.split(" - ")[0])

        if not all([nombre, descripcion, enfermedad_id]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO signos (nombre, descripcion, enfermedad_id)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (nombre, descripcion, enfermedad_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Signo añadido correctamente.")
                window.destroy()
                self.manage_signos()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo añadir el signo: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def edit_signo(self, signo):
        edit_signo_window = tk.Toplevel(self.root)
        edit_signo_window.title("Editar Signo")
        edit_signo_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0, signo[1]),
            ("Descripción", 1, signo[2]),
            ("Enfermedad", 2, signo[3])
        ]

        entries = {}
        for label_text, row, value in fields:
            tk.Label(edit_signo_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Enfermedad":
                enfermedad_var = tk.StringVar(edit_signo_window)
                # Obtener la lista de enfermedades para seleccionar
                conn = connect_db()
                enfermedades = []
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nombre FROM enfermedades")
                    enfermedades = cursor.fetchall()
                    cursor.close()
                    conn.close()

                enfermedad_options = [f"{enf[0]} - {enf[1]}" for enf in enfermedades]
                if not enfermedad_options:
                    messagebox.showwarning("Sin Enfermedades", "No hay enfermedades disponibles. Por favor, añade una enfermedad primero.")
                    edit_signo_window.destroy()
                    return

                # Establecer la enfermedad actual como seleccionada
                selected_enfermedad = next((f"{enf[0]} - {enf[1]}" for enf in enfermedades if enf[1] == value), enfermedad_options[0])
                enfermedad_var.set(selected_enfermedad)
                enfermedad_dropdown = tk.OptionMenu(edit_signo_window, enfermedad_var, *enfermedad_options)
                enfermedad_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["enfermedad_id"] = enfermedad_var
            elif label_text == "Descripción":
                descripcion_text = tk.Text(edit_signo_window, width=40, height=5)
                descripcion_text.insert("1.0", value)
                descripcion_text.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["descripcion"] = descripcion_text
            else:
                entry = tk.Entry(edit_signo_window)
                entry.insert(0, value)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.lower()
                entries[key] = entry

        tk.Button(
            edit_signo_window,
            text="Guardar Cambios",
            command=lambda: self.save_edited_signo(signo[0], entries, edit_signo_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_edited_signo(self, signo_id, entries, window):
        nombre = entries["nombre"].get().strip()
        descripcion = entries["descripcion"].get("1.0", tk.END).strip()
        enfermedad_selected = entries["enfermedad_id"].get()
        enfermedad_id = int(enfermedad_selected.split(" - ")[0])

        if not all([nombre, descripcion, enfermedad_id]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE signos
                    SET nombre=%s, descripcion=%s, enfermedad_id=%s
                    WHERE id=%s
                """
                cursor.execute(query, (nombre, descripcion, enfermedad_id, signo_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Signo actualizado correctamente.")
                window.destroy()
                self.manage_signos()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo actualizar el signo: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def delete_signo(self, signo_id):
        confirm = messagebox.askyesno("Confirmación de Eliminación", "¿Está seguro de que desea eliminar este signo?")
        if confirm:
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM signos WHERE id=%s", (signo_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Signo eliminado correctamente.")
                    self.manage_signos()
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"No se pudo eliminar el signo: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()

    def manage_sintomas(self):
        self.clear_frame()
        tk.Label(self.display_frame, text="Gestión de Síntomas", font=("Arial", 16)).pack(pady=10)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = """
                    SELECT sintomas.id, sintomas.nombre, sintomas.descripcion, enfermedades.nombre
                    FROM sintomas
                    JOIN enfermedades ON sintomas.enfermedad_id = enfermedades.id
                """
                cursor.execute(query)
                sintomas = cursor.fetchall()

                for sintoma in sintomas:
                    sintoma_frame = tk.Frame(self.display_frame, borderwidth=1, relief=tk.SOLID)
                    sintoma_frame.pack(fill=tk.X, padx=10, pady=5)

                    sintoma_info = (
                        f"ID: {sintoma[0]}, Nombre: {sintoma[1]}, "
                        f"Descripción: {sintoma[2]}, Enfermedad: {sintoma[3]}"
                    )
                    tk.Label(sintoma_frame, text=sintoma_info, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                    tk.Button(sintoma_frame, text="Editar", command=lambda s=sintoma: self.edit_sintoma(s)).pack(side=tk.RIGHT, padx=5)
                    tk.Button(sintoma_frame, text="Eliminar", command=lambda s=sintoma: self.delete_sintoma(s[0])).pack(side=tk.RIGHT)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de síntomas: {str(e)}")
            finally:
                cursor.close()
                conn.close()

        tk.Button(self.display_frame, text="Añadir Síntoma", command=self.add_sintoma).pack(pady=10)

    def add_sintoma(self):
        add_sintoma_window = tk.Toplevel(self.root)
        add_sintoma_window.title("Añadir Síntoma")
        add_sintoma_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0),
            ("Descripción", 1),
            ("Enfermedad", 2)
        ]

        entries = {}
        for label_text, row in fields:
            tk.Label(add_sintoma_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Enfermedad":
                enfermedad_var = tk.StringVar(add_sintoma_window)
                # Obtener la lista de enfermedades para seleccionar
                conn = connect_db()
                enfermedades = []
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nombre FROM enfermedades")
                    enfermedades = cursor.fetchall()
                    cursor.close()
                    conn.close()

                enfermedad_options = [f"{enf[0]} - {enf[1]}" for enf in enfermedades]
                if not enfermedad_options:
                    messagebox.showwarning("Sin Enfermedades", "No hay enfermedades disponibles. Por favor, añade una enfermedad primero.")
                    add_sintoma_window.destroy()
                    return

                enfermedad_var.set(enfermedad_options[0])
                enfermedad_dropdown = tk.OptionMenu(add_sintoma_window, enfermedad_var, *enfermedad_options)
                enfermedad_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["enfermedad_id"] = enfermedad_var
            elif label_text == "Descripción":
                descripcion_text = tk.Text(add_sintoma_window, width=40, height=5)
                descripcion_text.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["descripcion"] = descripcion_text
            else:
                entry = tk.Entry(add_sintoma_window)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.lower()
                entries[key] = entry

        tk.Button(
            add_sintoma_window,
            text="Guardar",
            command=lambda: self.save_sintoma(entries, add_sintoma_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_sintoma(self, entries, window):
        nombre = entries["nombre"].get().strip()
        descripcion = entries["descripcion"].get("1.0", tk.END).strip()
        enfermedad_selected = entries["enfermedad_id"].get()
        enfermedad_id = int(enfermedad_selected.split(" - ")[0])

        if not all([nombre, descripcion, enfermedad_id]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO sintomas (nombre, descripcion, enfermedad_id)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (nombre, descripcion, enfermedad_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Síntoma añadido correctamente.")
                window.destroy()
                self.manage_sintomas()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo añadir el síntoma: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def edit_sintoma(self, sintoma):
        edit_sintoma_window = tk.Toplevel(self.root)
        edit_sintoma_window.title("Editar Síntoma")
        edit_sintoma_window.grab_set()  # Modal

        fields = [
            ("Nombre", 0, sintoma[1]),
            ("Descripción", 1, sintoma[2]),
            ("Enfermedad", 2, sintoma[3])
        ]

        entries = {}
        for label_text, row, value in fields:
            tk.Label(edit_sintoma_window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky=tk.E)
            if label_text == "Enfermedad":
                enfermedad_var = tk.StringVar(edit_sintoma_window)
                # Obtener la lista de enfermedades para seleccionar
                conn = connect_db()
                enfermedades = []
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nombre FROM enfermedades")
                    enfermedades = cursor.fetchall()
                    cursor.close()
                    conn.close()

                enfermedad_options = [f"{enf[0]} - {enf[1]}" for enf in enfermedades]
                if not enfermedad_options:
                    messagebox.showwarning("Sin Enfermedades", "No hay enfermedades disponibles. Por favor, añade una enfermedad primero.")
                    edit_sintoma_window.destroy()
                    return

                # Establecer la enfermedad actual como seleccionada
                selected_enfermedad = next((f"{enf[0]} - {enf[1]}" for enf in enfermedades if enf[1] == value), enfermedad_options[0])
                enfermedad_var.set(selected_enfermedad)
                enfermedad_dropdown = tk.OptionMenu(edit_sintoma_window, enfermedad_var, *enfermedad_options)
                enfermedad_dropdown.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["enfermedad_id"] = enfermedad_var
            elif label_text == "Descripción":
                descripcion_text = tk.Text(edit_sintoma_window, width=40, height=5)
                descripcion_text.insert("1.0", value)
                descripcion_text.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                entries["descripcion"] = descripcion_text
            else:
                entry = tk.Entry(edit_sintoma_window)
                entry.insert(0, value)
                entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
                key = label_text.lower()
                entries[key] = entry

        tk.Button(
            edit_sintoma_window,
            text="Guardar Cambios",
            command=lambda: self.save_edited_sintoma(sintoma[0], entries, edit_sintoma_window)
        ).grid(row=len(fields), columnspan=2, pady=10)

    def save_edited_sintoma(self, sintoma_id, entries, window):
        nombre = entries["nombre"].get().strip()
        descripcion = entries["descripcion"].get("1.0", tk.END).strip()
        enfermedad_selected = entries["enfermedad_id"].get()
        enfermedad_id = int(enfermedad_selected.split(" - ")[0])

        if not all([nombre, descripcion, enfermedad_id]):
            messagebox.showwarning("Datos Faltantes", "Por favor, completa todos los campos.")
            return

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE sintomas
                    SET nombre=%s, descripcion=%s, enfermedad_id=%s
                    WHERE id=%s
                """
                cursor.execute(query, (nombre, descripcion, enfermedad_id, sintoma_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Síntoma actualizado correctamente.")
                window.destroy()
                self.manage_sintomas()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo actualizar el síntoma: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def delete_sintoma(self, sintoma_id):
        confirm = messagebox.askyesno("Confirmación de Eliminación", "¿Está seguro de que desea eliminar este síntoma?")
        if confirm:
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM sintomas WHERE id=%s", (sintoma_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Síntoma eliminado correctamente.")
                    self.manage_sintomas()
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"No se pudo eliminar el síntoma: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()


    def clear_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
