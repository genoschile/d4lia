from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer

TEMPLATES = Jinja2Templates(directory="app/templates")
SECRET_KEY = "super_secreto"
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generar_token(paciente_id: int, cita_id: int):
    return serializer.dumps({"paciente_id": paciente_id, "cita_id": cita_id})
