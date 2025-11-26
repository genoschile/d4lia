from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config.config import TEMPLATES


router = APIRouter(prefix="/gracias", tags=["Gracias"])


@router.get("/", response_class=HTMLResponse)
def pagina_gracias(request: Request):
    return TEMPLATES.TemplateResponse("gracias.html", {"request": request})
