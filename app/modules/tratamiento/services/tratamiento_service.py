from typing import List
from app.modules.tratamiento.interfaces.tratamiento_interfaces import ITratamientoRepository
from app.modules.tratamiento.schemas.tratamiento_schema import (
    TratamientoResponse,
    TratamientoCreate,
    TratamientoUpdate,
)
from app.modules.tratamiento.entities.tratamiento_entity import Tratamiento
from app.core.exceptions import ConflictError, NotFoundError


class TratamientoService:
    def __init__(self, pool, tratamiento_repo: ITratamientoRepository):
        self.pool = pool
        self.tratamiento_repo = tratamiento_repo

    async def list_all(self) -> List[TratamientoResponse]:
        async with self.pool.acquire() as conn:
            tratamientos = await self.tratamiento_repo.list_all(conn)
            return [TratamientoResponse.model_validate(t) for t in tratamientos]

    async def get_by_id(self, id: int) -> TratamientoResponse:
        async with self.pool.acquire() as conn:
            tratamiento = await self.tratamiento_repo.get_by_id(conn, id)
            if not tratamiento:
                raise NotFoundError("Tratamiento no encontrado")
            return TratamientoResponse.model_validate(tratamiento)

    async def create(self, data: TratamientoCreate) -> TratamientoResponse:
        # Verificar si ya existe un tratamiento con el mismo nombre
        async with self.pool.acquire() as conn:
            existing = await self.tratamiento_repo.get_by_nombre(conn, data.nombre_tratamiento)
            if existing:
                raise ConflictError(f"Ya existe un tratamiento con el nombre '{data.nombre_tratamiento}'")
        
        tratamiento_ent = Tratamiento(
            id_tratamiento=None,
            nombre_tratamiento=data.nombre_tratamiento,
            descripcion=data.descripcion,
            duracion_estimada=data.duracion_estimada,
            costo_aprox=data.costo_aprox,
            observaciones=data.observaciones,
        )
        async with self.pool.acquire() as conn:
            created = await self.tratamiento_repo.create(conn, tratamiento_ent)
            return TratamientoResponse.model_validate(created)

    async def update(self, id: int, data: TratamientoUpdate) -> TratamientoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe
            existing = await self.tratamiento_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Tratamiento no encontrado")
            
            # Si se está actualizando el nombre, verificar que no exista otro con ese nombre
            if data.nombre_tratamiento:
                nombre_exists = await self.tratamiento_repo.get_by_nombre(conn, data.nombre_tratamiento)
                if nombre_exists and nombre_exists.id_tratamiento != id:
                    raise ConflictError(f"Ya existe otro tratamiento con el nombre '{data.nombre_tratamiento}'")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.tratamiento_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Tratamiento no encontrado")
            return TratamientoResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.tratamiento_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Tratamiento no encontrado")
