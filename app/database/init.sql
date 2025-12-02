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

-- 🔹 Tablas de hospitalización (nuevas)
DROP TABLE IF EXISTS medicamento_hospitalizacion CASCADE;
DROP TABLE IF EXISTS tratamiento_hospitalizacion CASCADE;
DROP TABLE IF EXISTS hospitalizacion CASCADE;
DROP TABLE IF EXISTS orden_hospitalizacion CASCADE;

-- 🔹 Tablas de condiciones personales
DROP TABLE IF EXISTS paciente_condicion CASCADE;
DROP TABLE IF EXISTS condicion_personal CASCADE;

-- 🔹 Consultas médicas y profesionales
DROP TABLE IF EXISTS diagnostico CASCADE;
DROP TABLE IF EXISTS cie10_ges CASCADE; 
DROP TABLE IF EXISTS cie10 CASCADE;
DROP TABLE IF EXISTS ges CASCADE;


DROP TABLE IF EXISTS consulta_medica CASCADE;
DROP TABLE IF EXISTS consulta_profesional CASCADE;
DROP TABLE IF EXISTS medico CASCADE;
DROP TABLE IF EXISTS especializacion CASCADE;
DROP TABLE IF EXISTS estado CASCADE;

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
-- TABLA: ESTADO (Tabla de estados generales)
-- =============================================
CREATE TABLE estado (
    id_estado SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);

INSERT INTO estado (nombre, descripcion) VALUES
('PENDIENTE', 'Pendiente de realización o atención'),
('PROGRAMADO', 'Programado para una fecha futura'),
('RESULTADO', 'Resultados disponibles'),
('CRITICO', 'Estado crítico o urgente'),
('CANCELADO', 'Cancelado por el usuario o sistema');

-- =============================================
-- TABLA: CONSULTA_MEDICA (relación paciente ↔ profesional)
-- =============================================
CREATE TABLE consulta_medica (
    id_consulta SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    id_estado INT REFERENCES estado(id_estado) ON DELETE SET NULL,
    especialidad TEXT, -- redundante, pero útil para historial textual
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_programada TIMESTAMP,
    fecha_atencion TIMESTAMP,
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
    id_estado INT REFERENCES estado(id_estado) ON DELETE SET NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    fecha_programada TIMESTAMP,
    fecha_solicitada TIMESTAMP,
    motivo TEXT,
    documento TEXT -- puede guardar ruta o referencia del documento adjunto
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
    id_estado INT REFERENCES estado(id_estado) ON DELETE SET NULL,
    documento TEXT, -- informe PDF o imagen escaneada
    fecha DATE DEFAULT CURRENT_DATE,
    resultados TEXT,
    resumen_resultado TEXT,
    observaciones TEXT
);

-- =============================================
-- TABLA: ORDEN_DE_HOSPITALIZACION
-- =============================================
CREATE TABLE orden_hospitalizacion (
    id_orden_hospitalizacion SERIAL PRIMARY KEY,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    motivo TEXT,
    documento TEXT, -- puede ser ruta o referencia al archivo adjunto
    estado TEXT CHECK (estado IN ('pendiente', 'en_proceso', 'completada', 'cancelada')) DEFAULT 'pendiente'
);

-- =============================================
-- TABLA: HOSPITALIZACION
-- =============================================
CREATE TABLE hospitalizacion (
    id_hospitalizacion SERIAL PRIMARY KEY,
    id_orden_hospitalizacion INT REFERENCES orden_hospitalizacion(id_orden_hospitalizacion) ON DELETE CASCADE,
    id_paciente INT REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    fecha_ingreso DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_alta DATE,
    habitacion TEXT,
    observacion TEXT,
    estado TEXT CHECK (estado IN ('activa', 'alta', 'cancelada')) DEFAULT 'activa'
);

-- =============================================
-- TABLA: TRATAMIENTO_HOSPITALIZACION
-- =============================================
CREATE TABLE tratamiento_hospitalizacion (
    id_hospitalizacion INT REFERENCES hospitalizacion(id_hospitalizacion) ON DELETE CASCADE,
    id_tratamiento INT REFERENCES tratamiento(id_tratamiento) ON DELETE SET NULL,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    fecha_aplicacion DATE DEFAULT CURRENT_DATE,
    dosis TEXT,
    duracion TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_hospitalizacion, id_tratamiento)
);

