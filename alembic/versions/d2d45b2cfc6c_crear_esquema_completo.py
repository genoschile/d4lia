"""crear_esquema_completo

Revision ID: d2d45b2cfc6c
Revises: 2376a47bb708
Create Date: 2025-12-03 16:14:36.972555

"""
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd2d45b2cfc6c'
down_revision: Union[str, Sequence[str], None] = '2376a47bb708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crear esquema completo con SQL puro"""
    
    # Leer el archivo init.sql y ejecutarlo
    import os
    
    # Obtener la ruta del archivo SQL
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(current_dir, '..', '..', 'app', 'database', 'init.sql')
    
    # Leer el contenido del archivo SQL
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Ejecutar el SQL completo
    op.execute(sql_content)


def downgrade() -> None:
    """Eliminar todas las tablas"""
    op.execute("""
        DROP TABLE IF EXISTS examen CASCADE;
        DROP TABLE IF EXISTS orden_examen CASCADE;
        DROP TABLE IF EXISTS instalacion CASCADE;
        DROP TABLE IF EXISTS tipo_examen CASCADE;
        DROP TABLE IF EXISTS receta_medicamento CASCADE;
        DROP TABLE IF EXISTS receta CASCADE;
        DROP TABLE IF EXISTS medicamento CASCADE;
        DROP TABLE IF EXISTS medicamento_hospitalizacion CASCADE;
        DROP TABLE IF EXISTS tratamiento_hospitalizacion CASCADE;
        DROP TABLE IF EXISTS hospitalizacion CASCADE;
        DROP TABLE IF EXISTS orden_hospitalizacion CASCADE;
        DROP TABLE IF EXISTS paciente_condicion CASCADE;
        DROP TABLE IF EXISTS condicion_personal CASCADE;
        DROP TABLE IF EXISTS paciente_ges CASCADE;
        DROP TABLE IF EXISTS diagnostico CASCADE;
        DROP TABLE IF EXISTS cie10_ges CASCADE; 
        DROP TABLE IF EXISTS cie10 CASCADE;
        DROP TABLE IF EXISTS ges CASCADE;
        DROP TABLE IF EXISTS consulta_medica CASCADE;
        DROP TABLE IF EXISTS consulta_profesional CASCADE;
        DROP TABLE IF EXISTS medico CASCADE;
        DROP TABLE IF EXISTS especializacion CASCADE;
        DROP TABLE IF EXISTS estado CASCADE;
        DROP TABLE IF EXISTS encuesta_paciente_json CASCADE;
        DROP TABLE IF EXISTS encuesta_sesion_json CASCADE;
        DROP TABLE IF EXISTS encuesta_token CASCADE;
        DROP TABLE IF EXISTS sesion CASCADE;
        DROP TABLE IF EXISTS paciente CASCADE;
        DROP TABLE IF EXISTS encargado CASCADE;
        DROP TABLE IF EXISTS sillon CASCADE;
        DROP TABLE IF EXISTS patologia_tratamiento CASCADE;
        DROP TABLE IF EXISTS tratamiento CASCADE;
        DROP TABLE IF EXISTS patologia CASCADE;
        DROP TABLE IF EXISTS alembic_test CASCADE;
    """)
