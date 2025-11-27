from typing import List, Optional
from datetime import date
from app.modules.consulta_medica.entities.consulta_medica_entity import ConsultaMedica
from app.modules.consulta_medica.interfaces.consulta_medica_interfaces import IConsultaMedicaRepository


class ConsultaMedicaRepository(IConsultaMedicaRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[ConsultaMedica]:
        query = """
            SELECT id_consulta, id_paciente, id_profesional, id_estado, especialidad,
                   fecha, fecha_programada, fecha_atencion, motivo, tratamiento, observaciones
            FROM consulta_medica
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query)
        return [ConsultaMedica(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[ConsultaMedica]:
        query = """
            SELECT id_consulta, id_paciente, id_profesional, id_estado, especialidad,
                   fecha, fecha_programada, fecha_atencion, motivo, tratamiento, observaciones
            FROM consulta_medica
            WHERE id_consulta = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return ConsultaMedica(**dict(row))
        return None

    async def create(self, conn, consulta: ConsultaMedica) -> ConsultaMedica:
        query = """
            INSERT INTO consulta_medica (id_paciente, id_profesional, id_estado, especialidad, fecha, fecha_programada, fecha_atencion, motivo, tratamiento, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id_consulta;
        """
        id_consulta = await conn.fetchval(
            query,
            consulta.id_paciente,
            consulta.id_profesional,
            consulta.id_estado,
            consulta.especialidad,
            consulta.fecha,
            consulta.fecha_programada,
            consulta.fecha_atencion,
            consulta.motivo,
            consulta.tratamiento,
            consulta.observaciones
        )
        consulta.id_consulta = id_consulta
        return consulta

    async def update(self, conn, id: int, data: dict) -> Optional[ConsultaMedica]:
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
            UPDATE consulta_medica 
            SET {', '.join(set_clauses)} 
            WHERE id_consulta = ${idx} 
            RETURNING id_consulta, id_paciente, id_profesional, id_estado, especialidad, fecha, fecha_programada, fecha_atencion, motivo, tratamiento, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return ConsultaMedica(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM consulta_medica WHERE id_consulta = $1 RETURNING id_consulta;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[ConsultaMedica]:
        query = """
            SELECT id_consulta, id_paciente, id_profesional, especialidad,
                   fecha, motivo, tratamiento, observaciones
            FROM consulta_medica
            WHERE id_paciente = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [ConsultaMedica(**dict(row)) for row in rows]

    async def get_by_profesional(self, conn, id_profesional: int) -> List[ConsultaMedica]:
        query = """
            SELECT id_consulta, id_paciente, id_profesional, especialidad,
                   fecha, motivo, tratamiento, observaciones
            FROM consulta_medica
            WHERE id_profesional = $1
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, id_profesional)
        return [ConsultaMedica(**dict(row)) for row in rows]

    async def get_by_fecha_range(self, conn, fecha_inicio: date, fecha_fin: date) -> List[ConsultaMedica]:
        query = """
            SELECT id_consulta, id_paciente, id_profesional, especialidad,
                   fecha, motivo, tratamiento, observaciones
            FROM consulta_medica
            WHERE fecha BETWEEN $1 AND $2
            ORDER BY fecha DESC;
        """
        rows = await conn.fetch(query, fecha_inicio, fecha_fin)
        return [ConsultaMedica(**dict(row)) for row in rows]
