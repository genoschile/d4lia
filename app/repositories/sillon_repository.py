from typing import Optional
from app.domain.sillon import Sillon
from app.interfaces.sillon_interfaces import ISillonRepository


class SillonRepository(ISillonRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create_sillon(self, conn, sillon: Sillon) -> str:
        query = """
            INSERT INTO sillon (ubicacion_sala, estado, observaciones)
            VALUES ($1, $2, $3)
            RETURNING id_sillon;  -- Pide explícitamente el ID generado
        """

        generated_id = await conn.fetchval(
            query,
            sillon.ubicacion_sala.value,
            sillon.estado.value,
            sillon.observaciones,
        )

        return generated_id

    async def get_all(self, conn) -> list[Sillon]:
        query = """
            SELECT id_sillon, ubicacion_sala, estado, observaciones
            FROM sillon
            ORDER BY id_sillon;
        """
        rows = await conn.fetch(query)
        return [Sillon(**dict(r)) for r in rows]

    async def get_by_id(self, conn, id_sillon: int) -> Sillon:
        query = """
            SELECT id_sillon, ubicacion_sala, estado, observaciones
            FROM sillon
            WHERE id_sillon = $1;
        """
        row = await conn.fetchrow(query, id_sillon)
        if row:
            return Sillon(**dict(row))
        else:
            raise ValueError(f"Sillón con ID {id_sillon} no encontrado.")

    async def delete_sillon(self, conn, id_sillon: str) -> bool:
        query = """
            DELETE FROM sillon
            WHERE id_sillon = $1
            RETURNING id_sillon;
        """
        deleted_id = await conn.fetchval(query, id_sillon)
        return bool(deleted_id)

    async def change_state_sillon(self, conn, sillon: Sillon) -> None:
        query = """
            UPDATE sillon
            SET estado = $1,
                observaciones = $2
            WHERE id_sillon = $3;
        """
        await conn.execute(
            query, sillon.estado.value, sillon.observaciones, sillon.id_sillon
        )
