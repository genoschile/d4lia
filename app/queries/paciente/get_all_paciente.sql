SELECT 
    id_paciente,
    rut,
    nombre_completo,
    correo,
    telefono,
    edad,
    direccion,
    antecedentes_medicos,
    id_patologia,
    fecha_inicio_tratamiento,
    observaciones
FROM paciente
ORDER BY id_paciente;
