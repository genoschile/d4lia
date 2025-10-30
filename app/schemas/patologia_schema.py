from pydantic import BaseModel
from typing import Optional


from pydantic import BaseModel, ConfigDict
from typing import Optional


class PatologiaCreate(BaseModel):
    nombre_patologia: str
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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nombre_patologia": "Cáncer de mama HER2 positivo",
                "especialidad": "Oncología Mamaria",
                "tiempo_estimado": "1 hora/sesión - duración total 6 meses",
                "explicacion": "Tratamiento con quimioterapia dirigida y terapia hormonal.",
                "tratamientos_principales": "Trastuzumab, Docetaxel",
                "farmacos": "Trastuzumab, Pertuzumab, Docetaxel",
                "efectos_adversos": "Fatiga, caída de cabello, náuseas leves",
                "gravedad": "Moderada",
                "costo_aprox": "US$3.000 por sesión",
                "evidencia": "Alta",
                "exito_porcentaje": "85%",
                "edad_promedio": "45-65 años",
                "notas": "Se recomienda control cardiológico trimestral durante el tratamiento.",
            }
        },
    )


class PatologiaResponse(BaseModel):
    id_patologia: int
    nombre_patologia: str
    especialidad: Optional[str] = None
    explicacion: Optional[str] = None


class PatologiaUpdate(BaseModel):
    nombre_patologia: Optional[str] = None
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre_patologia": "Cáncer de pulmón avanzado",
                "gravedad": "Alta",
                "tratamientos_principales": "Inmunoterapia combinada con quimioterapia",
                "efectos_adversos": "Fatiga, tos persistente, pérdida de apetito",
            }
        }
    )
