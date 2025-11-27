from typing import List
from app.modules.cie10.repositories.cie10_repository import Cie10Repository
from app.modules.cie10.schemas.cie10_schema import (
    Cie10Response,
    Cie10Create,
    Cie10Update,
)
from app.modules.cie10.entities.cie10_entity import Cie10
from app.core.exceptions import ConflictError, NotFoundError


class Cie10Service:
    def __init__(self, pool, cie10_repo: Cie10Repository):
        self.pool = pool
        self.cie10_repo = cie10_repo

    async def list_all(self) -> List[Cie10Response]:
        async with self.pool.acquire() as conn:
            items = await self.cie10_repo.list_all(conn)
            return [Cie10Response.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> Cie10Response:
        async with self.pool.acquire() as conn:
            item = await self.cie10_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Código CIE-10 no encontrado")
            return Cie10Response.model_validate(item)

    async def create(self, data: Cie10Create) -> Cie10Response:
        async with self.pool.acquire() as conn:
            # Verificar duplicados por código
            existing = await self.cie10_repo.get_by_codigo(conn, data.codigo)
            if existing:
                raise ConflictError(f"El código CIE-10 '{data.codigo}' ya existe")
            
            entity = Cie10(
                id_cie10=None,
                codigo=data.codigo,
                nombre=data.nombre,
                categoria=data.categoria,
                descripcion=data.descripcion,
                activo=data.activo,
            )
            created = await self.cie10_repo.create(conn, entity)
            return Cie10Response.model_validate(created)

    async def update(self, id: int, data: Cie10Update) -> Cie10Response:
        async with self.pool.acquire() as conn:
            existing = await self.cie10_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Código CIE-10 no encontrado")
            
            if data.codigo:
                code_exists = await self.cie10_repo.get_by_codigo(conn, data.codigo)
                if code_exists and code_exists.id_cie10 != id:
                    raise ConflictError(f"El código CIE-10 '{data.codigo}' ya existe")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.cie10_repo.update(conn, id, update_data)
            return Cie10Response.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.cie10_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Código CIE-10 no encontrado")

    async def search(self, term: str) -> List[Cie10Response]:
        async with self.pool.acquire() as conn:
            items = await self.cie10_repo.search(conn, term)
            return [Cie10Response.model_validate(i) for i in items]
