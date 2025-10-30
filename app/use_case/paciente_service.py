# app/services/paciente_service.py
from typing import List
import httpx
from app.domain.paciente_entity import Paciente
from app.interfaces.paciente_interfaces import IPacienteRepository
from app.schemas.paciente_schema import PacienteCreate
from app.config.environment import settings

WEBHOOK_URL_PACIENTE_ADD = settings.WEBHOOK_PACIENTE_ADD

class PacienteService:
    def __init__(self, pool, paciente_repo: IPacienteRepository):
        self.pool = pool
        self.paciente_repo = paciente_repo

    async def get_all_pacientes(self) -> List[Paciente]:
        async with self.pool.acquire() as conn:
            sillones = await self.paciente_repo.get_all(conn)
            return sillones
        
    async def create_paciente(self, paciente_data: PacienteCreate) -> Paciente:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 1️⃣ Crear paciente en la DB
                paciente = await self.paciente_repo.create(conn, paciente_data)

                # 2️⃣ Llamar webhook solo en producción
                if settings.ENV == "production":
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(
                            WEBHOOK_URL_PACIENTE_ADD,
                            json={
                                "evento": "nuevo_paciente",
                                "nombre": paciente.nombre_completo,
                                "rut": paciente.rut,
                                "correo": paciente.correo,
                                "fecha_inicio_tratamiento": str(paciente.fecha_inicio_tratamiento),
                            },
                            timeout=5
                        )
                        resp.raise_for_status()

                return paciente
