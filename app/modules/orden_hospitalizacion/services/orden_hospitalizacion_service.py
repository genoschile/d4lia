from typing import List
from app.modules.orden_hospitalizacion.repositories.orden_hospitalizacion_repository import OrdenHospitalizacionRepository
from app.modules.orden_hospitalizacion.schemas.orden_hospitalizacion_schema import (
    OrdenHospitalizacionResponse,
    OrdenHospitalizacionCreate,
    OrdenHospitalizacionUpdate,
)
from app.modules.orden_hospitalizacion.entities.orden_hospitalizacion_entity import OrdenHospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class OrdenHospitalizacionService:
    def __init__(
        self, 
        pool, 
        orden_repo: OrdenHospitalizacionRepository,
        paciente_repo
    ):
        self.pool = pool
        self.orden_repo = orden_repo
        self.paciente_repo = paciente_repo

    async def list_all(self) -> List[OrdenHospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.orden_repo.list_all(conn)
            return [OrdenHospitalizacionResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> OrdenHospitalizacionResponse:
        async with self.pool.acquire() as conn:
            item = await self.orden_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Orden de hospitalización no encontrada")
            return OrdenHospitalizacionResponse.model_validate(item)

    async def create(self, data: OrdenHospitalizacionCreate) -> OrdenHospitalizacionResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de paciente
            paciente = await self.paciente_repo.get_by_id(conn, data.id_paciente)
            if not paciente:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            entity = OrdenHospitalizacion(
                id_orden_hospitalizacion=None,
                id_paciente=data.id_paciente,
                id_profesional=data.id_profesional,
                fecha=data.fecha,
                motivo=data.motivo,
                documento=data.documento,
                estado=data.estado.value,
            )
            created = await self.orden_repo.create(conn, entity)
            return OrdenHospitalizacionResponse.model_validate(created)

    async def update(self, id: int, data: OrdenHospitalizacionUpdate) -> OrdenHospitalizacionResponse:
        async with self.pool.acquire() as conn:
            existing = await self.orden_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Orden de hospitalización no encontrada")
            
            update_data = data.model_dump(exclude_none=True)
            if 'estado' in update_data and hasattr(update_data['estado'], 'value'):
                update_data['estado'] = update_data['estado'].value
            
            updated = await self.orden_repo.update(conn, id, update_data)
            return OrdenHospitalizacionResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.orden_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Orden de hospitalización no encontrada")

    async def get_by_paciente(self, id_paciente: int) -> List[OrdenHospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.orden_repo.get_by_paciente(conn, id_paciente)
            return [OrdenHospitalizacionResponse.model_validate(i) for i in items]
