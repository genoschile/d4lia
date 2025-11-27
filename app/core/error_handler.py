from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_core import ValidationError

from asyncpg import CheckViolationError, PostgresError, UniqueViolationError

from app.core.exceptions import (
    ApplicationError,
    DatabaseUnavailableError,
    NotImplementedException,
)
from app.helpers.response import error_response


def register_error_handlers(app):
    """
    Registra TODOS los manejadores de errores para evitar repetir código.
    """

    # ----- 🟦 ERRORES DE DOMINIO -----
    @app.exception_handler(ApplicationError)
    async def domain_error(_, exc: ApplicationError):
        return error_response(exc.message, exc.status_code)

    @app.exception_handler(DatabaseUnavailableError)
    async def db_unavailable(_, exc: DatabaseUnavailableError):
        return error_response(exc.message, exc.status_code)

    @app.exception_handler(NotImplementedException)
    async def not_implemented(_, exc: NotImplementedException):
        return error_response(
            exc.message or "Funcionalidad no implementada",
            exc.status_code,
        )

    # ----- 🟥 ERRORES DE POSTGRES -----
    @app.exception_handler(UniqueViolationError)
    async def pg_unique_violation(_, exc: UniqueViolationError):
        # De forma segura extraemos datos del error sin romper el typing
        constraint = getattr(exc, "constraint_name", "") or ""

        if "rut" in constraint:
            return error_response("El RUT ya existe", 409)
        if "codigo_fonasa" in constraint:
            return error_response("El código FONASA ya existe", 409)
        if "nombre" in constraint:
            return error_response("El nombre ya existe", 409)

        return error_response("Registro duplicado", 409)

    @app.exception_handler(CheckViolationError)
    async def pg_check_violation(_, exc: CheckViolationError):
        print("🔴 CheckViolationError:", repr(exc))
        return error_response("Valor inválido para campo con restricción", 400)

    @app.exception_handler(PostgresError)
    async def postgres_error(_, exc: PostgresError):
        print("🔴 PostgresError:", repr(exc))
        return error_response("Error en la base de datos", 500)

    # ----- 🟨 FASTAPI / STARLETTE HTTP -----
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):

        if request.url.path.startswith("/graphql"):
            raise exc  # evitar interferir con Strawberry

        if exc.status_code == 404:
            return error_response("Ruta no encontrada", 404)

        return error_response(exc.detail or "Error HTTP", exc.status_code)

    # ----- 🧪 ERRORES DE VALIDACIÓN -----
    @app.exception_handler(RequestValidationError)
    async def request_validation(request: Request, exc: RequestValidationError):
        if request.url.path.startswith("/graphql"):
            raise exc

        first = exc.errors()[0]["msg"]
        print("🔴 RequestValidationError:", exc.errors())
        return error_response(first, 422)

    @app.exception_handler(ValidationError)
    async def pydantic_validation(_, exc: ValidationError):
        first = exc.errors()[0]["msg"]
        print("🔴 ValidationError:", exc)
        return error_response(first, 422)

    # ----- 🏴 ERROR DESCONOCIDO -----
    @app.exception_handler(Exception)
    async def generic_error(_, exc: Exception):
        print("🔥 EXCEPCIÓN NO MANEJADA:", repr(exc))
        return error_response("Error interno del servidor", 500)
