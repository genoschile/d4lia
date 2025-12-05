from fastapi import APIRouter

# ---------- CONTROLLERS ----------
from app.modules.welcome.controllers import welcome_controller as welcome
from app.modules.patologia.controllers import patologias_controller as patologias
from app.modules.encuesta.controllers import encuesta_controller as encuesta
from app.modules.sillon.controllers import sillon_controller as sillon
from app.modules.paciente.controllers import paciente_controller as paciente
from app.modules.sesion.controllers import sesion_controller as sesion
from app.modules.estado.controllers import estado_controller as estado
from app.modules.agenda.controllers.agenda_controller import router as agenda

# ---------- API V2 () ----------
from app.modules.paciente_condicion.controllers import (
    paciente_condicion_controller as paciente_condicion,
)
from app.modules.medico_especialidad.controllers import (
    medico_especialidad_controller as medico_especialidad,
)
from app.modules.consulta_medica.controllers import (
    consulta_medica_controller as consulta_medica,
)
from app.modules.tratamiento.controllers import (
    tratamiento_controller as tratamiento,
)
from app.modules.patologia_tratamiento.controllers import (
    patologia_tratamiento_controller as patologia_tratamiento,
)
from app.modules.medicamento.controllers import (
    medicamento_controller as medicamento,
)
from app.modules.receta.controllers import (
    receta_controller as receta,
)
from app.modules.receta_medicamento.controllers import (
    receta_medicamento_controller as receta_medicamento,
)
from app.modules.encargado.controllers import (
    encargado_controller as encargado,
)
from app.modules.diagnostico.controllers import (
    diagnostico_controller as diagnostico,
)
from app.modules.cie10.controllers import (
    cie10_controller as cie10,
)
from app.modules.ges.controllers import (
    ges_controller as ges,
)
from app.modules.cie10_ges.controllers import (
    cie10_ges_controller as cie10_ges,
)
from app.modules.tipo_examen.controllers import (
    tipo_examen_controller as tipo_examen,
)
from app.modules.instalacion.controllers import (
    instalacion_controller as instalacion,
)
from app.modules.orden_examen.controllers import (
    orden_examen_controller as orden_examen,
)
from app.modules.examen.controllers import (
    examen_controller as examen,
)
from app.modules.orden_hospitalizacion.controllers import (
    orden_hospitalizacion_controller as orden_hospitalizacion,
)
from app.modules.hospitalizacion.controllers import (
    hospitalizacion_controller as hospitalizacion,
)
from app.modules.tratamiento_hospitalizacion.controllers import (
    tratamiento_hospitalizacion_controller as tratamiento_hospitalizacion,
)
from app.modules.medicamento_hospitalizacion.controllers import (
    medicamento_hospitalizacion_controller as medicamento_hospitalizacion,
)
from app.modules.paciente_ges.controllers import (
    paciente_ges_controller as paciente_ges,
)


# -------------------------------------------------------------------
# FUNCIÓN CENTRAL PARA EXPONER TODOS LOS ROUTERS
# -------------------------------------------------------------------


def get_all_routers() -> list[APIRouter]:
    """
    Devuelve una lista con todos los routers del sistema.
    Ordenados y organizados por secciones.
    """

    return [
        # ---------- API ----------
        welcome.router,
        patologias.router,
        encuesta.router,
        sillon.router,
        paciente.router,
        sesion.router,
        estado.router,
        agenda,
        # ---------- API V2 ----------
        paciente_condicion.router,
        medico_especialidad.router,
        consulta_medica.router,
        tratamiento.router,
        patologia_tratamiento.router,
        medicamento.router,
        receta.router,
        receta_medicamento.router,
        encargado.router,
        diagnostico.router,
        cie10.router,
        ges.router,
        cie10_ges.router,
        tipo_examen.router,
        instalacion.router,
        orden_examen.router,
        examen.router,
        orden_hospitalizacion.router,
        hospitalizacion.router,
        tratamiento_hospitalizacion.router,
        medicamento_hospitalizacion.router,
        paciente_ges.router,
    ]
