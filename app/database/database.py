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

    print(f"\n📂 Leyendo archivo: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    print(f"📊 Tamaño del script: {len(sql_script)} caracteres")

    async with pool.acquire() as conn:
        try:
            print("🚀 Ejecutando script completo...")
            await conn.execute(sql_script)
            print("✅ Script ejecutado exitosamente")
        except Exception as e:
            print(f"\n❌ Error ejecutando script completo:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensaje: {str(e)[:200]}")
            
            # Si falla, intentar modo de compatibilidad (dividiendo por sentencias simples)
            print("\n🔄 Intentando modo de compatibilidad (statement por statement)...")
            
            # Remover comentarios de una línea
            lines = sql_script.split('\n')
            clean_lines = []
            for line in lines:
                # Mantener líneas que no son solo comentarios
                if not line.strip().startswith('--'):
                    clean_lines.append(line)
            
            clean_script = '\n'.join(clean_lines)
            statements = [s.strip() for s in clean_script.split(";") if s.strip()]
            print(f"📝 Total de statements a ejecutar: {len(statements)}")
            
            success_count = 0
            error_count = 0
            
            for idx, stmt in enumerate(statements, 1):
                if not stmt:
                    continue
                    
                # Obtener primera línea para logging
                first_line = stmt.split('\n')[0][:80]
                
                try:
                    await conn.execute(stmt)
                    success_count += 1
                    if idx % 10 == 0:
                        print(f"   ✓ Procesados {idx}/{len(statements)} statements")
                except Exception as stmt_error:
                    error_count += 1
                    print(f"\n   ❌ Error en statement #{idx}:")
                    print(f"      Primera línea: {first_line}")
                    print(f"      Error: {str(stmt_error)[:150]}")
                    
            print(f"\n📊 Resumen: {success_count} exitosos, {error_count} errores")
