from typing import List
from datetime import date
from app.modules.consulta_medica.interfaces.consulta_medica_interfaces import (
    IConsultaMedicaRepository,
)
from app.modules.consulta_medica.schemas.consulta_medica_schema import (
    ConsultaMedicaResponse,
    ConsultaMedicaCreate,
    ConsultaMedicaUpdate,
)
from app.modules.consulta_medica.entities.consulta_medica_entity import ConsultaMedica
from app.core.exceptions import ConflictError, NotFoundError


class ConsultaMedicaService:
    def __init__(self, pool, consulta_repo: IConsultaMedicaRepository):
        self.pool = pool
        self.consulta_repo = consulta_repo

    async def list_all(self) -> List[ConsultaMedicaResponse]:
        async with self.pool.acquire() as conn:
            consultas = await self.consulta_repo.list_all(conn)
            return [ConsultaMedicaResponse.model_validate(c) for c in consultas]

    async def get_by_id(self, id: int) -> ConsultaMedicaResponse:
        async with self.pool.acquire() as conn:
            consulta = await self.consulta_repo.get_by_id(conn, id)
            if not consulta:
                raise NotFoundError("Consulta médica no encontrada")
            return ConsultaMedicaResponse.model_validate(consulta)

    async def create(self, data: ConsultaMedicaCreate) -> ConsultaMedicaResponse:
        # Ensure datetimes are naive
        fecha_programada = data.fecha_programada.replace(tzinfo=None) if data.fecha_programada else None
        fecha_atencion = data.fecha_atencion.replace(tzinfo=None) if data.fecha_atencion else None

        entity = ConsultaMedica(
            id_consulta=None,
            id_paciente=data.id_paciente,
            id_profesional=data.id_profesional,
            id_estado=data.id_estado,
            especialidad=data.especialidad,
            fecha=data.fecha,
            fecha_programada=fecha_programada,
            fecha_atencion=fecha_atencion,
            motivo=data.motivo,
            tratamiento=None,
            observaciones=data.observaciones,
        )
        async with self.pool.acquire() as conn:
            created = await self.consulta_repo.create(conn, entity)
            return ConsultaMedicaResponse.model_validate(created)

    async def update(self, id: int, data: ConsultaMedicaUpdate) -> ConsultaMedicaResponse:
        async with self.pool.acquire() as conn:
            update_data = data.model_dump(exclude_none=True)
            
            # Ensure datetimes are naive
            if 'fecha_programada' in update_data and update_data['fecha_programada']:
                update_data['fecha_programada'] = update_data['fecha_programada'].replace(tzinfo=None)
            if 'fecha_atencion' in update_data and update_data['fecha_atencion']:
                update_data['fecha_atencion'] = update_data['fecha_atencion'].replace(tzinfo=None)
            
            updated = await self.consulta_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Consulta médica no encontrada")
            return ConsultaMedicaResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.consulta_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Consulta médica no encontrada")

    async def get_by_paciente(self, id_paciente: int) -> List[ConsultaMedicaResponse]:
        async with self.pool.acquire() as conn:
            consultas = await self.consulta_repo.get_by_paciente(conn, id_paciente)
            return [ConsultaMedicaResponse.model_validate(c) for c in consultas]

    async def get_by_profesional(
        self, id_profesional: int
    ) -> List[ConsultaMedicaResponse]:
        async with self.pool.acquire() as conn:
            consultas = await self.consulta_repo.get_by_profesional(conn, id_profesional)
            return [ConsultaMedicaResponse.model_validate(c) for c in consultas]

    async def get_by_fecha_range(
        self, fecha_inicio: date, fecha_fin: date
    ) -> List[ConsultaMedicaResponse]:
        async with self.pool.acquire() as conn:
            consultas = await self.consulta_repo.get_by_fecha_range(
                conn, fecha_inicio, fecha_fin
            )
            return [ConsultaMedicaResponse.model_validate(c) for c in consultas]
