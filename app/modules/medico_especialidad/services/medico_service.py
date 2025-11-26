from typing import List, Optional
from app.modules.medico_especialidad.interfaces.medico_interfaces import (
    IMedicoRepository,
    IEspecialidadRepository,
)
from app.modules.medico_especialidad.schemas.medico_especialidad_schema import (
    MedicoResponse,
    MedicoCreate,
    EspecialidadDTO,
    VinculoProfesionalDTO,
    EspecialidadCreate,
)
from app.modules.medico_especialidad.entities.medico_especialidad_entity import (
    Medico,
    Rut,
    Especializacion,
)
from app.core.exceptions import ConflictError, NotFoundError


class MedicoService:
    def __init__(
        self,
        pool,
        medico_repo: IMedicoRepository,
        especialidad_repo: IEspecialidadRepository,
    ):
        self.pool = pool
        self.medico_repo = medico_repo
        self.especialidad_repo = especialidad_repo

    async def listar_medicos(self) -> list[MedicoResponse]:
        async with self.pool.acquire() as conn:
            medicos = await self.medico_repo.list_all(conn)
            response = []
            for medico in medicos:
                if medico.id_medico is None:
                    continue  # Skip doctors without ID (shouldn't happen)
                medico_resp = MedicoResponse.model_validate(medico)
                # Fetch specialties for each doctor
                specialties = await self.medico_repo.get_specialties_by_medico(
                    conn, medico.id_medico
                )
                medico_resp.especialidades = [
                    VinculoProfesionalDTO(
                        id_profesional=medico.id_medico,
                        especialidad=EspecialidadDTO.model_validate(s),
                        fecha_registro=None,
                    )
                    for s in specialties
                ]
                response.append(medico_resp)
            return response

    async def create_medico(self, medico_data: MedicoCreate) -> MedicoResponse:
        medico_ent = Medico(
            rut=Rut(medico_data.rut),
            nombre=medico_data.nombre,
            apellido=medico_data.apellido,
            sexo=medico_data.sexo,
        )
        async with self.pool.acquire() as conn:
            # Check if exists
            existing = await self.medico_repo.get_by_rut(conn, medico_data.rut)
            if existing:
                raise ConflictError("El médico ya existe")

            created = await self.medico_repo.create(conn, medico_ent)
            return MedicoResponse.model_validate(created)

    async def get_medico_by_id(self, id: int) -> MedicoResponse:
        async with self.pool.acquire() as conn:
            medico = await self.medico_repo.get_by_id(conn, id)
            if not medico:
                raise NotFoundError("Médico no encontrado")
            if medico.id_medico is None:
                raise NotFoundError("Médico sin ID válido")

            medico_resp = MedicoResponse.model_validate(medico)
            specialties = await self.medico_repo.get_specialties_by_medico(conn, id)
            medico_resp.especialidades = [
                VinculoProfesionalDTO(
                    id_profesional=medico.id_medico,
                    especialidad=EspecialidadDTO.model_validate(s),
                    fecha_registro=None,
                )
                for s in specialties
            ]
            return medico_resp

    async def assign_specialty(self, id_medico: int, id_especialidad: int):
        async with self.pool.acquire() as conn:
            medico = await self.medico_repo.get_by_id(conn, id_medico)
            if not medico:
                raise NotFoundError("Médico no encontrado")

            especialidad = await self.especialidad_repo.get_by_id(conn, id_especialidad)
            if not especialidad:
                raise NotFoundError("Especialidad no encontrada")

            # Check if already assigned
            current_specialties = await self.medico_repo.get_specialties_by_medico(
                conn, id_medico
            )
            if any(s.id == id_especialidad for s in current_specialties):
                raise ConflictError("El médico ya tiene esta especialidad")

            await self.medico_repo.assign_specialty(conn, id_medico, id_especialidad)

    # Especialidad methods
    async def list_specialties(self) -> List[EspecialidadDTO]:
        async with self.pool.acquire() as conn:
            specialties = await self.especialidad_repo.list_all(conn)
            return [EspecialidadDTO.model_validate(s) for s in specialties]

    async def create_specialty(self, data: EspecialidadCreate) -> EspecialidadDTO:
        ent = Especializacion(
            id=None,
            nombre=data.nombre,
            nivel=data.nivel,
            codigo_fonasa=data.codigo_fonasa,
        )
        async with self.pool.acquire() as conn:
            created = await self.especialidad_repo.create(conn, ent)
            return EspecialidadDTO.model_validate(created)

    async def update_specialty(self, id: int, data: dict) -> EspecialidadDTO:
        async with self.pool.acquire() as conn:
            updated = await self.especialidad_repo.update(conn, id, data)
            if not updated:
                raise NotFoundError("Especialidad no encontrada")
            return EspecialidadDTO.model_validate(updated)

    async def delete_specialty(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.especialidad_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Especialidad no encontrada")

    async def get_specialty_by_id(self, id: int) -> EspecialidadDTO:
        async with self.pool.acquire() as conn:
            spec = await self.especialidad_repo.get_by_id(conn, id)
            if not spec:
                raise NotFoundError("Especialidad no encontrada")
            return EspecialidadDTO.model_validate(spec)

    async def search_specialties(self, nombre: str) -> List[EspecialidadDTO]:
        async with self.pool.acquire() as conn:
            specialties = await self.especialidad_repo.search_by_name(conn, nombre)
            return [EspecialidadDTO.model_validate(s) for s in specialties]

    async def list_medico_specialties(self, id_medico: int) -> List[EspecialidadDTO]:
        async with self.pool.acquire() as conn:
            specialties = await self.medico_repo.get_specialties_by_medico(
                conn, id_medico
            )
            return [EspecialidadDTO.model_validate(s) for s in specialties]

    async def search_medicos_by_specialty(
        self, specialty_name: str
    ) -> List[MedicoResponse]:
        async with self.pool.acquire() as conn:
            medicos = await self.medico_repo.search_by_specialty(conn, specialty_name)
            return [MedicoResponse.model_validate(m) for m in medicos]

    async def list_active_medicos(self) -> List[MedicoResponse]:
        async with self.pool.acquire() as conn:
            medicos = await self.medico_repo.list_active(conn)
            return [MedicoResponse.model_validate(m) for m in medicos]
