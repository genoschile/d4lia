from typing import List, Optional
from app.modules.cie10.entities.cie10_entity import Cie10
from app.modules.cie10.schemas.cie10_schema import Cie10Create, Cie10Update
from app.core.exceptions import ConflictError, NotFoundError


class Cie10Repository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Cie10]:
        query = """
            SELECT id_cie10, codigo, nombre, categoria, descripcion, activo
            FROM cie10
            ORDER BY codigo;
        """
        rows = await conn.fetch(query)
        return [Cie10(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Cie10]:
        query = """
            SELECT id_cie10, codigo, nombre, categoria, descripcion, activo
            FROM cie10
            WHERE id_cie10 = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Cie10(**dict(row))
        return None

    async def get_by_codigo(self, conn, codigo: str) -> Optional[Cie10]:
        query = """
            SELECT id_cie10, codigo, nombre, categoria, descripcion, activo
            FROM cie10
            WHERE codigo = $1;
        """
        row = await conn.fetchrow(query, codigo)
        if row:
            return Cie10(**dict(row))
        return None

    async def create(self, conn, cie10: Cie10) -> Cie10:
        query = """
            INSERT INTO cie10 (codigo, nombre, categoria, descripcion, activo)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id_cie10;
        """
        id_cie10 = await conn.fetchval(
            query,
            cie10.codigo,
            cie10.nombre,
            cie10.categoria,
            cie10.descripcion,
            cie10.activo
        )
        cie10.id_cie10 = id_cie10
        return cie10

    async def update(self, conn, id: int, data: dict) -> Optional[Cie10]:
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
            UPDATE cie10 
            SET {', '.join(set_clauses)} 
            WHERE id_cie10 = ${idx} 
            RETURNING id_cie10, codigo, nombre, categoria, descripcion, activo;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Cie10(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM cie10 WHERE id_cie10 = $1 RETURNING id_cie10;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def search(self, conn, term: str) -> List[Cie10]:
        query = """
            SELECT id_cie10, codigo, nombre, categoria, descripcion, activo
            FROM cie10
            WHERE codigo ILIKE $1 OR nombre ILIKE $1 OR categoria ILIKE $1
            ORDER BY codigo
            LIMIT 50;
        """
        rows = await conn.fetch(query, f"%{term}%")
        return [Cie10(**dict(row)) for row in rows]
