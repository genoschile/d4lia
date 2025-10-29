# app/services/sesion_service.py
from typing import List, Optional
from app.domain.sesion_entity import Sesion
from app.interfaces.sesion_interfaces import ISesionRepository

class SesionService:
    def __init__(self, sesion_repo: ISesionRepository):
        self.sesion_repo = sesion_repo

    async def create_sesion(self, sesion: Sesion) -> Sesion:
        return await self.sesion_repo.create(sesion)

    async def get_all_sesiones(self) -> List[Sesion]:
        return await self.sesion_repo.get_all()

    async def get_sesion_by_id(self, sesion_id: int) -> Optional[Sesion]:
        sesiones = await self.sesion_repo.get_all()
        for s in sesiones:
            if s.id == sesion_id: # type: ignore
                return s
        return None

    async def update_sesion(self, sesion_id: int, sesion: Sesion) -> Optional[Sesion]:
        return await self.sesion_repo.update(sesion_id, sesion)

    async def delete_sesion(self, sesion_id: int) -> bool:
        return await self.sesion_repo.delete(sesion_id)
