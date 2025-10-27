from typing import Union
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database.database import close_db_connection, connect_to_db
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from app.config.config import TEMPLATES
from app.use_case.welcome_service import WelcomeService

# ------------- APP -------------
app = FastAPI()


@app.get("/")
async def read_root():
    try:
        use_case_welcome = WelcomeService()
        if not use_case_welcome:
            return {
                "success": False,
                "message": "No se pudo generar el mensaje de bienvenida",
                "status": "error",
            }, 500

        response = await use_case_welcome.execute()
        return response

    except Exception as e:
        return {
            "message": "Error interno del servidor",
            "success": False,
            "error": str(e),
        }, 500


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()


SECRET_KEY = "super_secreto"
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generar_token(paciente_id: int, cita_id: int):
    return serializer.dumps({"paciente_id": paciente_id, "cita_id": cita_id})


@app.get("/encuesta", response_class=HTMLResponse)
def mostrar_encuesta(request: Request, token: str):
    try:
        datos = serializer.loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        return HTMLResponse("<h3>El enlace ha expirado</h3>", status_code=401)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    return TEMPLATES.TemplateResponse(
        "encuesta.html", {"request": request, "token": token}
    )


@app.post("/encuesta")
def procesar_encuesta(token: str = Form(...), satisfaccion: str = Form(...)):
    try:
        datos = serializer.loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        return HTMLResponse("<h3>El enlace ha expirado</h3>", status_code=401)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    paciente_id = datos["paciente_id"]
    cita_id = datos["cita_id"]

    # Guardar en la base de datos aquí
    print(f"Respuesta de paciente {paciente_id}, cita {cita_id}: {satisfaccion}")

    return RedirectResponse("/gracias", status_code=303)


@app.get("/gracias", response_class=HTMLResponse)
def pagina_gracias(request: Request):
    return TEMPLATES.TemplateResponse("gracias.html", {"request": request})


# ---------- API ERROR ----------


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    first_error = exc.errors()[0]
    error_message = first_error.get("msg", "Error de validación")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": error_message,
            "data": None,
        },
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    first_error = exc.errors()[0]
    error_message = first_error.get("msg", "Error de validación")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": error_message,
            "data": None,
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/a", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse("base.html", {"request": request})


@app.get("/paciente/add", response_class=HTMLResponse)
async def add_paciente_form(request: Request):
    return TEMPLATES.TemplateResponse("add_paciente.html", {"request": request})


@app.get("/sillon/add", response_class=HTMLResponse)
async def add_sillon_form(request: Request):
    return TEMPLATES.TemplateResponse("add_sillon.html", {"request": request})


@app.get("/patologia/add", response_class=HTMLResponse)
async def add_patologia_form(request: Request):
    return TEMPLATES.TemplateResponse("add_patologia.html", {"request": request})
