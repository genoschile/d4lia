import asyncpg
from typing import Optional

DB_URL = "postgresql://user:password@localhost:5432/mi_basedatos"

pool: Optional[asyncpg.Pool] = None

async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(DB_URL)
    print("✅ Conectado a la base de datos")

async def close_db_connection():
    global pool
    await pool.close()
    print("🛑 Conexión cerrada")

async def fetch_query(query: str, *args):
    """Ejecuta SELECTs y devuelve filas"""
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def execute_query(query: str, *args):
    """Ejecuta INSERT, UPDATE, DELETE"""
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)
