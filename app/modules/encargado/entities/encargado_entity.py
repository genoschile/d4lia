from dataclasses import dataclass
from typing import Optional


@dataclass
class Encargado:
    """Entidad de dominio para Encargado (Personal médico/administrativo)"""
    
    nombre_completo: str
    id_encargado: Optional[int] = None
    rut: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    cargo: str = "otro"  # enfermero, doctor, técnico, administrativo, otro
    especialidad: Optional[str] = None
    activo: bool = True
    
    def __post_init__(self):
        if not self.nombre_completo or not self.nombre_completo.strip():
            raise ValueError("El nombre completo es obligatorio")
        
        cargos_validos = {'enfermero', 'doctor', 'técnico', 'administrativo', 'otro'}
        if self.cargo not in cargos_validos:
            raise ValueError(f"Cargo debe ser uno de: {', '.join(cargos_validos)}")
    
    def es_personal_medico(self) -> bool:
        """Verifica si es personal médico (doctor o enfermero)"""
        return self.cargo in {'doctor', 'enfermero'}
    
    def puede_registrar_pacientes(self) -> bool:
        """Verifica si puede registrar pacientes"""
        return self.activo and self.cargo in {'doctor', 'enfermero', 'administrativo'}
    
    def puede_atender_sesiones(self) -> bool:
        """Verifica si puede atender sesiones"""
        return self.activo and self.cargo in {'doctor', 'enfermero', 'técnico'}
