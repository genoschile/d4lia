from typing import List
from app.modules.cie10_ges.repositories.cie10_ges_repository import Cie10GesRepository
from app.modules.cie10_ges.schemas.cie10_ges_schema import (
    Cie10GesResponse,
    Cie10GesCreate,
    Cie10GesDetailed,
)
from app.modules.cie10_ges.entities.cie10_ges_entity import Cie10Ges
from app.core.exceptions import ConflictError, NotFoundError


class Cie10GesService:
    def __init__(
        self, 
        pool, 
        cie10_ges_repo: Cie10GesRepository,
        cie10_repo,
        ges_repo
    ):
        self.pool = pool
        self.cie10_ges_repo = cie10_ges_repo
        self.cie10_repo = cie10_repo
        self.ges_repo = ges_repo

    async def create(self, data: Cie10GesCreate) -> Cie10GesResponse:
        async with self.pool.acquire() as conn:
            # Verificar que CIE10 existe
            cie10 = await self.cie10_repo.get_by_id(conn, data.id_cie10)
            if not cie10:
                raise NotFoundError(f"CIE-10 con ID {data.id_cie10} no encontrado")
            
            # Verificar que GES existe
            ges = await self.ges_repo.get_by_id(conn, data.id_ges)
            if not ges:
                raise NotFoundError(f"GES con ID {data.id_ges} no encontrado")
            
            # Verificar que no exista ya la relación
            exists = await self.cie10_ges_repo.exists(conn, data.id_cie10, data.id_ges)
            if exists:
                raise ConflictError("La relación ya existe")
            
            entity = Cie10Ges(
                id_cie10=data.id_cie10,
                id_ges=data.id_ges
            )
            created = await self.cie10_ges_repo.create(conn, entity)
            return Cie10GesResponse.model_validate(created)

    async def delete(self, id_cie10: int, id_ges: int):
        async with self.pool.acquire() as conn:
            exists = await self.cie10_ges_repo.exists(conn, id_cie10, id_ges)
            if not exists:
                raise NotFoundError("La relación no existe")
            
            deleted = await self.cie10_ges_repo.delete(conn, id_cie10, id_ges)
            if not deleted:
                raise NotFoundError("No se pudo eliminar la relación")

    async def get_ges_by_cie10(self, id_cie10: int) -> List[Cie10GesDetailed]:
        async with self.pool.acquire() as conn:
            # Verificar que CIE10 existe
            cie10 = await self.cie10_repo.get_by_id(conn, id_cie10)
            if not cie10:
                raise NotFoundError(f"CIE-10 con ID {id_cie10} no encontrado")
            
            items = await self.cie10_ges_repo.get_ges_by_cie10(conn, id_cie10)
            return [Cie10GesDetailed(**i) for i in items]

    async def get_cie10_by_ges(self, id_ges: int) -> List[Cie10GesDetailed]:
        async with self.pool.acquire() as conn:
            # Verificar que GES existe
            ges = await self.ges_repo.get_by_id(conn, id_ges)
            if not ges:
                raise NotFoundError(f"GES con ID {id_ges} no encontrado")
            
            items = await self.cie10_ges_repo.get_cie10_by_ges(conn, id_ges)
            return [Cie10GesDetailed(**i) for i in items]

    async def list_all(self) -> List[Cie10GesDetailed]:
        async with self.pool.acquire() as conn:
            items = await self.cie10_ges_repo.list_all(conn)
            return [Cie10GesDetailed(**i) for i in items]
