import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from health import api_health
from log_filter import EndpointFilter

excluded_endpoints = ["/health"]

logging.getLogger("uvicorn.access").addFilter(EndpointFilter(excluded_endpoints))


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    openapi_url="/docs/openapi.json",
    title="API Feira Inteligente",
    description="API responsável pelo gerenciamento de feiras e histórico de preços.",
    version=settings.VERSION,
    root_path=settings.ROOT_PATH,
    lifespan=lifespan,
)

app.add_api_route("/health", api_health, name="Health Check", tags=["Health"])
