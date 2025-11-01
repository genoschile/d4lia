from typing import List
from app.domain.encuesta_entity import Encuesta
from app.interfaces.encuesta_interfaces import IEncuestaRepository
import asyncpg


class EncuestaRepository(IEncuestaRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, encuesta: Encuesta) -> Encuesta:
        query = """
            INSERT INTO encuesta (id_paciente, fecha, respuestas, observaciones)
            VALUES ($1, $2, $3, $4)
            RETURNING id, id_paciente, fecha, respuestas, observaciones
            """
        row = await self.pool.fetchrow(
            query,
            encuesta.id_paciente,  # type: ignore
            encuesta.fecha,  # type: ignore
            encuesta.respuestas,  # type: ignore
            encuesta.observaciones,  # type: ignore
        )
        return Encuesta(**dict(row))  # type: ignore
