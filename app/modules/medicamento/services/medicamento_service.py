from typing import List
from app.modules.medicamento.interfaces.medicamento_interfaces import IMedicamentoRepository
from app.modules.medicamento.schemas.medicamento_schema import (
    MedicamentoResponse,
    MedicamentoCreate,
    MedicamentoUpdate,
)
from app.modules.medicamento.entities.medicamento_entity import Medicamento
from app.core.exceptions import ConflictError, NotFoundError


class MedicamentoService:
    def __init__(self, pool, medicamento_repo: IMedicamentoRepository):
        self.pool = pool
        self.medicamento_repo = medicamento_repo

    async def list_all(self) -> List[MedicamentoResponse]:
        async with self.pool.acquire() as conn:
            medicamentos = await self.medicamento_repo.list_all(conn)
            return [MedicamentoResponse.model_validate(m) for m in medicamentos]

    async def get_by_id(self, id: int) -> MedicamentoResponse:
        async with self.pool.acquire() as conn:
            medicamento = await self.medicamento_repo.get_by_id(conn, id)
            if not medicamento:
                raise NotFoundError("Medicamento no encontrado")
            return MedicamentoResponse.model_validate(medicamento)

    async def create(self, data: MedicamentoCreate) -> MedicamentoResponse:
        # Verificar si ya existe un medicamento con el mismo nombre comercial
        async with self.pool.acquire() as conn:
            existing = await self.medicamento_repo.get_by_nombre_comercial(conn, data.nombre_comercial)
            if existing:
                raise ConflictError(f"Ya existe un medicamento con el nombre comercial '{data.nombre_comercial}'")
        
        medicamento_ent = Medicamento(
            id_medicamento=None,
            nombre_comercial=data.nombre_comercial,
            nombre_generico=data.nombre_generico,
            concentracion=data.concentracion,
            forma_farmaceutica=data.forma_farmaceutica,
            via_administracion=data.via_administracion,
            laboratorio=data.laboratorio,
            requiere_receta=data.requiere_receta,
            stock_disponible=data.stock_disponible,
            observaciones=data.observaciones,
        )
        async with self.pool.acquire() as conn:
            created = await self.medicamento_repo.create(conn, medicamento_ent)
            return MedicamentoResponse.model_validate(created)

    async def update(self, id: int, data: MedicamentoUpdate) -> MedicamentoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe
            existing = await self.medicamento_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Medicamento no encontrado")
            
            # Si se está actualizando el nombre comercial, verificar que no exista otro con ese nombre
            if data.nombre_comercial:
                nombre_exists = await self.medicamento_repo.get_by_nombre_comercial(conn, data.nombre_comercial)
                if nombre_exists and nombre_exists.id_medicamento != id:
                    raise ConflictError(f"Ya existe otro medicamento con el nombre comercial '{data.nombre_comercial}'")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.medicamento_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Medicamento no encontrado")
            return MedicamentoResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.medicamento_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Medicamento no encontrado")

    async def get_stock_bajo(self, umbral: int = 10) -> List[MedicamentoResponse]:
        async with self.pool.acquire() as conn:
            medicamentos = await self.medicamento_repo.get_stock_bajo(conn, umbral)
            return [MedicamentoResponse.model_validate(m) for m in medicamentos]

    async def get_by_laboratorio(self, laboratorio: str) -> List[MedicamentoResponse]:
        async with self.pool.acquire() as conn:
            medicamentos = await self.medicamento_repo.get_by_laboratorio(conn, laboratorio)
            return [MedicamentoResponse.model_validate(m) for m in medicamentos]
