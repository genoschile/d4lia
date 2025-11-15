from fastapi.exceptions import ValidationException
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

    async def get_by_id(self, conn, id_condicion: int) -> CondicionPersonal | None:
        query = """
            SELECT id_condicion, codigo, nombre_condicion, tipo, severidad, observaciones
            FROM condicion_personal
            WHERE id_condicion = $1;
        """
        row = await conn.fetchrow(query, id_condicion)

        if not row:
            return None

        try:
            return CondicionPersonal(
                id_condicion=row["id_condicion"],
                codigo=row["codigo"],
                nombre_condicion=row["nombre_condicion"],
                tipo=TipoCondicion(row["tipo"]),
                severidad=Severidad(row["severidad"]) if row["severidad"] else None,
                observaciones=row["observaciones"],
            )
        except ValueError as exc:
            raise ValidationException(f"Valor inválido en BD: {exc}")

    async def list_all(self, conn) -> list[CondicionPersonal]:
        query = """
            SELECT id_condicion, codigo, nombre_condicion, tipo, severidad, observaciones
            FROM condicion_personal;
        """
        rows = await conn.fetch(query)
        condiciones = []

        for row in rows:
            condiciones.append(
                CondicionPersonal(
                    id_condicion=row["id_condicion"],
                    codigo=row["codigo"],
                    nombre_condicion=row["nombre_condicion"],
                    tipo=TipoCondicion(row["tipo"]),
                    severidad=Severidad(row["severidad"]) if row["severidad"] else None,
                    observaciones=row["observaciones"],
                )
            )
        return condiciones


    async def update(self, conn, id_condicion: int, data: dict) -> CondicionPersonal | None:

        set_clauses = []
        values = []

        for i, (campo, valor) in enumerate(data.items(), start=1):
            set_clauses.append(f"{campo} = ${i}")
            values.append(valor)

        # Si no hay campos, no hacemos nada
        if not set_clauses:
            raise ValidationException("No se enviaron campos para actualizar")

        query = f"""
            UPDATE condicion_personal
            SET {', '.join(set_clauses)}
            WHERE id_condicion = ${len(values)+1}
            RETURNING id_condicion, codigo, nombre_condicion, tipo, severidad, observaciones;
        """

        values.append(id_condicion)

        row = await conn.fetchrow(query, *values)

        if not row:
            return None

        try:
            return CondicionPersonal(
                id_condicion=row["id_condicion"],
                codigo=row["codigo"],
                nombre_condicion=row["nombre_condicion"],
                tipo=TipoCondicion(row["tipo"]),
                severidad=Severidad(row["severidad"]) if row["severidad"] else None,
                observaciones=row["observaciones"],
            )
        except ValueError as exc:
            raise ValidationException(f"Valor inválido en BD: {exc}")


    async def delete(self, conn, id_condicion: int) -> bool:
        query = """
            DELETE FROM condicion_personal
            WHERE id_condicion = $1
        """
        result = await conn.execute(query, id_condicion)

        # result = "DELETE 1" si eliminó
        return result == "DELETE 1"

    async def search(self, conn, codigo: str = "", nombre: str = "") -> list[CondicionPersonal]:
        filtros = []
        valores = []

        if codigo:
            filtros.append("codigo ILIKE $" + str(len(valores) + 1))
            valores.append(f"%{codigo}%")

        if nombre:
            filtros.append("nombre_condicion ILIKE $" + str(len(valores) + 1))
            valores.append(f"%{nombre}%")

        where_clause = " AND ".join(filtros)

        query = f"""
            SELECT id_condicion, codigo, nombre_condicion, tipo, severidad, observaciones
            FROM condicion_personal
            WHERE {where_clause};
        """

        rows = await conn.fetch(query, *valores)

        condiciones = []
        for row in rows:
            condiciones.append(
                CondicionPersonal(
                    id_condicion=row["id_condicion"],
                    codigo=row["codigo"],
                    nombre_condicion=row["nombre_condicion"],
                    tipo=TipoCondicion(row["tipo"]),
                    severidad=Severidad(row["severidad"]) if row["severidad"] else None,
                    observaciones=row["observaciones"]
                )
            )

        return condiciones
