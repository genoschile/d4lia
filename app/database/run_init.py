import asyncio
from app.database.database import connect_to_db, close_db_connection, execute_sql_file


async def main():
    pool = await connect_to_db()

    # 🧱 1️⃣ Crear estructura base
    print("Ejecutando init.sql (estructura de tablas)...")
    await execute_sql_file("app/database/init.sql")

    # 🌱 2️⃣ Insertar datos iniciales
    print("Ejecutando seed.sql (datos iniciales)...")
    await execute_sql_file("app/database/seed.sql")

    await close_db_connection(pool)
    print("✅ Base de datos inicializada correctamente.")


if __name__ == "__main__":
    asyncio.run(main())
