from app.domain.condicion_personal_entity import PacienteCondicion
from app.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository


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
