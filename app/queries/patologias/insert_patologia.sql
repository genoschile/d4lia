INSERT INTO patologia (
    id_patologia,
    nombre_patologia,
    especialidad,
    tiempo_estimado,
    explicacion,
    tratamientos_principales,
    farmacos,
    efectos_adversos,
    gravedad,
    costo_aprox,
    evidencia,
    exito_porcentaje,
    edad_promedio,
    notas
)
VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
)
RETURNING 
    id_patologia,
    nombre_patologia,
    especialidad,
    tiempo_estimado,
    explicacion,
    tratamientos_principales,
    farmacos,
    efectos_adversos,
    gravedad,
    costo_aprox,
    evidencia,
    exito_porcentaje,
    edad_promedio,
    notas;
