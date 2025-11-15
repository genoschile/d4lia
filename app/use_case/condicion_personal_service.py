from app.core.exceptions import AlreadyExistsException, DatabaseError, NotFoundError, ValidationException
from app.domain.condicion_personal_entity import (
    CondicionPersonal,
    Severidad,
    TipoCondicion,
)
from app.interfaces.condicion_personal_interfaces import ICondicionPersonalRepository
from app.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalResponse,
    CondicionPersonalUpdateRequest,
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

    async def get_condicion_personal_by_id(
        self, id_condicion: int
    ) -> CondicionPersonal | None:
        condicion = await self.condicion_personal_repo.get_by_id(
            self.pool, id_condicion
        )

        if not condicion:
            raise NotFoundError("Condición personal no encontrada")

        return condicion

    async def list_all_condiciones_personales(self) -> list[CondicionPersonal]:
        condiciones = await self.condicion_personal_repo.list_all(self.pool)
        return condiciones

    async def update_condicion_personal(
        self, id_condicion: int, data: CondicionPersonalUpdateRequest
    ) -> CondicionPersonal:

        # 1. Verificar si existe
        existente = await self.condicion_personal_repo.get_by_id(
            self.pool, id_condicion
        )
        if existente is None:
            raise NotFoundError("Condición personal no encontrada")

        # 2. Aplicar los cambios solo en los campos enviados
        campos_actualizados = data.model_dump(exclude_unset=True)

        # 3. Llamar al repo para actualizar
        actualizado = await self.condicion_personal_repo.update(
            self.pool, id_condicion, campos_actualizados
        )

        if actualizado is None:
            raise NotFoundError("Condición personal no encontrada al actualizar")

        return actualizado
    

    async def delete_condicion_personal(self, id_condicion: int) -> None:
        try:
            deleted = await self.condicion_personal_repo.delete(self.pool, id_condicion)

            if not deleted:
                raise NotFoundError("Condición personal no encontrada")

        except NotFoundError:
            raise
        except Exception as exc:
            raise DatabaseError(f"Error al eliminar condición personal: {exc}") from exc


    async def buscar_condiciones(self, codigo: str = "", nombre: str = "") -> list[CondicionPersonal]:

        if not codigo and not nombre:
            raise ValidationException("Debe enviar al menos un parámetro de búsqueda (código o nombre).")

        resultados = await self.condicion_personal_repo.search(self.pool, codigo, nombre)

        return resultados