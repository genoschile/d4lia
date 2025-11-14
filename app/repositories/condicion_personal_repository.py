from app.domain.condicion_personal_entity import (
    CondicionPersonal,
    Severidad,
    TipoCondicion,
)
from app.interfaces.condicion_personal_interfaces import ICondicionPersonalRepository


class CondicionPersonalRepository(ICondicionPersonalRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(
        self, conn, condicion_personal: CondicionPersonal
    ) -> CondicionPersonal:
        query = """
            INSERT INTO condicion_personal (codigo, nombre_condicion, tipo, severidad, observaciones)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id_condicion, codigo, nombre_condicion, tipo, severidad, observaciones
            """
        row = await conn.fetchrow(
            query,
            condicion_personal.codigo,
            condicion_personal.nombre_condicion,
            condicion_personal.tipo,
            condicion_personal.severidad,
            condicion_personal.observaciones,
        )
        return CondicionPersonal(
            id_condicion=row["id_condicion"],
            codigo=row["codigo"],
            nombre_condicion=row["nombre_condicion"],
            tipo=TipoCondicion(row["tipo"]),
            severidad=Severidad(row["severidad"]) if row["severidad"] else None,
            observaciones=row["observaciones"],
        )

    async def exists_by_name(self, conn, nombre_condicion: str) -> bool:
        query = """
            SELECT 1
            FROM condicion_personal
            WHERE nombre_condicion = $1
            LIMIT 1;
        """
        row = await conn.fetchrow(query, nombre_condicion)
        return row is not None
