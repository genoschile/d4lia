from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
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

@router.get("/paciente/add", response_class=HTMLResponse)
async def add_paciente_form(request: Request):
    return TEMPLATES.TemplateResponse("add_paciente.html", {"request": request})