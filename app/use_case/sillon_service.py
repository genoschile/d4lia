from app.domain.sillon import Sillon
from app.repositories.sillon_repository import SillonRepository
from app.database.database import get_conn


class SillonService:
    """
    Caso de uso (application service) que maneja el ciclo de vida de la conexión
    y orquesta las operaciones sobre el repositorio.
    """

    async def create_sillon(self, sillon_data: dict) -> Sillon:
        conn = await get_conn() # type: ignore
        try:
            repo = SillonRepository(conn)
            sillon = Sillon(**sillon_data)
            return await repo.create(sillon)
        finally:
            await conn.close()

    async def get_all_sillones(self) -> list[Sillon]:
        conn = await get_conn() # type: ignore
        try:
            repo = SillonRepository(conn)
            return await repo.get_all()
        finally:
            await conn.close()

    async def update_sillon(self, sillon_id: int, sillon_data: dict) -> Sillon | None:
        conn = await get_conn() # type: ignore
        try:
            repo = SillonRepository(conn)
            sillon = Sillon(**sillon_data)
            return await repo.update(sillon_id, sillon)
        finally:
            await conn.close()

    async def delete_sillon(self, sillon_id: int) -> bool:
        conn = await get_conn() # type: ignore
        try:
            repo = SillonRepository(conn)
            return await repo.delete(sillon_id)
        finally:
            await conn.close()
