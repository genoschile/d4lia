from app.domain.condicion_personal_entity import PacienteCondicion
from app.core.exceptions import NotFoundError, ValidationException
from app.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository
from app.schemas.condicion_schema import PacienteCondicionBase


class CondicionPersonalService(IPacienteCondicionRepository):
    def __init__(
        self,
        pool,
        paciente_condicion_repo: IPacienteCondicionRepository,
    ):
        self.pool = pool
        self.paciente_condicion_repo = paciente_condicion_repo

    async def asociar_condicion_a_paciente(
        self, id_paciente: int, data: PacienteCondicionBase
    ) -> PacienteCondicion:

        # Validar que la condición exista
        condicion = await self.paciente_condicion_repo.get_by_id(
            self.pool, data.id_condicion
        )
        if condicion is None:
            raise NotFoundError("La condición no existe.")

        # Validar fechas
        if data.fecha_resolucion and data.fecha_inicio:
            if data.fecha_resolucion < data.fecha_inicio:
                raise ValidationException(
                    "La fecha de resolución no puede ser menor a la fecha de inicio."
                )

        entity = PacienteCondicion(
            id_paciente=id_paciente,
            id_condicion=data.id_condicion,
            fecha_inicio=data.fecha_inicio,
            fecha_resolucion=data.fecha_resolucion,
            observaciones=data.observaciones,
            validada_medico=False,
        )

        new_relation = await self.paciente_condicion_repo.create(self.pool, entity)

        new_relation.condicion = condicion

        return new_relation
