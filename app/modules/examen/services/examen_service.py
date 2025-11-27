from typing import List
from app.modules.examen.repositories.examen_repository import ExamenRepository
from app.modules.examen.schemas.examen_schema import (
    ExamenResponse,
    ExamenCreate,
    ExamenUpdate,
)
from app.modules.examen.entities.examen_entity import Examen
from app.core.exceptions import ConflictError, NotFoundError


class ExamenService:
    def __init__(
        self, 
        pool, 
        examen_repo: ExamenRepository,
        orden_repo,
        paciente_repo,
        tipo_examen_repo,
        instalacion_repo
    ):
        self.pool = pool
        self.examen_repo = examen_repo
        self.orden_repo = orden_repo
        self.paciente_repo = paciente_repo
        self.tipo_examen_repo = tipo_examen_repo
        self.instalacion_repo = instalacion_repo

    async def list_all(self) -> List[ExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.examen_repo.list_all(conn)
            return [ExamenResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> ExamenResponse:
        async with self.pool.acquire() as conn:
            item = await self.examen_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Resultado de examen no encontrado")
            return ExamenResponse.model_validate(item)

    async def create(self, data: ExamenCreate) -> ExamenResponse:
        async with self.pool.acquire() as conn:
            # Validar existencia de orden
            orden = await self.orden_repo.get_by_id(conn, data.id_orden_examen)
            if not orden:
                raise NotFoundError(f"Orden de examen con ID {data.id_orden_examen} no encontrada")
            
            # Validar existencia de paciente
            paciente = await self.paciente_repo.get_by_id(conn, data.id_paciente)
            if not paciente:
                raise NotFoundError(f"Paciente con ID {data.id_paciente} no encontrado")
            
            # Validar existencia de tipo de examen si se proporciona
            if data.id_tipo_examen:
                tipo = await self.tipo_examen_repo.get_by_id(conn, data.id_tipo_examen)
                if not tipo:
                    raise NotFoundError(f"Tipo de examen con ID {data.id_tipo_examen} no encontrado")
            
            # Validar existencia de instalación si se proporciona
            if data.id_instalacion:
                instalacion = await self.instalacion_repo.get_by_id(conn, data.id_instalacion)
                if not instalacion:
                    raise NotFoundError(f"Instalación con ID {data.id_instalacion} no encontrada")
            
            entity = Examen(
                id_examen=None,
                id_paciente=data.id_paciente,
                id_orden_examen=data.id_orden_examen,
                id_tipo_examen=data.id_tipo_examen,
                id_profesional=data.id_profesional,
                id_instalacion=data.id_instalacion,
                documento=data.documento,
                fecha=data.fecha,
                resultados=data.resultados,
                resumen_resultado=data.resumen_resultado,
                observaciones=data.observaciones,
            )
            created = await self.examen_repo.create(conn, entity)
            return ExamenResponse.model_validate(created)

    async def update(self, id: int, data: ExamenUpdate) -> ExamenResponse:
        async with self.pool.acquire() as conn:
            existing = await self.examen_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Resultado de examen no encontrado")
            
            # Validaciones opcionales para updates
            if data.id_tipo_examen:
                tipo = await self.tipo_examen_repo.get_by_id(conn, data.id_tipo_examen)
                if not tipo:
                    raise NotFoundError(f"Tipo de examen con ID {data.id_tipo_examen} no encontrado")
            
            if data.id_instalacion:
                instalacion = await self.instalacion_repo.get_by_id(conn, data.id_instalacion)
                if not instalacion:
                    raise NotFoundError(f"Instalación con ID {data.id_instalacion} no encontrada")
            
            update_data = data.model_dump(exclude_none=True)
            updated = await self.examen_repo.update(conn, id, update_data)
            return ExamenResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.examen_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Resultado de examen no encontrado")

    async def get_by_paciente(self, id_paciente: int) -> List[ExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.examen_repo.get_by_paciente(conn, id_paciente)
            return [ExamenResponse.model_validate(i) for i in items]

    async def get_by_orden(self, id_orden: int) -> List[ExamenResponse]:
        async with self.pool.acquire() as conn:
            items = await self.examen_repo.get_by_orden(conn, id_orden)
            return [ExamenResponse.model_validate(i) for i in items]
