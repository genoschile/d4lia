from typing import List
from app.modules.patologia_tratamiento.entities.patologia_tratamiento_entity import PatologiaTratamiento
from app.modules.patologia_tratamiento.interfaces.patologia_tratamiento_interfaces import IPatologiaTratamientoRepository


class PatologiaTratamientoRepository(IPatologiaTratamientoRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, conn, patologia_tratamiento: PatologiaTratamiento) -> PatologiaTratamiento:
        query = """
            INSERT INTO patologia_tratamiento (id_patologia, id_tratamiento)
            VALUES ($1, $2)
            RETURNING id_patologia, id_tratamiento;
        """
        row = await conn.fetchrow(
            query,
            patologia_tratamiento.id_patologia,
            patologia_tratamiento.id_tratamiento
        )
        return PatologiaTratamiento(**dict(row))

    async def delete(self, conn, id_patologia: int, id_tratamiento: int) -> bool:
        query = """
            DELETE FROM patologia_tratamiento 
            WHERE id_patologia = $1 AND id_tratamiento = $2
            RETURNING id_patologia;
        """
        deleted_id = await conn.fetchval(query, id_patologia, id_tratamiento)
        return deleted_id is not None

    async def get_tratamientos_by_patologia(self, conn, id_patologia: int) -> List[dict]:
        query = """
            SELECT pt.id_patologia, pt.id_tratamiento, 
                   t.nombre_tratamiento, t.descripcion, t.duracion_estimada, t.costo_aprox
            FROM patologia_tratamiento pt
            JOIN tratamiento t ON pt.id_tratamiento = t.id_tratamiento
            WHERE pt.id_patologia = $1
            ORDER BY t.nombre_tratamiento;
        """
        rows = await conn.fetch(query, id_patologia)
        return [dict(row) for row in rows]

    async def get_patologias_by_tratamiento(self, conn, id_tratamiento: int) -> List[dict]:
        query = """
            SELECT pt.id_patologia, pt.id_tratamiento,
                   p.nombre_patologia, p.especialidad, p.gravedad
            FROM patologia_tratamiento pt
            JOIN patologia p ON pt.id_patologia = p.id_patologia
            WHERE pt.id_tratamiento = $1
            ORDER BY p.nombre_patologia;
        """
        rows = await conn.fetch(query, id_tratamiento)
        return [dict(row) for row in rows]

    async def exists(self, conn, id_patologia: int, id_tratamiento: int) -> bool:
        query = """
            SELECT EXISTS(
                SELECT 1 FROM patologia_tratamiento 
                WHERE id_patologia = $1 AND id_tratamiento = $2
            );
        """
        return await conn.fetchval(query, id_patologia, id_tratamiento)

    async def list_all(self, conn) -> List[dict]:
        query = """
            SELECT pt.id_patologia, pt.id_tratamiento,
                   p.nombre_patologia, t.nombre_tratamiento
            FROM patologia_tratamiento pt
            JOIN patologia p ON pt.id_patologia = p.id_patologia
            JOIN tratamiento t ON pt.id_tratamiento = t.id_tratamiento
            ORDER BY p.nombre_patologia, t.nombre_tratamiento;
        """
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
