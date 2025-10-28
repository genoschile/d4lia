from asyncpg import PostgresError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.domain.sillon import Sillon
from app.helpers.responses.response import error_response, success_response
from app.instance import get_sillon_services

router = APIRouter(prefix="/sillones", tags=["Sillones"])


@router.post("/")
async def create_sillon(sillon: Sillon, sillon_service=Depends(get_sillon_services)):
    try:
        await sillon_service.create_sillon(sillon)
        return {"message": "Sillon creado correctamente"}
    except PostgresError as e:
        # Error técnico de base de datos
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/")
async def listar_sillones(sillon_service=Depends(get_sillon_services)):
    try:
        sillones = await sillon_service.get_all_sillones()
        
        return success_response(
            data=sillones, message="Sillones obtenidos correctamente"
        )

    except PostgresError as e:
        # Error técnico de base de datos
        return error_response(
            message=f"Error en base de datos: {str(e)}", status_code=500
        )

    except Exception as e:
        # Cualquier otro error inesperado
        return error_response(message=f"Error interno: {str(e)}", status_code=500)


@router.get("/{sillon_id}")
async def obtener_sillon(sillon_id: int, sillon_service=Depends(get_sillon_services)):
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
