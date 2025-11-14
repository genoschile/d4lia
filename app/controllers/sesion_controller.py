from dataclasses import asdict
from typing import List
from asyncpg import PostgresError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.helpers.responses.response import (
    error_response,
    success_response,
)
from app.core.instance import get_sesion_services
from app.schemas.sesion_schema import SesionCreate, SesionResponse

router = APIRouter(prefix="/sesion", tags=["Sesiones"])


@router.get("/add", response_class=HTMLResponse)
async def add_sesion_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sesion.html", {"request": request})


# ----------- LISTAR SESIONES -----------
@router.get("/")
async def listar_sesiones(sesion_service=Depends(get_sesion_services)):

    sesiones = await sesion_service.get_all_sesiones()
    if not sesiones:
        return error_response(status_code=400, message="No se encontraron sesiones.")

    sesiones_response = [SesionResponse.model_validate(asdict(s)) for s in sesiones]

    return success_response(
        data=[s.model_dump(mode="json") for s in sesiones_response],
        message="Sesiones obtenidas correctamente",
    )


# ----------- LISTAR ENCUESTAS DE SESIONES -----------
@router.get("/encuestas/{id_sesion}")
async def listar_encuestas_sesion(
    id_sesion: int, sesion_service=Depends(get_sesion_services)
):

    encuestas = await sesion_service.get_encuestas_by_sesion(id_sesion)

    if not encuestas:
        return error_response(
            status_code=400, message="No se encontraron encuestas para esta sesión."
        )

    return success_response(
        data=[encuesta for encuesta in encuestas],
        message="Encuestas obtenidas correctamente",
    )


# ----------- CREAR SESIÓN -----------
@router.post("/")
async def crear_sesion(
    sesion_data: SesionCreate,
    sesion_service=Depends(get_sesion_services),
):

    nueva_sesion = await sesion_service.create_sesion(sesion_data)

    nueva_sesion_response = SesionResponse.model_validate(asdict(nueva_sesion))

    return success_response(
        data=nueva_sesion_response.model_dump(mode="json"),
        message="Sesión creada correctamente",
    )


# ----------- OBTENER SESIÓN POR ID -----------
@router.get("/{id_sesion}")
async def obtener_sesion(id_sesion: int, sesion_service=Depends(get_sesion_services)):
    try:
        sesion = await sesion_service.get_sesion_by_id(id_sesion)

        if not sesion:
            return error_response(status_code=404, message="Sesión no encontrada.")

        sesion_response = SesionResponse.model_validate(asdict(sesion))

        return success_response(
            data=sesion_response.model_dump(mode="json"),
            message="Sesión obtenida correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Sesiones por encargado
@router.get("/encargado/{id_encargado}")
async def obtener_sesiones_por_encargado(
    id_encargado: int, sesion_service=Depends(get_sesion_services)
):
    pass


# Actualizar sesión
@router.put("/{id_sesion}")
async def actualizar_sesion(
    id_sesion: int,
    sesion_data: SesionCreate,
    sesion_service=Depends(get_sesion_services),
):
    pass


# Cancelar sesión
@router.delete("/{id_sesion}")
async def cancelar_sesion(id_sesion: int, sesion_service=Depends(get_sesion_services)):
    pass
