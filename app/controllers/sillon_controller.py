from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
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


@router.get("/sillon/add", response_class=HTMLResponse)
async def add_sillon_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sillon.html", {"request": request})
