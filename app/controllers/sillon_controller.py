from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.domain.sillon import Sillon
from app.instance import get_sillon_services

router = APIRouter(prefix="/sillones", tags=["Sillones"])


@router.post("/")
async def create_sillon(sillon: Sillon, sillon_service=Depends(get_sillon_services)):
    await sillon_service.create_sillon(sillon)
    return {"message": "Sillon creado correctamente"}


@router.get("/")
async def listar_sillones(sillon_service=Depends(get_sillon_services)):
    return await sillon_service.get_all_sillones()

@router.get("/{sillon_id}")
async def obtener_sillon(
    sillon_id: int, sillon_service=Depends(get_sillon_services)
):
    sillones = await sillon_service.get_all_sillones()
    for s in sillones:
        if s.id == sillon_id:  # type: ignore
            return s
    return {"message": "Sillon no encontrado"}

@router.get("/add", response_class=HTMLResponse)
async def add_sillon_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sillon.html", {"request": request})


@router.delete("/{sillon_id}")
async def eliminar_sillon(sillon_id: int, sillon_service=Depends(get_sillon_services)):
    await sillon_service.delete_sillon(sillon_id)
    return {"message": "Sillon eliminado correctamente"}


@router.put("/{sillon_id}")
async def actualizar_sillon(
    sillon_id: int, sillon: Sillon, sillon_service=Depends(get_sillon_services)
):
    await sillon_service.update_sillon(sillon_id, sillon)
    return {"message": "Sillon actualizado correctamente"}
