from typing import List, Optional
from app.domain.paciente_entity import Paciente
from app.interfaces.paciente_interfaces import IPacienteRepository


class PacienteRepository(IPacienteRepository):

    def __init__(self, pool):
        self.pool = pool

    async def get_all(self, conn) -> List[Paciente]:
        query = """
            SELECT 
                id_paciente,
                rut,
                nombre_completo,
                correo,
                telefono,
                edad,
                direccion,
                antecedentes_medicos,
                id_patologia,
                fecha_inicio_tratamiento,
                observaciones
            FROM paciente
            ORDER BY id_paciente;
        """

        rows = await conn.fetch(query)

        pacientes = [Paciente(**dict(row)) for row in rows]
        return pacientes


    async def create(self, conn, paciente_data) -> Paciente:
        query = """
            INSERT INTO paciente (
                rut,
                nombre_completo,
                correo,
                telefono,
                edad,
                direccion,
                antecedentes_medicos,
                id_patologia,
                fecha_inicio_tratamiento,
                observaciones
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
            )
            RETURNING 
                id_paciente,
                rut,
                nombre_completo,
                correo,
                telefono,
                edad,
                direccion,
                antecedentes_medicos,
                id_patologia,
                fecha_inicio_tratamiento,
                observaciones;
        """
        row = await conn.fetchrow(
            query,
            paciente_data.rut,
            paciente_data.nombre_completo,
            paciente_data.correo,
            paciente_data.telefono,
            paciente_data.edad,
            paciente_data.direccion,
            paciente_data.antecedentes_medicos,
            paciente_data.id_patologia,
            paciente_data.fecha_inicio_tratamiento,
            paciente_data.observaciones,
        )
        paciente = Paciente(**dict(row))
        return paciente