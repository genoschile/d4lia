from fastapi import FastAPI, Request
from app.core.exceptions import AlreadyExistsException
from app.database.database import close_db_connection, connect_to_db
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException as StarletteHTTPException

# ---------- CONTROLLERS ----------
from app.controllers import welcome_controller as welcome
from app.controllers import gracias_controller as gracias
from app.controllers import patologias_controller as patologias
from app.controllers import encuesta_controller as encuesta
from app.controllers import sillon_controller as sillon
from app.controllers import base_controller as base
from app.controllers import dashboard_controller as admin
from app.controllers import paciente_controller as paciente


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
    finally:
        if app.state.db_pool:
            await close_db_connection(app.state.db_pool)
            print("🛑 Pool de conexiones cerrado")


app = FastAPI(lifespan=lifespan)

# ---------- API ROUTES ----------
app.include_router(welcome.router)
app.include_router(sillon.router)
app.include_router(paciente.router)
app.include_router(patologias.router)
# app.include_router(gracias.router)
# app.include_router(encuesta.router)
# app.include_router(base.router)
# app.include_router(admin.router)


# ---------- API ERROR ----------
@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=409,  # Conflict
        content={"detail": exc.message},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Si es un 404 (ruta no encontrada)
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "La ruta solicitada no existe o no fue encontrada.",
                "errors": [f"Ruta: {request.url.path}"],
                "data": None,
            },
        )
    # Para otros HTTPException (403, 401, etc.)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail or "Error HTTP",
            "errors": [exc.detail] if exc.detail else None,
            "data": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    errors = []
    for err in exc.errors():
        loc = ".".join([str(l) for l in err["loc"] if l != "body"])
        msg = err.get("msg", "Error de validación")
        if loc:
            errors.append(f"{loc}: {msg}")
        else:
            errors.append(msg)

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": errors[0],  # mensaje principal
            "errors": errors,  # lista completa de errores
            "data": None,
        },
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    first_error = exc.errors()[0]
    error_message = first_error.get("msg", "Error de validación")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": error_message,
            "data": None,
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
