import asyncpg
from typing import AsyncGenerator, Optional
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


async def execute_sql_file(file_path: str):
    """Ejecuta todas las sentencias SQL de un archivo .sql"""
    if pool is None:
        raise RuntimeError("Database not connected")

    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    async with pool.acquire() as conn:
        # divide el script en sentencias separadas por ';'
        statements = [s.strip() for s in sql_script.split(";") if s.strip()]
        for stmt in statements:
            try:
                await conn.execute(stmt)
            except Exception as e:
                print(f"⚠️ Error ejecutando sentencia: {stmt[:50]}...\n{e}")

async def get_conn() -> AsyncGenerator[asyncpg.Connection, None]:

    if pool is None:
        raise RuntimeError("Database not connected")

    async with pool.acquire() as conn:
        yield conn