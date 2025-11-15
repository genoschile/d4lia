from app.domain.condicion_personal_entity import PacienteCondicion
from app.core.exceptions import NotFoundError, ValidationException
from app.interfaces.condicion_personal_interfaces import ICondicionPersonalRepository
from app.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository
from app.interfaces.paciente_interfaces import IPacienteRepository
from app.schemas.condicion_schema import (
    AsociarCondicionPacienteRequest,
    PacienteConCondicionesResponse,
    PacienteCondicionBase,
    PacienteCondicionResponse,
)


class PacienteCondicionService:
    def __init__(
        self,
        pool,
        paciente_condicion_repo: IPacienteCondicionRepository,
        paciente_repo: IPacienteRepository,
        condicion_repo: ICondicionPersonalRepository,
    ):
        self.pool = pool
        self.paciente_condicion_repo = paciente_condicion_repo
        self.paciente_repo = paciente_repo
        self.condicion_repo = condicion_repo

    async def asociar_condicion_a_paciente(
        self, id_paciente: int, data: AsociarCondicionPacienteRequest
    ) -> PacienteCondicionResponse:

        # Validar que la condición exista
        condicion = await self.condicion_repo.get_by_id(self.pool, data.id_condicion)

        # Validar que el paciente exista
        paciente = await self.paciente_repo.get_by_id(self.pool, id_paciente)

        if paciente is None:
            raise NotFoundError("El paciente no existe.")

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

        new_relation = await self.paciente_condicion_repo.asociar_a_paciente(
            self.pool, entity
        )

        return PacienteCondicionResponse.from_entity(new_relation)

    async def get_pacientes_con_condiciones(self):
        async with self.pool.acquire() as conn:

            rows = await self.paciente_condicion_repo.get_all_with_condiciones(
                conn
            )

            pacientes = {}

            for row in rows:
                pid = row["id_paciente"]

                # si el paciente no existe en el diccionario, crearlo
                if pid not in pacientes:
                    pacientes[pid] = {
                        "id_paciente": row["id_paciente"],
                        "rut": row["rut"],
                        "nombre_completo": row["nombre_completo"],
                        "correo": row["correo"],
                        "telefono": row["telefono"],
                        "edad": row["edad"],
                        "direccion": row["direccion"],
                        "antecedentes_medicos": row["antecedentes_medicos"],
                        "id_patologia": row["id_patologia"],
                        "fecha_inicio_tratamiento": row["fecha_inicio_tratamiento"],
                        "observaciones": row["observaciones"],
                        "condiciones": [],
                    }

                # Si no hay condición asociada, c_id_condicion será None → no agregar
                if row["c_id_condicion"] is not None:
                    pacientes[pid]["condiciones"].append(
                        PacienteCondicionResponse(
                            id_paciente=pid,
                            id_condicion=row["c_id_condicion"],
                            fecha_inicio=row["c_fecha_inicio"],
                            fecha_resolucion=row["c_fecha_resolucion"],
                            validada_medico=row["c_validada_medico"],
                            observaciones=row["c_observaciones"],
                        )
                    )

            # convertir diccionario → lista de response models
            return [
                PacienteConCondicionesResponse(**data) for data in pacientes.values()
            ]
