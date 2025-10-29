from pydantic import BaseModel, ConfigDict


class SillonResponse(BaseModel):
    id_sillon: int
    ubicacion_sala: str
    estado: str
    observaciones: str | None = None

    model_config = ConfigDict(from_attributes=True)
