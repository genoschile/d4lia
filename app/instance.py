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

# ----------- RESPONSE -----------
from app.helpers.responses.response import error_response


# ----------- DEPENDENCIES -----------
def get_db_pool(request: Request) -> asyncpg.Pool:
    print(f"DEPENDENCIA: El ID del objeto 'app' es {id(request.app)}")

    pool = getattr(request.app.state, "db_pool", None)
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
    return SillonService(pool, repo)


def get_paciente_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PacienteService:
    repo = PacienteRepository(pool)
    return PacienteService(pool, repo)


def get_patologia_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PatologiaService:
    """Provee una instancia del servicio de Patología con su repositorio."""
    repo = PatologiaRepository(pool)
    return PatologiaService(repo)


def get_encuesta_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> EncuestaService:
    """Provee una instancia del servicio de Encuesta con su repositorio."""
    repo = EncuestaRepository(pool)
    return EncuestaService(repo)
