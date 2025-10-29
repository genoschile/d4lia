from typing import List

from app.domain.encuesta_entity import Encuesta
from app.interfaces.encuesta_interfaces import IEncuestaRepository

class EncuestaService:
    def __init__(self, encuesta_repo: IEncuestaRepository):
        self.encuesta_repo = encuesta_repo

    async def create_encuesta(self, encuesta: Encuesta) -> Encuesta:
        return await self.encuesta_repo.create(encuesta)

    async def get_all_encuestas(self) -> List[Encuesta]:
        return await self.encuesta_repo.get_all()
