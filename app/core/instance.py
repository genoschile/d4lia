import asyncpg
from fastapi import Depends, HTTPException, Request, status

# ----------- SILLON -----------
from app.modules.sillon.repositories.sillon_repository import SillonRepository
from app.modules.sillon.services.sillon_service import SillonService

# ----------- ENCUESTA -----------
from app.modules.encuesta.repositories.encuesta_repository import EncuestaRepository
from app.modules.encuesta.services.encuesta_service import EncuestaService

# ----------- SESION -----------
from app.modules.sesion.repositories.sesion_repository import SesionRepository
from app.modules.sesion.services.sesion_service import SesionService

# ----------- PACIENTE -----------
from app.modules.paciente.repositories.paciente_repository import PacienteRepository
from app.modules.paciente.services.paciente_service import PacienteService

# ----------- PATOLOGIA -----------
from app.modules.patologia.repositories.patologia_repository import PatologiaRepository
from app.modules.patologia.services.patologia_service import PatologiaService


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


# ----------- CONDICION PERSONAL -----------
from app.repositories.condicion_personal_repository import CondicionPersonalRepository
from app.use_case.condicion_personal_service import CondicionPersonalService


def get_condicion_personal_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> CondicionPersonalService:
    return CondicionPersonalService(pool, CondicionPersonalRepository(pool))


# ----------- PACIENTE CONDICION -----------
from app.repositories.paciente_condicion_repository import PacienteCondicionRepository
from app.use_case.paciente_condicion_service import PacienteCondicionService


def get_paciente_condicion_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PacienteCondicionService:
    return PacienteCondicionService(
        pool,
        PacienteCondicionRepository(pool),
        PacienteRepository(pool),
        CondicionPersonalRepository(pool),
    )


# ----------- MEDICO ESPECIALIDAD -----------
from app.modules.medico_especialidad.repositories.medico_repository import MedicoRepository
from app.modules.medico_especialidad.services.medico_service import MedicoService


def get_medico_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> MedicoService:
    return MedicoService(
        pool,
        MedicoRepository(pool),
    )
