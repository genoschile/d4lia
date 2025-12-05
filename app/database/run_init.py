import asyncio
from app.database.database import connect_to_db, close_db_connection, execute_sql_file


async def main():
    print("=" * 60)
    print("🚀 INICIANDO PROCESO DE INICIALIZACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    try:
        print("\n🔌 Paso 1: Conectando a la base de datos...")
        pool = await connect_to_db()
        print("✅ Conexión establecida\n")

        # 🧱 1️⃣ Crear estructura base
        print("🏗️  Paso 2: Creando estructura de tablas (init.sql)...")
        print("-" * 60)
        await execute_sql_file("app/database/init.sql")
        print("-" * 60)
        print("✅ Estructura de tablas creada\n")

        # 🌱 2️⃣ Insertar datos iniciales
        print("🌱 Paso 3: Insertando datos iniciales (seed.py)...")
        print("-" * 60)
        
        # Cerrar pool temporal y ejecutar seed.py
        await close_db_connection(pool)
        
        # Importar y ejecutar seed
        from app.database.seed import seed_database
        await seed_database()
        
        # Reconectar para finalizar limpiamente
        pool = await connect_to_db()
        
        print("-" * 60)
        print("✅ Datos iniciales insertados\n")

        print("🔒 Paso 4: Cerrando conexión...")
        await close_db_connection(pool)
        print("✅ Conexión cerrada\n")
        
        print("=" * 60)
        print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR CRÍTICO EN LA INICIALIZACIÓN")
        print("=" * 60)
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("=" * 60)
        raise


if __name__ == "__main__":
    asyncio.run(main())
