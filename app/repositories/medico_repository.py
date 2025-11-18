from app.domain.medico_especialidad_entity import Medico
from app.interfaces.medico_interfaces import IMedicoRepository


class MedicoRepository(IMedicoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> list[Medico]:
        query = "SELECT * FROM medicos;"
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            result = await cursor.fetchall()
            return result
