SELECT p.nombre_completo, e.*
FROM encuesta_satisfaccion e
JOIN sesion s ON e.id_sesion = s.id_sesion
JOIN paciente p ON s.id_paciente = p.id_paciente;
