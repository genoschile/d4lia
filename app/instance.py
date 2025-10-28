# instance.py

from fastapi.params import Depends
from app.repositories.sillon_repository import SillonRepository
from app.use_case.sillon_service import SillonService
from app.database.database import get_conn  # 👈 la nueva dependencia


def get_sillon_services(conn=Depends(get_conn)) -> SillonService:
    repo = SillonRepository(conn)
    return SillonService(repo)