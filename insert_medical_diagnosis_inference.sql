-- Inserting 30 sample records

-- Insert Users (Administrators and Doctors)
INSERT INTO usuarios (nombre, correo, rol, contraseña) VALUES
('Administrador 1', 'admin1@hospital.com', 'administrador', 'admin123'),
('Administrador 2', 'admin2@hospital.com', 'administrador', 'admin123'),
('Dr. Juan Pérez', 'juan.perez@hospital.com', 'medico', 'medico123'),
('Dr. Ana Gómez', 'ana.gomez@hospital.com', 'medico', 'medico123');

-- Insert Doctors
INSERT INTO medicos (usuario_id, especialidad) VALUES
(3, 'Cardiología'),
(4, 'Neurología');

-- Insert Patients
INSERT INTO pacientes (nombre, fecha_nacimiento, genero, direccion, telefono) VALUES
('Pedro García', '1980-05-12', 'Masculino', 'Av. Siempre Viva 123', '555-1234'),
('María López', '1992-08-23', 'Femenino', 'Calle Falsa 456', '555-5678');

-- Insert Diseases
INSERT INTO enfermedades (nombre, descripcion) VALUES
('Diabetes', 'Enfermedad crónica que afecta la regulación de la glucosa.'),
('Hipertensión', 'Elevación persistente de la presión arterial.'),
('Migraña', 'Dolor de cabeza recurrente asociado a síntomas neurológicos.');

-- Insert Signs
INSERT INTO signos (nombre, descripcion, enfermedad_id) VALUES
('Hiperglucemia', 'Nivel elevado de glucosa en sangre.', 1),
('Presión arterial alta', 'Tensión elevada en arterias.', 2),
('Sensibilidad a la luz', 'Sensibilidad excesiva a la luz.', 3);

-- Insert Symptoms
INSERT INTO sintomas (nombre, descripcion, enfermedad_id) VALUES
('Sed excesiva', 'Sensación constante de sed.', 1),
('Dolor de cabeza', 'Cefalea intensa.', 3),
('Cansancio', 'Fatiga sin causa aparente.', 1);

-- Insert Diagnoses
INSERT INTO diagnosticos (paciente_id, medico_id, enfermedad_id, fecha_diagnostico, tratamiento) VALUES
(1, 1, 1, '2024-10-12', 'Insulina y control de dieta.'),
(2, 2, 3, '2024-10-13', 'Analgésicos y descanso.');

-- Insert Medical History
INSERT INTO historial_medico (paciente_id, diagnostico_id, fecha, observaciones) VALUES
(1, 1, '2024-10-12', 'Paciente estable con control de glucosa.'),
(2, 2, '2024-10-13', 'Paciente en observación por migraña.');
