from enum import Enum


# ----------- ENUMERATIONS -----------
class eventWebHooks(str, Enum):
    paciente_add = "paciente_add"
    sillon_add = "sillon_add"
    sesion_add = "sesion_add"
    patologia_add = "patologia_add"
    encuesta_add = "encuesta_add"
