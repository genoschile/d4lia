UPDATE paciente
SET
    rut = $1,
    nombre_completo = $2,
    correo = $3,
    telefono = $4,
    edad = $5,
    direccion = $6,
    antecedentes_medicos = $7,
    id_patologia = $8,
    fecha_inicio_tratamiento = $9,
    observaciones = $10
WHERE id_paciente = $11
RETURNING
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
    observaciones;
