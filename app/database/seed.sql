-- =============================================
-- SEED.SQL - Datos iniciales base de Oncología
-- =============================================

-- 🔹 Encargados
INSERT INTO encargado (nombre_completo, rut, correo, telefono, cargo, especialidad)
VALUES
(E'Dra. Carolina Gómez Muñoz', '15.234.567-8', 'carolina.gomez@hospital.cl', '+56912345678', 'doctor', 'Oncología'),
(E'Enf. Rodrigo Salinas Paredes', '16.345.678-9', 'rodrigo.salinas@hospital.cl', '+56998765432', 'enfermero', 'Quimioterapia'),
(E'Téc. Ana Torres Fuentes', '17.987.654-3', 'ana.torres@hospital.cl', '+56955555555', 'técnico', 'Apoyo clínico');

-- 🔹 Patologías
INSERT INTO patologia (
    codigo, nombre_patologia, especialidad, tiempo_estimado, explicacion,
    tratamientos_principales, farmacos, efectos_adversos, gravedad,
    costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas
)
VALUES
('O001',
    E'Cáncer de próstata (local/alto riesgo)',
    E'Oncología',
    E'1 hr/sesión - total 6 meses',
    E'Tumor prostático tratado con radioterapia (RT), quimioterapia (QT) y/o hormonoterapia según riesgo.',
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

-- 🔹 Tratamientos
INSERT INTO tratamiento (nombre_tratamiento, descripcion, duracion_estimada, costo_aprox, observaciones)
VALUES
(E'Radioterapia', E'Terapia con radiación dirigida para destruir células cancerosas', E'6 meses', E'US$2.500/sesión', E'Requiere seguimiento de efectos secundarios'),
(E'Quimioterapia', E'Tratamiento con fármacos citotóxicos', E'6 meses', E'US$3.000/sesión', E'Control de toxicidad hematológica necesario'),
(E'Hormonoterapia', E'Bloqueo hormonal para cáncer hormono-dependiente', E'12 meses', E'US$1.500/sesión', E'Requiere control de testosterona y PSA');

-- 🔹 Vinculación Patología ↔ Tratamiento
INSERT INTO patologia_tratamiento (id_patologia, id_tratamiento)
VALUES
(1, 1),
(1, 2),
(1, 3);

-- 🔹 Pacientes
INSERT INTO paciente (
    rut, nombre_completo, correo, telefono, edad, direccion, antecedentes_medicos,
    id_patologia, id_encargado_registro, fecha_inicio_tratamiento, observaciones
)
VALUES
('12.345.678-9',
    E'Juan Pérez Soto',
    E'juan.perez@example.com',
    NULL,
    62,
    E'Avenida 2 Sur 1456, Talca, Región del Maule',
    E'Hipertensión, Diabetes',
    1,
    1, -- Registrado por la Dra. Carolina Gómez
    TO_DATE('01-09-2025', 'DD-MM-YYYY'),
    E'Buen estado general'
),
('9.876.543-2',
    E'María López Díaz',
    E'maria.lopez@example.com',
    NULL,
    45,
    E'Calle Estado 235, Curicó, Región del Maule',
    E'Ninguno',
    1,
    2, -- Registrada por el enfermero Rodrigo
    TO_DATE('15-09-2025', 'DD-MM-YYYY'),
    E'HER2 positivo'
);

-- 🔹 Sillones
INSERT INTO sillon (ubicacion_sala, estado, observaciones)
VALUES
    (E'consultorio_1', E'disponible', E'Sillón ergonómico, con bomba infusora'),
    (E'consultorio_2', E'disponible', E'Sillón con soporte reclinable');

-- 🔹 Sesiones
INSERT INTO sesion (
    id_paciente, id_patologia, id_tratamiento, id_sillon, id_encargado,
    fecha, hora_inicio, hora_fin, tiempo_aseo_min, materiales_usados, estado
)
VALUES
(1, 1, 1, 1, 2, TO_DATE('10-10-2025', 'DD-MM-YYYY'), '09:00', '11:40', 15, E'Guantes, Jeringas, Vías periféricas', E'confirmado'),
(2, 1, 2, 2, 3, TO_DATE('10-10-2025', 'DD-MM-YYYY'), '09:15', '13:25', 15, E'Guantes, Catéter central, Soluciones', E'confirmado');

-- 🔹 Encuestas de Sesión
INSERT INTO encuesta_sesion_json (id_sesion, tipo_encuesta, datos)
VALUES
(1, 'satisfaccion',
'{
    "puntaje_global": 9,
    "atencion_personal": 10,
    "comodidad_sillon": 8,
    "limpieza_area": 9,
    "puntualidad": 10,
    "comentarios": "Todo excelente, personal muy amable"
}'),
(1, 'pre_sesion',
'{
    "nivel_dolor": 3,
    "estado_animo": "positivo",
    "observaciones": "Sin fiebre ni molestias"
}'),
(2, 'satisfaccion',
'{
    "puntaje_global": 8,
    "atencion_personal": 9,
    "comodidad_sillon": 7,
    "limpieza_area": 8,
    "puntualidad": 9,
    "comentarios": "Buen servicio, aunque el sillón podría ser más cómodo"
}');

-- 🔹 Encuestas de Paciente (antecedentes, hábitos, etc.)
INSERT INTO encuesta_paciente_json (id_paciente, tipo_encuesta, datos)
VALUES
(1, 'antecedentes_medicos',
'{
    "fuma": false,
    "alcohol": "ocasional",
    "alergias": ["penicilina"],
    "cirugias_previas": ["apendicectomía"],
    "enfermedades_cronicas": ["diabetes tipo II"]
}'),
(2, 'habitos',
'{
    "fuma": true,
    "alcohol": "moderado",
    "actividad_fisica": "3 veces por semana",
    "dieta": "balanceada",
    "descanso": "7 horas diarias"
}');


-- =============================================
-- Parte new 
-- =============================================

-- =============================================
-- 🔹 Condiciones personales (preexistencias, alergias, etc.)
-- =============================================
INSERT INTO condicion_personal (codigo, nombre_condicion, tipo, severidad, observaciones)
VALUES
('E11', E'Diabetes tipo 2', 'preexistencia', 'moderada', E'Control con metformina'),
('I10', E'Hipertensión arterial esencial', 'preexistencia', 'alta', E'Tratada con losartán'),
('A001', E'Alergia a la penicilina', 'alergia', 'alta', E'Evitar antibióticos betalactámicos'),
('N001', E'Estrés crónico', 'otro', 'variable', E'Autodeclarado por el paciente');

-- =============================================
-- 🔹 Relación Paciente ↔ Condición personal
-- =============================================
INSERT INTO paciente_condicion (id_paciente, id_condicion, fecha_inicio, validada_medico, observaciones)
VALUES
(1, 1, TO_DATE('2015-03-10', 'YYYY-MM-DD'), TRUE, E'Diagnosticada hace 10 años'),
(1, 2, TO_DATE('2018-07-20', 'YYYY-MM-DD'), TRUE, E'Controlada con medicación'),
(1, 3, TO_DATE('2010-05-01', 'YYYY-MM-DD'), FALSE, E'Alergia reportada por el paciente'),
(2, 4, TO_DATE('2023-01-15', 'YYYY-MM-DD'), FALSE, E'Reportado durante la entrevista inicial');

-- =============================================
-- 🔹 Especializaciones médicas
-- =============================================
INSERT INTO especializacion (nombre, descripcion, codigo_fonasa, nivel)
VALUES
(E'Oncología Médica', E'Tratamiento del cáncer mediante quimioterapia, hormonoterapia y terapias dirigidas', 'F001', 'especialista'),
(E'Cardiología', E'Diagnóstico y tratamiento de enfermedades del corazón y vasos sanguíneos', 'F002', 'especialista'),
(E'Medicina Interna', E'Evaluación y manejo integral de pacientes adultos', 'F003', 'general'),
(E'Endocrinología', E'Tratamiento de trastornos hormonales y metabólicos', 'F004', 'especialista');

-- =============================================
-- 🔹 Médicos
-- =============================================
INSERT INTO medico (rut, nombre, apellido, sexo, correo, telefono, codigo_fonasa, activo)
VALUES
('15.234.567-8', E'Carolina', E'Gómez', 'femenino', 'carolina.gomez@hospital.cl', '+56912345678', 'M001', TRUE),
('18.111.222-3', E'Rodrigo', E'Salinas', 'masculino', 'rodrigo.salinas@hospital.cl', '+56998765432', 'M002', TRUE),
('19.333.444-5', E'Ana', E'Torres', 'femenino', 'ana.torres@hospital.cl', '+56955555555', 'M003', TRUE);

-- =============================================
-- 🔹 Consulta Profesional (Médico ↔ Especialización)
-- =============================================
INSERT INTO consulta_profesional (id_medico, id_especializacion)
VALUES
(1, 1), -- Dra. Carolina Gómez → Oncología Médica
(2, 3), -- Dr. Rodrigo Salinas → Medicina Interna
(3, 2), -- Dra. Ana Torres → Cardiología
(3, 4); -- Dra. Ana Torres → Endocrinología (subespecialista)

-- =============================================
-- 🔹 Consultas Médicas (Paciente ↔ Profesional)
-- =============================================
INSERT INTO consulta_medica (id_paciente, id_profesional, especialidad, fecha, motivo, tratamiento, observaciones)
VALUES
(1, 1, E'Oncología Médica', TO_DATE('2025-09-10', 'YYYY-MM-DD'),
 E'Control post-quimioterapia', 
 E'Revisión de análisis, ajuste de dosis de Docetaxel', 
 E'Paciente estable, continuar mismo régimen'),
(1, 2, E'Medicina Interna', TO_DATE('2025-09-25', 'YYYY-MM-DD'),
 E'Chequeo general y control de presión', 
 E'Losartán 50mg diario', 
 E'Presión controlada, sin efectos adversos'),
(2, 3, E'Cardiología', TO_DATE('2025-10-05', 'YYYY-MM-DD'),
 E'Dolor torácico leve', 
 E'Ecocardiograma + seguimiento', 
 E'Sin hallazgos relevantes, se sugiere control en 6 meses');


-- =============================================
-- 🔹 MEDICAMENTOS
-- =============================================
INSERT INTO medicamento (
    nombre_comercial, nombre_generico, concentracion, forma_farmaceutica,
    via_administracion, laboratorio, requiere_receta, stock_disponible, observaciones
)
VALUES
(E'Paracetamol 500 mg', E'Paracetamol', E'500 mg', E'Comprimido', E'Oral', E'Laboratorio Chile', FALSE, 250, E'Analgésico y antipirético de uso común'),
(E'Losartán 50 mg', E'Losartán potásico', E'50 mg', E'Comprimido', E'Oral', E'Recalcine', TRUE, 180, E'Antihipertensivo de primera línea'),
(E'Metformina 850 mg', E'Metformina clorhidrato', E'850 mg', E'Comprimido', E'Oral', E'Saval', TRUE, 300, E'Antidiabético oral, usar con precaución en insuficiencia renal'),
(E'Amoxicilina 500 mg', E'Amoxicilina', E'500 mg', E'Cápsula', E'Oral', E'Laboratorio Andrómaco', TRUE, 150, E'Antibiótico de amplio espectro'),
(E'Ibuprofeno 400 mg', E'Ibuprofeno', E'400 mg', E'Comprimido', E'Oral', E'Medipharm', FALSE, 500, E'Analgésico, antipirético y antiinflamatorio no esteroidal');

-- =============================================
-- 🔹 RECETAS MÉDICAS
-- =============================================
INSERT INTO receta (
    id_paciente, id_medico, id_consulta, fecha_inicio, fecha_fin, observaciones
)
VALUES
(1, 1, 1, TO_DATE('10-10-2025', 'DD-MM-YYYY'), TO_DATE('24-10-2025', 'DD-MM-YYYY'), E'Tratamiento para control de dolor y glucosa'),
(2, 2, 2, TO_DATE('12-10-2025', 'DD-MM-YYYY'), TO_DATE('26-10-2025', 'DD-MM-YYYY'), E'Antibiótico por infección respiratoria leve');

-- =============================================
-- 🔹 RELACIÓN RECETA ↔ MEDICAMENTO
-- =============================================
INSERT INTO receta_medicamento (
    id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones
)
VALUES
-- Receta 1 (Paciente Juan Pérez)
(1, 1, E'500 mg', E'Cada 8 horas', E'7 días', E'Tomar después de las comidas'),
(1, 3, E'850 mg', E'Cada 12 horas', E'Indefinido', E'Mantener control de glucosa semanal'),
(1, 5, E'400 mg', E'Cada 8 horas', E'3 días', E'Solo en caso de dolor o fiebre'),

-- Receta 2 (Paciente María López)
(2, 4, E'500 mg', E'Cada 8 horas', E'10 días', E'Completar el tratamiento aunque desaparezcan los síntomas'),
(2, 1, E'500 mg', E'Cada 8 horas', E'5 días', E'Para control de fiebre y malestar');


-- =============================================
-- 🔹 TIPO_EXAMEN
-- =============================================
INSERT INTO tipo_examen (nombre, descripcion, codigo_interno, requiere_ayuno, tiempo_estimado, observaciones)
VALUES
(E'Hemograma completo', E'Análisis de sangre para evaluar glóbulos rojos, blancos y plaquetas.', 'LAB001', FALSE, E'15 min', E'Requiere muestra de sangre'),
(E'Radiografía de tórax', E'Imagen del tórax para evaluar pulmones y corazón.', 'IMG002', FALSE, E'20 min', E'Evitar objetos metálicos'),
(E'TAC abdominal', E'Examen de tomografía computarizada del abdomen.', 'IMG003', TRUE, E'30 min', E'Ayuno de 6 horas requerido'),
(E'Prueba de función renal', E'Mide la capacidad de filtración de los riñones.', 'LAB004', TRUE, E'10 min', E'Se recomienda hidratación previa');

-- =============================================
-- 🔹 INSTALACION
-- =============================================
INSERT INTO instalacion (nombre, tipo, ubicacion, contacto, observaciones)
VALUES
(E'Laboratorio Central', 'laboratorio', E'Edificio B - Piso 1', E'laboratorio@hospital.cl', E'Muestra de sangre y orina'),
(E'Sala de Imagenología', 'imagenologia', E'Edificio C - Piso 2', E'imagenes@hospital.cl', E'Radiografías, TAC, resonancias'),
(E'Clínica Externa Curicó', 'externo', E'Calle San Martín 456, Curicó', E'contacto@clinicacurico.cl', E'Colaboración externa en exámenes de especialidad');

-- =============================================
-- 🔹 ORDEN_EXAMEN
-- =============================================
INSERT INTO orden_examen (id_consulta, id_profesional, id_paciente, id_tipo_examen, fecha, motivo, documento, estado)
VALUES
(1, 1, 1, 1, TO_DATE('05-10-2025', 'DD-MM-YYYY'), E'Control post-quimioterapia, revisión general', E'orden_juan_hemograma.pdf', 'en_proceso'),
(2, 2, 2, 2, TO_DATE('06-10-2025', 'DD-MM-YYYY'), E'Tos persistente y control pulmonar', E'orden_maria_rx_torax.pdf', 'pendiente'),
(1, 1, 1, 4, TO_DATE('07-10-2025', 'DD-MM-YYYY'), E'Chequeo función renal previo a tratamiento', NULL, 'pendiente');

-- =============================================
-- 🔹 EXAMEN
-- =============================================
INSERT INTO examen (id_paciente, id_tipo_examen, id_profesional, id_orden_examen, id_instalacion, documento, fecha, resultados, observaciones)
VALUES
(1, 1, 1, 1, 1, E'resultado_hemograma_juan.pdf', TO_DATE('06-10-2025', 'DD-MM-YYYY'),
 E'Hemoglobina: 13.5 g/dL, Leucocitos: 6.8 x10⁹/L, Plaquetas: 250 x10⁹/L',
 E'Valores normales, sin alteraciones.'),
(2, 2, 2, 2, 2, E'resultado_rx_maria.pdf', TO_DATE('07-10-2025', 'DD-MM-YYYY'),
 E'Imagen pulmonar sin signos de infección ni masas evidentes.',
 E'Resultado dentro de parámetros normales.'),
(1, 4, 1, 3, 1, E'resultado_funcion_renal_juan.pdf', TO_DATE('08-10-2025', 'DD-MM-YYYY'),
 E'Creatinina: 0.9 mg/dL, TFG estimada: 95 mL/min/1.73m²',
 E'Función renal normal, puede continuar tratamiento.');
