from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date


class IConsultaMedicaRepository(ABC):
    """Interface para el repositorio de Consulta Médica"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todas las consultas médicas"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener consulta médica por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, consulta):
        """Crear nueva consulta médica"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar consulta médica"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar consulta médica"""
        pass
    
    @abstractmethod
    async def get_by_paciente(self, conn, id_paciente: int) -> List:
        """Obtener consultas por paciente"""
        pass
    
    @abstractmethod
    async def get_by_profesional(self, conn, id_profesional: int) -> List:
        """Obtener consultas por profesional"""
        pass
    
    @abstractmethod
    async def get_by_fecha_range(self, conn, fecha_inicio: date, fecha_fin: date) -> List:
        """Obtener consultas en un rango de fechas"""
        pass
