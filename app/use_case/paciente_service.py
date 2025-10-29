# app/services/paciente_service.py
from typing import List, Optional
import httpx
from app.domain.paciente_entity import Paciente
from app.interfaces.paciente_interfaces import IPacienteRepository
from datetime import date
from app.schemas.paciente_schema import PacienteCreate


WEBHOOK_URL = "https://webhook.site/tu-url"


class PacienteService:
    def __init__(self, pool, paciente_repo: IPacienteRepository):
        self.pool = pool
        self.paciente_repo = paciente_repo

    async def get_all_pacientes(self) -> List[Paciente]:
        async with self.pool.acquire() as conn:
            sillones = await self.paciente_repo.get_all(conn)
            return sillones
        
    async def create_paciente(self, paciente_data: PacienteCreate) -> Paciente:
        # Abrimos conexión y transacción
        async with self.pool.acquire() as conn:
            async with conn.transaction():  # 👈 transacción atómica
                # 1️⃣ Crear paciente en la DB
                paciente = await self.paciente_repo.create(conn, paciente_data)

                # 2️⃣ Llamar webhook
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        WEBHOOK_URL,
                        json={
                            "evento": "nuevo_paciente",
                            "nombre": paciente.nombre_completo,
                            "rut": paciente.rut,
                            "correo": paciente.correo,
                            "fecha_inicio_tratamiento": str(paciente.fecha_inicio_tratamiento),
                        },
                        timeout=5  # opcional: limitar tiempo
                    )
                    # 👀 Verificamos que el webhook respondió 2xx
                    resp.raise_for_status()  # lanza excepción si falla

                # 3️⃣ Si todo salió bien, la transacción se confirma automáticamente
                return paciente


