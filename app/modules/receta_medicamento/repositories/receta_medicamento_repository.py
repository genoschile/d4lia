from typing import List
from app.modules.receta_medicamento.entities.receta_medicamento_entity import RecetaMedicamento
from app.modules.receta_medicamento.interfaces.receta_medicamento_interfaces import IRecetaMedicamentoRepository


class RecetaMedicamentoRepository(IRecetaMedicamentoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, conn, receta_medicamento: RecetaMedicamento) -> RecetaMedicamento:
        query = """
            INSERT INTO receta_medicamento (id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones;
        """
        row = await conn.fetchrow(
            query,
            receta_medicamento.id_receta,
            receta_medicamento.id_medicamento,
            receta_medicamento.dosis,
            receta_medicamento.frecuencia,
            receta_medicamento.duracion,
            receta_medicamento.instrucciones
        )
        return RecetaMedicamento(**dict(row))

    async def update(self, conn, id_receta: int, id_medicamento: int, data: dict) -> RecetaMedicamento:
        set_clauses = []
        values = []
        idx = 1
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
            idx += 1
        
        if not set_clauses:
            # Si no hay cambios, retornar el actual
            query = """
                SELECT id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones
                FROM receta_medicamento
                WHERE id_receta = $1 AND id_medicamento = $2;
            """
            row = await conn.fetchrow(query, id_receta, id_medicamento)
            return RecetaMedicamento(**dict(row)) if row else None
        
        values.extend([id_receta, id_medicamento])
        query = f"""
            UPDATE receta_medicamento 
            SET {', '.join(set_clauses)} 
            WHERE id_receta = ${idx} AND id_medicamento = ${idx + 1}
            RETURNING id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones;
        """
        
        row = await conn.fetchrow(query, *values)
        return RecetaMedicamento(**dict(row)) if row else None

    async def delete(self, conn, id_receta: int, id_medicamento: int) -> bool:
        query = """
            DELETE FROM receta_medicamento 
            WHERE id_receta = $1 AND id_medicamento = $2
            RETURNING id_receta;
        """
        deleted_id = await conn.fetchval(query, id_receta, id_medicamento)
        return deleted_id is not None

    async def get_medicamentos_by_receta(self, conn, id_receta: int) -> List[dict]:
        query = """
            SELECT rm.id_receta, rm.id_medicamento, rm.dosis, rm.frecuencia, rm.duracion, rm.instrucciones,
                   m.nombre_comercial, m.nombre_generico, m.concentracion, m.forma_farmaceutica
            FROM receta_medicamento rm
            JOIN medicamento m ON rm.id_medicamento = m.id_medicamento
            WHERE rm.id_receta = $1
            ORDER BY m.nombre_comercial;
        """
        rows = await conn.fetch(query, id_receta)
        return [dict(row) for row in rows]

    async def get_recetas_by_medicamento(self, conn, id_medicamento: int) -> List[dict]:
        query = """
            SELECT rm.id_receta, rm.id_medicamento, rm.dosis, rm.frecuencia, rm.duracion, rm.instrucciones,
                   r.id_paciente, r.fecha_inicio, r.fecha_fin
            FROM receta_medicamento rm
            JOIN receta r ON rm.id_receta = r.id_receta
            WHERE rm.id_medicamento = $1
            ORDER BY r.fecha_inicio DESC;
        """
        rows = await conn.fetch(query, id_medicamento)
        return [dict(row) for row in rows]

    async def exists(self, conn, id_receta: int, id_medicamento: int) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1 FROM receta_medicamento 
                WHERE id_receta = $1 AND id_medicamento = $2
            );
        """
        return await conn.fetchval(query, id_receta, id_medicamento)

    async def list_all(self, conn) -> List[dict]:
        query = """
            SELECT rm.id_receta, rm.id_medicamento, rm.dosis, rm.frecuencia, rm.duracion, rm.instrucciones,
                   m.nombre_comercial, m.nombre_generico
            FROM receta_medicamento rm
            JOIN medicamento m ON rm.id_medicamento = m.id_medicamento
            ORDER BY rm.id_receta, m.nombre_comercial;
        """
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
