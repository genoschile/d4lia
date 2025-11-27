from fastapi import APIRouter, Depends
from app.modules.estado.schemas.estado_schema import EstadoResponse
from app.modules.estado.services.estado_service import EstadoService
from app.modules.instance import get_estado_service
from app.helpers.response import success_response

router = APIRouter(prefix="/estado", tags=["Estado"])


@router.get("/", response_model=list[EstadoResponse])
async def listar_estados(
    service: EstadoService = Depends(get_estado_service),
):
    """Listar todos los estados disponibles"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Estados listados correctamente",
    )


@router.get("/{id}", response_model=EstadoResponse)
async def obtener_estado(
    id: int, service: EstadoService = Depends(get_estado_service)
):
    """Obtener un estado por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Estado obtenido correctamente"
    )
