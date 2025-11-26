from typing import List, Optional
from app.modules.medico_especialidad.entities.medico_especialidad_entity import Medico, Rut, Especializacion
from app.modules.medico_especialidad.interfaces.medico_interfaces import IMedicoRepository


class MedicoRepository(IMedicoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> list[Medico]:
        query = "SELECT id_medico, rut, nombre, apellido, sexo FROM medico;"
        rows = await conn.fetch(query)
        return [
            Medico(
                id_medico=row['id_medico'],
                rut=Rut(row['rut']),
                nombre=row['nombre'],
                apellido=row['apellido'],
                sexo=row['sexo']
            ) for row in rows
        ]

    async def create(self, conn, medico: Medico) -> Medico:
        query = """
            INSERT INTO medico (rut, nombre, apellido, sexo, activo)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id_medico;
        """
        id_medico = await conn.fetchval(
            query,
            medico.rut.value,
            medico.nombre,
            medico.apellido,
            medico.sexo,
            medico.activo
        )
        medico.id_medico = id_medico
        return medico

    async def get_by_id(self, conn, id: int) -> Optional[Medico]:
        query = "SELECT id_medico, rut, nombre, apellido, sexo FROM medico WHERE id_medico = $1;"
        row = await conn.fetchrow(query, id)
        if row:
            return Medico(
                id_medico=row['id_medico'],
                rut=Rut(row['rut']),
                nombre=row['nombre'],
                apellido=row['apellido'],
                sexo=row['sexo']
            )
        return None

    async def get_by_rut(self, conn, rut: str) -> Optional[Medico]:
        query = "SELECT id_medico, rut, nombre, apellido, sexo FROM medico WHERE rut = $1;"
        row = await conn.fetchrow(query, rut)
        if row:
            return Medico(
                id_medico=row['id_medico'],
                rut=Rut(row['rut']),
                nombre=row['nombre'],
                apellido=row['apellido'],
                sexo=row['sexo']
            )
        return None

    async def list_active(self, conn) -> List[Medico]:
        query = "SELECT id_medico, rut, nombre, apellido, sexo FROM medico WHERE activo = TRUE;"
        rows = await conn.fetch(query)
        return [
            Medico(
                id_medico=row['id_medico'],
                rut=Rut(row['rut']),
                nombre=row['nombre'],
                apellido=row['apellido'],
                sexo=row['sexo']
            ) for row in rows
        ]

    async def assign_specialty(self, conn, id_medico: int, id_especialidad: int):
        query = """
            INSERT INTO consulta_profesional (id_medico, id_especializacion, fecha_registro)
            VALUES ($1, $2, CURRENT_DATE);
        """
        await conn.execute(query, id_medico, id_especialidad)

    async def get_specialties_by_medico(self, conn, id_medico: int) -> List[Especializacion]:
        query = """
            SELECT e.id_especializacion, e.nombre, e.nivel, e.codigo_fonasa
            FROM especializacion e
            JOIN consulta_profesional cp ON e.id_especializacion = cp.id_especializacion
            WHERE cp.id_medico = $1;
        """
        rows = await conn.fetch(query, id_medico)
        return [
            Especializacion(
                id=row['id_especializacion'],
                nombre=row['nombre'],
                nivel=row['nivel'],
                codigo_fonasa=row['codigo_fonasa']
            ) for row in rows
        ]

    async def search_by_specialty(self, conn, especialidad_nombre: str) -> List[Medico]:
        query = """
            SELECT m.id_medico, m.rut, m.nombre, m.apellido, m.sexo
            FROM medico m
            JOIN consulta_profesional cp ON m.id_medico = cp.id_medico
            JOIN especializacion e ON cp.id_especializacion = e.id_especializacion
            WHERE e.nombre ILIKE $1;
        """
        rows = await conn.fetch(query, f"%{especialidad_nombre}%")
        return [
            Medico(
                id_medico=row['id_medico'],
                rut=Rut(row['rut']),
                nombre=row['nombre'],
                apellido=row['apellido'],
                sexo=row['sexo']
            ) for row in rows
        ]
