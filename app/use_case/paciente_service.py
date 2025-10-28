# app/services/paciente_service.py
from typing import List, Optional
from app.domain.paciente import Paciente
from app.interfaces.paciente_interfaces import IPacienteRepository
from datetime import date

class PacienteService:
    def __init__(self, paciente_repo: IPacienteRepository):
        self.paciente_repo = paciente_repo

    async def create_paciente(self, paciente: Paciente) -> Paciente:
        return await self.paciente_repo.create(paciente)

    async def get_all_pacientes(self) -> List[Paciente]:
        return await self.paciente_repo.get_all()

    async def get_paciente_by_id(self, paciente_id: str) -> Optional[Paciente]:
        pacientes = await self.paciente_repo.get_all()
        for p in pacientes:
            if p.id_paciente == paciente_id:
                return p
        return None

    async def update_paciente(self, paciente_id: str, paciente: Paciente) -> Optional[Paciente]:
        return await self.paciente_repo.update(paciente_id, paciente) # type: ignore

    async def delete_paciente(self, paciente_id: str) -> bool:
        return await self.paciente_repo.delete(paciente_id) # type: ignore

    async def pacientes_en_tratamiento(self) -> List[Paciente]:
        pacientes = await self.paciente_repo.get_all()
        return [p for p in pacientes if p.en_tratamiento(date.today())]
