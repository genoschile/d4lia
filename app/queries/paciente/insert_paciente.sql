INSERT INTO paciente (
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
)
VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
)
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
