UPDATE patologia
SET 
    nombre_patologia = $1,
    especialidad = $2,
    tiempo_estimado = $3,
    explicacion = $4,
    tratamientos_principales = $5,
    farmacos = $6,
    efectos_adversos = $7,
    gravedad = $8,
    costo_aprox = $9,
    evidencia = $10,
    exito_porcentaje = $11,
    edad_promedio = $12,
    notas = $13
WHERE id_patologia = $14
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
