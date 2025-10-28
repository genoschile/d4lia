from app.database.database import fetch_query
from app.domain.sillon import Sillon
from interfaces.sillon_interfaces import ISillonRepository


class SillonRepository(ISillonRepository):
    def __init__(self, conn):
        """
        Recibe una conexión asyncpg.Connection.
        Esto hace que el repositorio sea testeable y no dependa del pool global.
        """
        self.conn = conn

    async def create(self, sillon: Sillon) -> Sillon:
        query = """
            INSERT INTO sillon (ubicacion_sala, estado, observaciones)
            VALUES ($1, $2, $3)
            RETURNING id, ubicacion_sala, estado, observaciones
        """
        row = await self.conn.fetchrow(
            query,
            sillon.ubicacion_sala,
            sillon.estado,
            sillon.observaciones,
        )
        return Sillon(**dict(row)) if row else None # type: ignore

    async def get_all(self) -> list[Sillon]:
        query = "SELECT id, ubicacion_sala, estado, observaciones FROM sillon"
        rows = await self.conn.fetch(query)
        return [Sillon(**dict(r)) for r in rows]

    async def update(self, sillon_id: int, sillon: Sillon) -> Sillon | None:
        query = """
            UPDATE sillon
            SET ubicacion_sala = $1,
                estado = $2,
                observaciones = $3
            WHERE id = $4
            RETURNING id, ubicacion_sala, estado, observaciones
        """
        row = await self.conn.fetchrow(
            query,
            sillon.ubicacion_sala,
            sillon.estado,
            sillon.observaciones,
            sillon_id,
        )
        return Sillon(**dict(row)) if row else None

    async def delete(self, sillon_id: int) -> bool:
        query = "DELETE FROM sillon WHERE id = $1"
        result = await self.conn.execute(query, sillon_id)
        # asyncpg devuelve algo como "DELETE 1"
        return result.startswith("DELETE")
