from typing import List, Optional
from app.modules.tratamiento.entities.tratamiento_entity import Tratamiento
from app.modules.tratamiento.interfaces.tratamiento_interfaces import ITratamientoRepository


class TratamientoRepository(ITratamientoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def list_all(self, conn) -> List[Tratamiento]:
        query = """
            SELECT id_tratamiento, nombre_tratamiento, descripcion, 
                   duracion_estimada, costo_aprox, observaciones
            FROM tratamiento
            ORDER BY nombre_tratamiento;
        """
        rows = await conn.fetch(query)
        return [Tratamiento(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id: int) -> Optional[Tratamiento]:
        query = """
            SELECT id_tratamiento, nombre_tratamiento, descripcion,
                   duracion_estimada, costo_aprox, observaciones
            FROM tratamiento
            WHERE id_tratamiento = $1;
        """
        row = await conn.fetchrow(query, id)
        if row:
            return Tratamiento(**dict(row))
        return None

    async def create(self, conn, tratamiento: Tratamiento) -> Tratamiento:
        query = """
            INSERT INTO tratamiento (nombre_tratamiento, descripcion, duracion_estimada, costo_aprox, observaciones)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id_tratamiento;
        """
        id_tratamiento = await conn.fetchval(
            query,
            tratamiento.nombre_tratamiento,
            tratamiento.descripcion,
            tratamiento.duracion_estimada,
            tratamiento.costo_aprox,
            tratamiento.observaciones
        )
        tratamiento.id_tratamiento = id_tratamiento
        return tratamiento

    async def update(self, conn, id: int, data: dict) -> Optional[Tratamiento]:
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
            UPDATE tratamiento 
            SET {', '.join(set_clauses)} 
            WHERE id_tratamiento = ${idx} 
            RETURNING id_tratamiento, nombre_tratamiento, descripcion, duracion_estimada, costo_aprox, observaciones;
        """
        
        row = await conn.fetchrow(query, *values)
        if row:
            return Tratamiento(**dict(row))
        return None

    async def delete(self, conn, id: int) -> bool:
        query = "DELETE FROM tratamiento WHERE id_tratamiento = $1 RETURNING id_tratamiento;"
        deleted_id = await conn.fetchval(query, id)
        return deleted_id is not None

    async def get_by_nombre(self, conn, nombre: str) -> Optional[Tratamiento]:
        query = """
            SELECT id_tratamiento, nombre_tratamiento, descripcion,
                   duracion_estimada, costo_aprox, observaciones
            FROM tratamiento
            WHERE LOWER(nombre_tratamiento) = LOWER($1);
        """
        row = await conn.fetchrow(query, nombre)
        if row:
            return Tratamiento(**dict(row))
        return None
