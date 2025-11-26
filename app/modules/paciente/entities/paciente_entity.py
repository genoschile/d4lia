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
    condiciones: list = field(
        default_factory=list, repr=False
    )  

    # ---------------- Post-init ----------------
    def __post_init__(self):
        if self.edad is not None and self.edad <= 0:
            raise ValueError("La edad debe ser mayor a 0")

    # ---------------- Propiedades ----------------
    @property
    def nombre_corto(self) -> str:
        """Devuelve el primer nombre y primer apellido."""
        partes = self.nombre_completo.split()
        return " ".join(partes[:2]) if len(partes) >= 2 else self.nombre_completo

    # ---------------- Lógica de negocio ----------------
    def en_tratamiento(self, fecha_actual: date) -> bool:
        """Devuelve True si el paciente lleva menos de 6 meses desde inicio de tratamiento."""
        if not self.fecha_inicio_tratamiento:
            return False
        diff = (fecha_actual - self.fecha_inicio_tratamiento).days
        return diff <= 180

    def agregar_observacion(self, texto: str):
        """Añade observaciones al paciente."""
        if self.observaciones:
            self.observaciones += f"; {texto}"
        else:
            self.observaciones = texto

    def resumen(self) -> str:
        """Genera un resumen legible del paciente."""
        edad_str = f"{self.edad} años" if self.edad else "Edad desconocida"
        return (
            f"{self.nombre_completo} (ID: {self.id_paciente or 'sin ID'}), "
            f"{edad_str}, Patología: {self.id_patologia or 'N/A'}"
        )

    # ---------------- Sesiones ----------------
    def agregar_sesion(self, sesion):
        """Agrega una sesión al historial del paciente."""
        self.sesiones.append(sesion)

    def sesiones_activas(self, fecha_actual: date):
        """Devuelve las sesiones que aún no han ocurrido."""
        return [s for s in self.sesiones if s.fecha >= fecha_actual]

    def sesiones_pasadas(self, fecha_actual: date):
        """Devuelve las sesiones que ya ocurrieron."""
        return [s for s in self.sesiones if s.fecha < fecha_actual]

    def total_sesiones(self) -> int:
        """Cantidad total de sesiones registradas."""
        return len(self.sesiones)

    def tiene_sesion_en_fecha(self, fecha: date) -> bool:
        """True si el paciente tiene una sesión exactamente en esa fecha."""
        return any(s.fecha == fecha for s in self.sesiones)

    # ---------------- Condiciones médicas ----------------
    def agregar_condicion(self, condicion):
        """Agrega una condición personal si no está ya registrada."""
        if any(c.id_condicion == condicion.id_condicion for c in self.condiciones):
            raise ValueError("Condición ya registrada para este paciente.")
        self.condiciones.append(condicion)

    def quitar_condicion(self, id_condicion: int):
        """Elimina una condición del paciente."""
        self.condiciones = [
            c for c in self.condiciones if c.id_condicion != id_condicion
        ]

    def condiciones_activas(self):
        """Devuelve las condiciones médicas sin fecha de resolución."""
        return [
            c for c in self.condiciones if getattr(c, "fecha_resolucion", None) is None
        ]

    def tiene_alergias(self) -> bool:
        """True si alguna condición es del tipo 'alergia'."""
        return any(
            getattr(c.condicion, "tipo", None) == "alergia" for c in self.condiciones
        )

    # ---------------- Otras utilidades ----------------
    def tiempo_en_tratamiento_dias(self, fecha_actual: date) -> Optional[int]:
        """Días transcurridos desde el inicio del tratamiento."""
        if not self.fecha_inicio_tratamiento:
            return None
        return (fecha_actual - self.fecha_inicio_tratamiento).days

    def contacto_valido(self) -> bool:
        """Valida si tiene al menos un medio de contacto disponible."""
        return bool(self.correo or self.telefono)

    def actualizar_datos(self, **kwargs):
        """Permite actualizar dinámicamente campos del paciente."""
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def esta_activo(self, fecha_actual: date) -> bool:
        """Considera activo si tiene sesiones activas o tratamiento vigente."""
        return self.en_tratamiento(fecha_actual) or bool(
            self.sesiones_activas(fecha_actual)
        )
