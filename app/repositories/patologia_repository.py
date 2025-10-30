from typing import List, Optional
from app.domain.patologia_entity import Patologia
from app.interfaces.patologia_interfaces import IPatologiaRepository
import asyncpg


class PatologiaRepository(IPatologiaRepository):
    def __init__(self, pool):
        self.pool = pool

    async def create(self, conn, patologia: Patologia) -> Patologia:
        query = """
            INSERT INTO patologia (
                nombre_patologia, especialidad, tiempo_estimado, explicacion,
                tratamientos_principales, farmacos, efectos_adversos, gravedad,
                costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas
            )
            VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
            )
            RETURNING id_patologia, nombre_patologia, especialidad, tiempo_estimado,
                    explicacion, tratamientos_principales, farmacos, efectos_adversos,
                    gravedad, costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas;
        """
        row = await conn.fetchrow(
            query,
            patologia.nombre_patologia,
            patologia.especialidad,
            patologia.tiempo_estimado,
            patologia.explicacion,
            patologia.tratamientos_principales,
            patologia.farmacos,
            patologia.efectos_adversos,
            patologia.gravedad,
            patologia.costo_aprox,
            patologia.evidencia,
            patologia.exito_porcentaje,
            patologia.edad_promedio,
            patologia.notas,
        )
        return Patologia(**dict(row))

    async def get_all(self, conn) -> List[Patologia]:
        query = """
            SELECT id_patologia, nombre_patologia, explicacion
            FROM patologia
            ORDER BY id_patologia;
        """
        rows = await conn.fetch(query)
        return [Patologia(**dict(row)) for row in rows]

    async def get_by_id(self, conn, id_patologia: int) -> Patologia:
        query = """
            SELECT id_patologia, nombre_patologia, especialidad, tiempo_estimado,
                explicacion, tratamientos_principales, farmacos, efectos_adversos,
                gravedad, costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas
            FROM patologia
            WHERE id_patologia = $1;
        """
        row = await conn.fetchrow(query, id_patologia)

        if not row:
            raise ValueError(f"Patología con ID {id_patologia} no encontrada.")

        return Patologia(**dict(row))

    async def delete(self, conn, id_patologia: int) -> bool:
        query = """
            DELETE FROM patologia
            WHERE id_patologia = $1
            RETURNING id_patologia;
        """
        row = await conn.fetchrow(query, id_patologia)
        return bool(row)

    async def update(self, conn, id_patologia: int, data: dict) -> bool:
        set_clause = ", ".join([f"{k} = ${i+2}" for i, k in enumerate(data.keys())])
        values = list(data.values())

        query = f"""
            UPDATE patologia
            SET {set_clause}
            WHERE id_patologia = $1
            RETURNING id_patologia;
        """

        row = await conn.fetchrow(query, id_patologia, *values)
        return bool(row)
