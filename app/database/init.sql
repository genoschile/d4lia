-- =============================================
-- INIT.SQL - Base de datos de Oncología / FastAPI
-- Versión ampliada con encargados, tratamientos y encuestas de paciente
-- =============================================

-- Reinicio de tablas (en orden seguro)
DROP TABLE IF EXISTS encuesta_paciente_json CASCADE;
DROP TABLE IF EXISTS encuesta_sesion_json CASCADE;
DROP TABLE IF EXISTS encuesta_token CASCADE;
DROP TABLE IF EXISTS sesion CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS encargado CASCADE;
DROP TABLE IF EXISTS sillon CASCADE;
DROP TABLE IF EXISTS patologia_tratamiento CASCADE;
DROP TABLE IF EXISTS tratamiento CASCADE;
DROP TABLE IF EXISTS patologia CASCADE;

-- =============================================
-- TABLA: ENCARGADO
-- =============================================
CREATE TABLE encargado (
    id_encargado SERIAL PRIMARY KEY,
    nombre_completo TEXT NOT NULL,
    rut VARCHAR(12) UNIQUE,
    correo TEXT,
    telefono TEXT,
    cargo TEXT CHECK (cargo IN (
        'enfermero', 'doctor', 'técnico', 'administrativo', 'otro'
    )) DEFAULT 'otro',
    especialidad TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- =============================================
-- TABLA: PATOLOGIA
-- =============================================
CREATE TABLE patologia (
    id_patologia SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    nombre_patologia TEXT NOT NULL,
    especialidad TEXT,
    tiempo_estimado TEXT,
    explicacion TEXT,
    tratamientos_principales TEXT,
    farmacos TEXT,
    efectos_adversos TEXT,
    gravedad TEXT,
    costo_aprox TEXT,
    evidencia TEXT,
    exito_porcentaje TEXT,
    edad_promedio TEXT,
    notas TEXT
);

-- =============================================
-- TABLA: TRATAMIENTO
-- =============================================
CREATE TABLE tratamiento (
    id_tratamiento SERIAL PRIMARY KEY,
    nombre_tratamiento TEXT NOT NULL,
    descripcion TEXT,
    duracion_estimada TEXT,
    costo_aprox TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA INTERMEDIA: PATOLOGIA <-> TRATAMIENTO
-- =============================================
CREATE TABLE patologia_tratamiento (
    id_patologia INT REFERENCES patologia(id_patologia) ON DELETE CASCADE,
    id_tratamiento INT REFERENCES tratamiento(id_tratamiento) ON DELETE CASCADE,
    PRIMARY KEY (id_patologia, id_tratamiento)
);

-- =============================================
-- TABLA: PACIENTE
-- =============================================
CREATE TABLE paciente (
    id_paciente SERIAL PRIMARY KEY, 
    rut VARCHAR(12) UNIQUE NOT NULL, 
    nombre_completo TEXT NOT NULL,
    correo TEXT,
    telefono TEXT,
    edad INT CHECK (edad > 0),
    direccion TEXT,
    antecedentes_medicos TEXT,
    id_patologia INT REFERENCES patologia(id_patologia) ON DELETE SET NULL,
    id_encargado_registro INT REFERENCES encargado(id_encargado) ON DELETE SET NULL, -- quien registró
    fecha_inicio_tratamiento DATE,
    observaciones TEXT
);

-- =============================================
-- TABLA: SILLON
-- =============================================
CREATE TABLE sillon (
    id_sillon SERIAL PRIMARY KEY,
    ubicacion_sala TEXT CHECK (ubicacion_sala IN (
        'sala_espera', 'consultorio_1', 'consultorio_2', 'consultorio_3', 'DESCONOCIDO'
    )) NOT NULL DEFAULT 'DESCONOCIDO',
    estado TEXT CHECK (estado IN (
        'disponible', 'ocupado', 'mantenimiento', 'fuera_servicio'
    )) NOT NULL,
    observaciones TEXT
);

-- =============================================
-- TABLA: SESION
-- =============================================
CREATE TABLE sesion (
    id_sesion SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_patologia INT REFERENCES patologia(id_patologia) ON DELETE SET NULL,
    id_tratamiento INT REFERENCES tratamiento(id_tratamiento) ON DELETE SET NULL,
    id_sillon INT REFERENCES sillon(id_sillon) ON DELETE SET NULL,
    id_encargado INT REFERENCES encargado(id_encargado) ON DELETE SET NULL, -- quien atendió
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME,
    tiempo_aseo_min INT CHECK (tiempo_aseo_min >= 0),
    materiales_usados TEXT,
    estado TEXT CHECK (estado IN ('pendiente', 'confirmado', 'cancelado')) DEFAULT 'pendiente',
    CONSTRAINT sesion_unique_paciente_fecha_sillon UNIQUE (id_paciente, fecha, id_sillon)
);

-- =============================================
-- TABLA: ENCUESTA_PACIENTE_JSON (antecedentes, hábitos, etc.)
-- =============================================
CREATE TABLE encuesta_paciente_json (
    id_encuesta SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    tipo_encuesta TEXT CHECK (tipo_encuesta IN (
        'antecedentes_medicos', 'habitos', 'evaluacion_inicial'
    )) NOT NULL DEFAULT 'antecedentes_medicos',
    fecha_encuesta DATE DEFAULT CURRENT_DATE,
    datos JSONB,
    completada BOOLEAN DEFAULT TRUE,
    CONSTRAINT unique_encuesta_paciente_tipo UNIQUE (id_paciente, tipo_encuesta)
);

-- =============================================
-- TABLA: ENCUESTA_SESION_JSON
-- =============================================
CREATE TABLE encuesta_sesion_json (
    id_encuesta SERIAL PRIMARY KEY,
    id_sesion INT REFERENCES sesion(id_sesion) ON DELETE CASCADE,
    tipo_encuesta TEXT CHECK (tipo_encuesta IN (
        'pre_sesion', 
        'satisfaccion', 
        'seguimiento', 
        'confirmacion', 
        'evaluacion_medica'
    )) NOT NULL DEFAULT 'satisfaccion',
    fecha_encuesta DATE DEFAULT CURRENT_DATE,
    datos JSONB, 
    completada BOOLEAN DEFAULT TRUE,
    CONSTRAINT unique_encuesta_por_sesion_tipo UNIQUE (id_sesion, tipo_encuesta)
);

-- =============================================
-- TABLA: ENCUESTA_TOKEN
-- =============================================
CREATE TABLE encuesta_token (
    id_token SERIAL PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    id_sesion INT REFERENCES sesion(id_sesion) ON DELETE CASCADE,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_uso TIMESTAMP,
    usado BOOLEAN DEFAULT FALSE,
    expiracion TIMESTAMP NOT NULL
);

-- =============================================
-- ÍNDICES
-- =============================================
CREATE INDEX idx_paciente_rut ON paciente (rut);
CREATE INDEX idx_sesion_fecha ON sesion (fecha);
CREATE INDEX idx_sesion_estado ON sesion (estado);
CREATE INDEX idx_encuesta_sesion_json ON encuesta_sesion_json (id_sesion);
CREATE INDEX idx_encuesta_token_token ON encuesta_token (token);
CREATE INDEX idx_encuesta_token_usado ON encuesta_token (usado);
CREATE INDEX idx_paciente_encargado ON paciente (id_encargado_registro);
CREATE INDEX idx_sesion_encargado ON sesion (id_encargado);