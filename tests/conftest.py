"""Pytest configuration and fixtures for Agente de Atendimento tests."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from src.config import Settings, get_settings
from src.main import app


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings.

    Returns:
        Settings: Test settings instance.
    """
    return Settings(
        app_name="agente-atendimento-test",
        app_version="0.1.0-test",
        debug=True,
        log_level="DEBUG",
        host="0.0.0.0",
        port=8000,
        cors_origins=["http://localhost:3000"],
    )


@pytest.fixture
def client(test_settings: Settings) -> Generator[TestClient, None, None]:
    """Create a test client for FastAPI.

    Args:
        test_settings: Test settings fixture.

    Yields:
        TestClient: Configured test client.
    """
    # Override settings for testing
    original_settings = get_settings()
    os.environ["APP_NAME"] = test_settings.app_name
    os.environ["DEBUG"] = "true"

    def _get_test_settings() -> Settings:
        return test_settings

    app.dependency_overrides[get_settings] = _get_test_settings

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()
    if "APP_NAME" in os.environ:
        del os.environ["APP_NAME"]
    if "DEBUG" in os.environ:
        del os.environ["DEBUG"]
