from abc import ABC, abstractmethod
from typing import List, Optional


class IMedicamentoRepository(ABC):
    """Interface para el repositorio de Medicamento"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todos los medicamentos"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener medicamento por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, medicamento):
        """Crear nuevo medicamento"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar medicamento"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar medicamento"""
        pass
    
    @abstractmethod
    async def get_by_nombre_comercial(self, conn, nombre: str):
        """Obtener medicamento por nombre comercial"""
        pass
    
    @abstractmethod
    async def get_stock_bajo(self, conn, umbral: int) -> List:
        """Obtener medicamentos con stock bajo"""
        pass
    
    @abstractmethod
    async def get_by_laboratorio(self, conn, laboratorio: str) -> List:
        """Obtener medicamentos por laboratorio"""
        pass
