from dataclasses import dataclass
from typing import Optional

@dataclass
class Patologia:
    nombre_patologia: str
    id_patologia: Optional[int] = None
    especialidad: Optional[str] = None
    tiempo_estimado: Optional[str] = None
    explicacion: Optional[str] = None
    tratamientos_principales: Optional[str] = None
    farmacos: Optional[str] = None
    efectos_adversos: Optional[str] = None
    gravedad: Optional[str] = None
    costo_aprox: Optional[str] = None
    evidencia: Optional[str] = None
    exito_porcentaje: Optional[str] = None
    edad_promedio: Optional[str] = None
    notas: Optional[str] = None

    # =========================================
    # Lógica de negocio creativa
    # =========================================

    def riesgo_severo(self) -> bool:
        """Determina si la patología es severa según su gravedad."""
        return (self.gravedad or "").lower() in {"severa", "alta", "crítica"}

    def descripcion_resumida(self, max_chars: int = 100) -> str:
        """Devuelve un resumen de la patología limitado a max_chars."""
        resumen = f"{self.nombre_patologia}: {self.explicacion or 'Sin descripción'}"
        return resumen if len(resumen) <= max_chars else resumen[:max_chars] + "…"

    def necesita_tratamiento_intensivo(self) -> bool:
        """Sugiere si se requiere tratamiento intensivo según efectos y gravedad."""
        if not self.efectos_adversos:
            return False
        efectos = self.efectos_adversos.lower()
        return self.riesgo_severo() or any(e in efectos for e in ["neutropenia", "fatiga severa", "hospitalización"])

    def costo_estimado_float(self) -> Optional[float]:
        """Intenta extraer un costo aproximado en dólares como número."""
        if not self.costo_aprox:
            return None
        import re
        match = re.search(r"\$?([\d.,]+)", self.costo_aprox.replace("US", ""))
        if match:
            return float(match.group(1).replace(",", ""))
        return None
