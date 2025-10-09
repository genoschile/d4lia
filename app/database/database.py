import asyncpg
from typing import Optional
from app.config.environment import settings

DB_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

pool: Optional[asyncpg.Pool] = None


async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(DB_URL)
    print("✅ Conectado a la base de datos")


async def close_db_connection():
    global pool
    if pool is not None:
        await pool.close()
        print("🛑 Conexión cerrada")


async def fetch_query(query: str, *args):
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)


async def execute_query(query: str, *args):
    """Ejecuta INSERT, UPDATE, DELETE"""
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)
