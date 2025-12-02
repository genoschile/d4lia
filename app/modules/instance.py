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
        TratamientoRepository(pool),
    )


def get_encuesta_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> EncuestaService:
    return EncuestaService(
        pool, EncuestaRepository(pool), PacienteRepository(pool), SesionRepository(pool)
    )


# ----------- CONDICION PERSONAL -----------
from app.modules.paciente_condicion.repositories.condicion_personal_repository import (
    CondicionPersonalRepository,
)
from app.modules.paciente_condicion.services.condicion_personal_service import (
    CondicionPersonalService,
)


def get_condicion_personal_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> CondicionPersonalService:
    return CondicionPersonalService(pool, CondicionPersonalRepository(pool))


# ----------- PACIENTE CONDICION -----------
from app.modules.paciente_condicion.repositories.paciente_condicion_repository import (
    PacienteCondicionRepository,
)
from app.modules.paciente_condicion.services.paciente_condicion_service import (
    PacienteCondicionService,
)


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
from app.modules.medico_especialidad.repositories.medico_repository import (
    MedicoRepository,
)
from app.modules.medico_especialidad.repositories.especialidad_repository import (
    EspecialidadRepository,
)
from app.modules.medico_especialidad.services.medico_service import MedicoService


def get_medico_services(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> MedicoService:
    return MedicoService(
        pool,
        MedicoRepository(pool),
        EspecialidadRepository(pool),
    )

# ----------- CONSULTA MEDICA -----------
from app.modules.consulta_medica.repositories.consulta_medica_repository import (
    ConsultaMedicaRepository,
)
from app.modules.consulta_medica.services.consulta_medica_service import (
    ConsultaMedicaService,
)   

def get_consulta_medica_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> ConsultaMedicaService:
    return ConsultaMedicaService(
        pool,
        ConsultaMedicaRepository(pool),
    )

# ----------- TRATAMIENTO -----------
from app.modules.tratamiento.repositories.tratamiento_repository import (
    TratamientoRepository,
)
from app.modules.tratamiento.services.tratamiento_service import (
    TratamientoService,
)

def get_tratamiento_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> TratamientoService:
    return TratamientoService(
        pool,
        TratamientoRepository(pool),
    )

# ----------- PATOLOGIA TRATAMIENTO -----------
from app.modules.patologia_tratamiento.repositories.patologia_tratamiento_repository import (
    PatologiaTratamientoRepository,
)
from app.modules.patologia_tratamiento.services.patologia_tratamiento_service import (
    PatologiaTratamientoService,
)

def get_patologia_tratamiento_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PatologiaTratamientoService:
    return PatologiaTratamientoService(
        pool,
        PatologiaTratamientoRepository(pool),
        PatologiaRepository(pool),
        TratamientoRepository(pool),
    )

# ----------- MEDICAMENTO -----------
from app.modules.medicamento.repositories.medicamento_repository import (
    MedicamentoRepository,
)
from app.modules.medicamento.services.medicamento_service import (
    MedicamentoService,
)

def get_medicamento_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> MedicamentoService:
    return MedicamentoService(
        pool,
        MedicamentoRepository(pool),
    )

# ----------- RECETA -----------
from app.modules.receta.repositories.receta_repository import (
    RecetaRepository,
)
from app.modules.receta.services.receta_service import (
    RecetaService,
)

def get_receta_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> RecetaService:
    return RecetaService(
        pool,
        RecetaRepository(pool),
        PacienteRepository(pool),
        MedicoRepository(pool),
        ConsultaMedicaRepository(pool),
    )

# ----------- RECETA MEDICAMENTO -----------
from app.modules.receta_medicamento.repositories.receta_medicamento_repository import (
    RecetaMedicamentoRepository,
)
from app.modules.receta_medicamento.services.receta_medicamento_service import (
    RecetaMedicamentoService,
)

def get_receta_medicamento_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> RecetaMedicamentoService:
    return RecetaMedicamentoService(
        pool,
        RecetaMedicamentoRepository(pool),
        RecetaRepository(pool),
        MedicamentoRepository(pool),
    )

# ----------- ENCARGADO -----------
from app.modules.encargado.repositories.encargado_repository import (
    EncargadoRepository,
)
from app.modules.encargado.services.encargado_service import (
    EncargadoService,
)

def get_encargado_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> EncargadoService:
    return EncargadoService(
        pool,
        EncargadoRepository(pool),
    )

# ----------- DIAGNOSTICO -----------
from app.modules.diagnostico.repositories.diagnostico_repository import (
    DiagnosticoRepository,
)
from app.modules.diagnostico.services.diagnostico_service import (
    DiagnosticoService,
)

def get_diagnostico_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> DiagnosticoService:
    return DiagnosticoService(
        pool,
        DiagnosticoRepository(pool),
        ConsultaMedicaRepository(pool),
    )

# ----------- CIE10 -----------
from app.modules.cie10.repositories.cie10_repository import (
    Cie10Repository,
)
from app.modules.cie10.services.cie10_service import (
    Cie10Service,
)

def get_cie10_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> Cie10Service:
    return Cie10Service(
        pool,
        Cie10Repository(pool),
    )

from app.modules.estado.repositories.estado_repository import EstadoRepository
from app.modules.estado.services.estado_service import EstadoService

def get_estado_service(pool: asyncpg.Pool = Depends(get_db_pool)) -> EstadoService:
    return EstadoService(pool, EstadoRepository(pool))

# ----------- AUTH -----------
from app.modules.ges.repositories.ges_repository import (
    GesRepository,
)
from app.modules.ges.services.ges_service import (
    GesService,
)

def get_ges_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> GesService:
    return GesService(
        pool,
        GesRepository(pool),
    )

# ----------- CIE10 GES -----------
from app.modules.cie10_ges.repositories.cie10_ges_repository import (
    Cie10GesRepository,
)
from app.modules.cie10_ges.services.cie10_ges_service import (
    Cie10GesService,
)

def get_cie10_ges_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> Cie10GesService:
    return Cie10GesService(
        pool,
        Cie10GesRepository(pool),
        Cie10Repository(pool),
        GesRepository(pool),
    )

# ----------- TIPO EXAMEN -----------
from app.modules.tipo_examen.repositories.tipo_examen_repository import (
    TipoExamenRepository,
)
from app.modules.tipo_examen.services.tipo_examen_service import (
    TipoExamenService,
)

def get_tipo_examen_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> TipoExamenService:
    return TipoExamenService(
        pool,
        TipoExamenRepository(pool),
    )

# ----------- INSTALACION -----------
from app.modules.instalacion.repositories.instalacion_repository import (
    InstalacionRepository,
)
from app.modules.instalacion.services.instalacion_service import (
    InstalacionService,
)

def get_instalacion_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> InstalacionService:
    return InstalacionService(
        pool,
        InstalacionRepository(pool),
    )

# ----------- ORDEN EXAMEN -----------
from app.modules.orden_examen.repositories.orden_examen_repository import (
    OrdenExamenRepository,
)
from app.modules.orden_examen.services.orden_examen_service import (
    OrdenExamenService,
)

def get_orden_examen_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> OrdenExamenService:
    return OrdenExamenService(
        pool,
        OrdenExamenRepository(pool),
        ConsultaMedicaRepository(pool),
        PacienteRepository(pool),
        TipoExamenRepository(pool),
    )

# ----------- EXAMEN -----------
from app.modules.examen.repositories.examen_repository import (
    ExamenRepository,
)
from app.modules.examen.services.examen_service import (
    ExamenService,
)

def get_examen_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> ExamenService:
    return ExamenService(
        pool,
        ExamenRepository(pool),
        OrdenExamenRepository(pool),
        PacienteRepository(pool),
        TipoExamenRepository(pool),
        InstalacionRepository(pool),
    )

# ----------- ORDEN HOSPITALIZACION -----------
from app.modules.orden_hospitalizacion.repositories.orden_hospitalizacion_repository import (
    OrdenHospitalizacionRepository,
)
from app.modules.orden_hospitalizacion.services.orden_hospitalizacion_service import (
    OrdenHospitalizacionService,
)

def get_orden_hospitalizacion_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> OrdenHospitalizacionService:
    return OrdenHospitalizacionService(
        pool,
        OrdenHospitalizacionRepository(pool),
        PacienteRepository(pool),
    )

# ----------- HOSPITALIZACION -----------
from app.modules.hospitalizacion.repositories.hospitalizacion_repository import (
    HospitalizacionRepository,
)
from app.modules.hospitalizacion.services.hospitalizacion_service import (
    HospitalizacionService,
)

def get_hospitalizacion_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> HospitalizacionService:
    return HospitalizacionService(
        pool,
        HospitalizacionRepository(pool),
        OrdenHospitalizacionRepository(pool),
        PacienteRepository(pool),
    )

# ----------- TRATAMIENTO HOSPITALIZACION -----------
from app.modules.tratamiento_hospitalizacion.repositories.tratamiento_hospitalizacion_repository import (
    TratamientoHospitalizacionRepository,
)
from app.modules.tratamiento_hospitalizacion.services.tratamiento_hospitalizacion_service import (
    TratamientoHospitalizacionService,
)

def get_tratamiento_hospitalizacion_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> TratamientoHospitalizacionService:
    return TratamientoHospitalizacionService(
        pool,
        TratamientoHospitalizacionRepository(pool),
        HospitalizacionRepository(pool),
        TratamientoRepository(pool),
    )

# ----------- MEDICAMENTO HOSPITALIZACION -----------
from app.modules.medicamento_hospitalizacion.repositories.medicamento_hospitalizacion_repository import (
    MedicamentoHospitalizacionRepository,
)
from app.modules.medicamento_hospitalizacion.services.medicamento_hospitalizacion_service import (
    MedicamentoHospitalizacionService,
)

def get_medicamento_hospitalizacion_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> MedicamentoHospitalizacionService:
    return MedicamentoHospitalizacionService(
        pool,
        MedicamentoHospitalizacionRepository(pool),
        HospitalizacionRepository(pool),
        MedicamentoRepository(pool),
    )
# ----------- PACIENTE GES -----------
from app.modules.paciente_ges.repositories.paciente_ges_repository import (
    PacienteGesRepository,
)
from app.modules.paciente_ges.services.paciente_ges_service import (
    PacienteGesService,
)

def get_paciente_ges_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> PacienteGesService:
    return PacienteGesService(
        pool,
        PacienteGesRepository(pool),
        PacienteRepository(pool),
        GesRepository(pool),
        DiagnosticoRepository(pool),
    )
