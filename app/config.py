import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE"))

    ROOT_PATH: str = Field(default="", description="Url ROOT definido no ingress")
    ENVIRONMENT: str = Field(default="DEV", description="Ambiente de execução")
    VERSION: str = Field(default="v0.0.0", description="Versão da API")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
