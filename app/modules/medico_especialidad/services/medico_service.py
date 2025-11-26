from app.modules.medico_especialidad.interfaces.medico_interfaces import IMedicoRepository
from app.modules.medico_especialidad.schemas.medico_especialidad_schema import MedicoResponse


class MedicoService:
    def __init__(
        self,
        pool,
        medico_repo: IMedicoRepository,
    ):
        self.pool = pool
        self.medico_repo = medico_repo

    async def listar_medicos(self) -> list[MedicoResponse]:
        medicos = await self.medico_repo.list_all(self.pool)
        return [MedicoResponse.from_orm(medico) for medico in medicos]
