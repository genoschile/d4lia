from typing import List, Optional
from app.modules.medicamento.entities.medicamento_entity import Medicamento
from app.modules.medicamento.interfaces.medicamento_interfaces import IMedicamentoRepository


class MedicamentoRepository(IMedicamentoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Medicamento]:
        query = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, concentracion,
                   forma_farmaceutica, via_administracion, laboratorio, 
                   requiere_receta, stock_disponible, observaciones
            FROM medicamento
            ORDER BY nombre_comercial;
        """
        rows = await conn.fetch(query)
        return [Medicamento(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Medicamento]:
        query = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, concentracion,
                   forma_farmaceutica, via_administracion, laboratorio,
                   requiere_receta, stock_disponible, observaciones
            FROM medicamento
            WHERE id_medicamento = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Medicamento(**dict(row))
        return None

    async def create(self, conn, medicamento: Medicamento) -> Medicamento:
        query = """
            INSERT INTO medicamento (
                nombre_comercial, nombre_generico, concentracion, forma_farmaceutica,
                via_administracion, laboratorio, requiere_receta, stock_disponible, observaciones
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id_medicamento;
        """
        id_medicamento = await conn.fetchval(
            query,
            medicamento.nombre_comercial,
            medicamento.nombre_generico,
            medicamento.concentracion,
            medicamento.forma_farmaceutica,
            medicamento.via_administracion,
            medicamento.laboratorio,
            medicamento.requiere_receta,
            medicamento.stock_disponible,
            medicamento.observaciones
        )
        medicamento.id_medicamento = id_medicamento
        return medicamento

    async def update(self, conn, id: int, data: dict) -> Optional[Medicamento]:
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
            UPDATE medicamento 
            SET {', '.join(set_clauses)} 
            WHERE id_medicamento = ${idx} 
            RETURNING id_medicamento, nombre_comercial, nombre_generico, concentracion,
                      forma_farmaceutica, via_administracion, laboratorio,
                      requiere_receta, stock_disponible, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Medicamento(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM medicamento WHERE id_medicamento = $1 RETURNING id_medicamento;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_nombre_comercial(self, conn, nombre: str) -> Optional[Medicamento]:
        query = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, concentracion,
                   forma_farmaceutica, via_administracion, laboratorio,
                   requiere_receta, stock_disponible, observaciones
            FROM medicamento
            WHERE LOWER(nombre_comercial) = LOWER($1);
        """
        row = await conn.fetchrow(query, nombre)
        if row:
            return Medicamento(**dict(row))
        return None

    async def get_stock_bajo(self, conn, umbral: int = 10) -> List[Medicamento]:
        query = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, concentracion,
                   forma_farmaceutica, via_administracion, laboratorio,
                   requiere_receta, stock_disponible, observaciones
            FROM medicamento
            WHERE stock_disponible > 0 AND stock_disponible <= $1
            ORDER BY stock_disponible ASC;
        """
        rows = await conn.fetch(query, umbral)
        return [Medicamento(**dict(row)) for row in rows]

    async def get_by_laboratorio(self, conn, laboratorio: str) -> List[Medicamento]:
        query = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, concentracion,
                   forma_farmaceutica, via_administracion, laboratorio,
                   requiere_receta, stock_disponible, observaciones
            FROM medicamento
            WHERE LOWER(laboratorio) = LOWER($1)
            ORDER BY nombre_comercial;
        """
        rows = await conn.fetch(query, laboratorio)
        return [Medicamento(**dict(row)) for row in rows]
