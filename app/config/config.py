from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer
from enum import Enum

TEMPLATES = Jinja2Templates(directory="app/templates")
SECRET_KEY = "super_secreto"
serializer = URLSafeTimedSerializer(SECRET_KEY)


class APP_STATES(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
