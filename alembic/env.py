from logging.config import fileConfig
import os
from alembic import context
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def get_url():
    """URL de la base de datos desde variables de entorno"""
    db_name = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USER') 
    db_password = os.getenv('DATABASE_PASSWORD')
    env = os.getenv('ENV', 'development')
    
    if not all([db_name, db_user, db_password]):
        raise ValueError("Variables de entorno requeridas: DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD")
    
    # Determinar host y puerto según el entorno
    if env == 'production' or os.path.exists('/.dockerenv'):
        host = os.getenv('PROD_DB_HOST', 'd4lia_pgbouncer')
        port = int(os.getenv('PROD_DB_PORT', '6432'))
    else:
        host = os.getenv('DEV_DB_HOST', 'genomas.cl')
        port = int(os.getenv('DEV_DB_PORT', '5555'))
    
    return f"postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}"


def run_migrations():
    """Conectar y ejecutar migraciones"""
    url = get_url()
    engine = create_engine(url)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
