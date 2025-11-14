from app.core.exceptions import AlreadyExistsException
from app.domain.condicion_personal_entity import (
    CondicionPersonal,
    Severidad,
    TipoCondicion,
)
from app.interfaces.condicion_personal_interfaces import ICondicionPersonalRepository
from app.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalResponse,
)


class CondicionPersonalService:
    def __init__(
        self,
        pool,
        condicion_personal_repo: ICondicionPersonalRepository,
    ):
        self.pool = pool
        self.condicion_personal_repo = condicion_personal_repo

    @staticmethod
    def to_entity(dto: CondicionPersonalCreate) -> CondicionPersonal:
        tipo = TipoCondicion[dto.tipo] if dto.tipo else TipoCondicion.preexistencia
        severidad = Severidad[dto.severidad] if dto.severidad else None

        return CondicionPersonal(
            id_condicion=None,
            codigo=dto.codigo,
            nombre_condicion=dto.nombre_condicion,
            tipo=tipo,
            severidad=severidad,
            observaciones=dto.observaciones,
        )

    async def create_condicion_personal(
        self, data: CondicionPersonalCreate
    ) -> CondicionPersonal:

        entidad = self.to_entity(data)

        if await self.condicion_personal_repo.exists_by_name(
            self.pool, data.nombre_condicion
        ):
            raise AlreadyExistsException("La condición ya existe.")

        new_condition = await self.condicion_personal_repo.create(self.pool, entidad)

        return new_condition
