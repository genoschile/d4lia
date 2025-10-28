DELETE FROM sillon
WHERE id_sillon = $1
RETURNING id_sillon, ubicacion_sala, estado, observaciones;
