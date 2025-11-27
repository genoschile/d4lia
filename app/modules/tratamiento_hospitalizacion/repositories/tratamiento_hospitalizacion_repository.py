from typing import List, Optional
from app.modules.tratamiento_hospitalizacion.entities.tratamiento_hospitalizacion_entity import TratamientoHospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class TratamientoHospitalizacionRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[TratamientoHospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_tratamiento, id_profesional,
                   fecha_aplicacion, dosis, duracion, observaciones
            FROM tratamiento_hospitalizacion
            ORDER BY fecha_aplicacion DESC;
        """
        rows = await conn.fetch(query)
        return [TratamientoHospitalizacion(**dict(row)) for row in rows]

    async def create(self, conn, entity: TratamientoHospitalizacion) -> TratamientoHospitalizacion:
        query = """
            INSERT INTO tratamiento_hospitalizacion (id_hospitalizacion, id_tratamiento, id_profesional, fecha_aplicacion, dosis, duracion, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id_hospitalizacion, id_tratamiento, id_profesional, fecha_aplicacion, dosis, duracion, observaciones;
        """
        row = await conn.fetchrow(
            query,
            entity.id_hospitalizacion,
            entity.id_tratamiento,
            entity.id_profesional,
            entity.fecha_aplicacion,
            entity.dosis,
            entity.duracion,
            entity.observaciones
        )
        return TratamientoHospitalizacion(**dict(row))

    async def delete(self, conn, id_hospitalizacion: int, id_tratamiento: int) -> bool:
        query = """
            DELETE FROM tratamiento_hospitalizacion 
            WHERE id_hospitalizacion = $1 AND id_tratamiento = $2
            RETURNING id_hospitalizacion;
        """
        deleted_id = await conn.fetchval(query, id_hospitalizacion, id_tratamiento)
        return deleted_id is not None

    async def get_by_hospitalizacion(self, conn, id_hospitalizacion: int) -> List[dict]:
        # Retorna detalles con join a tratamiento
        query = """
            SELECT th.id_hospitalizacion, th.id_tratamiento, th.id_profesional,
                   th.fecha_aplicacion, th.dosis, th.duracion, th.observaciones,
                   t.nombre as nombre_tratamiento, t.descripcion as descripcion_tratamiento
            FROM tratamiento_hospitalizacion th
            JOIN tratamiento t ON th.id_tratamiento = t.id_tratamiento
            WHERE th.id_hospitalizacion = $1
            ORDER BY th.fecha_aplicacion DESC;
        """
        rows = await conn.fetch(query, id_hospitalizacion)
        return [dict(row) for row in rows]

    async def exists(self, conn, id_hospitalizacion: int, id_tratamiento: int) -> bool:
        query = """
            SELECT 1 FROM tratamiento_hospitalizacion 
            WHERE id_hospitalizacion = $1 AND id_tratamiento = $2;
        """
        val = await conn.fetchval(query, id_hospitalizacion, id_tratamiento)
        return val is not None
