from datetime import date
from typing import List, Optional
from app.core.error_handler import AlreadyExistsException
from app.modules.encuesta.entities.encuesta_entity import Encuesta
from app.modules.sesion.entities.sesion_entity import Sesion
from app.modules.sesion.interfaces.sesion_interfaces import ISesionRepository
import asyncpg


class SesionRepository(ISesionRepository):
    def __init__(self, pool):
        self.pool = pool

    async def get_all(self, conn) -> List[Sesion]:
        query = """
            SELECT 
                id_sesion,
                id_paciente,
                id_patologia,
                id_tratamiento,
                fecha,
                hora_inicio,
                estado
            FROM sesion
            ORDER BY id_sesion;
        """

        rows = await conn.fetch(query)

        sesiones = []
        for row in rows:
            data = dict(row)
            if data.get("estado"):
                data["estado"] = data["estado"].lower()
            sesiones.append(Sesion(**data))

        return sesiones

    async def get_encuestas_by_sesion(self, conn, id_sesion: int) -> List[dict]:
        query = """
            SELECT *
            FROM encuesta_sesion_json
            WHERE id_sesion = $1;
        """
        rows = await conn.fetch(query, id_sesion)
        return [dict(row) for row in rows]

    async def get_by_paciente_fecha_sillon(
        self, conn, id_paciente: int, fecha: date, id_sillon: int
    ):
        query = """
            SELECT *
            FROM sesion
            WHERE id_paciente = $1 AND fecha = $2 AND id_sillon = $3
        """
        row = await conn.fetchrow(query, id_paciente, fecha, id_sillon)
        return Sesion(**dict(row)) if row else None

    async def create(self, conn, sesion: Sesion) -> Sesion:
        query = """
            INSERT INTO sesion (
                id_paciente, id_patologia, id_tratamiento, id_sillon, fecha, hora_inicio, estado
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (id_paciente, fecha, id_sillon) DO NOTHING
            RETURNING id_sesion, id_paciente, fecha, hora_inicio, id_patologia, id_tratamiento, id_sillon, hora_fin, tiempo_aseo_min, materiales_usados, estado;
        """
        row = await conn.fetchrow(
            query,
            sesion.id_paciente,
            sesion.id_patologia,
            sesion.id_tratamiento,
            sesion.id_sillon,
            sesion.fecha,
            sesion.hora_inicio,
            sesion.estado,
        )
        if row is None:
            raise AlreadyExistsException(
                "Ya existe una sesión para este paciente en ese sillón a la misma fecha"
            )
        return Sesion(**dict(row))

    async def get_by_id(self, conn, id_sesion: int) -> Optional[Sesion]:
        query = """
            SELECT 
                id_sesion,
                id_paciente,
                id_patologia,
                id_tratamiento,
                id_sillon,
                fecha,
                hora_inicio,
                hora_fin,
                tiempo_aseo_min,
                materiales_usados,
                estado
            FROM sesion
            WHERE id_sesion = $1;
        """
        row = await conn.fetchrow(query, id_sesion)
        if row:
            data = dict(row)
            if data.get("estado"):
                data["estado"] = data["estado"].lower()
            return Sesion(**data)
        return None
