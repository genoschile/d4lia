from typing import List
from app.modules.tratamiento_hospitalizacion.repositories.tratamiento_hospitalizacion_repository import TratamientoHospitalizacionRepository
from app.modules.tratamiento_hospitalizacion.schemas.tratamiento_hospitalizacion_schema import (
    TratamientoHospitalizacionResponse,
    TratamientoHospitalizacionCreate,
    TratamientoHospitalizacionDetailed,
)
from app.modules.tratamiento_hospitalizacion.entities.tratamiento_hospitalizacion_entity import TratamientoHospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class TratamientoHospitalizacionService:
    def __init__(
        self, 
        pool, 
        repo: TratamientoHospitalizacionRepository,
        hospitalizacion_repo,
        tratamiento_repo
    ):
        self.pool = pool
        self.repo = repo
        self.hospitalizacion_repo = hospitalizacion_repo
        self.tratamiento_repo = tratamiento_repo

    async def list_all(self) -> List[TratamientoHospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.repo.list_all(conn)
            return [TratamientoHospitalizacionResponse.model_validate(i) for i in items]

    async def create(self, data: TratamientoHospitalizacionCreate) -> TratamientoHospitalizacionResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de hospitalización
            hosp = await self.hospitalizacion_repo.get_by_id(conn, data.id_hospitalizacion)
            if not hosp:
                raise NotFoundError(f"Hospitalización con ID {data.id_hospitalizacion} no encontrada")
            
            # Validar existencia de tratamiento
            trat = await self.tratamiento_repo.get_by_id(conn, data.id_tratamiento)
            if not trat:
                raise NotFoundError(f"Tratamiento con ID {data.id_tratamiento} no encontrado")
            
            # Verificar duplicados
            if await self.repo.exists(conn, data.id_hospitalizacion, data.id_tratamiento):
                raise ConflictError("Este tratamiento ya está asignado a esta hospitalización")
            
            entity = TratamientoHospitalizacion(
                id_hospitalizacion=data.id_hospitalizacion,
                id_tratamiento=data.id_tratamiento,
                id_profesional=data.id_profesional,
                fecha_aplicacion=data.fecha_aplicacion,
                dosis=data.dosis,
                duracion=data.duracion,
                observaciones=data.observaciones,
            )
            created = await self.repo.create(conn, entity)
            return TratamientoHospitalizacionResponse.model_validate(created)

    async def delete(self, id_hospitalizacion: int, id_tratamiento: int):
        async with self.pool.acquire() as conn:
            deleted = await self.repo.delete(conn, id_hospitalizacion, id_tratamiento)
            if not deleted:
                raise NotFoundError("Relación tratamiento-hospitalización no encontrada")

    async def get_by_hospitalizacion(self, id_hospitalizacion: int) -> List[TratamientoHospitalizacionDetailed]:
        async with self.pool.acquire() as conn:
            # Validar existencia de hospitalización
            hosp = await self.hospitalizacion_repo.get_by_id(conn, id_hospitalizacion)
            if not hosp:
                raise NotFoundError(f"Hospitalización con ID {id_hospitalizacion} no encontrada")
                
            items = await self.repo.get_by_hospitalizacion(conn, id_hospitalizacion)
            return [TratamientoHospitalizacionDetailed(**i) for i in items]
