from fastapi import APIRouter, HTTPException
from app.domain.paciente import Paciente
from app.repositories.paciente_repository import create_paciente, get_all_pacientes


router = APIRouter(prefix="/sillones", tags=["Sillones"])


@router.get("/pacientes")
async def listar_pacientes():
    return await get_all_pacientes()


@router.post("/sillones")
async def nuevo_paciente(paciente: Paciente):
    await create_paciente(paciente)
    return {"message": "Paciente creado correctamente"}
