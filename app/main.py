from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from app.core import lifespan
from app.core.error_handler import register_error_handlers
from fastapi.middleware.cors import CORSMiddleware

# ---------- ROUTES ----------
from app.modules.routes import get_all_routers

# ---------- graphql route
from strawberry.fastapi import GraphQLRouter
from app.modules.sillon.graphql.schema_sillon import schema


app = FastAPI(lifespan=lifespan.lifespan)

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
