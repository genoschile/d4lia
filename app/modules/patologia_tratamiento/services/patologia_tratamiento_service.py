from typing import List
from app.modules.patologia_tratamiento.interfaces.patologia_tratamiento_interfaces import IPatologiaTratamientoRepository
from app.modules.patologia_tratamiento.schemas.patologia_tratamiento_schema import (
    PatologiaTratamientoResponse,
    PatologiaTratamientoCreate,
    PatologiaTratamientoDetailed,
)
from app.modules.patologia_tratamiento.entities.patologia_tratamiento_entity import PatologiaTratamiento
from app.modules.patologia.interfaces.patologia_interfaces import IPatologiaRepository
from app.modules.tratamiento.interfaces.tratamiento_interfaces import ITratamientoRepository
from app.core.exceptions import ConflictError, NotFoundError


class PatologiaTratamientoService:
    def __init__(
        self, 
        pool, 
        patologia_tratamiento_repo: IPatologiaTratamientoRepository,
        patologia_repo: IPatologiaRepository,
        tratamiento_repo: ITratamientoRepository
    ):
        self.pool = pool
        self.patologia_tratamiento_repo = patologia_tratamiento_repo
        self.patologia_repo = patologia_repo
        self.tratamiento_repo = tratamiento_repo

    async def create(self, data: PatologiaTratamientoCreate) -> PatologiaTratamientoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que la patología existe
            patologia = await self.patologia_repo.get_by_id(conn, data.id_patologia)
            if not patologia:
                raise NotFoundError(f"Patología con ID {data.id_patologia} no encontrada")
            
            # Verificar que el tratamiento existe
            tratamiento = await self.tratamiento_repo.get_by_id(conn, data.id_tratamiento)
            if not tratamiento:
                raise NotFoundError(f"Tratamiento con ID {data.id_tratamiento} no encontrado")
            
            # Verificar que no exista ya la relación
            exists = await self.patologia_tratamiento_repo.exists(conn, data.id_patologia, data.id_tratamiento)
            if exists:
                raise ConflictError(
                    f"La patología '{patologia.nombre_patologia}' ya está vinculada con el tratamiento '{tratamiento.nombre_tratamiento}'"
                )
            
            # Crear la relación
            pt_entity = PatologiaTratamiento(
                id_patologia=data.id_patologia,
                id_tratamiento=data.id_tratamiento
            )
            created = await self.patologia_tratamiento_repo.create(conn, pt_entity)
            return PatologiaTratamientoResponse.model_validate(created)

    async def delete(self, id_patologia: int, id_tratamiento: int):
        async with self.pool.acquire() as conn:
            # Verificar que existe la relación
            exists = await self.patologia_tratamiento_repo.exists(conn, id_patologia, id_tratamiento)
            if not exists:
                raise NotFoundError("La relación patología-tratamiento no existe")
            
            deleted = await self.patologia_tratamiento_repo.delete(conn, id_patologia, id_tratamiento)
            if not deleted:
                raise NotFoundError("No se pudo eliminar la relación")

    async def get_tratamientos_by_patologia(self, id_patologia: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            # Verificar que la patología existe
            patologia = await self.patologia_repo.get_by_id(conn, id_patologia)
            if not patologia:
                raise NotFoundError(f"Patología con ID {id_patologia} no encontrada")
            
            return await self.patologia_tratamiento_repo.get_tratamientos_by_patologia(conn, id_patologia)

    async def get_patologias_by_tratamiento(self, id_tratamiento: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            # Verificar que el tratamiento existe
            tratamiento = await self.tratamiento_repo.get_by_id(conn, id_tratamiento)
            if not tratamiento:
                raise NotFoundError(f"Tratamiento con ID {id_tratamiento} no encontrado")
            
            return await self.patologia_tratamiento_repo.get_patologias_by_tratamiento(conn, id_tratamiento)

    async def list_all(self) -> List[PatologiaTratamientoDetailed]:
        async with self.pool.acquire() as conn:
            relations = await self.patologia_tratamiento_repo.list_all(conn)
            return [PatologiaTratamientoDetailed(**r) for r in relations]
