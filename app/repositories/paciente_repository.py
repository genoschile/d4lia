from app.database.database import execute_query, fetch_query
from app.domain.paciente import Paciente

async def get_all_pacientes():
    rows = await fetch_query("SELECT * FROM paciente")
    return [Paciente(**dict(row)) for row in rows]

async def get_paciente_by_id(id_paciente: str):
    rows = await fetch_query("SELECT * FROM paciente WHERE id_paciente = $1", id_paciente)
    return Paciente(**dict(rows[0])) if rows else None

async def create_paciente(paciente: Paciente):
    await execute_query("""
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
    paciente.observaciones)
