from app.repositories import paciente_repository
from app.domain.paciente import Paciente
from datetime import date

async def listar_pacientes():
    return await paciente_repository.get_all_pacientes()

async def obtener_paciente(id_paciente: str):
    return await paciente_repository.get_paciente_by_id(id_paciente)

async def pacientes_en_tratamiento():
    pacientes = await paciente_repository.get_all_pacientes()
    return [p for p in pacientes if p.en_tratamiento(date.today())]
