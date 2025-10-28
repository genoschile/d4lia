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
from app.helpers.database.get_pool import get_pool as get_conn
from app.helpers.database.get_pool import pool

async def get_sillon_services() -> SillonService:
    pool = get_conn()  # ya conectado en lifespan
    repo = SillonRepository(pool)
    return SillonService(repo)

async def get_sesion_services():
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        repo = SesionRepository(conn)
        yield SesionService(repo)


async def get_paciente_services():
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        repo = PacienteRepository(conn)
        yield PacienteService(repo)


async def get_patologia_services():
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        repo = PatologiaRepository(conn)
        yield PatologiaService(repo)


async def get_encuesta_services():
    if pool is None:
        raise RuntimeError("Database not connected")
    async with pool.acquire() as conn:
        repo = EncuestaRepository(conn)
        yield EncuestaService(repo)
