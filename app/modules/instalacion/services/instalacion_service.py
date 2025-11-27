from typing import List
from app.modules.instalacion.repositories.instalacion_repository import InstalacionRepository
from app.modules.instalacion.schemas.instalacion_schema import (
    InstalacionResponse,
    InstalacionCreate,
    InstalacionUpdate,
    TipoInstalacionEnum,
)
from app.modules.instalacion.entities.instalacion_entity import Instalacion
from app.core.exceptions import ConflictError, NotFoundError


class InstalacionService:
    def __init__(self, pool, instalacion_repo: InstalacionRepository):
        self.pool = pool
        self.instalacion_repo = instalacion_repo

    async def list_all(self) -> List[InstalacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.instalacion_repo.list_all(conn)
            return [InstalacionResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> InstalacionResponse:
        async with self.pool.acquire() as conn:
            item = await self.instalacion_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Instalación no encontrada")
            return InstalacionResponse.model_validate(item)

    async def create(self, data: InstalacionCreate) -> InstalacionResponse:
        async with self.pool.acquire() as conn:
            entity = Instalacion(
                id_instalacion=None,
                nombre=data.nombre,
                tipo=data.tipo.value,
                ubicacion=data.ubicacion,
                contacto=data.contacto,
                observaciones=data.observaciones,
            )
            created = await self.instalacion_repo.create(conn, entity)
            return InstalacionResponse.model_validate(created)

    async def update(self, id: int, data: InstalacionUpdate) -> InstalacionResponse:
        async with self.pool.acquire() as conn:
            existing = await self.instalacion_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Instalación no encontrada")
            
            update_data = data.model_dump(exclude_none=True)
            # Convertir enum a string si existe
            if 'tipo' in update_data and hasattr(update_data['tipo'], 'value'):
                update_data['tipo'] = update_data['tipo'].value
            
            updated = await self.instalacion_repo.update(conn, id, update_data)
            return InstalacionResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.instalacion_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Instalación no encontrada")

    async def get_by_tipo(self, tipo: TipoInstalacionEnum) -> List[InstalacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.instalacion_repo.get_by_tipo(conn, tipo.value)
            return [InstalacionResponse.model_validate(i) for i in items]
