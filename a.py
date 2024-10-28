import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection
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
        role_var.set("administrador")  # Set default role
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
        tk.Label(self.display_frame, text="Disease Management").pack()

    def clear_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