-- =============================================
-- TABLA: MEDICAMENTO_HOSPITALIZACION
-- (uso de medicamentos durante la hospitalización)
-- =============================================
CREATE TABLE medicamento_hospitalizacion (
    id_hospitalizacion INT REFERENCES hospitalizacion(id_hospitalizacion) ON DELETE CASCADE,
    id_medicamento INT REFERENCES medicamento(id_medicamento) ON DELETE SET NULL,
    id_profesional INT REFERENCES consulta_profesional(id_profesional) ON DELETE SET NULL,
    dosis TEXT,
    frecuencia TEXT,
    via_administracion TEXT,
    duracion TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_hospitalizacion, id_medicamento)
);

-- =============================================
-- TABLA: CIE10 (catálogo internacional de enfermedades)
-- =============================================
CREATE TABLE cie10 (
    id_cie10 SERIAL PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,   -- Ejemplo: "C50.1"
    nombre TEXT NOT NULL,                 -- Ejemplo: "Carcinoma de mama"
    categoria TEXT,                       -- Ejemplo: "Neoplasias malignas"
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- =============================================
-- TABLA: GES (programas de Garantías Explícitas en Salud - Chile)
-- =============================================
CREATE TABLE ges (
    id_ges SERIAL PRIMARY KEY,
    codigo_ges VARCHAR(10) UNIQUE,        -- Ejemplo: "GES 18"
    nombre TEXT NOT NULL,                 -- Ejemplo: "Cáncer de mama"
    descripcion TEXT,
    cobertura TEXT,                       -- Cobertura o etapa de atención cubierta
    dias_limite_diagnostico INT,          -- Días máximos para confirmar diagnóstico
    dias_limite_tratamiento INT,          -- Días máximos para iniciar tratamiento
    requiere_fonasa BOOLEAN DEFAULT TRUE, -- Si requiere cobertura FONASA
    vigente BOOLEAN DEFAULT TRUE
);

-- =============================================
-- TABLA INTERMEDIA: GES ↔ CIE10
-- (Un diagnóstico CIE10 puede estar cubierto por varios GES)
-- =============================================
CREATE TABLE cie10_ges (
    id_cie10 INT REFERENCES cie10(id_cie10) ON DELETE CASCADE,
    id_ges INT REFERENCES ges(id_ges) ON DELETE CASCADE,
    PRIMARY KEY (id_cie10, id_ges)
);

-- =============================================
-- TABLA: DIAGNOSTICO
-- (asociado a una consulta médica, con referencia a CIE10 y opcionalmente GES)
-- =============================================
CREATE TABLE diagnostico (
    id_diagnostico SERIAL PRIMARY KEY,
    id_consulta_medica INT REFERENCES consulta_medica(id_consulta) ON DELETE CASCADE,
    id_cie10 INT REFERENCES cie10(id_cie10) ON DELETE SET NULL,
    id_ges INT REFERENCES ges(id_ges) ON DELETE SET NULL,
    descripcion TEXT NOT NULL,               -- texto clínico del diagnóstico
    tipo TEXT CHECK (tipo IN ('presuntivo', 'confirmado', 'seguimiento')) DEFAULT 'presuntivo',
    fecha_registro DATE DEFAULT CURRENT_DATE,
    observaciones TEXT
);

-- =============================================
-- TABLA: PACIENTE_GES (tracking de GES por paciente con cuenta regresiva)
-- =============================================
CREATE TABLE paciente_ges (
    id_paciente_ges SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_ges INT NOT NULL REFERENCES ges(id_ges) ON DELETE CASCADE,
    id_diagnostico INT REFERENCES diagnostico(id_diagnostico) ON DELETE SET NULL,
    
    -- Tracking temporal
    fecha_activacion DATE NOT NULL DEFAULT CURRENT_DATE,
    dias_limite INT NOT NULL,  -- copiado de ges, pero puede ser ajustado manualmente
    fecha_vencimiento DATE,    -- calculado: fecha_activacion + dias_limite
    
    -- Estado y cobertura
    estado TEXT CHECK (estado IN ('activo', 'en_proceso', 'completado', 'vencido', 'cancelado')) DEFAULT 'activo',
    tipo_cobertura TEXT CHECK (tipo_cobertura IN ('fonasa', 'isapre', 'particular')) DEFAULT 'fonasa',
    
    -- Metadata
    activado_por INT REFERENCES medico(id_medico) ON DELETE SET NULL,
    fecha_completado DATE,
    observaciones TEXT,
    
    -- Constraint para evitar duplicados (mismo paciente, mismo ges, misma fecha)
    CONSTRAINT unique_paciente_ges_activacion UNIQUE(id_paciente, id_ges, fecha_activacion)
);

-- =============================================
-- VISTA: PACIENTE_GES_COUNTDOWN (cuenta regresiva automática)
-- =============================================
CREATE VIEW paciente_ges_countdown AS
SELECT 
    pg.id_paciente_ges,
    pg.id_paciente,
    p.nombre_completo,
    p.rut,
    pg.id_ges,
    g.nombre AS ges_nombre,
    g.codigo_ges,
    pg.fecha_activacion,
    pg.dias_limite,
    pg.fecha_vencimiento,
    pg.estado,
    pg.tipo_cobertura,
    pg.activado_por,
    pg.fecha_completado,
    pg.observaciones,
    -- Cuenta regresiva
    (pg.fecha_vencimiento - CURRENT_DATE) AS dias_restantes,
    CASE 
        WHEN pg.estado = 'completado' THEN 'Completado'
        WHEN pg.estado = 'cancelado' THEN 'Cancelado'
        WHEN CURRENT_DATE > pg.fecha_vencimiento THEN 'Vencido'
        WHEN (pg.fecha_vencimiento - CURRENT_DATE) <= 7 THEN 'Crítico'
        WHEN (pg.fecha_vencimiento - CURRENT_DATE) <= 30 THEN 'Urgente'
        ELSE 'Normal'
    END AS prioridad,
    -- Porcentaje de tiempo transcurrido
    ROUND(
        ((CURRENT_DATE - pg.fecha_activacion)::numeric / NULLIF(pg.dias_limite, 0)) * 100, 
        2
    ) AS porcentaje_transcurrido
FROM paciente_ges pg
JOIN paciente p ON pg.id_paciente = p.id_paciente
JOIN ges g ON pg.id_ges = g.id_ges
WHERE pg.estado IN ('activo', 'en_proceso');

-- =============================================
-- TRIGGER: Calcular fecha_vencimiento automáticamente
-- =============================================
CREATE OR REPLACE FUNCTION calcular_fecha_vencimiento()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_vencimiento = NEW.fecha_activacion + (NEW.dias_limite || ' days')::INTERVAL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calcular_vencimiento
BEFORE INSERT OR UPDATE OF fecha_activacion, dias_limite ON paciente_ges
FOR EACH ROW
EXECUTE FUNCTION calcular_fecha_vencimiento();

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

CREATE INDEX idx_orden_hosp_paciente ON orden_hospitalizacion (id_paciente);
CREATE INDEX idx_orden_hosp_profesional ON orden_hospitalizacion (id_profesional);
CREATE INDEX idx_hosp_paciente ON hospitalizacion (id_paciente);
CREATE INDEX idx_hosp_profesional ON hospitalizacion (id_profesional);
CREATE INDEX idx_hosp_orden ON hospitalizacion (id_orden_hospitalizacion);

-- =============================================
-- ÍNDICES: TRATAMIENTO_HOSPITALIZACION & MEDICAMENTO_HOSPITALIZACION
-- =============================================
CREATE INDEX idx_trat_hosp_hospitalizacion ON tratamiento_hospitalizacion (id_hospitalizacion);
CREATE INDEX idx_trat_hosp_tratamiento ON tratamiento_hospitalizacion (id_tratamiento);
CREATE INDEX idx_trat_hosp_profesional ON tratamiento_hospitalizacion (id_profesional);

CREATE INDEX idx_med_hosp_hospitalizacion ON medicamento_hospitalizacion (id_hospitalizacion);
CREATE INDEX idx_med_hosp_medicamento ON medicamento_hospitalizacion (id_medicamento);
CREATE INDEX idx_med_hosp_profesional ON medicamento_hospitalizacion (id_profesional);


CREATE INDEX idx_diagnostico_consulta ON diagnostico (id_consulta_medica);
CREATE INDEX idx_diagnostico_cie10 ON diagnostico (id_cie10);
CREATE INDEX idx_diagnostico_ges ON diagnostico (id_ges);
CREATE INDEX idx_cie10_codigo ON cie10 (codigo);
CREATE INDEX idx_ges_codigo ON ges (codigo_ges);

-- =============================================
-- ÍNDICES: PACIENTE_GES
-- =============================================
CREATE INDEX idx_paciente_ges_paciente ON paciente_ges(id_paciente);
CREATE INDEX idx_paciente_ges_ges ON paciente_ges(id_ges);
CREATE INDEX idx_paciente_ges_estado ON paciente_ges(estado);
CREATE INDEX idx_paciente_ges_vencimiento ON paciente_ges(fecha_vencimiento);
CREATE INDEX idx_paciente_ges_diagnostico ON paciente_ges(id_diagnostico);
CREATE INDEX idx_paciente_ges_prioridad ON paciente_ges(estado, fecha_vencimiento) WHERE estado IN ('activo', 'en_proceso');

