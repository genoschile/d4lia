from typing import List
from app.modules.ges.repositories.ges_repository import GesRepository
from app.modules.ges.schemas.ges_schema import (
    GesResponse,
    GesCreate,
    GesUpdate,
)
from app.modules.ges.entities.ges_entity import Ges
from app.core.exceptions import ConflictError, NotFoundError


class GesService:
    def __init__(self, pool, ges_repo: GesRepository):
        self.pool = pool
        self.ges_repo = ges_repo

    async def list_all(self) -> List[GesResponse]:
        async with self.pool.acquire() as conn:
            items = await self.ges_repo.list_all(conn)
            return [GesResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> GesResponse:
        async with self.pool.acquire() as conn:
            item = await self.ges_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Programa GES no encontrado")
            return GesResponse.model_validate(item)

    async def create(self, data: GesCreate) -> GesResponse:
        async with self.pool.acquire() as conn:
            # Verificar duplicados por código si existe
            if data.codigo_ges:
                existing = await self.ges_repo.get_by_codigo(conn, data.codigo_ges)
                if existing:
                    raise ConflictError(f"El código GES '{data.codigo_ges}' ya existe")
            
            entity = Ges(
                id_ges=None,
                codigo_ges=data.codigo_ges,
                nombre=data.nombre,
                descripcion=data.descripcion,
                cobertura=data.cobertura,
                dias_limite_diagnostico=data.dias_limite_diagnostico,
                dias_limite_tratamiento=data.dias_limite_tratamiento,
                requiere_fonasa=data.requiere_fonasa,
                vigente=data.vigente,
            )
            created = await self.ges_repo.create(conn, entity)
            return GesResponse.model_validate(created)

    async def update(self, id: int, data: GesUpdate) -> GesResponse:
        async with self.pool.acquire() as conn:
            existing = await self.ges_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Programa GES no encontrado")
            
            if data.codigo_ges:
                code_exists = await self.ges_repo.get_by_codigo(conn, data.codigo_ges)
                if code_exists and code_exists.id_ges != id:
                    raise ConflictError(f"El código GES '{data.codigo_ges}' ya existe")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.ges_repo.update(conn, id, update_data)
            return GesResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.ges_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Programa GES no encontrado")

    async def search(self, term: str) -> List[GesResponse]:
        async with self.pool.acquire() as conn:
            items = await self.ges_repo.search(conn, term)
            return [GesResponse.model_validate(i) for i in items]
