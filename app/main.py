from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.error_handler import register_error_handlers
from app.database.database import close_db_connection, connect_to_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ---------- ROUTES ----------
from app.modules.routes import get_all_routers

# ---------- graphql route
from strawberry.fastapi import GraphQLRouter
from app.modules.sillon.graphql.schema_sillon import schema


# ----------- LIFESPAN ----------
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


app = FastAPI(lifespan=lifespan)

for router in get_all_routers():
    app.include_router(router)


async def get_context(request: Request):
    return {"request": request}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
