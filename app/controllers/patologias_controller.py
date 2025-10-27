from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config.config import TEMPLATES


router = APIRouter(prefix="/patologia", tags=["Patologias"])


@router.get("/patologia/add", response_class=HTMLResponse)
async def add_patologia_form(request: Request):
    return TEMPLATES.TemplateResponse("add_patologia.html", {"request": request})
