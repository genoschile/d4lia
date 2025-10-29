from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository


class SillonService:
    def __init__(self, pool, sillon_repo: ISillonRepository):
        self.pool = pool
        self.sillon_repo = sillon_repo

    async def get_all_sillones(self) -> list[Sillon]:
        async with self.pool.acquire() as conn:
            sillones = await self.sillon_repo.get_all(conn)
            return sillones
