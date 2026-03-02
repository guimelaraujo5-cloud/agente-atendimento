"""Main FastAPI application for Agente de Atendimento."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Args:
        app: The FastAPI application instance.

    Yields:
        None
    """
    settings = get_settings()
    setup_logging(settings)
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/")
    async def root() -> dict[str, str]:
        """Health check endpoint.

        Returns:
            dict: Status message.
        """
        return {"status": "ok", "message": f"{settings.app_name} is running"}

    # Example endpoint
    @app.get("/api/v1/hello")
    async def hello() -> dict[str, str]:
        """Example hello endpoint.

        Returns:
            dict: Hello message.
        """
        return {"message": "Hello from Agente de Atendimento!"}

    return app


# Create the application instance
app = create_app()
