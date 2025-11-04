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
