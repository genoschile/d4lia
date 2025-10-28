SELECT pa.nombre_patologia, AVG(e.puntaje_global) AS promedio_satisfaccion
FROM encuesta_satisfaccion e
JOIN sesion s ON e.id_sesion = s.id_sesion
JOIN patologia pa ON s.id_patologia = pa.id_patologia
GROUP BY pa.nombre_patologia;
