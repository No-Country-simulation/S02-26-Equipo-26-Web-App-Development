CREATE DATABASE Medicae;
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE  
);


CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES roles(id),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR (20) UNIQUE NOT NULL, -- identificacion dada por el estado que valide que dicha persona es la que dice ser.
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    cbu_alias VARCHAR(50), -- deberiamos agregar el campo cbu_alias en "documentos" para que mas adelante se realice el pago en cuenta o que se quede en usuarios, es la duda preguntar en la proxima reunion
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo_documento VARCHAR(50), -- con este documento me nos referimos al la titulacion que habilita al colaborador que se dara de alta en este programa 
    -- disscleimer: en argentina le decimos documento al DNI no se si en otros paises se llamara de la misma forma
    url_archivo VARCHAR(255),
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);


CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    familiar_id INTEGER REFERENCES usuarios(id), -- Quien paga/supervisa, aqui surge la duda si el pago se realiza por mes lo liquida el admin o sera tipo "uber" y el pago sera luego de haber realizado el servicio 
    notas_medicas TEXT
);

CREATE TABLE guardias (
    id SERIAL PRIMARY KEY,
    cuidador_id INTEGER REFERENCES usuarios(id),
    paciente_id INTEGER REFERENCES pacientes(id),
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    informe_actividad TEXT,
    horas_totales NUMERIC(5,2), -- Este campo se calcula solo mediante el Trigger
    estado_pago VARCHAR(20) DEFAULT 'pendiente'  -- los 3 estados referentes al dinero serian 'pendiente', 'liquidado' y 'pagado'
);


