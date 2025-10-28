from typing import List, Optional
from app.domain.paciente import Paciente
from app.interfaces.paciente_interfaces import IPacienteRepository
import asyncpg  

class PacienteRepository(IPacienteRepository):

    def __init__(self, conn: asyncpg.Connection):
        """
        Recibe una conexión asyncpg.Connection.
        Esto hace que el repositorio sea testeable y no dependa del pool global.
        """
        self.conn = conn

    async def create(self, paciente: Paciente) -> Paciente:
        await self.conn.execute(
            """
            INSERT INTO paciente (
                id_paciente, nombre_completo, telefono, edad, direccion,
                antecedentes_medicos, id_patologia, fecha_inicio_tratamiento, observaciones
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
            paciente.id_paciente,
            paciente.nombre_completo,
            paciente.telefono,
            paciente.edad,
            paciente.direccion,
            paciente.antecedentes_medicos,
            paciente.id_patologia,
            paciente.fecha_inicio_tratamiento,
            paciente.observaciones
        )
        return paciente

    async def get_all(self) -> List[Paciente]:
        rows = await self.conn.fetch("SELECT * FROM paciente")
        return [Paciente(**dict(row)) for row in rows]

    async def update(self, paciente_id: int, paciente: Paciente) -> Optional[Paciente]:
        await self.conn.execute(
            """
            UPDATE paciente
            SET nombre_completo=$1, telefono=$2, edad=$3, direccion=$4,
                antecedentes_medicos=$5, id_patologia=$6, fecha_inicio_tratamiento=$7,
                observaciones=$8
            WHERE id_paciente=$9
            """,
            paciente.nombre_completo,
            paciente.telefono,
            paciente.edad,
            paciente.direccion,
            paciente.antecedentes_medicos,
            paciente.id_patologia,
            paciente.fecha_inicio_tratamiento,
            paciente.observaciones,
            paciente_id
        )
        return paciente  # Si no lanza error, se asumió que se actualizó

    async def delete(self, paciente_id: int) -> bool:
        result = await self.conn.execute(
            "DELETE FROM paciente WHERE id_paciente=$1",
            paciente_id
        )
        # result es algo como "DELETE X" donde X es el número de filas afectadas
        return result.startswith("DELETE")
