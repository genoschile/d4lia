from typing import List
from app.modules.receta_medicamento.interfaces.receta_medicamento_interfaces import IRecetaMedicamentoRepository
from app.modules.receta_medicamento.schemas.receta_medicamento_schema import (
    RecetaMedicamentoResponse,
    RecetaMedicamentoCreate,
    RecetaMedicamentoUpdate,
    RecetaMedicamentoDetailed,
)
from app.modules.receta_medicamento.entities.receta_medicamento_entity import RecetaMedicamento
from app.core.exceptions import ConflictError, NotFoundError


class RecetaMedicamentoService:
    def __init__(
        self, 
        pool, 
        receta_medicamento_repo: IRecetaMedicamentoRepository,
        receta_repo,
        medicamento_repo
    ):
        self.pool = pool
        self.receta_medicamento_repo = receta_medicamento_repo
        self.receta_repo = receta_repo
        self.medicamento_repo = medicamento_repo

    async def create(self, data: RecetaMedicamentoCreate) -> RecetaMedicamentoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que la receta existe
            receta = await self.receta_repo.get_by_id(conn, data.id_receta)
            if not receta:
                raise NotFoundError(f"Receta con ID {data.id_receta} no encontrada")
            
            # Verificar que el medicamento existe
            medicamento = await self.medicamento_repo.get_by_id(conn, data.id_medicamento)
            if not medicamento:
                raise NotFoundError(f"Medicamento con ID {data.id_medicamento} no encontrado")
            
            # Verificar que no exista ya la relación
            exists = await self.receta_medicamento_repo.exists(conn, data.id_receta, data.id_medicamento)
            if exists:
                raise ConflictError(
                    f"El medicamento '{medicamento.nombre_comercial}' ya está en la receta"
                )
            
            # Crear la relación
            rm_entity = RecetaMedicamento(
                id_receta=data.id_receta,
                id_medicamento=data.id_medicamento,
                dosis=data.dosis,
                frecuencia=data.frecuencia,
                duracion=data.duracion,
                instrucciones=data.instrucciones
            )
            created = await self.receta_medicamento_repo.create(conn, rm_entity)
            return RecetaMedicamentoResponse.model_validate(created)

    async def update(self, id_receta: int, id_medicamento: int, data: RecetaMedicamentoUpdate) -> RecetaMedicamentoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe la relación
            exists = await self.receta_medicamento_repo.exists(conn, id_receta, id_medicamento)
            if not exists:
                raise NotFoundError("La prescripción no existe")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.receta_medicamento_repo.update(conn, id_receta, id_medicamento, update_data)
            if not updated:
                raise NotFoundError("No se pudo actualizar la prescripción")
            return RecetaMedicamentoResponse.model_validate(updated)

    async def delete(self, id_receta: int, id_medicamento: int):
        async with self.pool.acquire() as conn:
            # Verificar que existe la relación
            exists = await self.receta_medicamento_repo.exists(conn, id_receta, id_medicamento)
            if not exists:
                raise NotFoundError("La prescripción no existe")
            
            deleted = await self.receta_medicamento_repo.delete(conn, id_receta, id_medicamento)
            if not deleted:
                raise NotFoundError("No se pudo eliminar la prescripción")

    async def get_medicamentos_by_receta(self, id_receta: int) -> List[RecetaMedicamentoDetailed]:
        async with self.pool.acquire() as conn:
            # Verificar que la receta existe
            receta = await self.receta_repo.get_by_id(conn, id_receta)
            if not receta:
                raise NotFoundError(f"Receta con ID {id_receta} no encontrada")
            
            medicamentos = await self.receta_medicamento_repo.get_medicamentos_by_receta(conn, id_receta)
            return [RecetaMedicamentoDetailed(**m) for m in medicamentos]

    async def get_recetas_by_medicamento(self, id_medicamento: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            # Verificar que el medicamento existe
            medicamento = await self.medicamento_repo.get_by_id(conn, id_medicamento)
            if not medicamento:
                raise NotFoundError(f"Medicamento con ID {id_medicamento} no encontrado")
            
            return await self.receta_medicamento_repo.get_recetas_by_medicamento(conn, id_medicamento)

    async def list_all(self) -> List[RecetaMedicamentoDetailed]:
        async with self.pool.acquire() as conn:
            relations = await self.receta_medicamento_repo.list_all(conn)
            return [RecetaMedicamentoDetailed(**r) for r in relations]
