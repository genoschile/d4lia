from typing import List, Optional
from app.modules.cie10_ges.entities.cie10_ges_entity import Cie10Ges


class Cie10GesRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create(self, conn, cie10_ges: Cie10Ges) -> Cie10Ges:
        query = """
            INSERT INTO cie10_ges (id_cie10, id_ges)
            VALUES ($1, $2)
            RETURNING id_cie10, id_ges;
        """
        row = await conn.fetchrow(
            query,
            cie10_ges.id_cie10,
            cie10_ges.id_ges
        )
        return Cie10Ges(**dict(row))

    async def delete(self, conn, id_cie10: int, id_ges: int) -> bool:
        query = """
            DELETE FROM cie10_ges 
            WHERE id_cie10 = $1 AND id_ges = $2
            RETURNING id_cie10;
        """
        deleted_id = await conn.fetchval(query, id_cie10, id_ges)
        return deleted_id is not None

    async def get_ges_by_cie10(self, conn, id_cie10: int) -> List[dict]:
        query = """
            SELECT cg.id_cie10, cg.id_ges,
                   g.codigo_ges as ges_codigo, g.nombre as ges_nombre
            FROM cie10_ges cg
            JOIN ges g ON cg.id_ges = g.id_ges
            WHERE cg.id_cie10 = $1
            ORDER BY g.nombre;
        """
        rows = await conn.fetch(query, id_cie10)
        return [dict(row) for row in rows]

    async def get_cie10_by_ges(self, conn, id_ges: int) -> List[dict]:
        query = """
            SELECT cg.id_cie10, cg.id_ges,
                   c.codigo as cie10_codigo, c.nombre as cie10_nombre
            FROM cie10_ges cg
            JOIN cie10 c ON cg.id_cie10 = c.id_cie10
            WHERE cg.id_ges = $1
            ORDER BY c.codigo;
        """
        rows = await conn.fetch(query, id_ges)
        return [dict(row) for row in rows]

    async def exists(self, conn, id_cie10: int, id_ges: int) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1 FROM cie10_ges 
                WHERE id_cie10 = $1 AND id_ges = $2
            );
        """
        return await conn.fetchval(query, id_cie10, id_ges)

    async def list_all(self, conn) -> List[dict]:
        query = """
            SELECT cg.id_cie10, cg.id_ges,
                   c.codigo as cie10_codigo, c.nombre as cie10_nombre,
                   g.codigo_ges as ges_codigo, g.nombre as ges_nombre
            FROM cie10_ges cg
            JOIN cie10 c ON cg.id_cie10 = c.id_cie10
            JOIN ges g ON cg.id_ges = g.id_ges
            ORDER BY c.codigo, g.nombre;
        """
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
