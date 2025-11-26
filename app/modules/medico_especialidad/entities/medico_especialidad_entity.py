from dataclasses import dataclass
import re
from typing import List, Optional
from datetime import date


@dataclass(frozen=True)
class Rut:
    value: str

    def __post_init__(self):
        if not self._validar_formato(self.value):
            raise ValueError("Formato de RUT inválido")

    def _validar_formato(self, rut: str) -> bool:
        # Accepts both formats: 12345678-9 and 12.345.678-9
        return bool(re.match(r"^\d{1,2}(\.\d{3}){0,2}\.\d{3}-[\dkK]$|^\d{1,8}-[\dkK]$", rut))


class Especializacion:
    def __init__(self, id: Optional[int], nombre: str, nivel: str, codigo_fonasa: Optional[str] = ""):
        self.id = id
        self.nombre = nombre
        self.nivel = nivel
        self.codigo_fonasa = codigo_fonasa or ""


class AcreditacionProfesional:
    """
    Equivalente a tu tabla 'consulta_profesional'.
    Representa que un médico tiene una especialidad activa.
    """

    def __init__(
        self, id_profesional: int, especialidad: Especializacion, fecha_registro: date
    ):
        self.id_profesional = id_profesional
        self.especialidad = especialidad
        self.fecha_registro = fecha_registro


class Medico:
    """
    Aggregate Root
    """

    def __init__(
        self,
        rut: Rut,
        nombre: str,
        apellido: str,
        sexo: str,
        id_medico: Optional[int] = None,
    ):
        self.id_medico = id_medico
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.sexo = sexo
        self.activo = True
        # El médico contiene sus acreditaciones (especialidades)
        self.acreditaciones: List[AcreditacionProfesional] = []

    def agregar_especialidad(
        self, especialidad: Especializacion, id_profesional_db: int
    ):
        # Lógica de negocio: Un médico no debería tener la misma especialidad dos veces
        for acr in self.acreditaciones:
            if acr.especialidad.id == especialidad.id:
                raise ValueError("El médico ya posee esta especialidad")

        nueva_acreditacion = AcreditacionProfesional(
            id_profesional=id_profesional_db,
            especialidad=especialidad,
            fecha_registro=date.today(),
        )
        self.acreditaciones.append(nueva_acreditacion)

    def nombre_completo(self) -> str:
        prefix = (
            "Dr."
            if self.sexo == "masculino"
            else "Dra." if self.sexo == "femenino" else "Dr/a."
        )
        return f"{prefix} {self.nombre} {self.apellido}"
