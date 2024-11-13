-- Create table for Users
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    rol VARCHAR(50) CHECK (rol IN ('administrador', 'medico')),
    contraseña VARCHAR(100)
);

-- Create table for Doctors (specific role)
CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    especialidad VARCHAR(100)
);

-- Create table for Patients
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    fecha_nacimiento DATE,
    genero VARCHAR(10),
    direccion VARCHAR(150),
    telefono VARCHAR(20) UNIQUE
);

-- Create table for Diseases
CREATE TABLE enfermedades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

-- Create table for Signs
CREATE TABLE signos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    enfermedad_id INT REFERENCES enfermedades(id)
);

-- Create table for Symptoms
CREATE TABLE sintomas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    enfermedad_id INT REFERENCES enfermedades(id)
);

-- Create table for Diagnoses
CREATE TABLE diagnosticos (
    id SERIAL PRIMARY KEY,
    paciente_id INT REFERENCES pacientes(id),
    medico_id INT REFERENCES medicos(id),
    enfermedad_id INT REFERENCES enfermedades(id),
    fecha_diagnostico DATE,
    tratamiento TEXT
);

-- Create table for Medical History
CREATE TABLE historial_medico (
    id SERIAL PRIMARY KEY,
    paciente_id INT REFERENCES pacientes(id),
    diagnostico_id INT REFERENCES diagnosticos(id),
    fecha DATE,
    observaciones TEXT
);

-- Inserting 30 sample records

-- Insert Users (Administrators and Doctors)
INSERT INTO usuarios (nombre, correo, rol, contraseña) VALUES
('Administrador 1', 'admin1@hospital.com', 'administrador', 'admin123'),
('Administrador 2', 'admin2@hospital.com', 'administrador', 'admin123'),
('Administrador 3', 'test', 'administrador', 'test'),
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
