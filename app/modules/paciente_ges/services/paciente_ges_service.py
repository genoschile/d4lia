from typing import List, Optional
from app.modules.paciente_ges.repositories.paciente_ges_repository import PacienteGesRepository
from app.modules.paciente_ges.interfaces.paciente_ges_service_interface import PacienteGesServiceInterface
from app.modules.paciente_ges.schemas.paciente_ges_schema import (
    PacienteGesCreate,
    PacienteGesUpdate,
    PacienteGesResponse,
    PacienteGesCountdownResponse,
    PacienteGesEstadisticas
)
from app.modules.paciente_ges.entities.paciente_ges_entity import PacienteGes
from app.modules.paciente.interfaces.paciente_interfaces import IPacienteRepository
from app.modules.ges.repositories.ges_repository import GesRepository
from app.modules.diagnostico.interfaces.diagnostico_interfaces import IDiagnosticoRepository
from app.core.exceptions import NotFoundError, ConflictError


class PacienteGesService(PacienteGesServiceInterface):
    def __init__(
        self, 
        pool, 
        paciente_ges_repo: PacienteGesRepository,
        paciente_repo: IPacienteRepository,
        ges_repo: GesRepository,
        diagnostico_repo: IDiagnosticoRepository
    ):
        self.pool = pool
        self.paciente_ges_repo = paciente_ges_repo
        self.paciente_repo = paciente_repo
        self.ges_repo = ges_repo
        self.diagnostico_repo = diagnostico_repo

    async def list_all(self) -> List[PacienteGesResponse]:
        async with self.pool.acquire() as conn:
            items = await self.paciente_ges_repo.list_all(conn)
            return [PacienteGesResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> PacienteGesResponse:
        async with self.pool.acquire() as conn:
            item = await self.paciente_ges_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Registro GES de paciente no encontrado")
            return PacienteGesResponse.model_validate(item)

    async def create(self, data: PacienteGesCreate) -> PacienteGesResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de paciente
            paciente = await self.paciente_repo.get_by_id(conn, data.id_paciente)
            if not paciente:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            # Validar existencia de GES
            ges = await self.ges_repo.get_by_id(conn, data.id_ges)
            if not ges:
                raise NotFoundError(f"GES con ID {data.id_ges} no encontrado")
            
            # Validar existencia de diagnóstico si se proporciona
            if data.id_diagnostico:
                diagnostico = await self.diagnostico_repo.get_by_id(conn, data.id_diagnostico)
                if not diagnostico:
                    raise NotFoundError(f"Diagnóstico con ID {data.id_diagnostico} no encontrado")

            # Calcular días límite si no se proporciona
            dias_limite = data.dias_limite
            if dias_limite is None:
                # Si hay diagnóstico -> Etapa de tratamiento
                if data.id_diagnostico:
                    dias_limite = ges.dias_limite_tratamiento
                # Si no hay diagnóstico -> Etapa de diagnóstico (sospecha)
                else:
                    dias_limite = ges.dias_limite_diagnostico
                
                if dias_limite is None:
                     # Fallback por si el GES no tiene configurados los días (aunque debería)
                     dias_limite = 30 # Valor por defecto seguro o lanzar error
            
            # Verificar si ya existe un GES activo para este paciente y patología
            # (Opcional: dependerá de si permitimos múltiples activaciones, 
            # pero la constraint unique en DB lo validará por fecha)
            
            entity = PacienteGes(
                id_paciente=data.id_paciente,
                id_ges=data.id_ges,
                dias_limite=dias_limite,
                id_diagnostico=data.id_diagnostico,
                fecha_activacion=data.fecha_activacion,
                estado=data.estado,
                tipo_cobertura=data.tipo_cobertura,
                activado_por=data.activado_por,
                observaciones=data.observaciones
            )
            
            try:
                created = await self.paciente_ges_repo.create(conn, entity)
                return PacienteGesResponse.model_validate(created)
            except Exception as e:
                # Capturar error de unicidad si es necesario
                if "unique_paciente_ges_activacion" in str(e):
                    raise ConflictError("Ya existe una activación GES para este paciente y patología en la misma fecha")
                raise e

    async def update(self, id: int, data: PacienteGesUpdate) -> PacienteGesResponse:
        async with self.pool.acquire() as conn:
            existing = await self.paciente_ges_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Registro GES de paciente no encontrado")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.paciente_ges_repo.update(conn, id, update_data)
            return PacienteGesResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.paciente_ges_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Registro GES de paciente no encontrado")

    async def get_by_paciente(self, id_paciente: int) -> List[PacienteGesResponse]:
        async with self.pool.acquire() as conn:
            items = await self.paciente_ges_repo.get_by_paciente(conn, id_paciente)
            return [PacienteGesResponse.model_validate(i) for i in items]

    async def get_activos_by_paciente(self, id_paciente: int) -> List[PacienteGesResponse]:
        async with self.pool.acquire() as conn:
            items = await self.paciente_ges_repo.get_activos_by_paciente(conn, id_paciente)
            return [PacienteGesResponse.model_validate(i) for i in items]

    async def get_countdown_view(self, filtro_estado: Optional[str] = None) -> List[PacienteGesCountdownResponse]:
        async with self.pool.acquire() as conn:
            items = await self.paciente_ges_repo.get_countdown_view(conn, filtro_estado)
            return [PacienteGesCountdownResponse.model_validate(i) for i in items]

    async def get_estadisticas(self) -> PacienteGesEstadisticas:
        async with self.pool.acquire() as conn:
            stats = await self.paciente_ges_repo.get_estadisticas(conn)
            return PacienteGesEstadisticas.model_validate(stats)
