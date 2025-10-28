INSERT INTO sillon (id_sillon, ubicacion_sala, estado, observaciones)
VALUES ($1, $2, $3, $4)
RETURNING id_sillon, ubicacion_sala, estado, observaciones;
