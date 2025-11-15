from app.domain.condicion_personal_entity import PacienteCondicion
from app.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository


class PacienteCondicionRepository(IPacienteCondicionRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, conn, entity: PacienteCondicion) -> PacienteCondicion:
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
            entity.observaciones
        )

        return PacienteCondicion(
            id_paciente=row["id_paciente"],
            id_condicion=row["id_condicion"],
            fecha_inicio=row["fecha_inicio"],
            fecha_resolucion=row["fecha_resolucion"],
            validada_medico=row["validada_medico"],
            observaciones=row["observaciones"],
        )
