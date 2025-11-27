from typing import List, Optional
from app.modules.encargado.entities.encargado_entity import Encargado
from app.modules.encargado.interfaces.encargado_interfaces import IEncargadoRepository


class EncargadoRepository(IEncargadoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Encargado]:
        query = """
            SELECT id_encargado, nombre_completo, rut, correo, telefono,
                   cargo, especialidad, activo
            FROM encargado
            ORDER BY nombre_completo;
        """
        rows = await conn.fetch(query)
        return [Encargado(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Encargado]:
        query = """
            SELECT id_encargado, nombre_completo, rut, correo, telefono,
                   cargo, especialidad, activo
            FROM encargado
            WHERE id_encargado = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Encargado(**dict(row))
        return None

    async def create(self, conn, encargado: Encargado) -> Encargado:
        query = """
            INSERT INTO encargado (nombre_completo, rut, correo, telefono, cargo, especialidad, activo)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id_encargado;
        """
        id_encargado = await conn.fetchval(
            query,
            encargado.nombre_completo,
            encargado.rut,
            encargado.correo,
            encargado.telefono,
            encargado.cargo,
            encargado.especialidad,
            encargado.activo
        )
        encargado.id_encargado = id_encargado
        return encargado

    async def update(self, conn, id: int, data: dict) -> Optional[Encargado]:
        set_clauses = []
        values = []
        idx = 1
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
            idx += 1
        
        if not set_clauses:
            return await self.get_by_id(conn, id)

        values.append(id)
        query = f"""
            UPDATE encargado 
            SET {', '.join(set_clauses)} 
            WHERE id_encargado = ${idx} 
            RETURNING id_encargado, nombre_completo, rut, correo, telefono, cargo, especialidad, activo;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Encargado(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM encargado WHERE id_encargado = $1 RETURNING id_encargado;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_rut(self, conn, rut: str) -> Optional[Encargado]:
        query = """
            SELECT id_encargado, nombre_completo, rut, correo, telefono,
                   cargo, especialidad, activo
            FROM encargado
            WHERE rut = $1;
        """
        row = await conn.fetchrow(query, rut)
        if row:
            return Encargado(**dict(row))
        return None

    async def get_by_cargo(self, conn, cargo: str) -> List[Encargado]:
        query = """
            SELECT id_encargado, nombre_completo, rut, correo, telefono,
                   cargo, especialidad, activo
            FROM encargado
            WHERE cargo = $1
            ORDER BY nombre_completo;
        """
        rows = await conn.fetch(query, cargo)
        return [Encargado(**dict(row)) for row in rows]

    async def get_activos(self, conn) -> List[Encargado]:
        query = """
            SELECT id_encargado, nombre_completo, rut, correo, telefono,
                   cargo, especialidad, activo
            FROM encargado
            WHERE activo = TRUE
            ORDER BY nombre_completo;
        """
        rows = await conn.fetch(query)
        return [Encargado(**dict(row)) for row in rows]
