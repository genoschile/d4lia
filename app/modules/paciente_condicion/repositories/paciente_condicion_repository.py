from typing import Optional
from app.core.exceptions import NotFoundException
from app.modules.paciente_condicion.entities.condicion_personal_entity import PacienteCondicion
from app.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository
from app.modules.paciente_condicion.schemas.condicion_schema import PacienteCondicionUpdate


class PacienteCondicionRepository(IPacienteCondicionRepository):
    def __init__(self, pool):
        self.pool = pool

    async def asociar_a_paciente(
        self, conn, entity: PacienteCondicion
    ) -> PacienteCondicion:
        query = """
            INSERT INTO paciente_condicion
            (id_paciente, id_condicion, fecha_inicio, fecha_resolucion, validada_medico, observaciones)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id_paciente, id_condicion, fecha_inicio, fecha_resolucion, validada_medico, observaciones
        """

        row = await conn.fetchrow(
            query,
            entity.id_paciente,
            entity.id_condicion,
            entity.fecha_inicio,
            entity.fecha_resolucion,
            entity.validada_medico,
            entity.observaciones,
        )

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )

    async def get_all_with_condiciones(self, conn) -> list[dict]:
        query = """
            SELECT
                p.id_paciente,
                p.rut,
                p.nombre_completo,
                p.correo,
                p.telefono,
                p.edad,
                p.direccion,
                p.antecedentes_medicos,
                p.id_patologia,
                p.fecha_inicio_tratamiento,
                p.observaciones,

                pc.id_condicion AS c_id_condicion,
                pc.fecha_inicio AS c_fecha_inicio,
                pc.fecha_resolucion AS c_fecha_resolucion,
                pc.validada_medico AS c_validada_medico,
                pc.observaciones AS c_observaciones

            FROM paciente p
            LEFT JOIN paciente_condicion pc
                ON p.id_paciente = pc.id_paciente
            ORDER BY p.id_paciente, pc.fecha_inicio;
        """

        return await conn.fetch(query)

    async def listar_condicion_por_paciente(
        self, conn, id_paciente: int
    ) -> list[PacienteCondicion]:

        query = """
            SELECT
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
            FROM paciente_condicion
            WHERE id_paciente = $1
            ORDER BY fecha_inicio;
        """

        rows = await conn.fetch(query, id_paciente)

        return [
            PacienteCondicion(
                id_paciente=row["id_paciente"],
                id_condicion=row["id_condicion"],
                fecha_inicio=row["fecha_inicio"],
                fecha_resolucion=row["fecha_resolucion"],
                validada_medico=row["validada_medico"],
                observaciones=row["observaciones"],
            )
            for row in rows
        ]

    async def obtener_por_ids(
        self, conn, id_paciente: int, id_condicion: int
    ) -> Optional[PacienteCondicion]:

        print("obtener_por_ids en repo llamado con:", id_paciente, id_condicion)

        query = """
                SELECT
                    id_paciente,
                    id_condicion,
                    fecha_inicio,
                    fecha_resolucion,
                    validada_medico,
                    observaciones
                FROM paciente_condicion
                WHERE id_paciente = $1 AND id_condicion = $2
            """

        row = await conn.fetchrow(query, id_paciente, id_condicion)

        if not row:
            return None

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )

    async def actualizar_condicion_de_paciente(
        self, conn, entity: PacienteCondicion
    ) -> PacienteCondicion:
        query = """
            UPDATE paciente_condicion
            SET
                fecha_inicio = COALESCE($3, fecha_inicio),
                fecha_resolucion = COALESCE($4, fecha_resolucion),
                validada_medico = COALESCE($5, validada_medico),
                observaciones = COALESCE($6, observaciones)
            WHERE id_paciente = $1 AND id_condicion = $2
            RETURNING
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
        """

        row = await conn.fetchrow(
            query,
            entity.id_paciente,
            entity.id_condicion,
            entity.fecha_inicio,
            entity.fecha_resolucion,
            entity.validada_medico,
            entity.observaciones,
        )

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )

    async def remover_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> None:
        query = """
            DELETE FROM paciente_condicion
            WHERE id_paciente = $1 AND id_condicion = $2
        """

        result = await conn.execute(query, id_paciente, id_condicion)

        # asyncpg retorna: "DELETE 1", "DELETE 0", etc.
        if result == "DELETE 0":
            # Por seguridad, aunque ya lo comprobamos arriba
            raise NotFoundException("La condición del paciente no existe")

    async def validar_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:

        query = """
            UPDATE paciente_condicion
            SET validada_medico = TRUE
            WHERE id_paciente = $1 AND id_condicion = $2
            RETURNING
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
        """

        row = await conn.fetchrow(query, id_paciente, id_condicion)

        if not row:
            raise NotFoundException("La condición del paciente no existe")

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )

    async def invalidar_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:

        query = """
            UPDATE paciente_condicion
            SET validada_medico = FALSE
            WHERE id_paciente = $1 AND id_condicion = $2
            RETURNING
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
        """

        row = await conn.fetchrow(query, id_paciente, id_condicion)

        if not row:
            raise NotFoundException("La condición del paciente no existe")

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )

    async def listar_condiciones_validadas(
        self, conn, id_paciente: int
    ) -> list[PacienteCondicion]:

        query = """
            SELECT
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
            FROM paciente_condicion
            WHERE id_paciente = $1
            AND validada_medico = TRUE
            ORDER BY fecha_inicio;
        """

        rows = await conn.fetch(query, id_paciente)

        return [
            PacienteCondicion(
                id_paciente=row["id_paciente"],
                id_condicion=row["id_condicion"],
                fecha_inicio=row["fecha_inicio"],
                fecha_resolucion=row["fecha_resolucion"],
                validada_medico=row["validada_medico"],
                observaciones=row["observaciones"],
            )
            for row in rows
        ]

    async def listar_condiciones_no_validadas(
        self, conn, id_paciente: int
    ) -> list[PacienteCondicion]:

        query = """
            SELECT
                id_paciente,
                id_condicion,
                fecha_inicio,
                fecha_resolucion,
                validada_medico,
                observaciones
            FROM paciente_condicion
            WHERE id_paciente = $1
            AND validada_medico = FALSE
            ORDER BY fecha_inicio;
        """

        rows = await conn.fetch(query, id_paciente)

        return [
            PacienteCondicion(
                id_paciente=row["id_paciente"],
                id_condicion=row["id_condicion"],
                fecha_inicio=row["fecha_inicio"],
                fecha_resolucion=row["fecha_resolucion"],
                validada_medico=row["validada_medico"],
                observaciones=row["observaciones"],
            )
            for row in rows
        ]
