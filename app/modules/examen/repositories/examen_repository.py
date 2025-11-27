from typing import List, Optional
from app.modules.examen.entities.examen_entity import Examen
from app.modules.examen.schemas.examen_schema import ExamenCreate, ExamenUpdate
from app.core.exceptions import ConflictError, NotFoundError


class ExamenRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Examen]:
        query = """
            SELECT id_examen, id_paciente, id_tipo_examen, id_profesional, id_orden_examen,
                   id_instalacion, documento, fecha, resultados, resumen_resultado, observaciones
            FROM examen
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query)
        return [Examen(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Examen]:
        query = """
            SELECT id_examen, id_paciente, id_tipo_examen, id_profesional, id_orden_examen,
                   id_instalacion, documento, fecha, resultados, resumen_resultado, observaciones
            FROM examen
            WHERE id_examen = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Examen(**dict(row))
        return None

    async def create(self, conn, examen: Examen) -> Examen:
        query = """
            INSERT INTO examen (id_paciente, id_tipo_examen, id_profesional, id_orden_examen, id_instalacion, documento, fecha, resultados, resumen_resultado, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id_examen;
        """
        id_examen = await conn.fetchval(
            query,
            examen.id_paciente,
            examen.id_tipo_examen,
            examen.id_profesional,
            examen.id_orden_examen,
            examen.id_instalacion,
            examen.documento,
            examen.fecha,
            examen.resultados,
            examen.resumen_resultado,
            examen.observaciones
        )
        examen.id_examen = id_examen
        return examen

    async def update(self, conn, id: int, data: dict) -> Optional[Examen]:
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
            UPDATE examen 
            SET {', '.join(set_clauses)} 
            WHERE id_examen = ${idx} 
            RETURNING id_examen, id_paciente, id_tipo_examen, id_profesional, id_orden_examen, id_instalacion, documento, fecha, resultados, resumen_resultado, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Examen(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM examen WHERE id_examen = $1 RETURNING id_examen;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[Examen]:
        query = """
            SELECT id_examen, id_paciente, id_orden_examen, id_tipo_examen,
                   id_profesional, id_instalacion, documento, fecha, resultados, observaciones
            FROM examen
            WHERE id_paciente = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [Examen(**dict(row)) for row in rows]

    async def get_by_orden(self, conn, id_orden: int) -> List[Examen]:
        query = """
            SELECT id_examen, id_paciente, id_orden_examen, id_tipo_examen,
                   id_profesional, id_instalacion, documento, fecha, resultados, observaciones
            FROM examen
            WHERE id_orden_examen = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_orden)
        return [Examen(**dict(row)) for row in rows]
