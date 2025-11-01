from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer

TEMPLATES = Jinja2Templates(directory="app/templates")
SECRET_KEY = "super_secreto"
serializer = URLSafeTimedSerializer(SECRET_KEY)
