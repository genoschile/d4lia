from typing import List, Optional
from app.domain.patologia_entity import Patologia
from app.interfaces.patologia_interfaces import IPatologiaRepository
import asyncpg

class PatologiaRepository(IPatologiaRepository):
    def __init__(self, conn: asyncpg.Connection):
        """
        Recibe una conexión asyncpg.Connection.
        Esto hace que el repositorio sea testeable y no dependa del pool global.
        """
        self.conn = conn

    async def create(self, patologia: Patologia) -> Patologia:
        row = await self.conn.fetchrow(
            """
            INSERT INTO patologia (nombre, descripcion)
            VALUES ($1, $2)
            RETURNING id, nombre, descripcion
            """,
            patologia.nombre,# type: ignore
            patologia.descripcion # type: ignore
        )
        return Patologia(**dict(row)) # type: ignore

    async def get_all(self) -> List[Patologia]:
        rows = await self.conn.fetch("SELECT id, nombre, descripcion FROM patologia")
        return [Patologia(**dict(row)) for row in rows]

    async def update(self, patologia_id: int, patologia: Patologia) -> Optional[Patologia]:
        row = await self.conn.fetchrow(
            """
            UPDATE patologia
            SET nombre=$1, descripcion=$2
            WHERE id=$3
            RETURNING id, nombre, descripcion
            """,
            patologia.nombre,# type: ignore
            patologia.descripcion, # type: ignore
            patologia_id
        )
        return Patologia(**dict(row)) if row else None

    async def delete(self, patologia_id: int) -> bool:
        result = await self.conn.execute(
            "DELETE FROM patologia WHERE id=$1",
            patologia_id
        )
        return result.startswith("DELETE")  # Devuelve True si se eliminó alguna fila
