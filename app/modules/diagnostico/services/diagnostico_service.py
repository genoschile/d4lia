from typing import List
from app.modules.diagnostico.interfaces.diagnostico_interfaces import IDiagnosticoRepository
from app.modules.diagnostico.schemas.diagnostico_schema import (
    DiagnosticoResponse,
    DiagnosticoCreate,
    DiagnosticoUpdate,
    TipoDiagnosticoEnum,
)
from app.modules.diagnostico.entities.diagnostico_entity import Diagnostico
from app.core.exceptions import NotFoundError


class DiagnosticoService:
    def __init__(self, pool, diagnostico_repo: IDiagnosticoRepository, consulta_repo):
        self.pool = pool
        self.diagnostico_repo = diagnostico_repo
        self.consulta_repo = consulta_repo

    async def list_all(self) -> List[DiagnosticoResponse]:
        async with self.pool.acquire() as conn:
            diagnosticos = await self.diagnostico_repo.list_all(conn)
            return [DiagnosticoResponse.model_validate(d) for d in diagnosticos]

    async def get_by_id(self, id: int) -> DiagnosticoResponse:
        async with self.pool.acquire() as conn:
            diagnostico = await self.diagnostico_repo.get_by_id(conn, id)
            if not diagnostico:
                raise NotFoundError("Diagnóstico no encontrado")
            return DiagnosticoResponse.model_validate(diagnostico)

    async def create(self, data: DiagnosticoCreate) -> DiagnosticoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que la consulta médica existe
            consulta = await self.consulta_repo.get_by_id(conn, data.id_consulta_medica)
            if not consulta:
                raise NotFoundError(f"Consulta médica con ID {data.id_consulta_medica} no encontrada")
        
        diagnostico_ent = Diagnostico(
            id_diagnostico=None,
            id_consulta_medica=data.id_consulta_medica,
            id_cie10=data.id_cie10,
            id_ges=data.id_ges,
            descripcion=data.descripcion,
            tipo=data.tipo.value,
            fecha_registro=data.fecha_registro,
            observaciones=data.observaciones,
        )
        async with self.pool.acquire() as conn:
            created = await self.diagnostico_repo.create(conn, diagnostico_ent)
            return DiagnosticoResponse.model_validate(created)

    async def update(self, id: int, data: DiagnosticoUpdate) -> DiagnosticoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe
            existing = await self.diagnostico_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Diagnóstico no encontrado")
            
            update_data = data.model_dump(exclude_none=True)
            # Convertir enum a string si existe
            if 'tipo' in update_data and hasattr(update_data['tipo'], 'value'):
                update_data['tipo'] = update_data['tipo'].value
            
            updated = await self.diagnostico_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Diagnóstico no encontrado")
            return DiagnosticoResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.diagnostico_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Diagnóstico no encontrado")

    async def get_by_consulta(self, id_consulta: int) -> List[DiagnosticoResponse]:
        async with self.pool.acquire() as conn:
            diagnosticos = await self.diagnostico_repo.get_by_consulta(conn, id_consulta)
            return [DiagnosticoResponse.model_validate(d) for d in diagnosticos]

    async def get_by_tipo(self, tipo: TipoDiagnosticoEnum) -> List[DiagnosticoResponse]:
        async with self.pool.acquire() as conn:
            diagnosticos = await self.diagnostico_repo.get_by_tipo(conn, tipo.value)
            return [DiagnosticoResponse.model_validate(d) for d in diagnosticos]

    async def get_con_ges(self) -> List[DiagnosticoResponse]:
        async with self.pool.acquire() as conn:
            diagnosticos = await self.diagnostico_repo.get_con_ges(conn)
            return [DiagnosticoResponse.model_validate(d) for d in diagnosticos]
