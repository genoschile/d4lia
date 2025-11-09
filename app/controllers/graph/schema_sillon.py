import strawberry
from typing import AsyncGenerator, List, Optional
from fastapi import Request
from app.events.sillon_event_manager import sillon_event_manager
from app.use_case.sillon_service import SillonService
from app.repositories.sillon_repository import SillonRepository

@strawberry.type
class SillonType:
    id_sillon: int
    ubicacion_sala: str
    estado: str
    observaciones: Optional[str]

@strawberry.type
class Query:
    @strawberry.field
    async def sillones(self, info) -> List[SillonType]:
        # Obtenemos la app y el pool desde el contexto
        request: Request = info.context["request"]
        pool = request.app.state.db_pool

        service = SillonService(pool, SillonRepository(pool))
        sillones = await service.get_all_sillones()
        return [SillonType(**s.to_dict()) for s in sillones]

    @strawberry.field
    async def sillon(self, info, id_sillon: int) -> Optional[SillonType]:
        request: Request = info.context["request"]
        pool = request.app.state.db_pool

        service = SillonService(pool, SillonRepository(pool))
        s = await service.get_sillon_by_id(id_sillon)
        return SillonType(**s.to_dict()) if s else None

# ------------------ SUBSCRIPTION ------------------
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def sillon_actualizado(self) -> AsyncGenerator[SillonType, None]:
        """
        Suscripción que envía cada sillón cuyo estado cambie.
        """
        async for sillon in sillon_event_manager.subscribe():
            yield SillonType(**sillon.to_dict())


# ------------------ SCHEMA ------------------
schema = strawberry.Schema(query=Query, subscription=Subscription)