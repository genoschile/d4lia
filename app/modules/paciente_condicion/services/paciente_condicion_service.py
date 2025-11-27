from app.modules.paciente_condicion.entities.condicion_personal_entity import PacienteCondicion
from app.core.exceptions import NotFoundError, ValidationException
from app.modules.paciente_condicion.interfaces.condicion_personal_interfaces import ICondicionPersonalRepository
from app.modules.paciente_condicion.interfaces.paciente_condicion_interfaces import IPacienteCondicionRepository
from app.modules.paciente.interfaces.paciente_interfaces import IPacienteRepository
from app.modules.paciente_condicion.schemas.condicion_schema import (
    AsociarCondicionPacienteRequest,
    PacienteConCondicionesResponse,
    PacienteCondicionBase,
    PacienteCondicionResponse,
    PacienteCondicionUpdate,
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

            rows = await self.paciente_condicion_repo.get_all_with_condiciones(conn)

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

    async def listar_condiciones_de_paciente(
        self, id_paciente: int
    ) -> list[PacienteCondicionBase]:

        # Validar que el paciente exista
        paciente = await self.paciente_repo.get_by_id(self.pool, id_paciente)

        if paciente is None:
            raise NotFoundError("El paciente no existe.")

        condiciones = await self.paciente_condicion_repo.listar_condicion_por_paciente(
            self.pool, id_paciente
        )
        return PacienteCondicionBase.from_entity_list(condiciones)

    async def obtener_detalle_condicion_paciente(
        self, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:

        # Validar que el paciente exista
        paciente = await self.paciente_repo.get_by_id(self.pool, id_paciente)

        if paciente is None:
            raise NotFoundError("El paciente no existe.")

        condiciones = await self.paciente_condicion_repo.listar_condicion_por_paciente(
            self.pool, id_paciente
        )

        for condicion in condiciones:
            if condicion.id_condicion == id_condicion:
                return condicion

        raise NotFoundError("La condición asociada al paciente no existe.")

    async def actualizar_condicion_de_paciente(
        self,
        id_paciente: int,
        id_condicion: int,
        data: PacienteCondicionUpdate,
    ) -> PacienteCondicion:

        async with self.pool.acquire() as conn:

            # Verificar existencia
            condicion_actual = await self.paciente_condicion_repo.obtener_por_ids(
                conn,
                id_paciente,
                id_condicion,
            )

            if not condicion_actual:
                raise NotFoundError("La condición del paciente no existe")

            # Convertir DTO -> Entidad de dominio
            entidad_actualizada = PacienteCondicion.from_update(
                id_paciente=id_paciente,
                id_condicion=id_condicion,
                update=data,
            )

            # Pasar entidad al repositorio
            condicion_actualizada = (
                await self.paciente_condicion_repo.actualizar_condicion_de_paciente(
                    conn,
                    entidad_actualizada,
                )
            )

            return condicion_actualizada

    async def remover_condicion_de_paciente(
        self,
        id_paciente: int,
        id_condicion: int,
    ):
        async with self.pool.acquire() as conn:

            # Verificar existencia
            condicion = await self.paciente_condicion_repo.obtener_por_ids(
                conn,
                id_paciente,
                id_condicion,
            )

            if not condicion:
                raise NotFoundError("La condición del paciente no existe")

            # Eliminar
            await self.paciente_condicion_repo.remover_condicion(
                conn,
                id_paciente,
                id_condicion,
            )

    async def validar_condicion(
        self,
        id_paciente: int,
        id_condicion: int,
    ) -> PacienteCondicion:

        async with self.pool.acquire() as conn:

            # 1. Obtener la entidad
            condicion = await self.paciente_condicion_repo.obtener_por_ids(
                conn,
                id_paciente,
                id_condicion,
            )

            if not condicion:
                raise NotFoundError("La condición del paciente no existe")

            # 2. Aplicar REGLA DE DOMINIO
            condicion.validar()

            # 3. Persistir cambio
            condicion_actualizada = (
                await self.paciente_condicion_repo.validar_condicion(
                    conn,
                    id_paciente,
                    id_condicion,
                )
            )

            return condicion_actualizada

    async def invalidar_condicion(
        self, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:

        async with self.pool.acquire() as conn:

            # 1. Obtener entidad
            condicion = await self.paciente_condicion_repo.obtener_por_ids(
                conn,
                id_paciente,
                id_condicion,
            )

            if not condicion:
                raise NotFoundError("La condición del paciente no existe")

            # 2. Aplicar regla de dominio
            condicion.invalidar()

            # 3. Persistir en BD
            condicion_actualizada = (
                await self.paciente_condicion_repo.invalidar_condicion(
                    conn,
                    id_paciente,
                    id_condicion,
                )
            )

            return condicion_actualizada


    async def listar_condiciones_validadas(
        self,
        id_paciente: int,
    ) -> list[PacienteCondicion]:

        async with self.pool.acquire() as conn:

            condiciones = await self.paciente_condicion_repo.listar_condiciones_validadas(
                conn,
                id_paciente,
            )

            return condiciones

    async def listar_condiciones_no_validadas(
        self,
        id_paciente: int,
    ) -> list[PacienteCondicion]:

        async with self.pool.acquire() as conn:

            condiciones = await self.paciente_condicion_repo.listar_condiciones_no_validadas(
                conn,
                id_paciente,
            )

            return condiciones
