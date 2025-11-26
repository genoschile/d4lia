from typing import List
import httpx
from app.config.config import APP_STATES
from app.core.error_handler import AlreadyExistsException
from app.modules.paciente.entities.paciente_entity import Paciente
from app.modules.patologia.entities.patologia_entity import Patologia
from app.helpers.validate_rut import validar_rut
from app.modules.paciente.interfaces.paciente_interfaces import IPacienteRepository
from app.modules.patologia.interfaces.patologia_interfaces import IPatologiaRepository
from app.modules.event_schema import eventWebHooks
from app.modules.paciente.schemas.paciente_schema import PacienteCreate
from app.config.environment import settings

WEBHOOK_URL_PACIENTE_ADD = settings.WEBHOOK_PACIENTE_ADD


class PacienteService:
    def __init__(
        self,
        pool,
        paciente_repo: IPacienteRepository,
        patologia_repo: IPatologiaRepository,
    ):
        self.pool = pool
        self.paciente_repo = paciente_repo
        self.patologia_repo = patologia_repo

    async def get_all_pacientes(self) -> List[Paciente]:
        async with self.pool.acquire() as conn:
            sillones = await self.paciente_repo.get_all(conn)
            return sillones

    async def create_paciente(self, paciente_data: PacienteCreate) -> Paciente:
        async with self.pool.acquire() as conn:

            patologias: list[Patologia] = await self.patologia_repo.get_all(conn)

            if paciente_data.id_patologia not in [p.id_patologia for p in patologias]:
                raise ValueError("La patología no existe")

            async with conn.transaction():

                existente = await self.paciente_repo.get_by_rut(conn, paciente_data.rut)

                if existente:
                    raise AlreadyExistsException(
                        f"Ya existe un paciente con el RUT {paciente_data.rut}"
                    )

                if settings.ENV == APP_STATES.PRODUCTION:
                    if not validar_rut(paciente_data.rut):
                        raise ValueError("RUT inválido")

                print(f"[DEV MODE] RUT no validado: {paciente_data.rut}")

                # 1️⃣ Crear paciente en la DB
                paciente = await self.paciente_repo.create(conn, paciente_data)

                # 2️⃣ Llamar webhook solo en producción
                if settings.ENV == APP_STATES.PRODUCTION:
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(
                            WEBHOOK_URL_PACIENTE_ADD,
                            json={
                                "evento": eventWebHooks.paciente_add.value,
                                "nombre": paciente.nombre_completo,
                                "rut": paciente.rut,
                                "correo": paciente.correo,
                                "fecha_inicio_tratamiento": str(
                                    paciente.fecha_inicio_tratamiento
                                ),
                            },
                            timeout=5,
                        )
                        resp.raise_for_status()

                return paciente

    async def delete_paciente(self, id_paciente: int) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                deleted = await self.paciente_repo.delete(conn, id_paciente)
                return deleted
