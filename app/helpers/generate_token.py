from app.config.config import serializer

def generar_token(paciente_id: int, cita_id: int):
    return serializer.dumps({"paciente_id": paciente_id, "cita_id": cita_id})