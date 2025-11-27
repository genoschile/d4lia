from typing import List
from app.modules.orden_examen.repositories.orden_examen_repository import OrdenExamenRepository
from app.modules.orden_examen.schemas.orden_examen_schema import (
    OrdenExamenResponse,
    OrdenExamenCreate,
    OrdenExamenUpdate,
)
from app.modules.orden_examen.entities.orden_examen_entity import OrdenExamen
from app.core.exceptions import ConflictError, NotFoundError


class OrdenExamenService:
    def __init__(
        self, 
        pool, 
        orden_repo: OrdenExamenRepository,
        consulta_repo,
        paciente_repo,
        tipo_examen_repo
    ):
        self.pool = pool
        self.orden_repo = orden_repo
        self.consulta_repo = consulta_repo
        self.paciente_repo = paciente_repo
        self.tipo_examen_repo = tipo_examen_repo

    async def list_all(self) -> List[OrdenExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.orden_repo.list_all(conn)
            return [OrdenExamenResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> OrdenExamenResponse:
        async with self.pool.acquire() as conn:
            item = await self.orden_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Orden de examen no encontrada")
            return OrdenExamenResponse.model_validate(item)

    async def create(self, data: OrdenExamenCreate) -> OrdenExamenResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de consulta
            consulta = await self.consulta_repo.get_by_id(conn, data.id_consulta)
            if not consulta:
                raise NotFoundError(f"Consulta médica con ID {data.id_consulta} no encontrada")
            
            # Validar existencia de paciente
            paciente = await self.paciente_repo.get_by_id(conn, data.id_paciente)
            if not paciente:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            # Validar existencia de tipo de examen si se proporciona
            if data.id_tipo_examen:
                tipo = await self.tipo_examen_repo.get_by_id(conn, data.id_tipo_examen)
                if not tipo:
                    raise NotFoundError(f"Tipo de examen con ID {data.id_tipo_examen} no encontrado")
            
            entity = OrdenExamen(
                id_orden_examen=None,
                id_consulta=data.id_consulta,
                id_profesional=data.id_profesional,
                id_paciente=data.id_paciente,
                id_tipo_examen=data.id_tipo_examen,
                id_estado=data.id_estado,
                fecha=data.fecha,
                fecha_programada=data.fecha_programada,
                fecha_solicitada=data.fecha_solicitada,
                motivo=data.motivo,
                documento=data.documento,
                estado=data.estado.value,
            )
            created = await self.orden_repo.create(conn, entity)
            return OrdenExamenResponse.model_validate(created)

    async def update(self, id: int, data: OrdenExamenUpdate) -> OrdenExamenResponse:
        async with self.pool.acquire() as conn:
            existing = await self.orden_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Orden de examen no encontrada")
            
            # Validar tipo de examen si se actualiza
            if data.id_tipo_examen:
                tipo = await self.tipo_examen_repo.get_by_id(conn, data.id_tipo_examen)
                if not tipo:
                    raise NotFoundError(f"Tipo de examen con ID {data.id_tipo_examen} no encontrado")
            
            update_data = data.model_dump(exclude_none=True)
            if 'estado' in update_data and hasattr(update_data['estado'], 'value'):
                update_data['estado'] = update_data['estado'].value
            
            updated = await self.orden_repo.update(conn, id, update_data)
            return OrdenExamenResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.orden_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Orden de examen no encontrada")

    async def get_by_paciente(self, id_paciente: int) -> List[OrdenExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.orden_repo.get_by_paciente(conn, id_paciente)
            return [OrdenExamenResponse.model_validate(i) for i in items]

    async def get_by_consulta(self, id_consulta: int) -> List[OrdenExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.orden_repo.get_by_consulta(conn, id_consulta)
            return [OrdenExamenResponse.model_validate(i) for i in items]
