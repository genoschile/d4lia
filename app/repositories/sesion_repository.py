from typing import List, Optional
from app.domain.sesion_entity import Sesion
from app.interfaces.sesion_interfaces import ISesionRepository
import asyncpg

class SesionRepository(ISesionRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, sesion: Sesion) -> Sesion:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO sesion (id_paciente, fecha, duracion, notas)
            VALUES ($1, $2, $3, $4)
            RETURNING id, id_paciente, fecha, duracion, notas
            """,
            sesion.id_paciente,
            sesion.fecha,
            sesion.duracion, # type: ignore
            sesion.notas # type: ignore
        )
        return Sesion(**dict(row)) # type: ignore

    async def get_all(self) -> List[Sesion]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, id_paciente, fecha, duracion, notas FROM sesion")
            return [Sesion(**dict(row)) for row in rows]

    async def update(self, sesion_id: int, sesion: Sesion) -> Optional[Sesion]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
            """
            UPDATE sesion
            SET id_paciente=$1, fecha=$2, duracion=$3, notas=$4
            WHERE id=$5
            RETURNING id, id_paciente, fecha, duracion, notas
            """,
            sesion.id_paciente,
            sesion.fecha,
            sesion.duracion, # type: ignore
            sesion.notas, # type: ignore
            sesion_id
        )
        return Sesion(**dict(row)) if row else None

    async def delete(self, sesion_id: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM sesion WHERE id=$1",
                sesion_id
            )
            return result.startswith("DELETE")  # True si se eliminó al menos una fila
