from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.config.config import TEMPLATES
from app.domain.patologia_entity import Patologia
from app.instance import get_patologia_services


router = APIRouter(prefix="/patologia", tags=["Patologias"])


@router.get("/")
async def listar_patologias(patologia_service=Depends(get_patologia_services)):
    return await patologia_service.get_all_patologias()


@router.get("/{patologia_id}")
async def obtener_patologia(
    patologia_id: int, patologia_service=Depends(get_patologia_services)
):
    patologias = await patologia_service.get_all_patologias()
    for p in patologias:
        if p.id == patologia_id:  # type: ignore
            return p
    return {"message": "Patologia no encontrada"}


@router.put("/{patologia_id}")
async def actualizar_patologia(
    patologia_id: int,
    patologia: Patologia,
    patologia_service=Depends(get_patologia_services),
):
    updated_patologia = await patologia_service.update_patologia(
        patologia_id, patologia
    )
    if updated_patologia:
        return {"message": "Patologia actualizada correctamente"}
    return {"message": "Patologia no encontrada"}


@router.post("/")
async def nueva_patologia(
    patologia: Patologia, patologia_service=Depends(get_patologia_services)
):
    await patologia_service.create_patologia(patologia)
    return {"message": "Patologia creada correctamente"}


@router.delete("/{patologia_id}")
async def eliminar_patologia(
    patologia_id: int, patologia_service=Depends(get_patologia_services)
):
    deleted = await patologia_service.delete_patologia(patologia_id)
    if deleted:
        return {"message": "Patologia eliminada correctamente"}
    return {"message": "Patologia no encontrada"}


@router.get("/add", response_class=HTMLResponse)
async def add_patologia_form(request: Request):
    return TEMPLATES.TemplateResponse("add_patologia.html", {"request": request})
