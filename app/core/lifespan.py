# ----------- LIFESPAN ----------
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.database.database import close_db_connection, connect_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"LIFESPAN: El ID del objeto 'app' es {id(app)}")

    app.state.db_pool = None
    try:
        app.state.db_pool = await connect_to_db()

        if app.state.db_pool:
            print(
                f"✅ Pool creado con éxito. El ID del pool es {id(app.state.db_pool)}"
            )
        else:
            print("❌ ¡ERROR! connect_to_db() devolvió None.")

        yield

        # validation state app pydanctic

    finally:
        pool = getattr(app.state, "db_pool", None)
        if pool is not None:
            await close_db_connection(pool)
            print("🛑 Pool de conexiones cerrado")
        else:
            print("⚠️ No se cerró el pool de conexiones porque no existía")
