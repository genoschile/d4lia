from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError, PositiveInt
from dotenv import load_dotenv

from app.config.config import APP_STATES

load_dotenv()


class Settings(BaseSettings):

    # ----- Variables obligatorias -----
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")  # type: ignore
    DATABASE_USER: str = Field(..., env="DATABASE_USER")  # type: ignore
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")  # type: ignore

    # ----- Environment -----
    ENV: APP_STATES = Field(APP_STATES.DEVELOPMENT, env="ENV")  # type: ignore

    # ----- Webhooks -----
    WEBHOOK_PACIENTE_ADD: str = Field(..., env="WEBHOOK_PACIENTE_ADD")  # type: ignore
    WEBHOOK_SESION_ADD: str = Field(..., env="WEBHOOK_SESION_ADD")  # type: ignore
    # ----- hosts por entorno -----
    DEV_DB_HOST: str = Field("genomas.cl", env="DEV_DB_HOST")  # type: ignore
    DEV_DB_PORT: int = Field(5555, env="DEV_DB_PORT")  # type: ignore

    PROD_DB_HOST: str = Field("d4lia_pgbouncer", env="PROD_DB_HOST")  # type: ignore
    PROD_DB_PORT: int = Field(6432, env="PROD_DB_PORT")  # type: ignore

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def DATABASE_URL(self) -> str:

        if self.ENV == APP_STATES.PRODUCTION:
            host = self.PROD_DB_HOST
            port = self.PROD_DB_PORT
        else:
            host = self.DEV_DB_HOST
            port = self.DEV_DB_PORT

        return (
            f"postgresql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{host}:{port}/{self.DATABASE_NAME}"
        )


if __name__ == "__main__":
    try:
        settings = Settings()  # type: ignore
        print("Configuración cargada exitosamente:")
        for field in [
            "DATABASE_NAME",
            "DATABASE_USER",
            "DATABASE_PASSWORD",
            "DATABASE_HOST",
            "DATABASE_PORT",
        ]:
            print(f"  {field}: {getattr(settings, field)}")

    except ValidationError as e:
        print("❌ Error de configuración de variables de entorno:")
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            msg = err["msg"]
            print(f"  - {loc}: {msg}")

settings = Settings()  # type: ignore
