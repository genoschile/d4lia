# app/services/sesion_service.py
from typing import List, Optional

import httpx
from app.core.exceptions import AlreadyExistsException
from app.domain.sesion_entity import Sesion
from app.interfaces.paciente_interfaces import IPacienteRepository
from app.interfaces.patologia_interfaces import IPatologiaRepository
from app.interfaces.sesion_interfaces import ISesionRepository
from app.interfaces.sillon_interfaces import ISillonRepository
from app.schemas.event_schema import eventWebHooks
from app.config.environment import settings

WEBHOOK_URL_SESION_ADD = settings.WEBHOOK_SESION_ADD


class SesionService:
    def __init__(
        self,
        pool,
        sesion_repo: ISesionRepository,
        paciente_repo: IPacienteRepository,
        sillon_repo: ISillonRepository,
        patologia_repo: IPatologiaRepository,
    ):
        self.pool = pool
        self.sesion_repo = sesion_repo
        self.paciente_repo = paciente_repo
        self.sillon_repo = sillon_repo
        self.patologia_repo = patologia_repo

    async def get_all_sesiones(self) -> List[Sesion]:
        async with self.pool.acquire() as conn:
            return await self.sesion_repo.get_all(conn)

    async def get_encuestas_by_sesion(self, id_sesion: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            return await self.sesion_repo.get_encuestas_by_sesion(conn, id_sesion)

    async def create_sesion(self, sesion_data) -> Sesion:
        async with self.pool.acquire() as conn:

            # ---------------- 1️⃣ Validar referencias ----------------
            pacientes = await self.paciente_repo.get_all(conn)
            sillones = await self.sillon_repo.get_all(conn)
            patologias = await self.patologia_repo.get_all(conn)

            # Validar IDs obligatorios
            if sesion_data.id_paciente is None:
                raise ValueError("id_paciente no puede ser None")

            id_paciente: int = sesion_data.id_paciente

            if sesion_data.id_sillon is None:
                raise ValueError("id_sillon no puede ser None")

            id_sillon: int = sesion_data.id_sillon

            if sesion_data.id_patologia is None:
                raise ValueError("id_patologia no puede ser None")

            if sesion_data.id_paciente not in [p.id_paciente for p in pacientes]:
                raise ValueError("Paciente no existe")
            if sesion_data.id_sillon not in [s.id_sillon for s in sillones]:
                raise ValueError("Sillón no existe")
            if sesion_data.id_patologia not in [p.id_patologia for p in patologias]:
                raise ValueError("Patología no existe")

            async with conn.transaction():

                # ---------------- 2️⃣ Verificar duplicados ----------------
                existente = await self.sesion_repo.get_by_paciente_fecha_sillon(
                    conn, id_paciente, sesion_data.fecha, id_sillon
                )
                if existente:
                    raise AlreadyExistsException(
                        "Ya existe una sesión para este paciente en ese sillón a la misma fecha"
                    )

                # ---------------- 3️⃣ Crear sesión ----------------
                sesion = await self.sesion_repo.create(conn, sesion_data)

                # Convertir hora_inicio a string si viene como time
                hora_inicio_str = (
                    sesion.hora_inicio.strftime("%H:%M")
                    if not isinstance(sesion.hora_inicio, str)
                    else sesion.hora_inicio
                )

                # ---------------- 4️⃣ Llamar webhook en producción ----------------
                if settings.ENV == "production":
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(
                            WEBHOOK_URL_SESION_ADD,
                            json={
                                "evento": eventWebHooks.sesion_add.value,
                                "id_sesion": sesion.id_sesion,
                                "id_paciente": sesion.id_paciente,
                                "fecha": str(sesion.fecha),
                                "hora_inicio": hora_inicio_str,
                                "estado": sesion.estado.lower(),
                            },
                            timeout=5,
                        )
                        resp.raise_for_status()

                return sesion
