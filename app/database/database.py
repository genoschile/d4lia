import asyncpg
from app.config.environment import settings

DB_URL = settings.DATABASE_URL


async def connect_to_db():
    global pool

    print("=======================================")
    print("DATABASE_URL in runtime:", settings.DATABASE_URL)
    print("ENV:", settings.ENV)
    print("=======================================")

    pool = await asyncpg.create_pool(DB_URL, min_size=20, max_size=200)
    print("✅ Conectado a la base de datos")
    return pool


async def close_db_connection(pool: asyncpg.Pool):
    """Cierra un pool de conexiones dado."""
    if pool:
        await pool.close()


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
        try:
            # Ejecutar todo el script de una vez
            await conn.execute(sql_script)
        except Exception as e:
            print(f"⚠️ Error ejecutando script SQL: {e}")
            # Si falla, intentar modo de compatibilidad (dividiendo por sentencias simples)
            print("Intentando modo de compatibilidad...")
            statements = [s.strip() for s in sql_script.split(";") if s.strip() and not s.strip().startswith('--')]
            for stmt in statements:
                try:
                    await conn.execute(stmt)
                except Exception as stmt_error:
                    print(f"⚠️ Error en sentencia: {stmt[:100]}...\n{stmt_error}")
