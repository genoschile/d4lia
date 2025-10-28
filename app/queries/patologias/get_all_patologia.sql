SELECT 
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
FROM patologia
ORDER BY id_patologia;
