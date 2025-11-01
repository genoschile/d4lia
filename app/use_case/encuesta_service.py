from app.helpers.generate_token import generar_token
from app.domain.encuesta_entity import Encuesta
from app.interfaces.encuesta_interfaces import IEncuestaRepository
from app.interfaces.paciente_interfaces import IPacienteRepository
from app.interfaces.sesion_interfaces import ISesionRepository


class EncuestaService:
    def __init__(
        self,
        pool,
        encuesta_repo: IEncuestaRepository,
        paciente_repo: IPacienteRepository,
        sesion_repo: ISesionRepository,
    ):
        self.pool = pool
        self.encuesta_repo = encuesta_repo
        self.paciente_repo = paciente_repo
        self.sesion_repo = sesion_repo

    async def create_encuesta(self, encuesta: Encuesta) -> Encuesta:
        return await self.encuesta_repo.create(encuesta)

    async def create_link(self, paciente_id: int, sesion_id: int) -> str:
        async with self.pool.acquire() as conn:
            async with conn.transaction():

                paciente = await self.paciente_repo.get_by_id(conn, paciente_id)
                if not paciente:
                    raise ValueError("Paciente no encontrado")

                sesion = await self.sesion_repo.get_by_id(conn, sesion_id)
                if not sesion:
                    raise ValueError("Sesión no encontrada")

                if sesion.id_paciente != paciente_id:
                    raise ValueError("La sesión no pertenece al paciente")

                token = generar_token(paciente_id, sesion_id)
                return token
