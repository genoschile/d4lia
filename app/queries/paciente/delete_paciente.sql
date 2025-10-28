DELETE FROM paciente
WHERE id_paciente = $1
RETURNING
    id_paciente,
    rut,
    nombre_completo;
