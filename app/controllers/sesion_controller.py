from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.instance import get_sesion_services

router = APIRouter(prefix="/sesion", tags=["Sesiones"])


@router.get("/add", response_class=HTMLResponse)
async def add_sesion_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sesion.html", {"request": request})


@router.post("/")
async def create_sesion(sesion: dict, sesion_service=Depends(get_sesion_services)):
    await sesion_service.create_sesion(sesion)
    return {"message": "Sesion creada correctamente"}


@router.get("/")
async def listar_sesiones(sesion_service=Depends(get_sesion_services)):
    return await sesion_service.get_all_sesiones()


@router.get("/{sesion_id}")
async def obtener_sesion(sesion_id: int, sesion_service=Depends(get_sesion_services)):
    sesiones = await sesion_service.get_all_sesiones()
    for s in sesiones:
        if s.id == sesion_id:  # type: ignore
            return s
    return {"message": "Sesion no encontrada"}


@router.delete("/{sesion_id}")
async def eliminar_sesion(sesion_id: int, sesion_service=Depends(get_sesion_services)):
    await sesion_service.delete_sesion(sesion_id)
    return {"message": "Sesion eliminada correctamente"}


@router.put("/{sesion_id}")
async def actualizar_sesion(
    sesion_id: int, sesion: dict, sesion_service=Depends(get_sesion_services)
):
    await sesion_service.update_sesion(sesion_id, sesion)
    return {"message": "Sesion actualizada correctamente"}
