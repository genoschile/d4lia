from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.error_handler import register_error_handlers
from app.database.database import close_db_connection, connect_to_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# ---------- CONTROLLERS ----------
from app.modules.welcome.controllers import welcome_controller as welcome
from app.modules.patologia.controllers import patologias_controller as patologias
from app.modules.encuesta.controllers import encuesta_controller as encuesta
from app.modules.sillon.controllers import sillon_controller as sillon
from app.modules.paciente.controllers import paciente_controller as paciente
from app.modules.sesion.controllers import sesion_controller as sesion
from app.modules.agenda.controllers.agenda_controller import router as agenda

# ---------- API V2 () ----------
from app.modules.paciente_condicion.controllers import (
    paciente_condicion_controller as paciente_condicion,
)
from app.modules.medico_especialidad.controllers import (
    medico_especialidad_controller as medico_especialidad,
)
from app.modules.consulta_medica.controllers import (
    consulta_medica_controller as consulta_medica,
)


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

# ---------- API ROUTES ----------
app.include_router(welcome.router)
app.include_router(sillon.router)
app.include_router(paciente.router)
app.include_router(patologias.router)
app.include_router(sesion.router)
app.include_router(encuesta.router)
app.include_router(agenda)

# ---------- API V2 ROUTES ----------
app.include_router(paciente_condicion.router)
app.include_router(medico_especialidad.router)
app.include_router(consulta_medica.router)

# graphql route
from strawberry.fastapi import GraphQLRouter
from app.modules.sillon.graphql.schema_sillon import schema


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
