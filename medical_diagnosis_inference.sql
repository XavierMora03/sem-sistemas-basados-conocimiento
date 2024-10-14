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
    telefono VARCHAR(20)
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

