from fastapi import APIRouter, HTTPException
from app.domain.paciente import Paciente
from app.repositories.paciente_repository import create_paciente, get_all_pacientes
from app.use_case import paciente_service


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/pacientes")
async def listar_pacientes():
    return await get_all_pacientes()


@router.post("/pacientes")
async def nuevo_paciente(paciente: Paciente):
    await create_paciente(paciente)
    return {"message": "Paciente creado correctamente"}
