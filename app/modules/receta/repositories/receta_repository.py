from typing import List, Optional
from app.modules.receta.entities.receta_entity import Receta
from app.modules.receta.interfaces.receta_interfaces import IRecetaRepository


class RecetaRepository(IRecetaRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Receta]:
        query = """
            SELECT id_receta, id_paciente, id_medico, id_consulta,
                   fecha_inicio, fecha_fin, observaciones
            FROM receta
            ORDER BY fecha_inicio DESC;
        """
        rows = await conn.fetch(query)
        return [Receta(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Receta]:
        query = """
            SELECT id_receta, id_paciente, id_medico, id_consulta,
                   fecha_inicio, fecha_fin, observaciones
            FROM receta
            WHERE id_receta = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Receta(**dict(row))
        return None

    async def create(self, conn, receta: Receta) -> Receta:
        query = """
            INSERT INTO receta (id_paciente, id_medico, id_consulta, fecha_inicio, fecha_fin, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_receta;
        """
        id_receta = await conn.fetchval(
            query,
            receta.id_paciente,
            receta.id_medico,
            receta.id_consulta,
            receta.fecha_inicio,
            receta.fecha_fin,
            receta.observaciones
        )
        receta.id_receta = id_receta
        return receta

    async def update(self, conn, id: int, data: dict) -> Optional[Receta]:
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
            UPDATE receta 
            SET {', '.join(set_clauses)} 
            WHERE id_receta = ${idx} 
            RETURNING id_receta, id_paciente, id_medico, id_consulta, fecha_inicio, fecha_fin, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Receta(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM receta WHERE id_receta = $1 RETURNING id_receta;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[Receta]:
        query = """
            SELECT id_receta, id_paciente, id_medico, id_consulta,
                   fecha_inicio, fecha_fin, observaciones
            FROM receta
            WHERE id_paciente = $1
            ORDER BY fecha_inicio DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [Receta(**dict(row)) for row in rows]

    async def get_by_medico(self, conn, id_medico: int) -> List[Receta]:
        query = """
            SELECT id_receta, id_paciente, id_medico, id_consulta,
                   fecha_inicio, fecha_fin, observaciones
            FROM receta
            WHERE id_medico = $1
            ORDER BY fecha_inicio DESC;
        """
        rows = await conn.fetch(query, id_medico)
        return [Receta(**dict(row)) for row in rows]

    async def get_by_consulta(self, conn, id_consulta: int) -> List[Receta]:
        query = """
            SELECT id_receta, id_paciente, id_medico, id_consulta,
                   fecha_inicio, fecha_fin, observaciones
            FROM receta
            WHERE id_consulta = $1
            ORDER BY fecha_inicio DESC;
        """
        rows = await conn.fetch(query, id_consulta)
        return [Receta(**dict(row)) for row in rows]
