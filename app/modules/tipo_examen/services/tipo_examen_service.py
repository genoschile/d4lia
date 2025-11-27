from typing import List
from app.modules.tipo_examen.repositories.tipo_examen_repository import TipoExamenRepository
from app.modules.tipo_examen.schemas.tipo_examen_schema import (
    TipoExamenResponse,
    TipoExamenCreate,
    TipoExamenUpdate,
)
from app.modules.tipo_examen.entities.tipo_examen_entity import TipoExamen
from app.core.exceptions import ConflictError, NotFoundError


class TipoExamenService:
    def __init__(self, pool, tipo_examen_repo: TipoExamenRepository):
        self.pool = pool
        self.tipo_examen_repo = tipo_examen_repo

    async def list_all(self) -> List[TipoExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.tipo_examen_repo.list_all(conn)
            return [TipoExamenResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> TipoExamenResponse:
        async with self.pool.acquire() as conn:
            item = await self.tipo_examen_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Tipo de examen no encontrado")
            return TipoExamenResponse.model_validate(item)

    async def create(self, data: TipoExamenCreate) -> TipoExamenResponse:
        async with self.pool.acquire() as conn:
            # Verificar duplicados por código si existe
            if data.codigo_interno:
                existing = await self.tipo_examen_repo.get_by_codigo(conn, data.codigo_interno)
                if existing:
                    raise ConflictError(f"El código interno '{data.codigo_interno}' ya existe")
            
            entity = TipoExamen(
                id_tipo_examen=None,
                nombre=data.nombre,
                descripcion=data.descripcion,
                codigo_interno=data.codigo_interno,
                requiere_ayuno=data.requiere_ayuno,
                tiempo_estimado=data.tiempo_estimado,
                observaciones=data.observaciones,
            )
            created = await self.tipo_examen_repo.create(conn, entity)
            return TipoExamenResponse.model_validate(created)

    async def update(self, id: int, data: TipoExamenUpdate) -> TipoExamenResponse:
        async with self.pool.acquire() as conn:
            existing = await self.tipo_examen_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Tipo de examen no encontrado")
            
            if data.codigo_interno:
                code_exists = await self.tipo_examen_repo.get_by_codigo(conn, data.codigo_interno)
                if code_exists and code_exists.id_tipo_examen != id:
                    raise ConflictError(f"El código interno '{data.codigo_interno}' ya existe")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.tipo_examen_repo.update(conn, id, update_data)
            return TipoExamenResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.tipo_examen_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Tipo de examen no encontrado")
