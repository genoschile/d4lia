SELECT *
FROM paciente
WHERE id_patologia = $1
ORDER BY id_paciente;
