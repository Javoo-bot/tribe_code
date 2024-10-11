import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:  #define la URL base del servidor según el entorno 
        # Si no lo hago en local uso HTTPS 
        if self.ENVIRONMENT == "local":  #si lo hago en local entonces el uso el https
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}" 

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors) #Valida que los orígenes de CORS sean URLs válidas y evita que haya fugas de seguridad
    ] = [] #de momento estan vacias
    #creo una conexion inicial
    PROJECT_NAME: str #le pongo un nombre
    SENTRY_DSN: HttpUrl | None = None  #mete sentry para los errores
    POSTGRES_SERVER: str  #dirección del servidor de PostgreSQL
    POSTGRES_PORT: int = 5432 #le pongo en este puerto 
    POSTGRES_USER: str #le pongo usuario
    POSTGRES_PASSWORD: str #contraseña 
    POSTGRES_DB: str = "" #el nombre se lo pongo yo de momento vacio

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn: #uso esto para identificar la base de datos
        return MultiHostUrl.build(   #como le meto muchos datos tengo que usar multihost 
            scheme="postgresql+psycopg",  #uso postgres y un adaptador para usar postgreSQL en python
            username=self.POSTGRES_USER, 
            password=self.POSTGRES_PASSWORD,  
            host=self.POSTGRES_SERVER, 
            port=self.POSTGRES_PORT,  
            path=self.POSTGRES_DB,    
        )

    @computed_field  # type: ignore[misc]
    @property
    def PG_DATABASE_URI(self) -> str:  #construye una cadena de conexión y verifica si los datos se han mandado bien 
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    PROTECTED_NAMES: list[str] = ["user", "ignore", "error"]

    def _check_default_secret(self, var_name: str, value: str | None) -> None: #verifica que las claves secretas no tengan valores por defecto inseguros
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

    # Qdrant
    QDRANT__SERVICE__API_KEY: str
    QDRANT_URL: str = "http://qdrant:6334"
    QDRANT_COLLECTION: str = "uploads"

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Embeddings
    DENSE_EMBEDDING_MODEL: str
    SPARSE_EMBEDDING_MODEL: str
    FASTEMBED_CACHE_PATH: str

    MAX_UPLOAD_SIZE: int = 50_000_000


settings = Settings()  # type: ignore
