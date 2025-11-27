from dataclasses import dataclass
from typing import Optional


@dataclass
class Instalacion:
    """Entidad de dominio para Instalación (Laboratorio, Clínica, etc.)"""
    
    nombre: str
    id_instalacion: Optional[int] = None
    tipo: str = "laboratorio"  # laboratorio, imagenologia, clinica, externo
    ubicacion: Optional[str] = None
    contacto: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la instalación es obligatorio")
        
        tipos_validos = {'laboratorio', 'imagenologia', 'clinica', 'externo'}
        if self.tipo not in tipos_validos:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(tipos_validos)}")
