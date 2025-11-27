from typing import List
from app.modules.hospitalizacion.repositories.hospitalizacion_repository import HospitalizacionRepository
from app.modules.hospitalizacion.schemas.hospitalizacion_schema import (
    HospitalizacionResponse,
    HospitalizacionCreate,
    HospitalizacionUpdate,
)
from app.modules.hospitalizacion.entities.hospitalizacion_entity import Hospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class HospitalizacionService:
    def __init__(
        self, 
        pool, 
        hospitalizacion_repo: HospitalizacionRepository,
        orden_repo,
        paciente_repo
    ):
        self.pool = pool
        self.hospitalizacion_repo = hospitalizacion_repo
        self.orden_repo = orden_repo
        self.paciente_repo = paciente_repo

    async def list_all(self) -> List[HospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.hospitalizacion_repo.list_all(conn)
            return [HospitalizacionResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> HospitalizacionResponse:
        async with self.pool.acquire() as conn:
            item = await self.hospitalizacion_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Hospitalización no encontrada")
            return HospitalizacionResponse.model_validate(item)

    async def create(self, data: HospitalizacionCreate) -> HospitalizacionResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de orden
            orden = await self.orden_repo.get_by_id(conn, data.id_orden_hospitalizacion)
            if not orden:
                raise NotFoundError(f"Orden de hospitalización con ID {data.id_orden_hospitalizacion} no encontrada")
            
            # Validar existencia de paciente
            paciente = await self.paciente_repo.get_by_id(conn, data.id_paciente)
            if not paciente:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            entity = Hospitalizacion(
                id_hospitalizacion=None,
                id_orden_hospitalizacion=data.id_orden_hospitalizacion,
                id_paciente=data.id_paciente,
                id_profesional=data.id_profesional,
                fecha_ingreso=data.fecha_ingreso,
                fecha_alta=data.fecha_alta,
                habitacion=data.habitacion,
                observacion=data.observacion,
                estado=data.estado.value,
            )
            created = await self.hospitalizacion_repo.create(conn, entity)
            return HospitalizacionResponse.model_validate(created)

    async def update(self, id: int, data: HospitalizacionUpdate) -> HospitalizacionResponse:
        async with self.pool.acquire() as conn:
            existing = await self.hospitalizacion_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Hospitalización no encontrada")
            
            update_data = data.model_dump(exclude_none=True)
            if 'estado' in update_data and hasattr(update_data['estado'], 'value'):
                update_data['estado'] = update_data['estado'].value
            
            updated = await self.hospitalizacion_repo.update(conn, id, update_data)
            return HospitalizacionResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.hospitalizacion_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Hospitalización no encontrada")

    async def get_by_paciente(self, id_paciente: int) -> List[HospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.hospitalizacion_repo.get_by_paciente(conn, id_paciente)
            return [HospitalizacionResponse.model_validate(i) for i in items]

    async def get_activas(self) -> List[HospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.hospitalizacion_repo.get_activas(conn)
            return [HospitalizacionResponse.model_validate(i) for i in items]
