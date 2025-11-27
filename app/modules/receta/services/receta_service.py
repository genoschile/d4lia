from typing import List
from app.modules.receta.interfaces.receta_interfaces import IRecetaRepository
from app.modules.receta.schemas.receta_schema import (
    RecetaResponse,
    RecetaCreate,
    RecetaUpdate,
)
from app.modules.receta.entities.receta_entity import Receta
from app.core.exceptions import NotFoundError


class RecetaService:
    def __init__(self, pool, receta_repo: IRecetaRepository, paciente_repo, medico_repo, consulta_repo):
        self.pool = pool
        self.receta_repo = receta_repo
        self.paciente_repo = paciente_repo
        self.medico_repo = medico_repo
        self.consulta_repo = consulta_repo

    async def list_all(self) -> List[RecetaResponse]:
        async with self.pool.acquire() as conn:
            recetas = await self.receta_repo.list_all(conn)
            return [RecetaResponse.model_validate(r) for r in recetas]

    async def get_by_id(self, id: int) -> RecetaResponse:
        async with self.pool.acquire() as conn:
            receta = await self.receta_repo.get_by_id(conn, id)
            if not receta:
                raise NotFoundError("Receta no encontrada")
            return RecetaResponse.model_validate(receta)

    async def create(self, data: RecetaCreate) -> RecetaResponse:
        async with self.pool.acquire() as conn:
            # Verificar que el paciente existe
            pacientes = await self.paciente_repo.get_all(conn)
            if data.id_paciente not in [p.id_paciente for p in pacientes]:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            # Verificar médico si se proporciona
            if data.id_medico:
                medicos = await self.medico_repo.list_all(conn)
                if data.id_medico not in [m.id_medico for m in medicos]:
                    raise NotFoundError(f"Médico con ID {data.id_medico} no encontrado")
            
            # Verificar consulta si se proporciona
            if data.id_consulta:
                consulta = await self.consulta_repo.get_by_id(conn, data.id_consulta)
                if not consulta:
                    raise NotFoundError(f"Consulta médica con ID {data.id_consulta} no encontrada")
        
        receta_ent = Receta(
            id_receta=None,
            id_paciente=data.id_paciente,
            id_medico=data.id_medico,
            id_consulta=data.id_consulta,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            observaciones=data.observaciones,
        )
        async with self.pool.acquire() as conn:
            created = await self.receta_repo.create(conn, receta_ent)
            return RecetaResponse.model_validate(created)

    async def update(self, id: int, data: RecetaUpdate) -> RecetaResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe
            existing = await self.receta_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Receta no encontrada")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.receta_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Receta no encontrada")
            return RecetaResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.receta_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Receta no encontrada")

    async def get_by_paciente(self, id_paciente: int) -> List[RecetaResponse]:
        async with self.pool.acquire() as conn:
            recetas = await self.receta_repo.get_by_paciente(conn, id_paciente)
            return [RecetaResponse.model_validate(r) for r in recetas]

    async def get_by_medico(self, id_medico: int) -> List[RecetaResponse]:
        async with self.pool.acquire() as conn:
            recetas = await self.receta_repo.get_by_medico(conn, id_medico)
            return [RecetaResponse.model_validate(r) for r in recetas]

    async def get_by_consulta(self, id_consulta: int) -> List[RecetaResponse]:
        async with self.pool.acquire() as conn:
            recetas = await self.receta_repo.get_by_consulta(conn, id_consulta)
            return [RecetaResponse.model_validate(r) for r in recetas]
