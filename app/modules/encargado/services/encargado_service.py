from typing import List
from app.modules.encargado.interfaces.encargado_interfaces import IEncargadoRepository
from app.modules.encargado.schemas.encargado_schema import (
    EncargadoResponse,
    EncargadoCreate,
    EncargadoUpdate,
)
from app.modules.encargado.entities.encargado_entity import Encargado
from app.core.exceptions import ConflictError, NotFoundError


class EncargadoService:
    def __init__(self, pool, encargado_repo: IEncargadoRepository):
        self.pool = pool
        self.encargado_repo = encargado_repo

    async def list_all(self) -> List[EncargadoResponse]:
        async with self.pool.acquire() as conn:
            encargados = await self.encargado_repo.list_all(conn)
            return [EncargadoResponse.model_validate(e) for e in encargados]

    async def get_by_id(self, id: int) -> EncargadoResponse:
        async with self.pool.acquire() as conn:
            encargado = await self.encargado_repo.get_by_id(conn, id)
            if not encargado:
                raise NotFoundError("Encargado no encontrado")
            return EncargadoResponse.model_validate(encargado)

    async def create(self, data: EncargadoCreate) -> EncargadoResponse:
        # Verificar si ya existe un encargado con el mismo RUT
        if data.rut:
            async with self.pool.acquire() as conn:
                existing = await self.encargado_repo.get_by_rut(conn, data.rut)
                if existing:
                    raise ConflictError(f"Ya existe un encargado con el RUT '{data.rut}'")
        
        encargado_ent = Encargado(
            id_encargado=None,
            nombre_completo=data.nombre_completo,
            rut=data.rut,
            correo=data.correo,
            telefono=data.telefono,
            cargo=data.cargo.value,  # Convertir enum a string
            especialidad=data.especialidad,
            activo=data.activo,
        )
        async with self.pool.acquire() as conn:
            created = await self.encargado_repo.create(conn, encargado_ent)
            return EncargadoResponse.model_validate(created)

    async def update(self, id: int, data: EncargadoUpdate) -> EncargadoResponse:
        async with self.pool.acquire() as conn:
            # Verificar que existe
            existing = await self.encargado_repo.get_by_id(conn, id)
            if not existing:
                raise NotFoundError("Encargado no encontrado")
            
            # Si se está actualizando el RUT, verificar que no exista otro con ese RUT
            if data.rut:
                rut_exists = await self.encargado_repo.get_by_rut(conn, data.rut)
                if rut_exists and rut_exists.id_encargado != id:
                    raise ConflictError(f"Ya existe otro encargado con el RUT '{data.rut}'")
            
            update_data = data.model_dump(exclude_none=True)
            # Convertir enum a string si existe
            if 'cargo' in update_data and hasattr(update_data['cargo'], 'value'):
                update_data['cargo'] = update_data['cargo'].value
            
            updated = await self.encargado_repo.update(conn, id, update_data)
            if not updated:
                raise NotFoundError("Encargado no encontrado")
            return EncargadoResponse.model_validate(updated)

    async def delete(self, id: int):
        async with self.pool.acquire() as conn:
            deleted = await self.encargado_repo.delete(conn, id)
            if not deleted:
                raise NotFoundError("Encargado no encontrado")

    async def get_by_cargo(self, cargo: str) -> List[EncargadoResponse]:
        async with self.pool.acquire() as conn:
            encargados = await self.encargado_repo.get_by_cargo(conn, cargo)
            return [EncargadoResponse.model_validate(e) for e in encargados]

    async def get_activos(self) -> List[EncargadoResponse]:
        async with self.pool.acquire() as conn:
            encargados = await self.encargado_repo.get_activos(conn)
            return [EncargadoResponse.model_validate(e) for e in encargados]
