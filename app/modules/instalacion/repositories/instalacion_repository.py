from typing import List, Optional
from app.modules.instalacion.entities.instalacion_entity import Instalacion
from app.modules.instalacion.schemas.instalacion_schema import InstalacionCreate, InstalacionUpdate
from app.core.exceptions import ConflictError, NotFoundError


class InstalacionRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Instalacion]:
        query = """
            SELECT id_instalacion, nombre, tipo, ubicacion, contacto, observaciones
            FROM instalacion
            ORDER BY nombre;
        """
        rows = await conn.fetch(query)
        return [Instalacion(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Instalacion]:
        query = """
            SELECT id_instalacion, nombre, tipo, ubicacion, contacto, observaciones
            FROM instalacion
            WHERE id_instalacion = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Instalacion(**dict(row))
        return None

    async def create(self, conn, instalacion: Instalacion) -> Instalacion:
        query = """
            INSERT INTO instalacion (nombre, tipo, ubicacion, contacto, observaciones)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id_instalacion;
        """
        id_instalacion = await conn.fetchval(
            query,
            instalacion.nombre,
            instalacion.tipo,
            instalacion.ubicacion,
            instalacion.contacto,
            instalacion.observaciones
        )
        instalacion.id_instalacion = id_instalacion
        return instalacion

    async def update(self, conn, id: int, data: dict) -> Optional[Instalacion]:
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
            UPDATE instalacion 
            SET {', '.join(set_clauses)} 
            WHERE id_instalacion = ${idx} 
            RETURNING id_instalacion, nombre, tipo, ubicacion, contacto, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Instalacion(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM instalacion WHERE id_instalacion = $1 RETURNING id_instalacion;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_tipo(self, conn, tipo: str) -> List[Instalacion]:
        query = """
            SELECT id_instalacion, nombre, tipo, ubicacion, contacto, observaciones
            FROM instalacion
            WHERE tipo = $1
            ORDER BY nombre;
        """
        rows = await conn.fetch(query, tipo)
        return [Instalacion(**dict(row)) for row in rows]
