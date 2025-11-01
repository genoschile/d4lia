from pydantic import BaseModel


class GenerarLinkSchema(BaseModel):
    paciente_id: int
    sesion_id: int
