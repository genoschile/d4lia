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
    return SillonService(pool, SillonRepository(pool))


def get_paciente_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PacienteService:
    return PacienteService(pool, PacienteRepository(pool), PatologiaRepository(pool))


def get_patologia_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PatologiaService:
    return PatologiaService(pool, PatologiaRepository(pool))


def get_sesion_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> SesionService:
    return SesionService(
        pool,
        SesionRepository(pool),
        PacienteRepository(pool),
        SillonRepository(pool),
        PatologiaRepository(pool),
    )


def get_encuesta_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> EncuestaService:
    return EncuestaService(
        pool, EncuestaRepository(pool), PacienteRepository(pool), SesionRepository(pool)
    )
