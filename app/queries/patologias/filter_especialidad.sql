SELECT *
FROM patologia
WHERE especialidad = $1
ORDER BY id_patologia;
