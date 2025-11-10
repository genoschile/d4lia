-- =============================================
-- INIT.SQL - Base de datos de Oncología / FastAPI
-- Versión ampliada con encargados, tratamientos y encuestas de paciente
-- =============================================
-- Reinicio de tablas (en orden seguro)
-- 🔹 tablas de exámenes
DROP TABLE IF EXISTS examen CASCADE;
DROP TABLE IF EXISTS orden_examen CASCADE;
DROP TABLE IF EXISTS instalacion CASCADE;
DROP TABLE IF EXISTS tipo_examen CASCADE;

-- 🔹 Tablas de recetas y medicamentos
DROP TABLE IF EXISTS receta_medicamento CASCADE;
DROP TABLE IF EXISTS receta CASCADE;
DROP TABLE IF EXISTS medicamento CASCADE;

-- 🔹 Tablas de condiciones personales
DROP TABLE IF EXISTS paciente_condicion CASCADE;
DROP TABLE IF EXISTS condicion_personal CASCADE;

-- 🔹 Consultas médicas y profesionales
DROP TABLE IF EXISTS consulta_medica CASCADE;
DROP TABLE IF EXISTS consulta_profesional CASCADE;
DROP TABLE IF EXISTS medico CASCADE;
DROP TABLE IF EXISTS especializacion CASCADE;

-- 🔹 Encuestas, sesiones, y estructura base
DROP TABLE IF EXISTS encuesta_paciente_json CASCADE;
DROP TABLE IF EXISTS encuesta_sesion_json CASCADE;
DROP TABLE IF EXISTS encuesta_token CASCADE;
DROP TABLE IF EXISTS sesion CASCADE;

-- 🔹 Entidades principales
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


-- ============================================
-- Parte new

-- =============================================
-- TABLA: CONDICION_PERSONAL (preexistencias, alergias, etc.)
-- =============================================
CREATE TABLE condicion_personal (
    id_condicion SERIAL PRIMARY KEY,
    codigo VARCHAR(20), -- opcional: CIE-10, SNOMED, o interno
    nombre_condicion TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('preexistencia', 'alergia', 'otro')) DEFAULT 'preexistencia',
    severidad TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA: PACIENTE_CONDICION (relación paciente <-> condicion_personal)
-- =============================================
CREATE TABLE paciente_condicion (
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_condicion INT REFERENCES condicion_personal(id_condicion) ON DELETE CASCADE,
    fecha_inicio DATE,
    fecha_resolucion DATE,
    validada_medico BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    PRIMARY KEY (id_paciente, id_condicion)
);


-- =============================================
-- TABLA: ESPECIALIZACION
-- =============================================
CREATE TABLE especializacion (
    id_especializacion SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    codigo_fonasa TEXT UNIQUE,
    nivel TEXT CHECK (nivel IN ('general', 'especialista', 'subespecialista')) DEFAULT 'general'
);

