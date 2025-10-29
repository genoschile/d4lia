from typing import List
from app.domain.encuesta_entity import Encuesta
from app.interfaces.encuesta_interfaces import IEncuestaRepository
import asyncpg


class EncuestaRepository(IEncuestaRepository):
    def __init__(self, conn: asyncpg.Connection):
        """
        Recibe una conexión asyncpg.Connection.
        Esto hace que el repositorio sea testeable y no dependa del pool global.
        """
        self.conn = conn

    async def create(self, encuesta: Encuesta) -> Encuesta:
        row = await self.conn.fetchrow(
            """
            INSERT INTO encuesta (id_paciente, fecha, respuestas, observaciones)
            VALUES ($1, $2, $3, $4)
            RETURNING id, id_paciente, fecha, respuestas, observaciones
            """,
            encuesta.id_paciente,  # type: ignore
            encuesta.fecha,  # type: ignore
            encuesta.respuestas,  # type: ignore
            encuesta.observaciones,  # type: ignore
        )
        return Encuesta(**dict(row)) # type: ignore

    async def get_all(self) -> List[Encuesta]:
        rows = await self.conn.fetch(
            "SELECT id, id_paciente, fecha, respuestas, observaciones FROM encuesta"
        )
        return [Encuesta(**dict(row)) for row in rows]
