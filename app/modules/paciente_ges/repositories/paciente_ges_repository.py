from typing import List, Optional
from datetime import date, timedelta
from app.modules.paciente_ges.entities.paciente_ges_entity import PacienteGes
from app.modules.paciente_ges.interfaces.paciente_ges_repository_interface import PacienteGesRepositoryInterface
from app.core.exceptions import NotFoundError


class PacienteGesRepository(PacienteGesRepositoryInterface):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[PacienteGes]:
        """Listar todos los GES de pacientes"""
        query = """
            SELECT id_paciente_ges, id_paciente, id_ges, id_diagnostico,
                   fecha_activacion, dias_limite, fecha_vencimiento,
                   estado, tipo_cobertura, activado_por, fecha_completado, observaciones
            FROM paciente_ges
            ORDER BY fecha_vencimiento ASC;
        """
        rows = await conn.fetch(query)
        return [PacienteGes(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[PacienteGes]:
        """Obtener un GES de paciente por ID"""
        query = """
            SELECT id_paciente_ges, id_paciente, id_ges, id_diagnostico,
                   fecha_activacion, dias_limite, fecha_vencimiento,
                   estado, tipo_cobertura, activado_por, fecha_completado, observaciones
            FROM paciente_ges
            WHERE id_paciente_ges = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return PacienteGes(**dict(row))
        return None

    async def create(self, conn, paciente_ges: PacienteGes) -> PacienteGes:
        """Crear un nuevo GES para paciente"""
        query = """
            INSERT INTO paciente_ges (
                id_paciente, id_ges, id_diagnostico, fecha_activacion,
                dias_limite, estado, tipo_cobertura, activado_por, observaciones
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id_paciente_ges, fecha_vencimiento;
        """
        row = await conn.fetchrow(
            query,
            paciente_ges.id_paciente,
            paciente_ges.id_ges,
            paciente_ges.id_diagnostico,
            paciente_ges.fecha_activacion,
            paciente_ges.dias_limite,
            paciente_ges.estado,
            paciente_ges.tipo_cobertura,
            paciente_ges.activado_por,
            paciente_ges.observaciones
        )
        paciente_ges.id_paciente_ges = row['id_paciente_ges']
        paciente_ges.fecha_vencimiento = row['fecha_vencimiento']
        return paciente_ges

    async def update(self, conn, id: int, data: dict) -> Optional[PacienteGes]:
        """Actualizar un GES de paciente"""
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
            UPDATE paciente_ges 
            SET {', '.join(set_clauses)} 
            WHERE id_paciente_ges = ${idx} 
            RETURNING id_paciente_ges, id_paciente, id_ges, id_diagnostico,
                      fecha_activacion, dias_limite, fecha_vencimiento,
                      estado, tipo_cobertura, activado_por, fecha_completado, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return PacienteGes(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        """Eliminar un GES de paciente"""
        query = "DELETE FROM paciente_ges WHERE id_paciente_ges = $1 RETURNING id_paciente_ges;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_paciente(self, conn, id_paciente: int) -> List[PacienteGes]:
        """Obtener todos los GES de un paciente"""
        query = """
            SELECT id_paciente_ges, id_paciente, id_ges, id_diagnostico,
                   fecha_activacion, dias_limite, fecha_vencimiento,
                   estado, tipo_cobertura, activado_por, fecha_completado, observaciones
            FROM paciente_ges
            WHERE id_paciente = $1
            ORDER BY fecha_vencimiento ASC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [PacienteGes(**dict(row)) for row in rows]

    async def get_activos_by_paciente(self, conn, id_paciente: int) -> List[PacienteGes]:
        """Obtener GES activos de un paciente"""
        query = """
            SELECT id_paciente_ges, id_paciente, id_ges, id_diagnostico,
                   fecha_activacion, dias_limite, fecha_vencimiento,
                   estado, tipo_cobertura, activado_por, fecha_completado, observaciones
            FROM paciente_ges
            WHERE id_paciente = $1 AND estado IN ('activo', 'en_proceso')
            ORDER BY fecha_vencimiento ASC;
        """
        rows = await conn.fetch(query, id_paciente)
        return [PacienteGes(**dict(row)) for row in rows]

    async def get_countdown_view(self, conn, filtro_estado: Optional[str] = None):
        """Obtener datos desde la vista de countdown"""
        if filtro_estado:
            query = """
                SELECT * FROM paciente_ges_countdown
                WHERE prioridad = $1
                ORDER BY dias_restantes ASC;
            """
            rows = await conn.fetch(query, filtro_estado)
        else:
            query = """
                SELECT * FROM paciente_ges_countdown
                ORDER BY dias_restantes ASC;
            """
            rows = await conn.fetch(query)
        
        return [dict(row) for row in rows]

    async def get_estadisticas(self, conn) -> dict:
        """Obtener estadísticas de GES"""
        query = """
            SELECT 
                COUNT(*) FILTER (WHERE estado IN ('activo', 'en_proceso')) as total_activos,
                COUNT(*) FILTER (WHERE estado IN ('activo', 'en_proceso') AND (fecha_vencimiento - CURRENT_DATE) <= 7) as criticos,
                COUNT(*) FILTER (WHERE estado IN ('activo', 'en_proceso') AND (fecha_vencimiento - CURRENT_DATE) <= 30) as urgentes,
                COUNT(*) FILTER (WHERE estado = 'vencido') as vencidos,
                COUNT(*) FILTER (WHERE estado = 'completado' AND fecha_completado >= CURRENT_DATE - INTERVAL '30 days') as completados_mes,
                COUNT(*) FILTER (WHERE estado = 'en_proceso') as en_proceso
            FROM paciente_ges;
        """
        row = await conn.fetchrow(query)
        return dict(row) if row else {}
