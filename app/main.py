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
from app.modules.estado.controllers import estado_controller as estado
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
from app.modules.tratamiento.controllers import (
    tratamiento_controller as tratamiento,
)
from app.modules.patologia_tratamiento.controllers import (
    patologia_tratamiento_controller as patologia_tratamiento,
)
from app.modules.medicamento.controllers import (
    medicamento_controller as medicamento,
)
from app.modules.receta.controllers import (
    receta_controller as receta,
)
from app.modules.receta_medicamento.controllers import (
    receta_medicamento_controller as receta_medicamento,
)
from app.modules.encargado.controllers import (
    encargado_controller as encargado,
)
from app.modules.diagnostico.controllers import (
    diagnostico_controller as diagnostico,
)
from app.modules.cie10.controllers import (
    cie10_controller as cie10,
)
from app.modules.ges.controllers import (
    ges_controller as ges,
)
from app.modules.cie10_ges.controllers import (
    cie10_ges_controller as cie10_ges,
)
from app.modules.tipo_examen.controllers import (
    tipo_examen_controller as tipo_examen,
)
from app.modules.instalacion.controllers import (
    instalacion_controller as instalacion,
)
from app.modules.orden_examen.controllers import (
    orden_examen_controller as orden_examen,
)
from app.modules.examen.controllers import (
    examen_controller as examen,
)
from app.modules.orden_hospitalizacion.controllers import (
    orden_hospitalizacion_controller as orden_hospitalizacion,
)
from app.modules.hospitalizacion.controllers import (
    hospitalizacion_controller as hospitalizacion,
)
from app.modules.tratamiento_hospitalizacion.controllers import (
    tratamiento_hospitalizacion_controller as tratamiento_hospitalizacion,
)
from app.modules.medicamento_hospitalizacion.controllers import (
    medicamento_hospitalizacion_controller as medicamento_hospitalizacion,
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
app.include_router(tratamiento.router)
app.include_router(patologia_tratamiento.router)
app.include_router(medicamento.router)
app.include_router(receta.router)
app.include_router(receta_medicamento.router)
app.include_router(encargado.router)
app.include_router(diagnostico.router)
app.include_router(estado.router)
app.include_router(cie10.router)
app.include_router(ges.router)
app.include_router(cie10_ges.router)
app.include_router(tipo_examen.router)
app.include_router(instalacion.router)
app.include_router(orden_examen.router)
app.include_router(examen.router)
app.include_router(orden_hospitalizacion.router)
app.include_router(hospitalizacion.router)
app.include_router(tratamiento_hospitalizacion.router)
app.include_router(medicamento_hospitalizacion.router)


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
