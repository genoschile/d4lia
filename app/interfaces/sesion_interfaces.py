from abc import ABC, abstractmethod
from datetime import date
from app.domain.sesion_entity import Sesion


class ISesionRepository(ABC):
    @abstractmethod
    async def get_all(self, conn) -> list[Sesion]:
        """
        Devuelve todas las sesiones de la base de datos.
        - conn: conexión a la DB
        - return: lista de objetos Sesion
        """
        ...

    @abstractmethod
    async def get_encuestas_by_sesion(self, conn, id_sesion: int) -> list[dict]:
        """
        Devuelve todas las encuestas asociadas a una sesión específica.
        - id_sesion: ID de la sesión
        - return: lista de diccionarios con los datos de las encuestas
        """
        ...

    @abstractmethod
    async def create(self, conn, sesion: Sesion) -> Sesion:
        """
        Crea una nueva sesión en la base de datos.
        - sesion: objeto Sesion con los datos a insertar
        - return: la sesión recién creada (con id_sesion asignado)
        """
        ...

    @abstractmethod
    async def get_by_paciente_fecha_sillon(
        self, conn, id_paciente: int, fecha: date, id_sillon: int
    ) -> Sesion | None:
        """
        Verifica si ya existe una sesión para un mismo paciente en un mismo sillón y fecha.
        - id_paciente: ID del paciente
        - fecha: fecha de la sesión
        - id_sillon: ID del sillón
        - return: Sesion si existe un conflicto, None si no existe
        - Uso: para evitar duplicados y conflictos de horarios antes de crear una nueva sesión
        """
        ...

    @abstractmethod
    async def get_by_id(self, conn, id_sesion: int) -> Sesion | None:
        """
        Devuelve una sesión por su ID.
        - id_sesion: ID de la sesión
        - return: objeto Sesion si se encuentra, None si no existe
        """
        ...
