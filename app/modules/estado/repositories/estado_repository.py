from typing import List, Optional
from app.modules.estado.entities.estado_entity import Estado
from app.core.exceptions import ConflictError, NotFoundError


class EstadoRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Estado]:
        query = """
            SELECT id_estado, nombre, descripcion
            FROM estado
            ORDER BY id_estado;
        """
        rows = await conn.fetch(query)
        return [Estado(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Estado]:
        query = """
            SELECT id_estado, nombre, descripcion
            FROM estado
            WHERE id_estado = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Estado(**dict(row))
        return None

    async def get_by_nombre(self, conn, nombre: str) -> Optional[Estado]:
        query = """
            SELECT id_estado, nombre, descripcion
            FROM estado
            WHERE nombre = $1;
        """
        row = await conn.fetchrow(query, nombre)
        if row:
            return Estado(**dict(row))
        return None
