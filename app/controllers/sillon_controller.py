from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.domain.paciente import Paciente
from app.domain.sillon import Sillon

router = APIRouter(prefix="/sillones", tags=["Sillones"])

@router.post("/")
async def create_sillon(sillon: Sillon):
    # await create_sillon(sillon)
    return {"message": "Sillon creado correctamente"}

@router.get("/")
async def listar_sillones():
    # return await get_all_sillones()
    pass

@router.get("/add", response_class=HTMLResponse)
async def add_sillon_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sillon.html", {"request": request})

@router.delete("/{sillon_id}")
async def eliminar_sillon(sillon_id: int):
    # await delete_sillon(sillon_id)
    return {"message": "Sillon eliminado correctamente"}

@router.put("/{sillon_id}")
async def actualizar_sillon(sillon_id: int, sillon: Sillon):
    # await update_sillon(sillon_id, sillon)
    pass