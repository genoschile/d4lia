import asyncpg
from fastapi import Depends, HTTPException, Request, status

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
def get_db_pool(request: Request) -> asyncpg.Pool:
    # --- AÑADE ESTA LÍNEA ---
    print(f"DEPENDENCIA: El ID del objeto 'app' es {id(request.app)}")

    pool = getattr(request.app.state, "db_pool", None) # Forma más segura de acceder
    if pool is None:
        print("DEPENDENCIA: ¡Error! No se encontró 'db_pool' en el estado de la app.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La base de datos no está disponible.",
        )
    print(f"DEPENDENCIA: Pool encontrado con éxito. El ID del pool es {id(pool)}")
    return pool


def get_sillon_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> SillonService:
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
