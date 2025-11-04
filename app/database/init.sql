-- =============================================
-- INIT.SQL - Base de datos de Oncología / FastAPI
-- =============================================

-- Reinicio de tablas (en orden seguro)
DROP TABLE IF EXISTS encuesta_sesion_json CASCADE;
DROP TABLE IF EXISTS encuesta_token CASCADE;
DROP TABLE IF EXISTS sesion CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS sillon CASCADE;
DROP TABLE IF EXISTS patologia CASCADE;

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
    id_sillon INT REFERENCES sillon(id_sillon) ON DELETE SET NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME,
    tiempo_aseo_min INT CHECK (tiempo_aseo_min >= 0),
    materiales_usados TEXT,
    estado TEXT CHECK (estado IN ('pendiente', 'confirmado', 'cancelado')) DEFAULT 'pendiente',
    CONSTRAINT sesion_unique_paciente_fecha_sillon UNIQUE (id_paciente, fecha, id_sillon)
);

-- =============================================
-- TABLA: ENCUESTA_Sesion_JSON
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
