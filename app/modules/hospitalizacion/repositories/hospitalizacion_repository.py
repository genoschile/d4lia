from typing import List, Optional
from app.modules.hospitalizacion.entities.hospitalizacion_entity import Hospitalizacion
from app.modules.hospitalizacion.schemas.hospitalizacion_schema import HospitalizacionCreate, HospitalizacionUpdate
from app.core.exceptions import ConflictError, NotFoundError


class HospitalizacionRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Hospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha_ingreso, fecha_alta, habitacion, observacion, estado
            FROM hospitalizacion
            ORDER BY fecha_ingreso DESC;
        """
        rows = await conn.fetch(query)
        return [Hospitalizacion(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Hospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha_ingreso, fecha_alta, habitacion, observacion, estado
            FROM hospitalizacion
            WHERE id_hospitalizacion = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Hospitalizacion(**dict(row))
        return None

    async def create(self, conn, hosp: Hospitalizacion) -> Hospitalizacion:
        query = """
            INSERT INTO hospitalizacion (id_orden_hospitalizacion, id_paciente, id_profesional, fecha_ingreso, fecha_alta, habitacion, observacion, estado)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id_hospitalizacion;
        """
        id_hosp = await conn.fetchval(
            query,
            hosp.id_orden_hospitalizacion,
            hosp.id_paciente,
            hosp.id_profesional,
            hosp.fecha_ingreso,
            hosp.fecha_alta,
            hosp.habitacion,
            hosp.observacion,
            hosp.estado
        )
        hosp.id_hospitalizacion = id_hosp
        return hosp

    async def update(self, conn, id: int, data: dict) -> Optional[Hospitalizacion]:
        set_clauses = []
        values = []
        idx = 1
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
            idx += 1
        
        if not set_clauses:
            return await self.get_by_id(conn, id)

        values.append(id)
        query = f"""
            UPDATE hospitalizacion 
            SET {', '.join(set_clauses)} 
            WHERE id_hospitalizacion = ${idx} 
            RETURNING id_hospitalizacion, id_orden_hospitalizacion, id_paciente, id_profesional, fecha_ingreso, fecha_alta, habitacion, observacion, estado;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Hospitalizacion(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM hospitalizacion WHERE id_hospitalizacion = $1 RETURNING id_hospitalizacion;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[Hospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha_ingreso, fecha_alta, habitacion, observacion, estado
            FROM hospitalizacion
            WHERE id_paciente = $1
            ORDER BY fecha_ingreso DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [Hospitalizacion(**dict(row)) for row in rows]

    async def get_activas(self, conn) -> List[Hospitalizacion]:
        query = """
            SELECT id_hospitalizacion, id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha_ingreso, fecha_alta, habitacion, observacion, estado
            FROM hospitalizacion
            WHERE estado = 'activa'
            ORDER BY fecha_ingreso DESC;
        """
        rows = await conn.fetch(query)
        return [Hospitalizacion(**dict(row)) for row in rows]
