from typing import Optional
from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository


class SillonRepository(ISillonRepository):
    def __init__(self, pool):
        self.pool = pool

    async def get_all(self, conn) -> list[Sillon]:
        query = """
            SELECT id_sillon, ubicacion_sala, estado, observaciones
            FROM sillon
            ORDER BY id_sillon;
        """
        rows = await conn.fetch(query)
        return [Sillon(**dict(r)) for r in rows]
