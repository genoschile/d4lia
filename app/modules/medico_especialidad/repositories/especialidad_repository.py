from app.modules.medico_especialidad.entities.medico_especialidad_entity import Especializacion
from app.modules.medico_especialidad.interfaces.medico_interfaces import IEspecialidadRepository

class EspecialidadRepository(IEspecialidadRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> list[Especializacion]:
        query = "SELECT id_especializacion, nombre, nivel, codigo_fonasa FROM especializacion;"
        rows = await conn.fetch(query)
        return [Especializacion(id=row['id_especializacion'], nombre=row['nombre'], nivel=row['nivel'], codigo_fonasa=row['codigo_fonasa']) for row in rows]

    async def get_by_id(self, conn, id: int) -> Especializacion | None:
        query = "SELECT id_especializacion, nombre, nivel, codigo_fonasa FROM especializacion WHERE id_especializacion = $1;"
        row = await conn.fetchrow(query, id)
        if row:
            return Especializacion(id=row['id_especializacion'], nombre=row['nombre'], nivel=row['nivel'], codigo_fonasa=row['codigo_fonasa'])
        return None

    async def create(self, conn, especialidad: Especializacion) -> Especializacion:
        query = """
            INSERT INTO especializacion (nombre, nivel, codigo_fonasa)
            VALUES ($1, $2, $3)
            RETURNING id_especializacion;
        """
        id_especializacion = await conn.fetchval(query, especialidad.nombre, especialidad.nivel, especialidad.codigo_fonasa)
        especialidad.id = id_especializacion
        return especialidad

    async def update(self, conn, id: int, especialidad: dict) -> Especializacion | None:
        # Construct dynamic update query
        set_clauses = []
        values = []
        idx = 1
        for key, value in especialidad.items():
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
            idx += 1
        
        if not set_clauses:
            return await self.get_by_id(conn, id)

        values.append(id)
        query = f"UPDATE especializacion SET {', '.join(set_clauses)} WHERE id_especializacion = ${idx} RETURNING id_especializacion, nombre, nivel, codigo_fonasa;"
        
        row = await conn.fetchrow(query, *values)
        if row:
             return Especializacion(id=row['id_especializacion'], nombre=row['nombre'], nivel=row['nivel'], codigo_fonasa=row['codigo_fonasa'])
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM especializacion WHERE id_especializacion = $1 RETURNING id_especializacion;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def search_by_name(self, conn, nombre: str) -> list[Especializacion]:
        query = "SELECT id_especializacion, nombre, nivel, codigo_fonasa FROM especializacion WHERE nombre ILIKE $1;"
        rows = await conn.fetch(query, f"%{nombre}%")
        return [Especializacion(id=row['id_especializacion'], nombre=row['nombre'], nivel=row['nivel'], codigo_fonasa=row['codigo_fonasa']) for row in rows]
