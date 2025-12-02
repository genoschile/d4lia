from typing import List, Optional
from app.modules.ges.entities.ges_entity import Ges
from app.modules.ges.schemas.ges_schema import GesCreate, GesUpdate
from app.core.exceptions import ConflictError, NotFoundError


class GesRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Ges]:
        query = """
            SELECT id_ges, codigo_ges, nombre, descripcion, cobertura, 
                   dias_limite_diagnostico, dias_limite_tratamiento, 
                   requiere_fonasa, vigente
            FROM ges
            ORDER BY nombre;
        """
        rows = await conn.fetch(query)
        return [Ges(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Ges]:
        query = """
            SELECT id_ges, codigo_ges, nombre, descripcion, cobertura, 
                   dias_limite_diagnostico, dias_limite_tratamiento, 
                   requiere_fonasa, vigente
            FROM ges
            WHERE id_ges = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Ges(**dict(row))
        return None

    async def get_by_codigo(self, conn, codigo: str) -> Optional[Ges]:
        query = """
            SELECT id_ges, codigo_ges, nombre, descripcion, cobertura, 
                   dias_limite_diagnostico, dias_limite_tratamiento, 
                   requiere_fonasa, vigente
            FROM ges
            WHERE codigo_ges = $1;
        """
        row = await conn.fetchrow(query, codigo)
        if row:
            return Ges(**dict(row))
        return None

    async def create(self, conn, ges: Ges) -> Ges:
        query = """
            INSERT INTO ges (codigo_ges, nombre, descripcion, cobertura, 
                           dias_limite_diagnostico, dias_limite_tratamiento, 
                           requiere_fonasa, vigente)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id_ges;
        """
        id_ges = await conn.fetchval(
            query,
            ges.codigo_ges,
            ges.nombre,
            ges.descripcion,
            ges.cobertura,
            ges.dias_limite_diagnostico,
            ges.dias_limite_tratamiento,
            ges.requiere_fonasa,
            ges.vigente
        )
        ges.id_ges = id_ges
        return ges

    async def update(self, conn, id: int, data: dict) -> Optional[Ges]:
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
            UPDATE ges 
            SET {', '.join(set_clauses)} 
            WHERE id_ges = ${idx} 
            RETURNING id_ges, codigo_ges, nombre, descripcion, cobertura, vigente;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Ges(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM ges WHERE id_ges = $1 RETURNING id_ges;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def search(self, conn, term: str) -> List[Ges]:
        query = """
            SELECT id_ges, codigo_ges, nombre, descripcion, cobertura, vigente
            FROM ges
            WHERE codigo_ges ILIKE $1 OR nombre ILIKE $1
            ORDER BY nombre
            LIMIT 50;
        """
        rows = await conn.fetch(query, f"%{term}%")
        return [Ges(**dict(row)) for row in rows]
