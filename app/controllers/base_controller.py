from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config.config import TEMPLATES


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/a", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse("base.html", {"request": request})
