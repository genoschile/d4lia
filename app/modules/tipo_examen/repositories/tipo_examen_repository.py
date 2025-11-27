from typing import List, Optional
from app.modules.tipo_examen.entities.tipo_examen_entity import TipoExamen
from app.modules.tipo_examen.schemas.tipo_examen_schema import TipoExamenCreate, TipoExamenUpdate
from app.core.exceptions import ConflictError, NotFoundError


class TipoExamenRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[TipoExamen]:
        query = """
            SELECT id_tipo_examen, nombre, descripcion, codigo_interno,
                   requiere_ayuno, tiempo_estimado, observaciones
            FROM tipo_examen
            ORDER BY nombre;
        """
        rows = await conn.fetch(query)
        return [TipoExamen(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[TipoExamen]:
        query = """
            SELECT id_tipo_examen, nombre, descripcion, codigo_interno,
                   requiere_ayuno, tiempo_estimado, observaciones
            FROM tipo_examen
            WHERE id_tipo_examen = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return TipoExamen(**dict(row))
        return None

    async def get_by_codigo(self, conn, codigo: str) -> Optional[TipoExamen]:
        query = """
            SELECT id_tipo_examen, nombre, descripcion, codigo_interno,
                   requiere_ayuno, tiempo_estimado, observaciones
            FROM tipo_examen
            WHERE codigo_interno = $1;
        """
        row = await conn.fetchrow(query, codigo)
        if row:
            return TipoExamen(**dict(row))
        return None

    async def create(self, conn, tipo: TipoExamen) -> TipoExamen:
        query = """
            INSERT INTO tipo_examen (nombre, descripcion, codigo_interno, requiere_ayuno, tiempo_estimado, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_tipo_examen;
        """
        id_tipo_examen = await conn.fetchval(
            query,
            tipo.nombre,
            tipo.descripcion,
            tipo.codigo_interno,
            tipo.requiere_ayuno,
            tipo.tiempo_estimado,
            tipo.observaciones
        )
        tipo.id_tipo_examen = id_tipo_examen
        return tipo

    async def update(self, conn, id: int, data: dict) -> Optional[TipoExamen]:
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
            UPDATE tipo_examen 
            SET {', '.join(set_clauses)} 
            WHERE id_tipo_examen = ${idx} 
            RETURNING id_tipo_examen, nombre, descripcion, codigo_interno, requiere_ayuno, tiempo_estimado, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return TipoExamen(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM tipo_examen WHERE id_tipo_examen = $1 RETURNING id_tipo_examen;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None
