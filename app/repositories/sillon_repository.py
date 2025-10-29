from typing import Optional
from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository


class SillonRepository(ISillonRepository):
    def __init__(self, pool):  # Recibe el pool
        self.pool = pool

    async def create(self, sillon: Sillon) -> Sillon:
        query = """
            INSERT INTO sillon (ubicacion_sala, estado, observaciones)
            VALUES ($1, $2, $3)
            RETURNING id_sillon, ubicacion_sala, estado, observaciones
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                sillon.ubicacion_sala,
                sillon.estado,
                sillon.observaciones,
            )
            return Sillon(**dict(row)) if row else None # type: ignore

    async def get_all(self):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id_sillon, ubicacion_sala, estado, observaciones FROM sillon ORDER BY id_sillon;"
            )
            return [Sillon(**dict(r)) for r in rows]

    async def update(self, sillon_id: int, sillon: Sillon) -> Optional[Sillon]:
        query = """
            UPDATE sillon
            SET ubicacion_sala = $1,
                estado = $2,
                observaciones = $3
            WHERE id_sillon = $4
            RETURNING id_sillon, ubicacion_sala, estado, observaciones
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                sillon.ubicacion_sala,
                sillon.estado,
                sillon.observaciones,
                sillon_id,
            )
            return Sillon(**dict(row)) if row else None

    async def delete(self, sillon_id: int) -> bool:
        query = "DELETE FROM sillon WHERE id_sillon = $1"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, sillon_id)
            return result.startswith("DELETE")
