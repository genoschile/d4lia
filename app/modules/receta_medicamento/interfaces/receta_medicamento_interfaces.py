from abc import ABC, abstractmethod
from typing import List


class IRecetaMedicamentoRepository(ABC):
    """Interface para el repositorio de Receta-Medicamento"""
    
    @abstractmethod
    async def create(self, conn, receta_medicamento):
        """Agregar un medicamento a una receta"""
        pass
    
    @abstractmethod
    async def update(self, conn, id_receta: int, id_medicamento: int, data: dict):
        """Actualizar prescripción de un medicamento en una receta"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id_receta: int, id_medicamento: int) -> bool:
        """Eliminar un medicamento de una receta"""
        pass
    
    @abstractmethod
    async def get_medicamentos_by_receta(self, conn, id_receta: int) -> List:
        """Obtener todos los medicamentos de una receta con detalles"""
        pass
    
    @abstractmethod
    async def get_recetas_by_medicamento(self, conn, id_medicamento: int) -> List:
        """Obtener todas las recetas que incluyen un medicamento"""
        pass
    
    @abstractmethod
    async def exists(self, conn, id_receta: int, id_medicamento: int) -> bool:
        """Verificar si existe la relación"""
        pass
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todas las relaciones receta-medicamento"""
        pass
