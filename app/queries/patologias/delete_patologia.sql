DELETE FROM patologia
WHERE id_patologia = $1
RETURNING 
    id_patologia,
    nombre_patologia,
    especialidad;
