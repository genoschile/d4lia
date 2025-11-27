from typing import List, Optional
from app.modules.diagnostico.entities.diagnostico_entity import Diagnostico
from app.modules.diagnostico.interfaces.diagnostico_interfaces import IDiagnosticoRepository


class DiagnosticoRepository(IDiagnosticoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Diagnostico]:
        query = """
            SELECT id_diagnostico, id_consulta_medica, id_cie10, id_ges,
                   descripcion, tipo, fecha_registro, observaciones
            FROM diagnostico
            ORDER BY fecha_registro DESC;
        """
        rows = await conn.fetch(query)
        return [Diagnostico(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Diagnostico]:
        query = """
            SELECT id_diagnostico, id_consulta_medica, id_cie10, id_ges,
                   descripcion, tipo, fecha_registro, observaciones
            FROM diagnostico
            WHERE id_diagnostico = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Diagnostico(**dict(row))
        return None

    async def create(self, conn, diagnostico: Diagnostico) -> Diagnostico:
        query = """
            INSERT INTO diagnostico (id_consulta_medica, id_cie10, id_ges, descripcion, tipo, fecha_registro, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id_diagnostico;
        """
        id_diagnostico = await conn.fetchval(
            query,
            diagnostico.id_consulta_medica,
            diagnostico.id_cie10,
            diagnostico.id_ges,
            diagnostico.descripcion,
            diagnostico.tipo,
            diagnostico.fecha_registro,
            diagnostico.observaciones
        )
        diagnostico.id_diagnostico = id_diagnostico
        return diagnostico

    async def update(self, conn, id: int, data: dict) -> Optional[Diagnostico]:
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
            UPDATE diagnostico 
            SET {', '.join(set_clauses)} 
            WHERE id_diagnostico = ${idx} 
            RETURNING id_diagnostico, id_consulta_medica, id_cie10, id_ges, descripcion, tipo, fecha_registro, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Diagnostico(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM diagnostico WHERE id_diagnostico = $1 RETURNING id_diagnostico;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_consulta(self, conn, id_consulta: int) -> List[Diagnostico]:
        query = """
            SELECT id_diagnostico, id_consulta_medica, id_cie10, id_ges,
                   descripcion, tipo, fecha_registro, observaciones
            FROM diagnostico
            WHERE id_consulta_medica = $1
            ORDER BY fecha_registro DESC;
        """
        rows = await conn.fetch(query, id_consulta)
        return [Diagnostico(**dict(row)) for row in rows]

    async def get_by_tipo(self, conn, tipo: str) -> List[Diagnostico]:
        query = """
            SELECT id_diagnostico, id_consulta_medica, id_cie10, id_ges,
                   descripcion, tipo, fecha_registro, observaciones
            FROM diagnostico
            WHERE tipo = $1
            ORDER BY fecha_registro DESC;
        """
        rows = await conn.fetch(query, tipo)
        return [Diagnostico(**dict(row)) for row in rows]

    async def get_con_ges(self, conn) -> List[Diagnostico]:
        query = """
            SELECT id_diagnostico, id_consulta_medica, id_cie10, id_ges,
                   descripcion, tipo, fecha_registro, observaciones
            FROM diagnostico
            WHERE id_ges IS NOT NULL
            ORDER BY fecha_registro DESC;
        """
        rows = await conn.fetch(query)
        return [Diagnostico(**dict(row)) for row in rows]
