from app.domain.patologia import Patologia
from app.interfaces.patologia_interfaces import IPatologiaRepository


class PatologiaService:
    def __init__(self, patologia_repo: IPatologiaRepository):
        self.patologia_repo = patologia_repo

    async def create_patologia(self, patologia: Patologia):
        return await self.patologia_repo.create(patologia)

    async def get_all_patologias(self):
        return await self.patologia_repo.get_all()

    async def update_patologia(self, patologia_id: int, patologia: Patologia):
        return await self.patologia_repo.update(patologia_id, patologia)

    async def delete_patologia(self, patologia_id: int):
        return await self.patologia_repo.delete(patologia_id)
