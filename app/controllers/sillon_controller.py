from asyncpg import PostgresError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES
from app.domain.sillon_entity import Sillon
from app.helpers.responses.response import error_response, success_response
from app.instance import get_sillon_services

# ----------- SCHEMAS -----------
from app.schemas.sillon_schema import (
    EstadoSillon,
    SillonCreate,
    SillonResponse,
    ubicacionSala,
)
from app.use_case.sillon_service import SillonService

router = APIRouter(prefix="/sillones", tags=["Sillones"])

# ----------- FORMULARIO PARA AGREGAR SILLON -----------
@router.get("/add", response_class=HTMLResponse)
async def add_sillon_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sillon.html", {"request": request})


# ----------- CREAR SILLON -----------
@router.post("/", response_model=SillonResponse)
async def create_sillon(
    sillon: SillonCreate, sillon_service=Depends(get_sillon_services)
):
    try:
        sillon_create = await sillon_service.create_sillon(sillon)

        if not sillon_create:
            return error_response(
                status_code=400, message="No se pudo crear el sillón."
            )

        return success_response(
            data=SillonResponse.model_validate(sillon_create).model_dump(),
            message="Sillón creado correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- LISTAR SILLONES -----------
@router.get("/", response_model=list[SillonResponse])
async def listar_sillones(sillon_service=Depends(get_sillon_services)):
    try:
        sillones = await sillon_service.get_all_sillones()
        sillones_response = [SillonResponse.model_validate(s) for s in sillones]

        return success_response(
            data=[s.model_dump() for s in sillones_response],
            message="Sillones obtenidos correctamente",
        )

    except PostgresError as e:
        return error_response(
            message=f"Error en base de datos: {str(e)}", status_code=500
        )

    except Exception as e:
        return error_response(message=f"Error interno: {str(e)}", status_code=500)


# ----------- OBTENER SILLON POR ID -----------
@router.get("/{sillon_id}")
async def obtener_sillon(sillon_id: int, sillon_service=Depends(get_sillon_services)):
    try:
        sillon = await sillon_service.get_sillon_by_id(sillon_id)
        sillon_response = SillonResponse.model_validate(sillon)

        return success_response(
            data=sillon_response.model_dump(),
            message="Sillón obtenido correctamente",
        )

    except ValueError as ve:
        return error_response(message=str(ve), status_code=404)

    except PostgresError as e:
        return error_response(
            message=f"Error en base de datos: {str(e)}", status_code=500
        )

    except Exception as e:
        return error_response(message=f"Error interno: {str(e)}", status_code=500)


# ----------- CAMBIAR ESTADO DEL SILLON -----------
@router.patch("/{id_sillon}/estado", response_model=SillonResponse)
async def cambiar_estado_sillon(
    id_sillon: int,
    nuevo_estado: EstadoSillon,
    motivo: str | None = None,
    sillon_service: SillonService = Depends(get_sillon_services),
):
    try:
        sillon_actualizado = await sillon_service.change_state_sillon(
            id_sillon, nuevo_estado, motivo
        )
        sillon_response = SillonResponse.model_validate(sillon_actualizado)

        return success_response(
            data=sillon_response.model_dump(),
            message="Estado del sillón actualizado correctamente",
        )

    except ValueError as ve:
        return error_response(message=str(ve), status_code=404)

    except PostgresError as e:
        return error_response(
            message=f"Error en base de datos: {str(e)}", status_code=500
        )

    except Exception as e:
        return error_response(message=f"Error interno: {str(e)}", status_code=500)


# ----------- ELIMINAR SILLON -----------
@router.delete("/{sillon_id}")
async def eliminar_sillon(
    sillon_id: int,
    sillon_service=Depends(get_sillon_services),
):
    try:
        await sillon_service.delete_sillon(sillon_id)
        return success_response(data=None, message="Sillón eliminado correctamente")

    except ValueError as ve:
        return error_response(status_code=404, message=str(ve))
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- CAMBIAR SALA DEL SILLON -----------
@router.patch("/{id_sillon}/sala", response_model=SillonResponse)
async def cambiar_sala_sillon(
    id_sillon: int,
    nueva_sala: ubicacionSala,
    sillon_service: SillonService = Depends(get_sillon_services),
):
    try:
        sillon_actualizado = await sillon_service.change_sala_sillon(
            id_sillon, nueva_sala
        )
        sillon_response = SillonResponse.model_validate(sillon_actualizado)

        return success_response(
            data=sillon_response.model_dump(),
            message="Sala del sillón actualizada correctamente",
        )

    except ValueError as ve:
        return error_response(message=str(ve), status_code=404)

    except PostgresError as e:
        return error_response(
            message=f"Error en base de datos: {str(e)}", status_code=500
        )

    except Exception as e:
        return error_response(message=f"Error interno: {str(e)}", status_code=500)
