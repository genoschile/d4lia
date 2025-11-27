from typing import List, Optional
from app.modules.orden_hospitalizacion.entities.orden_hospitalizacion_entity import OrdenHospitalizacion
from app.modules.orden_hospitalizacion.schemas.orden_hospitalizacion_schema import OrdenHospitalizacionCreate, OrdenHospitalizacionUpdate
from app.core.exceptions import ConflictError, NotFoundError


class OrdenHospitalizacionRepository:
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[OrdenHospitalizacion]:
        query = """
            SELECT id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha, motivo, documento, estado
            FROM orden_hospitalizacion
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query)
        return [OrdenHospitalizacion(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[OrdenHospitalizacion]:
        query = """
            SELECT id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha, motivo, documento, estado
            FROM orden_hospitalizacion
            WHERE id_orden_hospitalizacion = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return OrdenHospitalizacion(**dict(row))
        return None

    async def create(self, conn, orden: OrdenHospitalizacion) -> OrdenHospitalizacion:
        query = """
            INSERT INTO orden_hospitalizacion (id_paciente, id_profesional, fecha, motivo, documento, estado)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_orden_hospitalizacion;
        """
        id_orden = await conn.fetchval(
            query,
            orden.id_paciente,
            orden.id_profesional,
            orden.fecha,
            orden.motivo,
            orden.documento,
            orden.estado
        )
        orden.id_orden_hospitalizacion = id_orden
        return orden

    async def update(self, conn, id: int, data: dict) -> Optional[OrdenHospitalizacion]:
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
            UPDATE orden_hospitalizacion 
            SET {', '.join(set_clauses)} 
            WHERE id_orden_hospitalizacion = ${idx} 
            RETURNING id_orden_hospitalizacion, id_paciente, id_profesional, fecha, motivo, documento, estado;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return OrdenHospitalizacion(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM orden_hospitalizacion WHERE id_orden_hospitalizacion = $1 RETURNING id_orden_hospitalizacion;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[OrdenHospitalizacion]:
        query = """
            SELECT id_orden_hospitalizacion, id_paciente, id_profesional,
                   fecha, motivo, documento, estado
            FROM orden_hospitalizacion
            WHERE id_paciente = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [OrdenHospitalizacion(**dict(row)) for row in rows]
