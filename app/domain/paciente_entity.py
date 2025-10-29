from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class Paciente:
    id_paciente: Optional[int]  
    rut: str
    nombre_completo: str
    correo: Optional[str] = None 
    telefono: Optional[str] = None
    edad: Optional[int] = None
    direccion: Optional[str] = None
    antecedentes_medicos: Optional[str] = None
    id_patologia: Optional[int] = None 
    fecha_inicio_tratamiento: Optional[date] = None
    observaciones: Optional[str] = None
    sesiones: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        if self.edad is not None and self.edad <= 0:
            raise ValueError("La edad debe ser mayor a 0")

    # ---------------- Lógica de negocio ----------------
    def en_tratamiento(self, fecha_actual: date) -> bool:
        """Devuelve True si el paciente lleva menos de 6 meses desde inicio de tratamiento."""
        if not self.fecha_inicio_tratamiento:
            return False
        diff = (fecha_actual - self.fecha_inicio_tratamiento).days
        return diff <= 180

    def agregar_observacion(self, texto: str):
        """Añade observaciones al paciente"""
        if self.observaciones:
            self.observaciones += f"; {texto}"
        else:
            self.observaciones = texto

    def resumen(self) -> str:
        """Genera un resumen legible del paciente"""
        edad_str = f"{self.edad} años" if self.edad else "Edad desconocida"
        return f"{self.nombre_completo} ({self.id_paciente}), {edad_str}, Patología: {self.id_patologia}"

    def agregar_sesion(self, sesion):
        """Agrega una sesión al historial del paciente"""
        self.sesiones.append(sesion)

    def sesiones_activas(self, fecha_actual: date):
        """Devuelve las sesiones que aún no han ocurrido"""
        return [s for s in self.sesiones if s.fecha >= fecha_actual]
