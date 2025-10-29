from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository
from app.schemas.sillon_schema import EstadoSillon, SillonCreate, ubicacionSala


class SillonService:
    def __init__(self, pool, sillon_repo: ISillonRepository):
        self.pool = pool
        self.sillon_repo = sillon_repo

    async def get_all_sillones(self) -> list[Sillon]:
        async with self.pool.acquire() as conn:
            sillones = await self.sillon_repo.get_all(conn)
            return sillones

    async def create_sillon(self, sillon_data: SillonCreate) -> Sillon:
        sillon = Sillon(
            id_sillon=None,
            ubicacion_sala=sillon_data.ubicacion_sala,
            estado=sillon_data.estado,
            observaciones=sillon_data.observaciones,
        )
        async with self.pool.acquire() as conn:
            generated_id = await self.sillon_repo.create_sillon(conn, sillon)
            sillon.id_sillon = generated_id
            return sillon

    async def get_sillon_by_id(self, id_sillon: int) -> Sillon:
        async with self.pool.acquire() as conn:
            sillon = await self.sillon_repo.get_by_id(conn, id_sillon)
            return sillon

    async def delete_sillon(self, id_sillon: int) -> None:
        async with self.pool.acquire() as conn:
            deleted = await self.sillon_repo.delete_sillon(conn, id_sillon)
            if not deleted:
                raise ValueError("Sillón no encontrado o ya eliminado")

    async def change_state_sillon(
        self, id_sillon: int, new_state: EstadoSillon, motivo: str | None = None
    ) -> Sillon:
        async with self.pool.acquire() as conn:
            sillon = await self.sillon_repo.get_by_id(conn, id_sillon)
            if not sillon:
                raise ValueError("Sillón no encontrado")

            match new_state:
                case EstadoSillon.OCUPADO:
                    sillon.ocupar(motivo)
                case EstadoSillon.DISPONIBLE:
                    sillon.liberar()
                case EstadoSillon.MANTENIMIENTO:
                    sillon.poner_en_mantenimiento(motivo or "Motivo no especificado")
                case EstadoSillon.FUERA_SERVICIO:
                    sillon.inhabilitar(motivo or "Motivo no especificado")
                case _:
                    raise ValueError("Estado no válido")

            await self.sillon_repo.change_state_sillon(conn, sillon)
            return sillon

    async def change_sala_sillon(self, id_sillon: int, nueva_sala: ubicacionSala) -> Sillon:
        async with self.pool.acquire() as conn:
            sillon = await self.sillon_repo.get_by_id(conn, id_sillon)
            if not sillon:
                raise ValueError("Sillón no encontrado")

            sillon.cambiar_sala(nueva_sala)
            await self.sillon_repo.change_sala_sillon(conn, sillon)
            return sillon
