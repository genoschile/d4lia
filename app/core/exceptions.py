class ApplicationError(Exception):
    """Base para excepciones de dominio."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BadRequestError(ApplicationError):
    """Datos incorrectos o inválidos."""

    pass


class ConflictError(ApplicationError):
    """Conflicto: ya existe, no se puede crear, etc."""

    pass


class NotFoundError(ApplicationError):
    """No existe el recurso solicitado."""

    pass


class ForbiddenError(ApplicationError):
    """No autorizado para esta acción."""

    pass


# ----- ERRORES DE BASE DE DATOS -----


class DatabaseError(ApplicationError):
    """Error general de base de datos."""

    pass


class DatabaseUnavailableError(DatabaseError):
    """La base de datos no responde."""

    pass


class UniqueConstraintError(DatabaseError):
    """Violación de llave única."""

    pass


class AlreadyExistsException(ApplicationError):
    """El recurso que se intenta crear ya existe."""

    pass


class NotFoundException(ApplicationError):
    """El recurso solicitado no existe."""

    pass


class InvalidStateException(ApplicationError):
    """Acción inválida para el estado actual del recurso."""

    pass


class ValidationException(ApplicationError):
    """Datos inconsistentes o inválidos según reglas de negocio."""

    pass


class PermissionDeniedException(ApplicationError):
    """El usuario no tiene permisos para realizar esta acción."""

    pass


class LimitExceededException(ApplicationError):
    """Se intentó superar un límite permitido por negocio."""

    pass


class DependencyMissingException(ApplicationError):
    """Se requiere otra entidad o recurso para continuar."""

    pass


class ConflictException(ApplicationError):
    """Conflicto en las reglas de negocio (similar a AlreadyExists pero más amplio)."""

    pass


class ResourceLockedException(ApplicationError):
    """El recurso está bloqueado o en uso y no puede modificarse."""

    pass


class OperationNotAllowedException(ApplicationError):
    """La operación, aunque válida, está prohibida por reglas de negocio."""

    pass


class NotImplementedException(ApplicationError):
    """Funcionalidad no implementada."""
    pass