from fastapi import Depends

# ----------- SILLON -----------
from app.repositories.sillon_repository import SillonRepository
from app.use_case.sillon_service import SillonService

# ----------- ENCUESTA -----------
from app.repositories.encuesta_repository import EncuestaRepository
from app.use_case.encuesta_service import EncuestaService

# ----------- SESION -----------
from app.repositories.sesion_repository import SesionRepository
from app.use_case.sesion_service import SesionService

# ----------- PACIENTE -----------
from app.repositories.paciente_repository import PacienteRepository
from app.use_case.paciente_service import PacienteService

# ----------- PATOLOGIA -----------
from app.repositories.patologia_repository import PatologiaRepository
from app.use_case.patologia_service import PatologiaService

# ----------- DEPENDENCIES -----------
from app.database.database import get_conn


def get_sillon_services(conn=Depends(get_conn)) -> SillonService:
    repo = SillonRepository(conn)
    return SillonService(repo)


def get_sesion_services(conn=Depends(get_conn)) -> SesionService:
    repo = SesionRepository(conn)
    return SesionService(repo)


def get_paciente_services(conn=Depends(get_conn)) -> PacienteService:
    repo = PacienteRepository(conn)
    return PacienteService(repo)


def get_patologia_services(conn=Depends(get_conn)) -> PatologiaService:
    repo = PatologiaRepository(conn)
    return PatologiaService(repo)


def get_encuesta_services(conn=Depends(get_conn)) -> EncuestaService:
    repo = EncuestaRepository(conn)
    return EncuestaService(repo)
