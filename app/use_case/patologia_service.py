from app.domain.patologia_entity import Patologia
from app.interfaces.patologia_interfaces import IPatologiaRepository


class PatologiaService:
    def __init__(self, pool, patologia_repo: IPatologiaRepository):
        self.pool = pool
        self.patologia_repo = patologia_repo

    async def create_patologia(self, patologia: Patologia) -> Patologia:
        async with self.pool.acquire() as conn:
            return await self.patologia_repo.create(conn, patologia)

    async def get_all_patologias(self) -> list[Patologia]:
        async with self.pool.acquire() as conn:
            return await self.patologia_repo.get_all(conn)

    async def get_patologia_by_id(self, id_patologia: int) -> Patologia | None:
        async with self.pool.acquire() as conn:
            return await self.patologia_repo.get_by_id(conn, id_patologia)

    async def delete_patologia(self, id_patologia: int) -> bool:
        async with self.pool.acquire() as conn:
            eliminado = await self.patologia_repo.delete(conn, id_patologia)
            return eliminado

    async def update_patologia(self, id_patologia: int, data: dict) -> bool:
        async with self.pool.acquire() as conn:
            return await self.patologia_repo.update(conn, id_patologia, data)
