from typing import List, Optional
from app.modules.orden_examen.entities.orden_examen_entity import OrdenExamen
from app.modules.orden_examen.schemas.orden_examen_schema import OrdenExamenCreate, OrdenExamenUpdate
from app.core.exceptions import ConflictError, NotFoundError


class OrdenExamenRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[OrdenExamen]:
        query = """
            SELECT id_orden_examen, id_consulta, id_profesional, id_paciente, id_tipo_examen, id_estado,
                   fecha, fecha_programada, fecha_solicitada, motivo, documento, estado
            FROM orden_examen
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query)
        return [OrdenExamen(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[OrdenExamen]:
        query = """
            SELECT id_orden_examen, id_consulta, id_profesional, id_paciente, id_tipo_examen, id_estado,
                   fecha, fecha_programada, fecha_solicitada, motivo, documento, estado
            FROM orden_examen
            WHERE id_orden_examen = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return OrdenExamen(**dict(row))
        return None

    async def create(self, conn, orden: OrdenExamen) -> OrdenExamen:
        query = """
            INSERT INTO orden_examen (id_consulta, id_profesional, id_paciente, id_tipo_examen, id_estado, fecha, fecha_programada, fecha_solicitada, motivo, documento, estado)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id_orden_examen;
        """
        id_orden = await conn.fetchval(
            query,
            orden.id_consulta,
            orden.id_profesional,
            orden.id_paciente,
            orden.id_tipo_examen,
            orden.id_estado,
            orden.fecha,
            orden.fecha_programada,
            orden.fecha_solicitada,
            orden.motivo,
            orden.documento,
            orden.estado
        )
        orden.id_orden_examen = id_orden
        return orden

    async def update(self, conn, id: int, data: dict) -> Optional[OrdenExamen]:
        set_clauses = []
        values = []
        idx = 1
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
            idx += 1
        
        if not set_clauses:
            return await self.get_by_id(conn, id)

        values.append(id)
        query = f"""
            UPDATE orden_examen 
            SET {', '.join(set_clauses)} 
            WHERE id_orden_examen = ${idx} 
            RETURNING id_orden_examen, id_consulta, id_profesional, id_paciente, id_tipo_examen, id_estado, fecha, fecha_programada, fecha_solicitada, motivo, documento, estado;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return OrdenExamen(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM orden_examen WHERE id_orden_examen = $1 RETURNING id_orden_examen;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[OrdenExamen]:
        query = """
            SELECT id_orden_examen, id_consulta, id_profesional, id_paciente,
                   id_tipo_examen, fecha, motivo, documento, estado
            FROM orden_examen
            WHERE id_paciente = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [OrdenExamen(**dict(row)) for row in rows]

    async def get_by_consulta(self, conn, id_consulta: int) -> List[OrdenExamen]:
        query = """
            SELECT id_orden_examen, id_consulta, id_profesional, id_paciente,
                   id_tipo_examen, fecha, motivo, documento, estado
            FROM orden_examen
            WHERE id_consulta = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_consulta)
        return [OrdenExamen(**dict(row)) for row in rows]
