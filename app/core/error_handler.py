from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_core import ValidationError

from asyncpg import (
    CheckViolationError,
    CheckViolationError,
    PostgresError,
    UniqueViolationError,
)

from app.core.exceptions import (
    AlreadyExistsException,
    BadRequestError,
    ConflictError,
    DatabaseUnavailableError,
    NotFoundError,
    NotImplementedException,
    ValidationException,
)
from app.helpers.responses.response import error_response


def register_error_handlers(app):
    """
    Registra TODOS los manejadores de errores para evitar repetir código.
    """

    # ----- EXCEPCIONES DE DOMINIO -----
    @app.exception_handler(BadRequestError)
    async def bad_request_handler(_, exc: BadRequestError):
        return error_response(exc.message, 400)

    @app.exception_handler(ConflictError)
    async def conflict_handler(_, exc: ConflictError):
        return error_response(exc.message, 409)

    @app.exception_handler(DatabaseUnavailableError)
    async def db_unavailable_handler(_, exc: DatabaseUnavailableError):
        return error_response(exc.message, 503)

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_exception_handler(_, exc: AlreadyExistsException):
        return error_response(exc.message, 409)

    # ----- ERRORES DE POSTGRES -----
    @app.exception_handler(UniqueViolationError)
    async def pg_unique_violation(_, exc: UniqueViolationError):
        return error_response("Registro duplicado", 409)

    @app.exception_handler(PostgresError)
    async def postgres_error_handler(_, exc: PostgresError):
        print("🔴 PostgresError:", repr(exc))
        return error_response("Error en base de datos", 500)

    @app.exception_handler(CheckViolationError)
    async def check_violation_handler(_, exc: CheckViolationError):
        print("🔴 CheckViolationError:", exc)
        return error_response("Valor inválido para tipo o severidad", 400)

    # ----- FASTAPI HTTP ERRORS -----
    @app.exception_handler(StarletteHTTPException)
    async def http_exception(request: Request, exc: StarletteHTTPException):

        if request.url.path.startswith("/graphql"):
            raise exc  # evitar interferir con Strawberry

        if exc.status_code == 404:
            return error_response(
                "La ruta solicitada no existe o no fue encontrada.",
                404,
                # errors=[f"Ruta: {request.url.path}"],
            )

        return error_response(
            exc.detail or "Error HTTP",
            exc.status_code,
            # , errors=[exc.detail]
        )

    # ----- VALIDACIÓN -----
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):

        if request.url.path.startswith("/graphql"):
            raise exc

        errors = []
        for err in exc.errors():
            loc = ".".join([str(x) for x in err["loc"] if x != "body"])
            errors.append(f"{loc}: {err['msg']}" if loc else err["msg"])

        return error_response(
            errors[0],
            422,
            #   , errors=errors
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_error(request: Request, exc: ValidationError):

        if request.url.path.startswith("/graphql"):
            raise exc

        first = exc.errors()[0]["msg"]
        print("🔴 ValidationError:", exc)

        return error_response(first, 422)

    @app.exception_handler(ValidationException)
    async def domain_validation_exception_handler(_, exc: ValidationException):
        print("🔴 ValidationException:", exc)
        return error_response(exc.message, 422)
    
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        print("🔴 RequestValidationError:", exc)
        print("🔴 RUTA:", request.url.path)
        print("🔴 DETALLES:", exc.errors())
        return error_response("Error de validación en request", 422)

    # ----- NOT FOUND -----
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_, exc: NotFoundError):
        return error_response(exc.message, 404)

    # ----- VALUE ERROR -----
    @app.exception_handler(ValueError)
    async def value_error_handler(_, exc: ValueError):
        return error_response(str(exc), 400)

    # ----- ATTRIBUTE ERROR -----
    @app.exception_handler(AttributeError)
    async def attribute_error_handler(_, exc: AttributeError):
        return error_response(str(exc), 400)

    @app.exception_handler(NotImplementedException)
    async def not_implemented_handler(_, exc: NotImplementedException):
        return error_response(
            exc.message or "Funcionalidad no implementada",
            501,  # HTTP 501 Not Implemented
        )

    # ----- ERROR DESCONOCIDO -----
    @app.exception_handler(Exception)
    async def internal_error(_, __):
        return error_response("Error interno del servidor", 500)
