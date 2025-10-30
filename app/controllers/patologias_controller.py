from typing import List
from asyncpg import PostgresError
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse
from dataclasses import asdict
from app.config.config import TEMPLATES
from app.domain.patologia_entity import Patologia
from app.helpers.responses.response import (
    error_response,
    success_response,
    success_response,
)
from app.instance import get_patologia_services
from app.schemas.patologia_schema import (
    PatologiaCreate,
    PatologiaResponse,
    PatologiaUpdate,
)
from app.use_case.patologia_service import PatologiaService


router = APIRouter(prefix="/patologia", tags=["Patologias"])


# ----------- FORMULARIO PARA AGREGAR PATOLOGIA -----------
@router.get("/add", response_class=HTMLResponse)
async def add_patologia_form(request: Request):
    return TEMPLATES.TemplateResponse("add_patologia.html", {"request": request})


# ----------- LISTAR PATOLOGIAS -----------
@router.get("/", response_model=List[PatologiaResponse])
async def listar_patologias(patologia_service=Depends(get_patologia_services)):
    try:
        patologias = await patologia_service.get_all_patologias()

        data = [
            PatologiaResponse.model_validate(asdict(p)).model_dump() for p in patologias
        ]

        return success_response(
            data=data,
            message="Patologías obtenidas correctamente",
        )
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- OBTENER PATOLOGIA POR ID -----------
@router.get("/{id_patologia}")
async def obtener_patologia_por_id(
    id_patologia: int,
    patologia_service: PatologiaService = Depends(get_patologia_services),
):
    try:
        patologia = await patologia_service.get_patologia_by_id(id_patologia)
        if not patologia:
            return error_response(status_code=404, message="Patología no encontrada")

        data = PatologiaResponse.model_validate(asdict(patologia)).model_dump()

        return success_response(data=data, message="Patología obtenida correctamente")

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- CREAR PATOLOGIA -----------
@router.post("/")
async def crear_patologia(
    patologia_in: PatologiaCreate, patologia_service=Depends(get_patologia_services)
):
    try:
        nueva_patologia = Patologia(**patologia_in.model_dump())

        creada = await patologia_service.create_patologia(nueva_patologia)
        data = PatologiaResponse.model_validate(asdict(creada)).model_dump()

        return success_response(data=data, message="Patología creada correctamente")

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- ELIMINAR PATOLOGIA -----------
@router.delete("/{id_patologia}")
async def eliminar_patologia(
    id_patologia: int, patologia_service=Depends(get_patologia_services)
):
    try:
        eliminado = await patologia_service.delete_patologia(id_patologia)

        if not eliminado:
            return error_response(
                status_code=404, message="Patología no encontrada o ya eliminada"
            )

        return success_response(
            data={"id_eliminado": id_patologia},
            message="Patología eliminada correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- ACTUALIZAR PATOLOGIA -----------
@router.patch("/{id_patologia}")
async def actualizar_patologia(
    id_patologia: int,
    body: PatologiaUpdate = Body(...),
    patologia_service=Depends(get_patologia_services),
):
    try:
        data = body.model_dump(exclude_unset=True)
        if not data:
            return error_response(
                status_code=400, message="No se enviaron campos para actualizar"
            )

        actualizado = await patologia_service.update_patologia(id_patologia, data)

        if not actualizado:
            return error_response(status_code=404, message="Patología no encontrada")

        return success_response(
            data={
                "id_actualizado": id_patologia,
                "campos_modificados": list(data.keys()),
            },
            message="Patología actualizada correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
