import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE"))

    ROOT_PATH: str = Field(default="", description="Url ROOT definido no ingress")
    ENVIRONMENT: str = Field(default="DEV", description="Ambiente de execução")
    VERSION: str = Field(default="v0.0.0", description="Versão da API")

    MYSQL_HOST: str = Field(default="127.0.0.1", description="Host do MySQL")
    MYSQL_PORT: int = Field(default=3306, description="Porta do MySQL")
    MYSQL_USER: str = Field(default="appuser", description="Usuário do MySQL")
    MYSQL_PASSWORD: str = Field(default="apppassword", description="Senha do MySQL")
    MYSQL_DATABASE: str = Field(default="local", description="Nome do banco de dados")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
