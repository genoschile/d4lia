from typing import List
from app.modules.estado.repositories.estado_repository import EstadoRepository
from app.modules.estado.schemas.estado_schema import EstadoResponse
from app.core.exceptions import NotFoundError


class EstadoService:
    def __init__(self, pool, estado_repo: EstadoRepository):
        self.pool = pool
        self.estado_repo = estado_repo

    async def list_all(self) -> List[EstadoResponse]:
        async with self.pool.acquire() as conn:
            items = await self.estado_repo.list_all(conn)
            return [EstadoResponse.model_validate(i) for i in items]

    async def get_by_id(self, id: int) -> EstadoResponse:
        async with self.pool.acquire() as conn:
            item = await self.estado_repo.get_by_id(conn, id)
            if not item:
                raise NotFoundError("Estado no encontrado")
            return EstadoResponse.model_validate(item)
