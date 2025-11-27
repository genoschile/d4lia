from typing import List, Optional
from app.modules.medicamento_hospitalizacion.entities.medicamento_hospitalizacion_entity import MedicamentoHospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class MedicamentoHospitalizacionRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[MedicamentoHospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_medicamento, id_profesional,
                   dosis, frecuencia, via_administracion, duracion, observaciones
            FROM medicamento_hospitalizacion
            ORDER BY id_hospitalizacion DESC;
        """
        rows = await conn.fetch(query)
        return [MedicamentoHospitalizacion(**dict(row)) for row in rows]

    async def create(self, conn, entity: MedicamentoHospitalizacion) -> MedicamentoHospitalizacion:
        query = """
            INSERT INTO medicamento_hospitalizacion (id_hospitalizacion, id_medicamento, id_profesional, dosis, frecuencia, via_administracion, duracion, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id_hospitalizacion, id_medicamento, id_profesional, dosis, frecuencia, via_administracion, duracion, observaciones;
        """
        row = await conn.fetchrow(
            query,
            entity.id_hospitalizacion,
            entity.id_medicamento,
            entity.id_profesional,
            entity.dosis,
            entity.frecuencia,
            entity.via_administracion,
            entity.duracion,
            entity.observaciones
        )
        return MedicamentoHospitalizacion(**dict(row))

    async def delete(self, conn, id_hospitalizacion: int, id_medicamento: int) -> bool:
        query = """
            DELETE FROM medicamento_hospitalizacion 
            WHERE id_hospitalizacion = $1 AND id_medicamento = $2
            RETURNING id_hospitalizacion;
        """
        deleted_id = await conn.fetchval(query, id_hospitalizacion, id_medicamento)
        return deleted_id is not None

    async def get_by_hospitalizacion(self, conn, id_hospitalizacion: int) -> List[dict]:
        # Retorna detalles con join a medicamento
        query = """
            SELECT mh.id_hospitalizacion, mh.id_medicamento, mh.id_profesional,
                   mh.dosis, mh.frecuencia, mh.via_administracion, mh.duracion, mh.observaciones,
                   m.nombre as nombre_medicamento, m.descripcion as descripcion_medicamento
            FROM medicamento_hospitalizacion mh
            JOIN medicamento m ON mh.id_medicamento = m.id_medicamento
            WHERE mh.id_hospitalizacion = $1;
        """
        rows = await conn.fetch(query, id_hospitalizacion)
        return [dict(row) for row in rows]

    async def exists(self, conn, id_hospitalizacion: int, id_medicamento: int) -> bool:
        query = """
            SELECT 1 FROM medicamento_hospitalizacion 
            WHERE id_hospitalizacion = $1 AND id_medicamento = $2;
        """
        val = await conn.fetchval(query, id_hospitalizacion, id_medicamento)
        return val is not None
