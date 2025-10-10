-- =============================================
-- INIT.SQL - Base de datos de Oncología / FastAPI
-- =============================================

-- Borrar tablas si existen (para reinicializar)
DROP TABLE IF EXISTS sesion CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS sillon CASCADE;
DROP TABLE IF EXISTS patologia CASCADE;

-- =============================================
-- TABLA: PATOLOGIA
-- =============================================
CREATE TABLE patologia (
    id_patologia VARCHAR(10) PRIMARY KEY,
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
    id_paciente VARCHAR(10) PRIMARY KEY,
    nombre_completo TEXT NOT NULL,
    telefono TEXT,
    edad INT,
    direccion TEXT,
    antecedentes_medicos TEXT,
    id_patologia VARCHAR(10) REFERENCES patologia(id_patologia) ON DELETE SET NULL,
    fecha_inicio_tratamiento DATE,
    observaciones TEXT
);

-- =============================================
-- TABLA: SILLON
-- =============================================
CREATE TABLE sillon (
    id_sillon VARCHAR(10) PRIMARY KEY,
    ubicacion_sala TEXT,
    estado TEXT CHECK (estado IN ('Disponible', 'Invalido', 'Mantención')),
    observaciones TEXT
);

-- =============================================
-- TABLA: SESION
-- =============================================
CREATE TABLE sesion (
    id_sesion VARCHAR(10) PRIMARY KEY,
    id_paciente VARCHAR(10) REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_patologia VARCHAR(10) REFERENCES patologia(id_patologia) ON DELETE SET NULL,
    id_sillon VARCHAR(10) REFERENCES sillon(id_sillon) ON DELETE SET NULL,
    fecha DATE,
    hora_inicio TIME,
    hora_fin TIME,
    tiempo_aseo_min INT,
    materiales_usados TEXT,
    estado TEXT
);

-- =============================================
-- DATOS INICIALES
-- =============================================

-- 🔹 Patologías
INSERT INTO patologia (
    id_patologia, nombre_patologia, especialidad, tiempo_estimado, explicacion,
    tratamientos_principales, farmacos, efectos_adversos, gravedad,
    costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas
)
VALUES
('O001',
 E'Cáncer de próstata (local/alto riesgo)',
 E'Oncología',
 E'1 hr/sesión - total 6 meses',
 E'Tumor prostático tratado con RT y QT/hormonoterapia según riesgo',
 E'Radioterapia, Quimioterapia, Hormonoterapia',
 E'Docetaxel, Bicalutamida (± Goserelina/Leuprorelina)',
 E'Fatiga, náuseas, neutropenia, sofocos',
 E'Severa',
 E'US$2.000–5.000/sesión',
 E'Alta',
 E'70–80% control',
 E'65+',
 E'Puede requerir deprivación androgénica prolongada'
);

-- 🔹 Pacientes
INSERT INTO paciente (
    id_paciente, nombre_completo, telefono, edad, direccion, antecedentes_medicos,
    id_patologia, fecha_inicio_tratamiento, observaciones
)
VALUES
('P001',
 E'Juan Pérez Soto',
 NULL,
 62,
 E'Avenida 2 Sur 1456, Talca, Región del Maule',
 E'Hipertensión, Diabetes',
 'O001',
 TO_DATE('01-09-2025', 'DD-MM-YYYY'),
 E'Buen estado general'
),
('P002',
 E'María López Díaz',
 NULL,
 45,
 E'Calle Estado 235, Curicó, Región del Maule',
 E'Ninguno',
 'O001',
 TO_DATE('15-09-2025', 'DD-MM-YYYY'),
 E'HER2 positivo'
);

-- 🔹 Sillones
INSERT INTO sillon (id_sillon, ubicacion_sala, estado, observaciones)
VALUES
('SILL01',
 E'Sala 1',
 E'Disponible',
 E'Sillón ergonómico, con bomba infusora'
),
('SILL02',
 E'Sala 2',
 E'Disponible',
 E'Sillón con soporte reclinable'
);

-- 🔹 Sesiones
INSERT INTO sesion (
    id_sesion, id_paciente, id_patologia, id_sillon, fecha,
    hora_inicio, hora_fin, tiempo_aseo_min, materiales_usados, estado
)
VALUES
('SES001',
 'P001',
 'O001',
 'SILL01',
 TO_DATE('10-10-2025', 'DD-MM-YYYY'),
 '09:00',
 '11:40',
 15,
 E'Guantes, Jeringas, Vías periféricas',
 E'Confirmado'
),
('SES002',
 'P002',
 'O001',
 'SILL02',
 TO_DATE('10-10-2025', 'DD-MM-YYYY'),
 '09:15',
 '13:25',
 15,
 E'Guantes, Catéter central, Soluciones',
 E'Confirmado'
);
