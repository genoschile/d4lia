from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.domain.paciente import Paciente
from app.instance import get_paciente_services


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/")
async def listar_pacientes(paciente_service=Depends(get_paciente_services)):
    return await paciente_service.get_all_pacientes()


@router.get("/{paciente_id}")
async def obtener_paciente(
    paciente_id: str, paciente_service=Depends(get_paciente_services)
):
    pacientes = await paciente_service.get_all_pacientes()
    for p in pacientes:
        if p.id_paciente == paciente_id:
            return p
    return {"message": "Paciente no encontrado"}


@router.put("/{paciente_id}")
async def actualizar_paciente(
    paciente_id: str,
    paciente: Paciente,
    paciente_service=Depends(get_paciente_services),
):
    updated_paciente = await paciente_service.update_paciente(paciente_id, paciente)
    if updated_paciente:
        return {"message": "Paciente actualizado correctamente"}
    return {"message": "Paciente no encontrado"}


@router.delete("/{paciente_id}")
async def eliminar_paciente(
    paciente_id: str, paciente_service=Depends(get_paciente_services)
):
    deleted = await paciente_service.delete_paciente(paciente_id)
    if deleted:
        return {"message": "Paciente eliminado correctamente"}
    return {"message": "Paciente no encontrado"}


@router.post("/")
async def nuevo_paciente(
    paciente: Paciente, paciente_service=Depends(get_paciente_services)
):
    await paciente_service.create_paciente(paciente)
    return {"message": "Paciente creado correctamente"}


@router.get("/add", response_class=HTMLResponse)
async def add_paciente_form(request: Request):
    return TEMPLATES.TemplateResponse("add_paciente.html", {"request": request})
