class ApplicationError(Exception):
    """Error base para las excepciones de dominio."""

    status_code: int = 400  # Por defecto, Bad Request

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# ----------- ERRORES COMUNES DE NEGOCIO -----------


class BadRequestError(ApplicationError):
    """Datos incorrectos o inválidos."""

    status_code = 400


class ConflictError(ApplicationError):
    """Conflicto: registro ya existe, operación inválida, etc."""

    status_code = 409


class NotFoundError(ApplicationError):
    """El recurso solicitado no existe."""

    status_code = 404


class ForbiddenError(ApplicationError):
    """El usuario no tiene permisos para esta acción."""

    status_code = 403


class ValidationException(ApplicationError):
    """Datos inconsistentes según reglas de negocio."""

    status_code = 422


class OperationNotAllowedException(ApplicationError):
    """La operación está prohibida según reglas de negocio."""

    status_code = 403


# ----------- ERRORES RELACIONADOS A BASE DE DATOS -----------


class DatabaseError(ApplicationError):
    """Error general de base de datos."""

    status_code = 500


class DatabaseUnavailableError(DatabaseError):
    """La base de datos no responde."""

    status_code = 503


class UniqueConstraintError(DatabaseError):
    """Violación de llave única en base de datos."""

    status_code = 409


# ----------- ERRORES ADICIONALES DE NEGOCIO -----------


class PermissionDeniedException(ApplicationError):
    """Usuario sin permisos para la acción."""

    status_code = 403


class LimitExceededException(ApplicationError):
    """Se excedió un límite de negocio."""

    status_code = 429  # Too Many Requests / Rate Limit


class ResourceLockedException(ApplicationError):
    """Recurso bloqueado o en uso."""

    status_code = 423  # Locked


class DependencyMissingException(ApplicationError):
    """Falta una entidad o recurso requerido."""

    status_code = 424  # Failed Dependency


class NotImplementedException(ApplicationError):
    """Funcionalidad no implementada."""

    status_code = 501
