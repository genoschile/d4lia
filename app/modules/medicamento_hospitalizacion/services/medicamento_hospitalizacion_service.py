from typing import List
from app.modules.medicamento_hospitalizacion.repositories.medicamento_hospitalizacion_repository import MedicamentoHospitalizacionRepository
from app.modules.medicamento_hospitalizacion.schemas.medicamento_hospitalizacion_schema import (
    MedicamentoHospitalizacionResponse,
    MedicamentoHospitalizacionCreate,
    MedicamentoHospitalizacionDetailed,
)
from app.modules.medicamento_hospitalizacion.entities.medicamento_hospitalizacion_entity import MedicamentoHospitalizacion
from app.core.exceptions import ConflictError, NotFoundError


class MedicamentoHospitalizacionService:
    def __init__(
        self, 
        pool, 
        repo: MedicamentoHospitalizacionRepository,
        hospitalizacion_repo,
        medicamento_repo
    ):
        self.pool = pool
        self.repo = repo
        self.hospitalizacion_repo = hospitalizacion_repo
        self.medicamento_repo = medicamento_repo

    async def list_all(self) -> List[MedicamentoHospitalizacionResponse]:
        async with self.pool.acquire() as conn:
            items = await self.repo.list_all(conn)
            return [MedicamentoHospitalizacionResponse.model_validate(i) for i in items]

    async def create(self, data: MedicamentoHospitalizacionCreate) -> MedicamentoHospitalizacionResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de hospitalización
            hosp = await self.hospitalizacion_repo.get_by_id(conn, data.id_hospitalizacion)
            if not hosp:
                raise NotFoundError(f"Hospitalización con ID {data.id_hospitalizacion} no encontrada")
            
            # Validar existencia de medicamento
            med = await self.medicamento_repo.get_by_id(conn, data.id_medicamento)
            if not med:
                raise NotFoundError(f"Medicamento con ID {data.id_medicamento} no encontrado")
            
            # Verificar duplicados
            if await self.repo.exists(conn, data.id_hospitalizacion, data.id_medicamento):
                raise ConflictError("Este medicamento ya está asignado a esta hospitalización")
            
            entity = MedicamentoHospitalizacion(
                id_hospitalizacion=data.id_hospitalizacion,
                id_medicamento=data.id_medicamento,
                id_profesional=data.id_profesional,
                dosis=data.dosis,
                frecuencia=data.frecuencia,
                via_administracion=data.via_administracion,
                duracion=data.duracion,
                observaciones=data.observaciones,
            )
            created = await self.repo.create(conn, entity)
            return MedicamentoHospitalizacionResponse.model_validate(created)

    async def delete(self, id_hospitalizacion: int, id_medicamento: int):
        async with self.pool.acquire() as conn:
            deleted = await self.repo.delete(conn, id_hospitalizacion, id_medicamento)
            if not deleted:
                raise NotFoundError("Relación medicamento-hospitalización no encontrada")

    async def get_by_hospitalizacion(self, id_hospitalizacion: int) -> List[MedicamentoHospitalizacionDetailed]:
        async with self.pool.acquire() as conn:
            # Validar existencia de hospitalización
            hosp = await self.hospitalizacion_repo.get_by_id(conn, id_hospitalizacion)
            if not hosp:
                raise NotFoundError(f"Hospitalización con ID {id_hospitalizacion} no encontrada")
                
            items = await self.repo.get_by_hospitalizacion(conn, id_hospitalizacion)
            return [MedicamentoHospitalizacionDetailed(**i) for i in items]
