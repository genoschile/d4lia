-- =============================================
-- SEED.SQL - Datos iniciales base de Oncología
-- =============================================

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
    rut, nombre_completo, correo, telefono, edad, direccion, antecedentes_medicos,
    id_patologia, fecha_inicio_tratamiento, observaciones
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
    id_paciente, id_patologia, id_sillon, fecha,
    hora_inicio, hora_fin, tiempo_aseo_min, materiales_usados, estado
)
VALUES
(1, 1, 1, TO_DATE('10-10-2025', 'DD-MM-YYYY'), '09:00', '11:40', 15, E'Guantes, Jeringas, Vías periféricas', E'confirmado'),
(2, 1, 2, TO_DATE('10-10-2025', 'DD-MM-YYYY'), '09:15', '13:25', 15, E'Guantes, Catéter central, Soluciones', E'confirmado');

-- 🔹 Encuestas
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
