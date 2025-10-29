from typing import Optional
from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository
from app.repositories.sillon_repository import SillonRepository


class SillonService:
    def __init__(self, sillon_repo: ISillonRepository):
        self.sillon_repo = sillon_repo

    async def create_sillon(self, sillon_data: dict) -> Sillon:
        sillon = Sillon(**sillon_data)
        return await self.sillon_repo.create(sillon)

    async def get_all_sillones(self) -> list[Sillon]:
        return await self.sillon_repo.get_all()

    async def update_sillon(self, sillon_id: int, sillon_data: dict) -> Optional[Sillon]:
        sillon = Sillon(**sillon_data)
        return await self.sillon_repo.update(sillon_id, sillon)

    async def delete_sillon(self, sillon_id: int) -> bool:
        return await self.sillon_repo.delete(sillon_id)