-- =============================================
-- TABLA: MEDICO
-- =============================================
CREATE TABLE medico (
    id_medico SERIAL PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    sexo TEXT CHECK (sexo IN ('masculino', 'femenino', 'otro')) DEFAULT 'otro',
    correo TEXT,
    telefono TEXT,
    codigo_fonasa TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- =============================================
-- TABLA: CONSULTA_PROFESIONAL (relación médico ↔ especialización)
-- =============================================
CREATE TABLE consulta_profesional (
    id_profesional SERIAL PRIMARY KEY,
    id_medico INT REFERENCES medico(id_medico) ON DELETE CASCADE,
    id_especializacion INT REFERENCES especializacion(id_especializacion) ON DELETE SET NULL,
    fecha_registro TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- TABLA: CONSULTA_MEDICA (relación paciente ↔ profesional)
-- =============================================
CREATE TABLE consulta_medica (
    id_consulta SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    especialidad TEXT, -- redundante, pero útil para historial textual
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    motivo TEXT,
    tratamiento TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA: MEDICAMENTO
-- =============================================
CREATE TABLE medicamento (
    id_medicamento SERIAL PRIMARY KEY,
    nombre_comercial TEXT NOT NULL,
    nombre_generico TEXT,
    concentracion TEXT,
    forma_farmaceutica TEXT,
    via_administracion TEXT,
    laboratorio TEXT,
    requiere_receta BOOLEAN DEFAULT TRUE,
    stock_disponible INT DEFAULT 0,
    observaciones TEXT
);

-- =============================================
-- TABLA: RECETA
-- =============================================
CREATE TABLE receta (
    id_receta SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_medico INT REFERENCES medico(id_medico) ON DELETE SET NULL,
    id_consulta INT REFERENCES consulta_medica(id_consulta) ON DELETE CASCADE,
    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin DATE,
    observaciones TEXT
);

-- =============================================
-- TABLA INTERMEDIA: RECETA <-> MEDICAMENTO
-- =============================================
CREATE TABLE receta_medicamento (
    id_receta INT REFERENCES receta(id_receta) ON DELETE CASCADE,
    id_medicamento INT REFERENCES medicamento(id_medicamento) ON DELETE CASCADE,
    dosis TEXT,
    frecuencia TEXT,
    duracion TEXT,
    instrucciones TEXT,
    PRIMARY KEY (id_receta, id_medicamento)
);

-- =============================================
-- TABLA: TIPO_EXAMEN
-- =============================================
CREATE TABLE tipo_examen (
    id_tipo_examen SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    codigo_interno TEXT UNIQUE,
    requiere_ayuno BOOLEAN DEFAULT FALSE,
    tiempo_estimado TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA: INSTALACION (laboratorio, clínica, sala, etc.)
-- =============================================
CREATE TABLE instalacion (
    id_instalacion SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('laboratorio', 'imagenologia', 'clinica', 'externo')) DEFAULT 'laboratorio',
    ubicacion TEXT,
    contacto TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA: ORDEN_EXAMEN (emitida desde una consulta médica)
-- =============================================
CREATE TABLE orden_examen (
    id_orden_examen SERIAL PRIMARY KEY,
    id_consulta INT REFERENCES consulta_medica(id_consulta) ON DELETE CASCADE,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_tipo_examen INT REFERENCES tipo_examen(id_tipo_examen) ON DELETE SET NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    motivo TEXT,
    documento TEXT, -- puede guardar ruta o referencia del documento adjunto
    estado TEXT CHECK (estado IN ('pendiente', 'en_proceso', 'finalizado', 'cancelado')) DEFAULT 'pendiente'
);

-- =============================================
-- TABLA: EXAMEN (resultado concreto de una orden)
-- =============================================
CREATE TABLE examen (
    id_examen SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_tipo_examen INT REFERENCES tipo_examen(id_tipo_examen) ON DELETE SET NULL,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    id_orden_examen INT REFERENCES orden_examen(id_orden_examen) ON DELETE CASCADE,
    id_instalacion INT REFERENCES instalacion(id_instalacion) ON DELETE SET NULL,
    documento TEXT, -- informe PDF o imagen escaneada
    fecha DATE DEFAULT CURRENT_DATE,
    resultados TEXT,
    observaciones TEXT
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

-- =============================================
-- Parte new 
-- =============================================

CREATE INDEX idx_paciente_condicion_paciente ON paciente_condicion (id_paciente);
CREATE INDEX idx_paciente_condicion_condicion ON paciente_condicion (id_condicion);
CREATE INDEX idx_consulta_medica_paciente ON consulta_medica (id_paciente);
CREATE INDEX idx_consulta_medica_profesional ON consulta_medica (id_profesional);
CREATE INDEX idx_consulta_profesional_medico ON consulta_profesional (id_medico);
CREATE INDEX idx_consulta_profesional_especializacion ON consulta_profesional (id_especializacion);

-- 🔹 Condiciones personales
CREATE INDEX idx_condicion_personal_codigo ON condicion_personal (codigo);

-- 🔹 Consultas médicas
CREATE INDEX idx_consulta_medica_fecha ON consulta_medica (fecha);

-- 🔹 Recetas
CREATE INDEX idx_receta_paciente ON receta (id_paciente);
CREATE INDEX idx_receta_consulta ON receta (id_consulta);
CREATE INDEX idx_orden_examen_paciente ON orden_examen (id_paciente);
CREATE INDEX idx_orden_examen_profesional ON orden_examen (id_profesional);
CREATE INDEX idx_orden_examen_tipo ON orden_examen (id_tipo_examen);

CREATE INDEX idx_examen_paciente ON examen (id_paciente);
CREATE INDEX idx_examen_orden ON examen (id_orden_examen);
CREATE INDEX idx_examen_instalacion ON examen (id_instalacion);
CREATE INDEX idx_examen_tipo ON examen (id_tipo_examen);